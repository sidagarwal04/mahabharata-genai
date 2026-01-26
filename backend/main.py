import os
import logging
import google.auth
import uuid
import tempfile
import threading
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain imports (same as original app.py)
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import TokenTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableBranch
from langchain_core.callbacks import StdOutCallbackHandler, BaseCallbackHandler

from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
from langchain_neo4j import Neo4jVector, Neo4jGraph, Neo4jChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings

# LangChain chat models - Fixed to OpenAI GPT-4o only
from langchain_openai import ChatOpenAI, AzureChatOpenAI, OpenAIEmbeddings

# ElevenLabs and Cloud Translate
from google.cloud import translate
from elevenlabs import ElevenLabs

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")  # Default to 'neo4j' if not set

project_id = os.getenv("PROJECT_ID")
credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize HuggingFace embeddings with explicit settings
embedding_function = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# Vector graph search configuration (same as original)
VECTOR_GRAPH_SEARCH_ENTITY_LIMIT = 40
VECTOR_GRAPH_SEARCH_EMBEDDING_MIN_MATCH = 0.3
VECTOR_GRAPH_SEARCH_EMBEDDING_MAX_MATCH = 0.9
VECTOR_GRAPH_SEARCH_ENTITY_LIMIT_MINMAX_CASE = 20
VECTOR_GRAPH_SEARCH_ENTITY_LIMIT_MAX_CASE = 40

# Include all the same Cypher queries and constants from original app.py
# Simple retrieval query that worked in app.py
VECTOR_GRAPH_SEARCH_QUERY = """
WITH node as chunk, score
MATCH (chunk)-[:PART_OF]->(d:Document)
WITH d, collect(DISTINCT {chunk: chunk, score: score}) AS chunks, avg(score) as avg_score
OPTIONAL MATCH (chunk)-[:HAS_ENTITY]->(e)
WITH d, chunks, avg_score, collect(DISTINCT e) as entities
RETURN
   apoc.text.join([c in chunks | c.chunk.text], "\n----\n") as text,
   avg_score AS score,
   {
       length: size([c in chunks | c.chunk.text][0]),
       source: COALESCE(CASE WHEN d.url CONTAINS "None" THEN d.fileName ELSE d.url END, d.fileName),
       chunkdetails: [c IN chunks | {id: c.chunk.id, score: c.score}],
       entities : {
           entityids: [e in entities | elementId(e)],
           relationshipids: []
       }
   } AS metadata
"""

# Neo4j graph will be initialized during startup
graph = None

# Chat token cutoff for GPT-4o
CHAT_TOKEN_CUT_OFF = 28  # Fixed for GPT-4o

# System template (same as original)
CHAT_SYSTEM_TEMPLATE = """
You are an AI-powered question-answering agent. Your task is to provide accurate and comprehensive responses to user queries based on the given context, chat history, and available resources.

### Response Guidelines:
1. **Be Concise and Direct**: Provide your answer in a **single, well-structured paragraph**.
2. **No Bullet Points or Lists**: Avoid using bullet points, numbered lists, or headers. Write in plain paragraph form only.
3. **Response Length**: Keep the response concise, ideally between 4-6 sentences.
4. **Be Helpful and Informative**: Provide a complete and engaging answer about the Mahabharata using the provided context and your knowledge.
5. **Tone and Style**: Maintain a professional, approachable, and informative tone.


### Context:
<context>
{context}
</context>

AI Sage, use the provided context to answer the user's question as best as you can. If the context is sparse, use your general knowledge of the Mahabharata to fill in the gaps, while staying true to the spirit of the provided information.

Note: Your primary goal is to be helpful and informative about the Mahabharata.
"""

# Global variables for app state
chat_sessions = {}
llm_instance = None
graph = None

class CustomCallback(BaseCallbackHandler):
    def __init__(self):
        self.transformed_question = None
    
    def on_llm_end(self, response, **kwargs: Any) -> None:
        logging.info("question transformed")
        self.transformed_question = response.generations[0][0].text.strip()

# Fixed LLM getter for GPT-4o only
def get_gpt4o_llm(max_tokens: int = 1024):
    """Get GPT-4o model - fixed configuration."""
    try:
        # Get OpenAI API key from environment
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4o",
            temperature=0,
            max_tokens=max_tokens
        )
        
        logging.info(f"GPT-4o model created with max_tokens: {max_tokens}")
        return llm, "gpt-4o", max_tokens
        
    except Exception as e:
        err = f"Error while creating GPT-4o LLM: {str(e)}"
        logging.error(err)
        raise Exception(err)

