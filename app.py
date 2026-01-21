import os
import logging
import google.auth
from dotenv import load_dotenv
import gradio as gr
import threading
import time
import tempfile
import uuid
import sys

from datetime import datetime
from typing import Any


from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import TokenTextSplitter
from langchain.retrievers.document_compressors import EmbeddingsFilter, DocumentCompressorPipeline
from langchain.retrievers import ContextualCompressionRetriever
from langchain_core.runnables import RunnableBranch
from langchain_core.callbacks import StdOutCallbackHandler, BaseCallbackHandler



from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.document_compressors import EmbeddingsFilter, DocumentCompressorPipeline
from langchain.retrievers import ContextualCompressionRetriever


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.retrievers.document_compressors import EmbeddingsFilter, DocumentCompressorPipeline
from langchain_core.retrievers import ContextualCompressionRetriever

from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
from langchain_neo4j import Neo4jVector, Neo4jGraph, Neo4jChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings

# LangChain chat models
from langchain_openai import ChatOpenAI, AzureChatOpenAI, OpenAIEmbeddings
from langchain_google_vertexai import ChatVertexAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama

# ElevenLabs and Cloud Translate
from google.cloud import translate
from elevenlabs import ElevenLabs, play

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,  # Use DEBUG if you want more detail
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logging.info("✅ Logging is working!")


os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

project_id = os.getenv("PROJECT_ID")
credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")

### Vector graph search 
VECTOR_GRAPH_SEARCH_ENTITY_LIMIT = 40
VECTOR_GRAPH_SEARCH_EMBEDDING_MIN_MATCH = 0.3
VECTOR_GRAPH_SEARCH_EMBEDDING_MAX_MATCH = 0.9
VECTOR_GRAPH_SEARCH_ENTITY_LIMIT_MINMAX_CASE = 20
VECTOR_GRAPH_SEARCH_ENTITY_LIMIT_MAX_CASE = 40

# VECTOR_GRAPH_SEARCH_QUERY: Hybrid vector + graph retrieval Cypher query
VECTOR_GRAPH_SEARCH_QUERY_PREFIX = """
WITH node as chunk, score
// find the document of the chunk
MATCH (chunk)-[:PART_OF]->(d:Document)
// aggregate chunk-details
WITH d, collect(DISTINCT {chunk: chunk, score: score}) AS chunks, avg(score) as avg_score
// fetch entities
CALL { WITH chunks
UNWIND chunks as chunkScore
WITH chunkScore.chunk as chunk
"""

VECTOR_GRAPH_SEARCH_ENTITY_QUERY = """
    OPTIONAL MATCH (chunk)-[:HAS_ENTITY]->(e)
    WITH e, count(*) AS numChunks 
    ORDER BY numChunks DESC 
    LIMIT {no_of_entites}

    WITH 
    CASE 
        WHEN e.embedding IS NULL OR ({embedding_match_min} <= vector.similarity.cosine($embedding, e.embedding) AND vector.similarity.cosine($embedding, e.embedding) <= {embedding_match_max}) THEN 
            collect {{
                OPTIONAL MATCH path=(e)(()-[rels:!HAS_ENTITY&!PART_OF]-()){{0,1}}(:!Chunk&!Document&!__Community__) 
                RETURN path LIMIT {entity_limit_minmax_case}
            }}
        WHEN e.embedding IS NOT NULL AND vector.similarity.cosine($embedding, e.embedding) >  {embedding_match_max} THEN
            collect {{
                OPTIONAL MATCH path=(e)(()-[rels:!HAS_ENTITY&!PART_OF]-()){{0,2}}(:!Chunk&!Document&!__Community__) 
                RETURN path LIMIT {entity_limit_max_case} 
            }} 
        ELSE 
            collect {{ 
                MATCH path=(e) 
                RETURN path 
            }}
    END AS paths, e
"""

