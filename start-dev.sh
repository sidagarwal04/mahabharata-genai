#!/bin/bash

# Mahabharata AI Sage - Development Startup Script

echo "🚀 Starting Mahabharata AI Sage Development Environment"
echo "=================================================="

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Backend .env file not found. Please copy example.backend.env to .env and configure it."
    exit 1
fi

# Check if frontend .env file exists
if [ ! -f "frontend/.env" ]; then
    echo "❌ Frontend .env file not found. Please copy frontend/.env.example to frontend/.env and configure it."
    exit 1
fi

echo "✅ Environment files found"

# Activate virtual environment
echo "🐍 Activating Python virtual environment..."
source venv/bin/activate

# Install Python dependencies if needed
echo "📦 Checking Python dependencies..."
pip install -q -r requirements.txt

# Start backend server in background
echo "🚀 Starting FastAPI backend server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 3

# Install frontend dependencies if needed
echo "📦 Checking Frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Start frontend development server
echo "🎨 Starting Nuxt.js frontend server..."
npm run dev &
FRONTEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on SIGINT (Ctrl+C)
trap cleanup SIGINT

echo ""
echo "🎉 Development environment is ready!"
echo "=================================="
echo "📋 Backend API: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for servers
wait