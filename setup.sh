#!/bin/bash

# Development setup script for wixplore refactored app

echo " Setting up wixplore development environment..."

# Install frontend dependencies
echo " Installing frontend dependencies..."
cd frontend && npm install
if [ $? -ne 0 ]; then
    echo "❌ Frontend dependency installation failed"
    exit 1
fi

# Install API dependencies
echo "📦 Installing API dependencies..."
cd ../api && npm install
if [ $? -ne 0 ]; then
    echo "❌ API dependency installation failed"
    exit 1
fi

# Install Python agent dependencies
echo "🐍 Installing Python agent dependencies..."
cd ../agents
if command -v python3 &> /dev/null; then
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "⚠️  Python dependency installation failed - some agent features may not work"
    fi
else
    echo "⚠️  Python3 not found - some agent features may not work"
fi

# Copy environment file
cd ..
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file - please update with your configuration"
fi

echo "✅ Setup complete!"
echo ""
echo "To start development:"
echo "  npm run dev:frontend    # Start Vue frontend (port 3000)"
echo "  npm run dev:api         # Start Node.js API (port 5000)"
echo ""
echo "Or use the combined development script:"
echo "  ./dev.sh"