VECTOR_GRAPH_SEARCH_QUERY_SUFFIX = """
   WITH apoc.coll.toSet(apoc.coll.flatten(collect(DISTINCT paths))) AS paths,
        collect(DISTINCT e) AS entities
   // De-duplicate nodes and relationships across chunks
   RETURN
       collect {
           UNWIND paths AS p
           UNWIND relationships(p) AS r
           RETURN DISTINCT r
       } AS rels,
       collect {
           UNWIND paths AS p
           UNWIND nodes(p) AS n
           RETURN DISTINCT n
       } AS nodes,
       entities
}
// Generate metadata and text components for chunks, nodes, and relationships
WITH d, avg_score,
    [c IN chunks | c.chunk.text] AS texts,
    [c IN chunks | {id: c.chunk.id, score: c.score}] AS chunkdetails,
    [n IN nodes | elementId(n)] AS entityIds,
    [r IN rels | elementId(r)] AS relIds,
    apoc.coll.sort([
        n IN nodes |
        coalesce(apoc.coll.removeAll(labels(n), ['__Entity__'])[0], "") + ":" +
        coalesce(
            n.id,
            n[head([k IN keys(n) WHERE k =~ "(?i)(name|title|id|description)$"])],
            ""
        ) +
        (CASE WHEN n.description IS NOT NULL THEN " (" + n.description + ")" ELSE "" END)
    ]) AS nodeTexts,
    apoc.coll.sort([
        r IN rels |
        coalesce(apoc.coll.removeAll(labels(startNode(r)), ['__Entity__'])[0], "") + ":" +
        coalesce(
            startNode(r).id,
            startNode(r)[head([k IN keys(startNode(r)) WHERE k =~ "(?i)(name|title|id|description)$"])],
            ""
        ) + " " + type(r) + " " +
        coalesce(apoc.coll.removeAll(labels(endNode(r)), ['__Entity__'])[0], "") + ":" +
        coalesce(
            endNode(r).id,
            endNode(r)[head([k IN keys(endNode(r)) WHERE k =~ "(?i)(name|title|id|description)$"])],
            ""
        )
    ]) AS relTexts,
    entities
// Combine texts into response text
WITH d, avg_score, chunkdetails, entityIds, relIds,
    "Text Content:\n" + apoc.text.join(texts, "\n----\n") +
    "\n----\nEntities:\n" + apoc.text.join(nodeTexts, "\n") +
    "\n----\nRelationships:\n" + apoc.text.join(relTexts, "\n") AS text,
    entities
RETURN
   text,
   avg_score AS score,
   {
       length: size(text),
       source: COALESCE(CASE WHEN d.url CONTAINS "None" THEN d.fileName ELSE d.url END, d.fileName),
       chunkdetails: chunkdetails,
       entities : {
           entityids: entityIds,
           relationshipids: relIds
       }
   } AS metadata
"""


VECTOR_GRAPH_SEARCH_QUERY = VECTOR_GRAPH_SEARCH_QUERY_PREFIX+ VECTOR_GRAPH_SEARCH_ENTITY_QUERY.format(
    no_of_entites=VECTOR_GRAPH_SEARCH_ENTITY_LIMIT,
    embedding_match_min=VECTOR_GRAPH_SEARCH_EMBEDDING_MIN_MATCH,
    embedding_match_max=VECTOR_GRAPH_SEARCH_EMBEDDING_MAX_MATCH,
    entity_limit_minmax_case=VECTOR_GRAPH_SEARCH_ENTITY_LIMIT_MINMAX_CASE,
    entity_limit_max_case=VECTOR_GRAPH_SEARCH_ENTITY_LIMIT_MAX_CASE
) + VECTOR_GRAPH_SEARCH_QUERY_SUFFIX


graph = Neo4jGraph(
    url=NEO4J_URI, 
    username=NEO4J_USERNAME, 
    password=NEO4J_PASSWORD,
    database=NEO4J_DATABASE
)

CHAT_TOKEN_CUT_OFF = {
     ('openai_gpt_3.5','azure_ai_gpt_35',"gemini_1.0_pro","gemini_1.5_pro", "gemini_1.5_flash","groq-llama3",'anthropic_claude_3_5_sonnet','bedrock_claude_3_5_sonnet', ) : 4, 
     ("openai-gpt-4","diffbot" ,'azure_ai_gpt_4o',"openai_gpt_4o", "openai_gpt_4o_mini") : 28,
     ("ollama_llama3") : 2  
}  

