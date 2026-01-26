import os
import logging
import traceback
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_neo4j import Neo4jVector, Neo4jGraph

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load env
load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

def get_gpt4o_llm(max_tokens: int = 1024):
    print("Initializing GPT-4o LLM...")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    llm = ChatOpenAI(
        api_key=openai_api_key,
        model="gpt-4o",
        temperature=0,
        max_tokens=max_tokens
    )
    print("GPT-4o LLM OK")
    return llm

def test_startup():
    print("--- Starting Full Startup Debug ---")
    
    try:
        get_gpt4o_llm()
    except Exception as e:
        print(f"LLM Init Failed: {e}")
        traceback.print_exc()

    try:
        print("Initializing Embeddings...")
        embedding_function = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("Embeddings OK")

        print("Initializing Graph...")
        graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE
        )
        print("Graph OK")

        print("Initializing Vector Store...")
        vector_store = Neo4jVector.from_existing_index(
            embedding=embedding_function,
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE,
            index_name="vector",
            node_label="Chunk",
            text_node_property="text",
            embedding_node_property="embedding"
        )
        print("Vector Store OK")
        
        print("Initializing Retriever...")
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.8, "k": 15}
        )
        print("Retriever OK")
        
    except Exception as e:
        print(f"Neo4j Init Failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_startup()
