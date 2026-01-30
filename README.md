# 🏛️ Mahabharata AI Sage

> Dive into the timeless wisdom of an ancient Indian epic! Ask questions, explore characters, unravel mysteries, and gain insights from the vast knowledge powered by AI and graph databases.

## 🌟 Features

- **🤖 OpenAI Powered**: Advanced AI responses using OpenAI's GPT models
- **🗄️ Graph Database**: Neo4j-powered knowledge graph for rich contextual information
- **🎨 Modern UI**: Beautiful Nuxt.js frontend with responsive design
- **🚀 FastAPI Backend**: High-performance API with automatic documentation
- **🇮🇳 Hindi Audio**: Listen to responses in Hindi using Sarvam AI TTS
- **📱 Responsive**: Works perfectly on desktop and mobile devices
- **🔍 Source Attribution**: See exactly where information comes from
- **💬 Session Management**: Maintains conversation context with automatic summarization
- **🌐 Live Demo**: Ready-to-use deployment on Netlify

## 🏗️ Architecture

This project follows a modern, scalable architecture with separate frontend and backend services:

### Backend (`backend/`)
- **FastAPI** server with automatic API documentation
- **OpenAI integration** for advanced language processing
- **Neo4j GraphRAG** for graph-based retrieval augmented generation
- **Session management** with automatic conversation summarization
- **Sarvam AI integration** for Hindi translation and text-to-speech
- **CORS enabled** for frontend integration

### Frontend (`frontend/`)
- **Nuxt.js 3** application with TypeScript support
- **Tailwind CSS** for modern, responsive styling
- **Custom chat interface** with real-time interactions
- **Audio playback** for Hindi responses
- **Mobile-first responsive design**

## 🚀 Live Demo

