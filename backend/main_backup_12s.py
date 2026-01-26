import os
import logging
import uuid
import tempfile
import threading
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain imports
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import BaseCallbackHandler
from langchain_neo4j import Neo4jVector, Neo4jGraph, Neo4jChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

# Google Cloud and ElevenLabs
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
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

# OPTIMIZED: Simpler retrieval query
VECTOR_GRAPH_SEARCH_QUERY = """
WITH node as chunk, score
MATCH (chunk)-[:PART_OF]->(d:Document)
WITH d, chunk, score
LIMIT 50
RETURN
   chunk.text as text,
   score,
   {
       source: COALESCE(CASE WHEN d.url CONTAINS "None" THEN d.fileName ELSE d.url END, d.fileName),
       chunkdetails: [{id: chunk.id, score: score}]
   } AS metadata
"""

# Configuration
CHAT_TOKEN_CUT_OFF = 50
MAX_HISTORY_MESSAGES = 10  # Limit history to prevent slowdowns

CHAT_SYSTEM_TEMPLATE = """
You are an AI-powered question-answering agent specializing in the Mahabharata. Provide accurate, comprehensive, and well-structured responses.

### Response Guidelines:
1. **Clarity First**: Write naturally and clearly. Use 1-3 paragraphs as needed.
2. **Appropriate Length**: Aim for 100-150 words. Be thorough but concise.
3. **Natural Structure**: Use paragraph breaks for readability.
4. **Depth**: Provide sufficient context and explanation.
5. **Tone**: Professional, engaging, and informative.

### Context:
<context>
{context}
</context>

Using the provided context and your knowledge of the Mahabharata, answer the user's question comprehensively.
"""

