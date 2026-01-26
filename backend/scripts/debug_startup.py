import os
import logging
import traceback
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_neo4j import Neo4jVector, Neo4jGraph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env
load_dotenv()

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

def test_startup():
    print("--- Starting Debug ---")
    
    # 1. Initialize Embeddings
    try:
        print("Initializing Embeddings...")
        embedding_function = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("Embeddings OK")
    except Exception as e:
        print(f"Embeddings Failed: {e}")
        traceback.print_exc()
        return

    # 2. Initialize Graph
    try:
        print("Initializing Graph...")
        graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE
        )
        print("Graph OK")
    except Exception as e:
        print(f"Graph Failed: {e}")
        traceback.print_exc()
        # Continue to vector store to see if it also fails

    # 3. Initialize Vector Store
    try:
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
        print(f"Vector Store/Retriever Failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_startup()
