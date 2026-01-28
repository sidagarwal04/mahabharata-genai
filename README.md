# 🏛️ Mahabharata AI Sage

> Dive into the timeless wisdom of an ancient Indian epic! Ask questions, explore characters, unravel mysteries, and gain insights from the vast knowledge powered by AI and graph databases.

## 🌟 Features

- **🤖 GPT-5.2 Powered**: Advanced AI responses using OpenAI's latest model
- **🗄️ Graph Database**: Neo4j-powered knowledge graph for rich contextual information
- **🎨 Modern UI**: Beautiful Nuxt.js frontend with responsive design
- **🚀 FastAPI Backend**: High-performance API with automatic documentation
- **🇮🇳 Hindi Audio**: Listen to responses in Hindi using Sarvam AI TTS
- **📱 Responsive**: Works perfectly on desktop and mobile devices
- **🔍 Source Attribution**: See exactly where information comes from
- **💬 Session Management**: Maintains conversation context with automatic summarization

## 🏗️ Architecture

This project has been upgraded from a simple Gradio interface to a modern, scalable architecture:

### Backend (`main.py`)
- **FastAPI** server with automatic API documentation
- **Fixed to GPT-5.2** model (no more model selection)
- **Neo4j integration** for graph-based retrieval
- **Session management** with automatic conversation summarization
- **CORS enabled** for frontend integration

### Frontend (`frontend/`)
- **Nuxt.js 3** application with TypeScript support
- **Tailwind CSS** for modern styling
- **Custom chat interface** replacing Gradio
- **Real-time typing indicators**
- **Audio playback** for Hindi translations using Sarvam AI
- **Responsive design** for all devices

### Legacy (`app.py`)
- Original Gradio interface (preserved but not actively used)
- Multiple model support (kept for reference)

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Neo4j Database** (with your Mahabharata data loaded)
- **OpenAI API Key**
- **Sarvam AI API Key** (for Hindi translation and audio)

### 1. Initial Setup

```bash
# Clone the repository
git clone https://github.com/sidagarwal04/mahabharata-genai.git
cd mahabharata-genai

# Run the setup script
./setup.sh
```

### 2. Configure Environment

Edit the `.env` file with your credentials:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Neo4j Database
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=your_database

# Sarvam AI (for Hindi translation and audio)
SARVAM_API_KEY=your_sarvam_api_key