# Prompt template
CHAT_SYSTEM_TEMPLATE = """
You are an AI-powered question-answering agent. Your task is to provide accurate and comprehensive responses to user queries based on the given context, chat history, and available resources.

### Response Guidelines:
1. **Direct Answers**: Provide clear and thorough answers to the user's queries without headers unless requested. Avoid speculative responses.
2. **Utilize History and Context**: Leverage relevant information from previous interactions, the current user input, and the context provided below.
3. **No Greetings in Follow-ups**: Start with a greeting in initial interactions. Avoid greetings in subsequent responses unless there's a significant break or the chat restarts.
4. **Admit Unknowns**: Clearly state if an answer is unknown. Avoid making unsupported statements.
5. **Avoid Hallucination**: Only provide information based on the context provided. Do not invent information.
6. **Response Length**: Keep responses concise and relevant. Aim for clarity and completeness within 4-5 sentences unless more detail is requested.
7. **Tone and Style**: Maintain a professional and informative tone. Be friendly and approachable.
8. **Error Handling**: If a query is ambiguous or unclear, ask for clarification rather than providing a potentially incorrect answer.
9. **Fallback Options**: If the required information is not available in the provided context, provide a polite and helpful response. Example: "I don't have that information right now." or "I'm sorry, but I don't have that information. Is there something else I can help with?"
10. **Context Availability**: If the context is empty, do not provide answers based solely on internal knowledge. Instead, respond appropriately by indicating the lack of information.


**IMPORTANT** : DO NOT ANSWER FROM YOUR KNOWLEDGE BASE USE THE BELOW CONTEXT

### Context:
<context>
{context}
</context>

### Example Responses:
User: Hi 
AI Response: 'Hello there! How can I assist you today?'

User: "What is Langchain?"
AI Response: "Langchain is a framework that enables the development of applications powered by large language models, such as chatbots. It simplifies the integration of language models into various applications by providing useful tools and components."

User: "Can you explain how to use memory management in Langchain?"
AI Response: "Langchain's memory management involves utilizing built-in mechanisms to manage conversational context effectively. It ensures that the conversation remains coherent and relevant by maintaining the history of interactions and using it to inform responses."

User: "I need help with PyCaret's classification model."
AI Response: "PyCaret simplifies the process of building and deploying machine learning models. For classification tasks, you can use PyCaret's setup function to prepare your data. After setup, you can compare multiple models to find the best one, and then fine-tune it for better performance."

User: "What can you tell me about the latest realtime trends in AI?"
AI Response: "I don't have that information right now. Is there something else I can help with?"

Note: This system does not generate answers based solely on internal knowledge. It answers from the information provided in the user's current and previous inputs, and from the context.
"""

QUESTION_TRANSFORM_TEMPLATE = "Given the below conversation, generate a search query to look up in order to get information relevant to the conversation. Only respond with the query, nothing else." 


prompt_template = ChatPromptTemplate.from_messages([
    ("system", CHAT_SYSTEM_TEMPLATE),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "User question: {input}")
])

class CustomCallback(BaseCallbackHandler):

    def __init__(self):
        self.transformed_question = None
    
    def on_llm_end(
        self,response, **kwargs: Any
    ) -> None:
        logging.info("question transformed")
        self.transformed_question = response.generations[0][0].text.strip()

# LLM selector supporting OpenAI, Gemini, Claude
def get_llm(model: str, max_tokens: int = 1024):
    """Retrieve the specified language model based on the model name."""
    model = model.strip().replace(" ", "_").lower()  # Replace spaces with underscores and convert to lowercase
    env_key = f"LLM_MODEL_CONFIG_{model.replace('-', '_').replace('.', '_')}".upper()  # Convert to uppercase
    env_value = os.getenv(env_key)

    if not env_value:
        err = f"Environment variable '{env_key}' is not defined as per format or missing"
        logging.error(err)
        raise Exception(err)

    logging.info("Model: {}".format(env_key))
    try:
        if "gemini" in model:
            model_name = env_value
            credentials, project_id = google.auth.default()
            llm = ChatVertexAI(
                model_name=model_name,
                credentials=credentials,
                project=project_id,
                temperature=0,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                },
                max_output_tokens=max_tokens,
            )

        elif "openai" in model:
            model_name, api_key = env_value.split(",")
            llm = ChatOpenAI(api_key=api_key, model=model_name, temperature=0, max_tokens=max_tokens)
            logging.info(f"OpenAI tokens used: {max_tokens}")

        elif "claude" in model or "anthropic" in model:
            model_name, api_key = env_value.split(",")
            logging.info(f"Anthropic model: {model_name}")
            logging.info(f"Anthropic API key: {api_key}")
            llm = ChatAnthropic(api_key=api_key, model=model_name, temperature=0, max_tokens=max_tokens)

        else:
            raise ValueError(f"Unsupported model type for: {model}")

    except Exception as e:
        err = f"Error while creating LLM '{model}': {str(e)}"
        logging.error(err)
        raise Exception(err)

    logging.info(f"Model created - Model Version: {model_name}")
    return llm, model_name, max_tokens


