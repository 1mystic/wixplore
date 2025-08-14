#!/bin/bash

# Development runner script for wixplore refactored app

echo "🚀 Starting wixplore development servers..."

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down development servers..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Start API server in background
echo "🔧 Starting Node.js API server on port 5000..."
cd api && npm run dev &
API_PID=$!

# Wait a moment for API to start
sleep 2

# Start frontend server in background
echo "🎨 Starting Vue frontend on port 3000..."
cd ../frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Development servers started!"
echo "   Frontend: http://localhost:3000"
echo "   API:      http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for background processes
wait