# COMMENTED OUT: Legacy services (replaced with Sarvam AI)
# Google Cloud (for translation)
# PROJECT_ID=your_project_id
# GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
# ElevenLabs (for Hindi audio)
# ELEVENLABS_API_KEY=your_elevenlabs_key
```

### 3. Start Development Servers

```bash
# Start both backend and frontend
./start-dev.sh
```

This will start:
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

## Background
Have you ever been captivated by a story brimming with complex relationships? Stories like the Mahabharata, an ancient Indian epic, weave a spell with a multitude of characters and their intricate connections. These connections - familial bonds, alliances, rivalries - form the very foundation of the narrative, driving the plot and shaping the destinies of its heroes and villains.

It all began with a simple conversation. My wife, engrossed in C. Rajagopalachari's masterful translation of the [Mahabharata](https://www.amazon.in/Mahabharata-C-Rajagopalachari/dp/8172764766), sparked my curiosity about the intricate web of relationships within the epic. The idea of translating these connections into a powerful graph model, leveraging the capabilities of [Neo4j](www.neo4j.com) (a leader in Graph Database Industry), became an irresistible challenge.

![alt text](https://github.com/sidagarwal04/mahabharata-genai/blob/main/frontend/public/images/dall-e-mahabharata.png)

This is when I decided to embark on a fascinating journey to explore the Mahabharata through the lens of graph theory. But this was just the first chapter in my journey. I then decided to unveil an ambitious step forward: a Neo4j-powered chatbot. This innovative tool stems from a desire to make the epic’s complex relationships accessible to everyone, transcending traditional query methods.

Read the three-part blog series on this project:

+ [Unveiling the Mahabharata’s Web: A Graph Journey using Neo4j — (Part 1)](https://sidagarwal04.medium.com/unveiling-the-mahabharatas-web-a-graph-journey-using-neo4j-from-epic-relationships-to-7be4a7a29b6d)
+ [Bringing the Mahabharata Epic to Life: A Neo4j-Powered Chatbot using Google Gemini — (Part 2)](https://sidagarwal04.medium.com/bringing-the-mahabharata-epic-to-life-a-neo4j-powered-chatbot-using-google-gemini-part-2-6eef8676e757)
+ [From Ancient Epic to Modern Marvel: Demystifying the Mahabharata Chatbot with GraphRAG (Part 3)](https://medium.com/@sidagarwal04/from-ancient-epic-to-modern-marvel-demystifying-the-mahabharata-chatbot-with-graphrag-part-3-5942260a9560)

Read more about GraphRAG here: [Building a GraphRAG application](https://neo4j.com/developer-blog/knowledge-graph-rag-application/)

## Features
+ **Contextual Understanding:** Provides answers based on the context of the Mahabharata.
+ **Interactive Q&A:** Users can ask questions and get detailed answers.
+ **Relationship Mapping:** Visualizes and explains relationships between characters.
+ **Deployment Ready:** Easily deployable on platforms like Firebase.

## Architecture

The Mahabharata Chatbot is built using:

+ **Backend:** Python, Google Vertex AI (Google Gemini API), Gradio
+ **Frontend:** Nuxt.js
+ **Database:** Neo4j
+ **Deployment:** Hugging Face Space, Firebase

## Configuration
## 🚀 Deployment

This application is deployed using a modern architecture:
- **Backend**: Deployed on Render (FastAPI + Neo4j)
- **Frontend**: Deployed on Netlify (Nuxt.js)

### Live Demo
🎯 **[https://mb-aisage.netlify.app/](https://mb-aisage.netlify.app/)**

### Deploy Your Own
See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

## 💻 Local Development

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **Neo4j Database** (with your Mahabharata data loaded)
- **OpenAI API Key**
- **Sarvam AI API Key** (for Hindi translation and audio)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure environment file
cp example.backend.env .env
# Edit .env with your API keys and database credentials

# Start backend
uvicorn main:app --reload --port 8001
```

### Frontend Setup
```bash
cd frontend
npm install

# Copy and configure environment file
cp example.frontend.env .env
# Edit .env with your backend URL (default: http://localhost:8001)

# Start frontend
npm run dev
```

### Database Setup
1. **Start Neo4j Database**: Follow the official [Neo4j installation guide](https://neo4j.com/developer/)
2. **Load Data**: Use the provided [mahabharata-db-setup.cypher](backend/mahabharata-db-setup.cypher) script

### Environment Variables
**Backend (.env)**:
```
OPENAI_API_KEY=your_openai_api_key_here
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
SARVAM_API_KEY=your_sarvam_api_key_here
PROJECT_ID=your_google_cloud_project_id
```

**Frontend (.env)**:
```
API_BASE_URL=http://localhost:8001
```

## Contributing
Do share your feedback [here](https://docs.google.com/forms/d/e/1FAIpQLSdradX2oOSBpBGAla01tEroQJGDrA62ZsD8Sa_x7IXbGjkRfg/viewform) to make the Mahabharata chatbot the best resource for exploring this epic tale. I am welcoming contributions! Please follow these steps:

+ Fork the repository.
+ Create a new branch: `git checkout -b feature/YourFeature`
+ Make your changes and commit them: `git commit -m 'Add some feature'`.
+ Push to the branch: `git push origin feature/YourFeature`.
+ Create a pull request.

## License
This project is licensed under the [Apache License](mahabharata-genai/blob/main/LICENSE).

## Acknowledgements
Special thanks to my friend, [Vrijraj Singh](https://vrijraj.xyz/) for all his support in building web design for this app, [LLM Graph Builder Tool](https://neo4j.com/labs/genai-ecosystem/llm-graph-builder/) for converting external PDF sources into Knowledge Graph and the open-source community for their valuable resources and support.