def summarize_and_log(history, stored_messages, llm):
    logging.info("Starting summarization in a separate thread.")
    if not stored_messages:
        logging.info("No messages to summarize.")
        return False

    try:
        start_time = time.time()

        summarization_prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "human",
                    "Summarize the above chat messages into a concise message, focusing on key points and relevant details that could be useful for future conversations. Exclude all introductions and extraneous information."
                ),
            ]
        )
        summarization_chain = summarization_prompt | llm

        summary_message = summarization_chain.invoke({"chat_history": stored_messages})

        with threading.Lock():
            history.clear()
            history.add_user_message("Our current conversation summary till now")
            history.add_message(summary_message)

        history_summarized_time = time.time() - start_time
        logging.info(f"Chat History summarized in {history_summarized_time:.2f} seconds")

        return True

    except Exception as e:
        logging.error(f"An error occurred while summarizing messages: {e}", exc_info=True)
        return False 

def get_total_tokens(ai_response, llm):
    try:
        if isinstance(llm, (ChatOpenAI, AzureChatOpenAI)):
            total_tokens = ai_response.response_metadata.get('token_usage', {}).get('total_tokens', 0)
        
        elif isinstance(llm, ChatVertexAI):
            total_tokens = ai_response.response_metadata.get('usage_metadata', {}).get('prompt_token_count', 0)
        
        elif isinstance(llm, ChatAnthropic):
            input_tokens = int(ai_response.response_metadata.get('usage', {}).get('input_tokens', 0))
            output_tokens = int(ai_response.response_metadata.get('usage', {}).get('output_tokens', 0))
            total_tokens = input_tokens + output_tokens
        
        elif isinstance(llm, ChatOllama):
            total_tokens = ai_response.response_metadata.get("prompt_eval_count", 0)
        
        else:
            logging.warning(f"Unrecognized language model: {type(llm)}. Returning 0 tokens.")
            total_tokens = 0

    except Exception as e:
        logging.error(f"Error retrieving total tokens: {e}")
        total_tokens = 0

    return total_tokens

def get_sources_and_chunks(sources_used, docs):
    chunkdetails_list = []
    sources_used_set = set(sources_used)
    seen_ids_and_scores = set()  

    for doc in docs:
        try:
            source = doc.metadata.get("source")
            chunkdetails = doc.metadata.get("chunkdetails", [])

            if source in sources_used_set:
                for chunkdetail in chunkdetails:
                    id = chunkdetail.get("id")
                    score = round(chunkdetail.get("score", 0), 4)

                    id_and_score = (id, score)

                    if id_and_score not in seen_ids_and_scores:
                        seen_ids_and_scores.add(id_and_score)
                        chunkdetails_list.append({**chunkdetail, "score": score})

        except Exception as e:
            logging.error(f"Error processing document: {e}")

    result = {
        'sources': sources_used,
        'chunkdetails': chunkdetails_list,
    }
    return result


def get_rag_chain(llm, system_template=CHAT_SYSTEM_TEMPLATE):
    try:
        question_answering_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_template),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "human",
                    "User question: {input}"
                ),
            ]
        )

        question_answering_chain = question_answering_prompt | llm

        return question_answering_chain

    except Exception as e:
        logging.error(f"Error creating RAG chain: {e}")
        raise