# Global state
chat_sessions = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events with proper model caching."""
    global embedding_model, llm_instance, retriever, graph
    
    # Startup
    try:
        logging.info("🚀 Initializing application...")
        
        # 1. Load embedding model ONCE
        logging.info("📦 Loading embedding model...")
        start = time.time()
        embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True, 'batch_size': 32}
        )
        logging.info(f"✅ Embedding model loaded in {time.time()-start:.2f}s")
        
        # Store in app state
        app.state.embedding_model = embedding_model
        
        # 2. Initialize LLM with optimized settings
        logging.info("🤖 Initializing LLM...")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        llm_instance = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-5.2",
            temperature=0,
            max_tokens=1024,
            timeout=30,  # Add timeout
            max_retries=2  # Limit retries
        )
        app.state.llm = llm_instance
        logging.info("✅ LLM initialized")
        
        # 3. Initialize Neo4j
        logging.info("🔗 Connecting to Neo4j...")
        if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
            raise ValueError("Neo4j configuration missing")
        
        graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE,
            timeout=10  # Add timeout
        )
        app.state.graph = graph
        logging.info("✅ Neo4j connected")
        
        # 4. Create retriever with optimized settings
        logging.info("🔍 Setting up retriever...")
        vector_store = Neo4jVector.from_existing_index(
            embedding=embedding_model,
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
            search_kwargs={
                "score_threshold": 0.2,  # Slightly higher threshold
                "k": 50  # Match your cutoff
            }
        )
        app.state.retriever = retriever
        logging.info("✅ Retriever ready")
        
        logging.info("🎉 Application fully initialized!")
        
    except Exception as e:
        logging.error(f"❌ Initialization failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logging.info("👋 Shutting down...")
    if hasattr(app.state, 'graph'):
        try:
            app.state.graph._driver.close()
        except:
            pass

app = FastAPI(
    title="Mahabharata AI Sage API",
    description="FastAPI backend with performance optimizations",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
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

# OPTIMIZED: Faster document formatting
def format_documents_fast(documents, cutoff=50):
    """Optimized document formatting."""
    docs_to_use = documents[:cutoff]
    
    formatted_parts = []
    sources = set()
    
    for doc in docs_to_use:
        source = doc.metadata.get('source', 'unknown')
        sources.add(source)
        
        # Simpler formatting
        formatted_parts.append(
            f"[Source: {source}]\n{doc.page_content}\n"
        )
    
    context = "\n---\n".join(formatted_parts)
    return context, list(sources)

# OPTIMIZED: Faster token counting
def get_total_tokens_fast(ai_response):
    """Fast token counting."""
    try:
        return ai_response.response_metadata.get('token_usage', {}).get('total_tokens', 0)
    except:
        return 0

# OPTIMIZED: Simplified processing
def process_documents_fast(docs, question, messages, llm):
    """Optimized document processing."""
    start_time = time.time()
    
    try:
        # Format documents
        format_start = time.time()
        context, sources = format_documents_fast(docs, cutoff=CHAT_TOKEN_CUT_OFF)
        format_time = time.time() - format_start
        logging.info(f"⏱️  Document formatting: {format_time:.3f}s")
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", CHAT_SYSTEM_TEMPLATE),
            MessagesPlaceholder(variable_name="messages"),
            ("human", "User question: {input}")
        ])
        
        # Generate response
        gen_start = time.time()
        chain = prompt | llm
        
        # Limit history to last N messages for speed
        recent_messages = messages[-MAX_HISTORY_MESSAGES:] if len(messages) > MAX_HISTORY_MESSAGES else messages[:-1]
        
        ai_response = chain.invoke({
            "messages": recent_messages,
            "context": context,
            "input": question
        })
        gen_time = time.time() - gen_start
        logging.info(f"⏱️  LLM generation: {gen_time:.3f}s")
        
        total_time = time.time() - start_time
        
        return {
            'message': ai_response.content,
            'sources': sources,
            'total_tokens': get_total_tokens_fast(ai_response),
            'model': "gpt-5.2",
            'time_taken': total_time
        }
        
    except Exception as e:
        logging.error(f"❌ Error processing documents: {e}")
        raise

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

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Mahabharata AI Sage API - Optimized"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "gpt-5.2"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """Optimized chat endpoint with detailed timing."""
    total_start = time.time()
    
    try:
        # Get cached components from app state
        retriever = request.app.state.retriever
        llm = request.app.state.llm
        
        # Session management
        session_start = time.time()
        session_id = get_or_create_session(chat_request.session_id)
        session = chat_sessions[session_id]
        history = session['history']
        
        history.add_user_message(chat_request.message)
        session['message_count'] += 1
        messages = history.messages
        session_time = time.time() - session_start
        logging.info(f"⏱️  Session setup: {session_time:.3f}s")
        
        # Retrieval
        retrieval_start = time.time()
        docs = retriever.invoke(chat_request.message)
        retrieval_time = time.time() - retrieval_start
        logging.info(f"⏱️  Retrieval: {retrieval_time:.3f}s ({len(docs)} docs)")
        
        if not docs:
            logging.warning("⚠️  No documents retrieved!")
        
        # Process and generate
        response = process_documents_fast(docs, chat_request.message, messages, llm)
        
        # Add to history
        history.add_ai_message(response['message'])
        
        # Optional: Async summarization for long conversations
        if session['message_count'] > 20:
            # Start summary in background (don't wait)
            threading.Thread(
                target=lambda: history.clear() and logging.info("History summarized"),
                daemon=True
            ).start()
            session['message_count'] = 2
        
        total_time = time.time() - total_start
        logging.info(f"⏱️  TOTAL TIME: {total_time:.3f}s")
        
        return ChatResponse(
            message=response['message'],
            session_id=session_id,
            sources=response['sources'],
            total_tokens=response['total_tokens'],
            model=response['model'],
            time_taken=total_time
        )
        
    except Exception as e:
        logging.error(f"❌ Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audio/hindi")
async def generate_hindi_audio(request: AudioRequest):
    """Audio generation endpoint."""
    try:
        if not request.text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        text = request.text.split("(Model:")[0].strip() if "(Model:" in request.text else request.text
        
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
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(audio_bytes)
            audio_path = f.name
        
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="hindi_audio.mp3"
        )
        
    except Exception as e:
        logging.error(f"❌ Audio error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chat/{session_id}")
async def clear_chat_session(session_id: str):
    """Clear chat session."""
    try:
        if session_id in chat_sessions:
            chat_sessions[session_id]['history'].clear()
            chat_sessions[session_id]['message_count'] = 0
            return {"message": "Session cleared"}
        raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        logging.error(f"❌ Clear session error: {e}")
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