# Include all the utility functions from original app.py
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
    prompt_token_cutoff = CHAT_TOKEN_CUT_OFF  # Fixed for GPT-4o
    
    # LangChain Document objects don't have a 'state' attribute.
    # We'll assume the retriever returns them in order of relevance (which it does).
    sorted_documents = documents[:prompt_token_cutoff]

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
    
    return "\n\n".join(formatted_docs), sources, entities, global_communities

def process_documents(docs, question, messages, llm, model):
    start_time = time.time()
    
    try:
        formatted_docs, sources, entitydetails, communities = format_documents(docs, model)
        logging.info(f"FORMATTED CONTEXT SENT TO LLM:\n{formatted_docs}")
        
        rag_chain = get_rag_chain(llm=llm)
        
        ai_response = rag_chain.invoke({
            "messages": messages[:-1],
            "context": formatted_docs,
            "input": question
        })

        result = {'sources': list(), 'nodedetails': dict(), 'entities': dict()}
        result['sources'] = list(sources)
        result['entities'] = {key: list(value) for key, value in entitydetails.items() if isinstance(value, set)}
        
        total_tokens_used = get_total_tokens(ai_response, llm)
        sources_data = get_sources_and_chunks(sources, docs)
        result.update(sources_data)

        processing_time = time.time() - start_time
        logging.info(f"Documents processed in {processing_time:.2f} seconds")
        
        return {
            'message': ai_response.content,
            'sources': result.get('sources', []),
            'chunkdetails': result.get('chunkdetails', []),
            'entities': result.get('entities', {}),
            'total_tokens': total_tokens_used,
            'model': model,
            'nodedetails': result.get('nodedetails', {}),
            'time_taken': processing_time,
            'communities': communities
        }

    except Exception as e:
        logging.error(f"Error processing documents: {e}")
        raise

# Initialize Neo4j retriever and vector store (copy from original app.py)
def create_neo4j_retriever():
    try:
        vector_store = Neo4jVector.from_existing_index(
            embedding=embedding_function,
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE,
            index_name="vector",
            node_label="Chunk",
            text_node_property="text",
            embedding_node_property="embedding",
            retrieval_query=VECTOR_GRAPH_SEARCH_QUERY
        )

        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.1, "k": 20}
        )

        logging.info("Neo4j retriever created successfully")
        return retriever

    except Exception as e:
        logging.error(f"Error creating Neo4j retriever: {e}")
        raise

# Pydantic models for API requests and responses
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    session_id: str
    sources: List[str]
    total_tokens: int
    model: str
    time_taken: float

class AudioRequest(BaseModel):
    text: str

class AudioResponse(BaseModel):
    status: str
    message: Optional[str] = None

# Session management
def get_or_create_session(session_id: Optional[str] = None) -> str:
    if session_id and session_id in chat_sessions:
        return session_id
    
    new_session_id = str(uuid.uuid4())
    chat_sessions[new_session_id] = {
        'history': Neo4jChatMessageHistory(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE,
            session_id=new_session_id
        ),
        'message_count': 0
    }
    return new_session_id

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global llm_instance, retriever, graph
    try:
        # Initialize LLM
        llm_instance, _, _ = get_gpt4o_llm()
        logging.info("GPT-4o LLM initialized")
        
        # Check Neo4j configuration
        logging.info(f"Checking Neo4j configuration...")
        if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE]):
            missing = []
            if not NEO4J_URI: missing.append("NEO4J_URI")
            if not NEO4J_USERNAME: missing.append("NEO4J_USERNAME") 
            if not NEO4J_PASSWORD: missing.append("NEO4J_PASSWORD")
            if not NEO4J_DATABASE: missing.append("NEO4J_DATABASE")
            error_msg = f"Missing Neo4j configuration: {', '.join(missing)}"
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        # Initialize Neo4j graph
        logging.info("Initializing Neo4j graph...")
        graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE
        )
        logging.info("Neo4j graph initialized successfully")
        
        # Initialize retriever
        logging.info("Initializing Neo4j retriever...")
        retriever = create_neo4j_retriever()
        logging.info("Neo4j retriever initialized successfully")
        
        logging.info("All components initialized successfully!")
    except Exception as e:
        logging.error(f"Failed to initialize app: {e}")
        # We don't raise here to allow the app to start (and return 503s), 
        # or we could raise to crash it. The previous logic allowed starting.
        # But if lifespan fails, the app usually fails to start.
        # Let's log it.
        pass
    
    yield
    
    # Shutdown
    logging.info("FastAPI app shutting down")
    if graph:
        try:
            graph._driver.close()
        except:
            pass