def format_documents(documents, model):
    prompt_token_cutoff = 4
    for model_names, value in CHAT_TOKEN_CUT_OFF.items():
        if model in model_names:
            prompt_token_cutoff = value
            break

    sorted_documents = sorted(documents, key=lambda doc: doc.state.get("query_similarity_score", 0), reverse=True)
    sorted_documents = sorted_documents[:prompt_token_cutoff]

    formatted_docs = list()
    sources = set()
    entities = dict()
    global_communities = list()


    for doc in sorted_documents:
        try:
            source = doc.metadata.get('source', "unknown")
            sources.add(source)
            if 'entities' in doc.metadata:
                if 'entityids' in doc.metadata['entities']:
                    entities.setdefault('entityids', set()).update(doc.metadata['entities']['entityids'])
                if 'relationshipids' in doc.metadata['entities']:
                    entities.setdefault('relationshipids', set()).update(doc.metadata['entities']['relationshipids'])
                
            if 'communitydetails' in doc.metadata:
                existing_ids = {entry['id'] for entry in global_communities}
                new_entries = [entry for entry in doc.metadata["communitydetails"] if entry['id'] not in existing_ids]
                global_communities.extend(new_entries)

            formatted_doc = (
                "Document start\n"
                f"This Document belongs to the source {source}\n"
                f"Content: {doc.page_content}\n"
                "Document end\n"
            )
            formatted_docs.append(formatted_doc)
        
        except Exception as e:
            logging.error(f"Error formatting document: {e}")
    
    return "\n\n".join(formatted_docs), sources,entities,global_communities


def process_documents(docs, question, messages, llm, model):
    start_time = time.time()
    
    try:
        formatted_docs, sources, entitydetails, communities = format_documents(docs, model)
        
        rag_chain = get_rag_chain(llm=llm)
        
        ai_response = rag_chain.invoke({
            "messages": messages[:-1],
            "context": formatted_docs,
            "input": question
        })

        result = {'sources': list(), 'nodedetails': dict(), 'entities': dict()}
        node_details = {"chunkdetails":list(),"entitydetails":list(),"communitydetails":list()}
        entities = {'entityids':list(),"relationshipids":list()}

        sources_and_chunks = get_sources_and_chunks(sources, docs)
        result['sources'] = sources_and_chunks['sources']
        node_details["chunkdetails"] = sources_and_chunks["chunkdetails"]
        entities.update(entitydetails)

        result["nodedetails"] = node_details
        result["entities"] = entities

        content = ai_response.content
        total_tokens = get_total_tokens(ai_response, llm)
        logging.info(f"Total tokens used: {total_tokens}")
        
        predict_time = time.time() - start_time
        logging.info(f"Final response predicted in {predict_time:.2f} seconds")

    except Exception as e:
        logging.error(f"Error processing documents: {e}")
        raise
    
    return content, result, total_tokens, formatted_docs

def retrieve_documents(doc_retriever, messages):

    start_time = time.time()
    try:
        handler = CustomCallback()
        docs = doc_retriever.invoke({"messages": messages},{"callbacks":[handler]})
        transformed_question = handler.transformed_question
        if transformed_question:
            logging.info(f"Transformed question : {transformed_question}")
        doc_retrieval_time = time.time() - start_time
        logging.info(f"Documents retrieved in {doc_retrieval_time:.2f} seconds")
        
    except Exception as e:
        error_message = f"Error retrieving documents: {str(e)}"
        logging.error(error_message)
        docs = None
        transformed_question = None
    
    return docs,transformed_question

def create_document_retriever_chain(llm, retriever):
    try:
        logging.info("Starting to create document retriever chain")

        query_transform_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", QUESTION_TRANSFORM_TEMPLATE),
                MessagesPlaceholder(variable_name="messages")
            ]
        )

        output_parser = StrOutputParser()

        splitter = TokenTextSplitter(chunk_size=5000, chunk_overlap=100)
        embeddings_filter = EmbeddingsFilter(
            embeddings=embedding_function,
            similarity_threshold=0.10
        )

        pipeline_compressor = DocumentCompressorPipeline(
            transformers=[splitter, embeddings_filter]
        )

        compression_retriever = ContextualCompressionRetriever(
            base_compressor=pipeline_compressor, base_retriever=retriever
        )

        query_transforming_retriever_chain = RunnableBranch(
            (
                lambda x: len(x.get("messages", [])) == 1,
                (lambda x: x["messages"][-1].content) | compression_retriever,
            ),
            query_transform_prompt | llm | output_parser | compression_retriever,
        ).with_config(run_name="chat_retriever_chain")

        logging.info("Successfully created document retriever chain")
        return query_transforming_retriever_chain

    except Exception as e:
        logging.error(f"Error creating document retriever chain: {e}", exc_info=True)
        raise

