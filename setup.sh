#!/bin/bash

# Setup script for Predictive Student Performance Application
# This script automates the setup process for both backend and frontend

echo "=================================================="
echo "Student Performance Predictor - Setup Script"
echo "=================================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check Python version
print_info "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    print_success "Python 3 found: $(python3 --version)"
else
    print_error "Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check Node.js version
print_info "Checking Node.js version..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
else
    print_error "Node.js not found. Please install Node.js 14 or higher."
    exit 1
fi

echo ""
echo "=================================================="
echo "Setting up Backend"
echo "=================================================="
echo ""

# Navigate to backend directory
cd backend

# Create virtual environment
print_info "Creating Python virtual environment..."
python3 -m venv venv
print_success "Virtual environment created"

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install backend dependencies
print_info "Installing Python dependencies (this may take a few minutes)..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Backend dependencies installed"
else
    print_error "Failed to install backend dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f "../.env" ]; then
    print_info "Creating .env file..."
    cp ../.env.example ../.env
    print_success ".env file created"
    print_info "Please edit .env file to add your API keys"
else
    print_info ".env file already exists"
fi

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p data/uploads
mkdir -p models
print_success "Directories created"

cd ..

echo ""
echo "=================================================="
echo "Setting up Frontend"
echo "=================================================="
echo ""

# Navigate to frontend directory
cd frontend

# Install frontend dependencies
print_info "Installing Node.js dependencies (this may take a few minutes)..."
npm install > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Frontend dependencies installed"
else
    print_error "Failed to install frontend dependencies"
    exit 1
fi

cd ..

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start the Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "2. In a new terminal, start the Frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Open your browser to http://localhost:3000"
echo ""
echo "For more information, see README.md"
echo ""
print_success "Happy coding! 🚀"