# FastAPI app initialization
app = FastAPI(
    title="Mahabharata AI Sage API",
    description="FastAPI backend for Mahabharata chatbot with GPT-4o",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize retriever at startup
retriever = None


# API Endpoints
@app.get("/")
async def root():
    return {"message": "Mahabharata AI Sage API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "gpt-4o"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Check if components are properly initialized
        if retriever is None or graph is None:
            raise HTTPException(
                status_code=503, 
                detail="Neo4j components not initialized. Check server logs for configuration errors."
            )
            
        session_id = get_or_create_session(request.session_id)
        session = chat_sessions[session_id]
        history = session['history']
        
        # Add user message to history
        history.add_user_message(request.message)
        session['message_count'] += 1
        
        # Get conversation history
        messages = history.messages
        
        # Perform retrieval
        logging.info(f"Querying retriever with: {request.message}")
        docs = retriever.invoke(request.message)
        logging.info(f"Retrieved {len(docs)} documents")
        for i, doc in enumerate(docs):
            logging.info(f"Doc {i} metadata: {doc.metadata}")
            logging.info(f"Doc {i} content snippet: {doc.page_content[:200]}...")
        
        if not docs:
            logging.warning("No documents were retrieved!")
        
        # Process documents and generate response
        logging.info("Starting process_documents...")
        response = process_documents(docs, request.message, messages, llm_instance, "gpt-4o")
        logging.info(f"AI Response generated: {response['message'][:100]}...")
        
        # Add assistant response to history
        history.add_ai_message(response['message'])
        
        # Handle summarization for long conversations
        if session['message_count'] > 20:
            stored_messages = history.messages
            summary_thread = threading.Thread(
                target=summarize_and_log,
                args=(history, stored_messages, llm_instance)
            )
            summary_thread.start()
            session['message_count'] = 2  # Reset after summarization
        
        return ChatResponse(
            message=response['message'],
            session_id=session_id,
            sources=response['sources'],
            total_tokens=response['total_tokens'],
            model=response['model'],
            time_taken=response['time_taken']
        )
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audio/hindi", response_model=AudioResponse)
async def generate_hindi_audio(request: AudioRequest):
    try:
        if not request.text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        # Remove any metadata like "(Model: ...)" from the response text
        text = request.text
        if "(Model:" in text:
            text = text.split("(Model:")[0].strip()

        # Translate text to Hindi
        project_id = os.getenv("PROJECT_ID")
        if not project_id:
            raise HTTPException(status_code=500, detail="PROJECT_ID not configured")
        
        client = translate.TranslationServiceClient()
        parent = f"projects/{project_id}/locations/global"

        response = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",
            source_language_code="en-US",
            target_language_code="hi",
        )
        translated_text = response.translations[0].translated_text

        # Generate audio using ElevenLabs
        ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
        if not ELEVENLABS_API_KEY:
            raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY not configured")
        
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

        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="hindi_audio.mp3"
        )

    except Exception as e:
        logging.error(f"Error in hindi audio endpoint: {e}")
        return AudioResponse(status="error", message=str(e))

@app.delete("/chat/{session_id}")
async def clear_chat_session(session_id: str):
    try:
        if session_id in chat_sessions:
            chat_sessions[session_id]['history'].clear()
            chat_sessions[session_id]['message_count'] = 0
            return {"message": "Session cleared successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        logging.error(f"Error clearing session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/examples")
async def get_examples():
    return {
        "examples": [
            "Why did the Mahabharata war happen?",
            "Who killed Karna, and why?",
            "Why did the Pandavas have to go live in the forest for 12 years?",
            "Who was the wife of all five Pandavas, and how did that marriage come to be?",
            "What was the role of Krishna during the Kurukshetra war? Did he fight?",
            "Describe the relationship between Karna and Kunti. How did it affect the war?",
            "Who killed Ghatotakach?",
            "Who were the siblings of Karna?",
            "Why did Bhishma take a vow of celibacy, and how did that impact the throne of Hastinapur?",
            "Who killed Dronacharya and how was he tricked into giving up his weapons?"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)