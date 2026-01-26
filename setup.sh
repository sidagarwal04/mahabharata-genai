#!/bin/bash

# Mahabharata AI Sage - Setup Script

echo "🏛️ Mahabharata AI Sage - Initial Setup"
echo "====================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

echo "✅ Python and Node.js found"

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "✅ Python virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
else
    pip install -r requirements.txt
fi

# Setup environment files
echo "⚙️ Setting up environment configuration..."

# Backend environment
if [ ! -f "backend/.env" ]; then
    if [ -f "backend/example.backend.env" ]; then
        cp backend/example.backend.env backend/.env
        echo "📋 Created backend/.env from backend/example.backend.env"
        echo "⚠️  Please edit backend/.env with your actual credentials"
    fi
else
    echo "✅ Backend .env file already exists"
fi

# Frontend environment
cd frontend

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Frontend environment
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📋 Created frontend .env from .env.example"
else
    echo "✅ Frontend .env file already exists"
fi

cd ..

echo ""
echo "🎉 Setup completed!"
echo "=================="
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys and database credentials"
echo "2. Edit frontend/.env if needed (defaults should work for development)"
echo "3. Run './start-dev.sh' to start both backend and frontend servers"
echo ""
echo "📚 Required environment variables in .env:"
echo "   - OPENAI_API_KEY (for GPT-5.2)"
echo "   - NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE"
echo "   - PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS (for translation)"
echo "   - ELEVENLABS_API_KEY (for Hindi audio)"
echo ""