def initialize_neo4j_vector(graph):
    try:
        retrieval_query = VECTOR_GRAPH_SEARCH_QUERY
        index_name = "vector"
        keyword_index = "keyword"
        node_label = "Chunk"
        embedding_node_property = "embedding"
        text_node_properties = ["text"]


        if not retrieval_query or not index_name:
            raise ValueError("Required settings 'retrieval_query' or 'index_name' are missing.")

        if keyword_index:
            neo_db = Neo4jVector.from_existing_graph(
                embedding=embedding_function,
                index_name=index_name,
                retrieval_query=retrieval_query,
                graph=graph,
                search_type="hybrid",
                node_label=node_label,
                embedding_node_property=embedding_node_property,
                text_node_properties=text_node_properties,
                keyword_index_name=keyword_index
            )
            logging.info(f"Successfully retrieved Neo4jVector Fulltext index '{index_name}' and keyword index '{keyword_index}'")
        else:
            neo_db = Neo4jVector.from_existing_graph(
                embedding=embedding_function,
                index_name=index_name,
                retrieval_query=retrieval_query,
                graph=graph,
                node_label=node_label,
                embedding_node_property=embedding_node_property,
                text_node_properties=text_node_properties
            )
            logging.info(f"Successfully retrieved Neo4jVector index '{index_name}'")
    except Exception as e:
        index_name = "vector"
        logging.error(f"Error retrieving Neo4jVector index {index_name} : {e}")
        raise
    return neo_db

def create_retriever(neo_db, document_names,search_k, score_threshold,ef_ratio):
    if document_names and "False":
        retriever = neo_db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                'k': search_k,
                'effective_search_ratio': ef_ratio,
                'score_threshold': score_threshold,
                'filter': {'fileName': {'$in': document_names}}
            }
        )
        logging.info(f"Successfully created retriever with search_k={search_k}, score_threshold={score_threshold} for documents {document_names}")
    else:
        retriever = neo_db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={'k': search_k,'effective_search_ratio': ef_ratio, 'score_threshold': score_threshold}
        )
        logging.info(f"Successfully created retriever with search_k={search_k}, score_threshold={score_threshold}")
    return retriever


def get_neo4j_retriever(graph, document_names, score_threshold=0.5):
    try:

        neo_db = initialize_neo4j_vector(graph)
        # document_names= list(map(str.strip, json.loads(document_names)))
        search_k = 5
        ef_ratio = int(os.getenv("EFFECTIVE_SEARCH_RATIO", "2")) if os.getenv("EFFECTIVE_SEARCH_RATIO", "2").isdigit() else 2
        retriever = create_retriever(neo_db, document_names, search_k, score_threshold,ef_ratio)
        return retriever
    except Exception as e:
        index_name = "vector"
        logging.error(f"Error retrieving Neo4jVector index  {index_name} or creating retriever: {e}")
        raise Exception(f"An error occurred while retrieving the Neo4jVector index or creating the retriever. Please drop and create a new vector index '{index_name}': {e}") from e 

def setup_chat(model, graph, document_names, max_tokens=1024):
    start_time = time.time()
    try:
        if model == "diffbot":
            model = os.getenv('DEFAULT_DIFFBOT_CHAT_MODEL')
        
        llm, model_name, max_tokens = get_llm(model=model, max_tokens=max_tokens)
        logging.info(f"Model called in chat: {model} (version: {model_name})")

        retriever = get_neo4j_retriever(graph=graph, document_names=document_names)
        doc_retriever = create_document_retriever_chain(llm, retriever)
        
        chat_setup_time = time.time() - start_time
        logging.info(f"Chat setup completed in {chat_setup_time:.2f} seconds")
        
    except Exception as e:
        logging.error(f"Error during chat setup: {e}", exc_info=True)
        raise
    
    return llm, doc_retriever, model_name

def create_neo4j_chat_message_history(graph, session_id):
    try:
        history = Neo4jChatMessageHistory(
            graph=graph,
            session_id=session_id
        )
        return history
    except Exception as e:
        logging.error(f"Error creating Neo4jChatMessageHistory: {e}")
        raise

