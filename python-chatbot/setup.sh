#!/bin/bash
# Quick Start Script for Zer3aZ Python Chatbot

set -e

echo "================================================"
echo "Zer3aZ Chatbot - Quick Start Setup"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r python-chatbot/requirements.txt

echo ""
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f "python-chatbot/.env" ]; then
    echo "📝 Creating .env file from template..."
    cp python-chatbot/.env.example python-chatbot/.env
    echo "✓ .env file created. Please edit it with your API keys if needed."
else
    echo "✓ .env file already exists"
fi

echo ""
echo "================================================"
echo "Setup Complete! 🎉"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Test the configuration:"
echo "   python3 python-chatbot/test_chatbot.py"
echo ""
echo "2. Start the API server:"
echo "   python3 src/api/chatbot_api.py"
echo ""
echo "3. (Optional) Configure AI services:"
echo "   - Edit python-chatbot/.env with your API keys"
echo "   - Uncomment AI integration code in src/services/ai_service.py"
echo ""
echo "================================================"
