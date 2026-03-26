#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Dog Shelter Application Startup${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

# Install backend dependencies
echo -e "\n${GREEN}[1/4] Installing Python dependencies...${NC}"
cd server
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt

# Install frontend dependencies
echo -e "\n${GREEN}[2/4] Installing Node dependencies...${NC}"
cd ../client
npm install --silent

# Start the backend server
echo -e "\n${GREEN}[3/4] Starting Flask backend server...${NC}"
cd ../server
source venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
python3 app.py &
BACKEND_PID=$!
echo -e "${BLUE}Backend running on http://localhost:5100 (PID: $BACKEND_PID)${NC}"

# Wait for backend to be ready
sleep 2

# Start the frontend server
echo -e "\n${GREEN}[4/4] Starting Astro frontend server...${NC}"
cd ../client
npm run dev &
FRONTEND_PID=$!
echo -e "${BLUE}Frontend running on http://localhost:4321 (PID: $FRONTEND_PID)${NC}"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  Application is running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "Frontend: ${BLUE}http://localhost:4321${NC}"
echo -e "Backend:  ${BLUE}http://localhost:5100${NC}"
echo -e "\nPress ${RED}Ctrl+C${NC} to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${RED}Shutting down servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
