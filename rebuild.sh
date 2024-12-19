#!/bin/bash
# This runs on PythonAnywhere servers: fetches new code,
# installs needed packages, and restarts the server.

# Set environment variables
PROJECT_DIR="/home/ktn3138/kdnc_swe_journal"
VENV_PATH="$PROJECT_DIR/venv"
WSGI_PATH="/var/www/ktn3138.pythonanywhere_com_wsgi.py"

echo "Rebuilding the web app for $PROJECT_DIR"

# Navigate to the project directory
echo "Navigating to the project directory..."
cd $PROJECT_DIR || { echo "Error: Project directory not found!"; exit 1; }

# Debug: Show current directory and contents
echo "Current directory: $(pwd)"
ls -a

# Verify we are in the Git repository
if [ ! -d ".git" ]; then
    echo "Error: Not a Git repository. Aborting."
    exit 1
fi

# Pull the latest code
echo "Pulling code from GitHub..."
git pull || { echo "Git pull failed!"; exit 1; }

# Activate the virtual environment
echo "Activating the virtual environment..."
source $VENV_PATH/bin/activate || { echo "Virtual environment activation failed!"; exit 1; }

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade -r requirements.txt || { echo "Dependency installation failed!"; exit 1; }

# Restart the web server
echo "Restarting the web server..."
touch $WSGI_PATH || { echo "Failed to restart web server!"; exit 1; }

echo "Rebuild finished successfully."
