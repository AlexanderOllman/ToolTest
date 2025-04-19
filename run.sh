#!/usr/bin/env bash

set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "🔧 Starting setup for Agentic Framework on macOS..."

# 1. Install Homebrew if not installed
if ! command_exists brew; then
    echo "🍺 Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 2. Install Python 3.10+ if not installed
if ! command_exists python3; then
    echo "🐍 Python3 not found. Installing Python3..."
    brew install python
fi

# 3. Install Node.js 18+ if not installed
if ! command_exists node; then
    echo "🟢 Node.js not found. Installing Node.js..."
    brew install node
fi

# 4. Install Git if not installed
if ! command_exists git; then
    echo "🔧 Git not found. Installing Git..."
    brew install git
fi

# 5. Install Tesseract (optional, for GUI text detection)
if ! command_exists tesseract; then
    echo "🖼️ Tesseract not found. Installing Tesseract..."
    brew install tesseract
fi

# 6. Clone the Agent Framework repository if not already present
if [ ! -d "agent_framework" ]; then
    echo "📁 Cloning Agent Framework repository..."
    git clone https://github.com/AlexanderOllman/ToolTest.git
fi

cd agent_framework

# 7. Set up Python virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 Setting up Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# 8. Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# 9. Install MCPO server if not installed
if ! command_exists mcpo; then
    echo "🧠 MCPO server not found. Installing MCPO server..."
    pip3 install mcpo
fi

# 10. Start MCPO server
echo "🚀 Starting MCPO server..."
mcpo run mcpo.json &

# 11. Start GUI agent
echo "🖥️ Starting GUI agent..."
python servers/gui_agent/server.py &

# 12. Start OAuth service
echo "🔐 Starting OAuth service..."
uvicorn oauth_service:app --port 9300 &

# 13. Start Task Executor
echo "⚙️ Starting Task Executor..."
uvicorn task_executor:app --port 8001 &

# 14. Set up and start the front-end
cd ui

echo "📦 Installing Node.js dependencies..."
npm install

echo "🖼️ Starting Electron + Next.js UI..."
npm run dev

echo "✅ Agentic Framework setup complete!"