# Final response logic
def process_chat_response(messages, history, question, model, graph, document_names, session_id=None):
    try:
        overall_start = time.time()

        ### STEP 1: Setup LLM + retriever
        setup_start = time.time()
        llm, doc_retriever, model_version = setup_chat(model, graph, document_names, max_tokens=2048)
        logging.info(f"[Timing] setup_chat() took {time.time() - setup_start:.2f} sec")

        ### STEP 2: Retrieve documents
        retrieval_start = time.time()
        docs, transformed_question = retrieve_documents(doc_retriever, messages)
        logging.info(f"[Timing] retrieve_documents() took {time.time() - retrieval_start:.2f} sec")

        ### STEP 3: Process documents and generate answer
        process_start = time.time()
        if docs:
            content, result, total_tokens, formatted_docs = process_documents(docs, question, messages, llm, model)
        else:
            content = "I couldn't find any relevant documents to answer your question."
            result = {"sources": list(), "nodedetails": list(), "entities": list()}
            total_tokens = 0
            formatted_docs = ""
        logging.info(f"[Timing] process_documents() took {time.time() - process_start:.2f} sec")

        ### STEP 4: Add to message history
        messages.append(AIMessage(content=content))

        ### STEP 5: Run async summarization
        summarization_start = time.time()
        summarization_thread = threading.Thread(target=summarize_and_log, args=(history, messages, llm))
        summarization_thread.start()
        logging.info(f"[Timing] summarization thread launched (not blocking)")

        ### Final timing
        total_time = time.time() - overall_start
        logging.info(f"[Timing] Total process_chat_response() took {total_time:.2f} sec")

        metric_details = {"question": question, "contexts": formatted_docs, "answer": content}
        return {
            "session_id": session_id or "",
            "message": content,
            "info": {
                "sources": result["sources"],
                "model": model_version,
                "nodedetails": result["nodedetails"],
                "total_tokens": total_tokens,
                "response_time": total_time,
                "entities": result["entities"],
                "metric_details": metric_details,
            },
            "user": "chatbot"
        }

    except Exception as e:
        logging.exception(f"Error processing chat response at {datetime.now()}: {str(e)}")
        return {
            "session_id": "",
            "message": "Something went wrong",
            "info": {
                "metrics": [],
                "sources": [],
                "nodedetails": [],
                "total_tokens": 0,
                "response_time": 0,
                "error": f"{type(e).__name__}: {str(e)}",
                "entities": [],
                "metric_details": {},
            },
            "user": "chatbot"
        }
def handle_chat(question, history, llm, session_id):
    if not llm:
        return history + [{"role": "assistant", "content": "Please select your AI Sage (LLM model) to proceed."}]

    neo4j_history = create_neo4j_chat_message_history(graph, session_id=session_id)
    logging.info(f"Using Neo4jChatMessageHistory for session_id: {session_id}")
    messages = neo4j_history.messages

    messages.append(HumanMessage(content=question))
    history.append({"role": "user", "content": question})

    response = process_chat_response(messages, neo4j_history, question, llm, graph, document_names=[], session_id=session_id)
    model_name = response["info"].get("model", "Unknown Model")

    assistant_response = response.get("message", "I couldn't process your request.")
    history.append({"role": "assistant", "content": f"{assistant_response}\n\n(Model: {model_name})"})

    return history, session_id

# Define your custom CSS
custom_css = """
/* Custom CSS for the chat interface */
.gradio-container {
    # background: #f0f0f0; /* Change background color */
    border: 0
    border-radius: 15px; /* Add border radius */
}
.primary.svelte-cmf5ev{
    background: linear-gradient(90deg, #9848FC 0%, #DC8855 100%);
    # background-clip: text;
    # -webkit-background-clip: text;
    # -webkit-text-fill-color: transparent;
}
.v-application .secondary{
    background-color: #EEEEEE !important
}
"""