🎯 **[https://mb-aisage.netlify.app/](https://mb-aisage.netlify.app/)**

## 💻 Local Development

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Neo4j Database** (with Mahabharata data loaded)
- **OpenAI API Key**
- **Sarvam AI API Key** (for Hindi translation and audio)

## Background
Have you ever been captivated by a story brimming with complex relationships? Stories like the Mahabharata, an ancient Indian epic, weave a spell with a multitude of characters and their intricate connections. These connections - familial bonds, alliances, rivalries - form the very foundation of the narrative, driving the plot and shaping the destinies of its heroes and villains.

It all began with a simple conversation. My wife, engrossed in C. Rajagopalachari's masterful translation of the [Mahabharata](https://www.amazon.in/Mahabharata-C-Rajagopalachari/dp/8172764766), sparked my curiosity about the intricate web of relationships within the epic. The idea of translating these connections into a powerful graph model, leveraging the capabilities of [Neo4j](www.neo4j.com) (a leader in Graph Database Industry), became an irresistible challenge.

![alt text](https://github.com/sidagarwal04/mahabharata-genai/blob/main/frontend/public/images/dall-e-mahabharata.png)

This is when I decided to embark on a fascinating journey to explore the Mahabharata through the lens of graph theory. But this was just the first chapter in my journey. I then decided to unveil an ambitious step forward: a Neo4j-powered chatbot. This innovative tool stems from a desire to make the epic’s complex relationships accessible to everyone, transcending traditional query methods.

Read the three-part blog series on this project:

+ [Unveiling the Mahabharata’s Web: A Graph Journey using Neo4j — (Part 1)](https://sidagarwal04.medium.com/unveiling-the-mahabharatas-web-a-graph-journey-using-neo4j-from-epic-relationships-to-7be4a7a29b6d)
+ [Bringing the Mahabharata Epic to Life: A Neo4j-Powered Chatbot using Google Gemini — (Part 2)](https://sidagarwal04.medium.com/bringing-the-mahabharata-epic-to-life-a-neo4j-powered-chatbot-using-google-gemini-part-2-6eef8676e757)
+ [From Ancient Epic to Modern Marvel: Demystifying the Mahabharata Chatbot with GraphRAG (Part 3)](https://medium.com/@sidagarwal04/from-ancient-epic-to-modern-marvel-demystifying-the-mahabharata-chatbot-with-graphrag-part-3-5942260a9560)

Learn more about GraphRAG: [Building a GraphRAG application](https://neo4j.com/developer-blog/knowledge-graph-rag-application/)

## 🚀 Deployment

This application supports modern cloud deployment with separate backend and frontend services:
- **Backend**: Compatible with Render, Railway, or any FastAPI-supporting platform
- **Frontend**: Deployable on Netlify, Vercel, or similar static hosting services
- **Database**: Neo4j AuraDB for managed cloud database

For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 💻 Local Development

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **Neo4j Database** (with your Mahabharata data loaded)
- **OpenAI API Key**
- **Sarvam AI API Key** (for Hindi translation and audio)

### Backend Setup

1. **Clone and navigate to the project**:
```bash
git clone https://github.com/sidagarwal04/mahabharata-genai.git
cd mahabharata-genai/backend
```

2. **Create and activate virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp example.backend.env .env
# Edit .env with your API keys and database credentials
```

5. **Start the backend server**:
```bash
uvicorn main:app --reload --port 8001
```

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Configure environment**:
```bash
cp example.frontend.env .env
# Edit .env with your backend URL
```

4. **Start development server**:
```bash
npm run dev
```

### Database Setup

1. **Install Neo4j**: Follow the official [Neo4j installation guide](https://neo4j.com/docs/operations-manual/current/installation/)
2. **Load Mahabharata data**: Use the provided [mahabharata-db-setup.cypher](backend/mahabharata-db-setup.cypher) script
3. **Configure connection**: Update your `.env` file with Neo4j credentials

### Environment Configuration

**Backend Environment (`backend/.env`)**:
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
NEO4J_DATABASE=neo4j

# Sarvam AI (for Hindi features)
SARVAM_API_KEY=your_sarvam_api_key_here

# Optional: Google Cloud Project ID
PROJECT_ID=your_google_cloud_project_id
```

**Frontend Environment (`frontend/.env`)**:
```env
# Backend API URL
API_BASE_URL=http://localhost:8001
```

## 🌍 Background & Story

Have you ever been captivated by a story brimming with complex relationships? The Mahabharata, an ancient Indian epic, weaves a spell with a multitude of characters and their intricate connections. These relationships form the foundation of the narrative, driving the plot and shaping destinies.

It all began with a conversation when my wife, reading C. Rajagopalachari's masterful [Mahabharata translation](https://www.amazon.in/Mahabharata-C-Rajagopalachari/dp/8172764766), sparked my curiosity about the epic's intricate relationship web. This inspired me to translate these connections into a powerful graph model using [Neo4j](https://neo4j.com).

![Mahabharata AI Visualization](https://github.com/sidagarwal04/mahabharata-genai/blob/main/frontend/public/images/dall-e-mahabharata.png)

This journey evolved from exploring the Mahabharata through graph theory to creating an innovative Neo4j-powered chatbot that makes the epic's complex relationships accessible to everyone.

### 📖 Blog Series

Read the comprehensive three-part blog series on this project:

1. [Unveiling the Mahabharata's Web: A Graph Journey using Neo4j — (Part 1)](https://sidagarwal04.medium.com/unveiling-the-mahabharatas-web-a-graph-journey-using-neo4j-from-epic-relationships-to-7be4a7a29b6d)
2. [Bringing the Mahabharata Epic to Life: A Neo4j-Powered Chatbot using Google Gemini — (Part 2)](https://sidagarwal04.medium.com/bringing-the-mahabharata-epic-to-life-a-neo4j-powered-chatbot-using-google-gemini-part-2-6eef8676e757)
3. [From Ancient Epic to Modern Marvel: Demystifying the Mahabharata Chatbot with GraphRAG (Part 3)](https://medium.com/@sidagarwal04/from-ancient-epic-to-modern-marvel-demystifying-the-mahabharata-chatbot-with-graphrag-part-3-5942260a9560)

Learn more about GraphRAG: [Building a GraphRAG application](https://neo4j.com/developer-blog/knowledge-graph-rag-application/)

## 🚀 Deployment

This application supports modern cloud deployment with separate backend and frontend services:

- **Backend**: Compatible with Render, Railway, or any FastAPI-supporting platform
- **Frontend**: Deployable on Netlify, Vercel, or similar static hosting services
- **Database**: Neo4j AuraDB for managed cloud database

For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 🤝 Contributing

We welcome contributions to make the Mahabharata chatbot the best resource for exploring this epic tale! 

**Share your feedback**: [Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSdradX2oOSBpBGAla01tEroQJGDrA62ZsD8Sa_x7IXbGjkRfg/viewform)

**Contributing Guidelines**:
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Make your changes and commit: `git commit -m 'Add some feature'`
4. Push to your branch: `git push origin feature/YourFeature`
5. Create a pull request

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).

## 🙏 Acknowledgements

Special thanks to:
- **[Vrijraj Singh](https://vrijraj.xyz/)** - For exceptional support with web design and development
- **[LLM Graph Builder Tool](https://neo4j.com/labs/genai-ecosystem/llm-graph-builder/)** - For converting PDF sources into Knowledge Graphs
- **The open-source community** - For valuable resources and support
- **C. Rajagopalachari** - For the masterful Mahabharata translation that inspired this project

---

⭐ **If you find this project helpful, please give it a star!** ⭐