# Add the "Listen this in Hindi" button logic
def listen_in_hindi(response_text):
    try:
        if not response_text:
            raise ValueError("No response text available to translate.")
        
        # Remove any metadata like "(Model: ...)" from the response text
        if "(Model:" in response_text:
            response_text = response_text.split("(Model:")[0].strip()

        # Translate text to Hindi
        project_id = os.getenv("PROJECT_ID")
        if not project_id:
            raise ValueError("PROJECT_ID not set in environment.")
        
        client = translate.TranslationServiceClient()
        parent = f"projects/{project_id}/locations/global"

        response = client.translate_text(
            parent=parent,
            contents=[response_text],
            mime_type="text/plain",
            source_language_code="en-US",
            target_language_code="hi",
        )
        translated_text = response.translations[0].translated_text

        # Generate audio using ElevenLabs
        ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
        if not ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY not set")
        
        elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio_generator = elevenlabs_client.text_to_speech.convert(
            text=translated_text,
            voice_id="MF4J4IDTRo0AxOO4dpFR",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        audio_bytes = b"".join(audio_generator)

        # Save to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(audio_bytes)
            audio_path = f.name

        return audio_path, "Hindi audio generated!"

    except Exception as e:
        logging.error(f"Error in 'listen_in_hindi': {e}")
        return None, f"Error: {e}"

def get_last_bot_response(chat_history):
    if not chat_history or not isinstance(chat_history, list):
        print("Chat history is empty or invalid.")
        return None
    
    # Reverse iterate to find the last assistant message
    for msg in reversed(chat_history):
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            print(f"Last assistant response: {msg.get('content')}")
            return msg.get("content")
    
    print("No assistant response found.")
    return None

with gr.Blocks(css=custom_css, theme="soft") as demo:
    # Title and description
    gr.Markdown(
        """
        # Mahabharata AI Sage
        Step into the epic world of the Mahabharata! Ask questions, explore characters, unravel mysteries, 
        and gain insights from the vast knowledge stored in the database. Let the wisdom of AI guide you!
        """
    )

    session_state = gr.Textbox(value=str(uuid.uuid4()), visible=False, interactive=False)

    # Dropdown for LLM selection
    llm_dropdown = gr.Dropdown(
        choices=["OpenAI GPT-5.1", "OpenAI GPT-4o", "Gemini 3 Pro Preview", "Gemini 2.5 Flash", "Gemini 2.5 Pro", "Claude 3.7 Sonnet"],
        label="Select Your AI Sage",
        value=None,
        interactive=True,
        key="llm",
        info="Choose the AI model to guide your journey through the Mahabharata."
    )

    # Textbox for user questions
    question_textbox = gr.Textbox(
        label="Ask Mahabharata AI Sage",
        placeholder="Type your query about the Mahabharata here..."
    )

    # Chat interface
    chatbot = gr.Chatbot(type="messages", height=450, label="Mahabharata Chat")

    # Examples component
    examples = gr.Examples(
        examples=[
            ["Why did the Mahabharata war happen?"],
            ["Who killed Karna, and why?"],
            ["Why did the Pandavas have to go live in the forest for 12 years?"],
            ["Who was the wife of all five Pandavas, and how did that marriage come to be?"],
            ["What was the role of Krishna during the Kurukshetra war? Did he fight?"],
            ["Describe the relationship between Karna and Kunti. How did it affect the war?"],
            ["Who killed Ghatotakach?"],
            ["Who were the siblings of Karna?"],
            ["Why did Bhishma take a vow of celibacy, and how did that impact the throne of Hastinapur?"],
            ["Who killed Dronacharya and how was he tricked into giving up his weapons?"]
        ],
        inputs=question_textbox,  # Link examples to the textbox component
        label="Example Questions"
    )

    # Submit button
    submit_button = gr.Button("Submit")

    # "Listen this in Hindi" button
    listen_button = gr.Button("Listen to this in Hindi", interactive=False)
    status_output = gr.Textbox(label="Status")
    audio_output = gr.Audio(label="Hindi Audio", type="filepath")

    # Define the interaction logic
    submit_button.click(
        fn=handle_chat,
        inputs=[question_textbox, chatbot, llm_dropdown, session_state],  # Pass the question, chat history, and LLM model
        outputs=[chatbot, session_state]  # Update the chatbot with the new chat history
    ).then(
        fn=lambda: gr.update(interactive=True),
        inputs=None,
        outputs=listen_button
    )

    # Define the interaction logic for the "Listen this in Hindi" button
    listen_button.click(
        fn=lambda chat_history: listen_in_hindi(get_last_bot_response(chat_history)),
        inputs=chatbot,
        outputs=[audio_output, status_output]
    )


    question_textbox.change(
        fn=lambda: gr.update(interactive=False),
        inputs=None,
        outputs=listen_button
    )

# # Launch the interface
# if __name__ == "__main__":
#     demo.launch()

# Launch the Gradio interface
demo.queue().launch(server_name="0.0.0.0", server_port=5050)