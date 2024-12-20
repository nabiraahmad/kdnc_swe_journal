#!/bin/bash
# This runs on PythonAnywhere servers: fetches new code,
# installs needed packages, and restarts the server.

# Set environment variables
# PROJECT_DIR="/home/ktn3138/kdnc_swe_journal"
# VENV_PATH="$PROJECT_DIR/venv"
# WSGI_PATH="/var/www/ktn3138_pythonanywhere_com_wsgi.py"

# echo "Rebuilding the web app for $PROJECT_DIR"

# Navigate to the project directory
# echo "Navigating to the project directory..."
# cd $PROJECT_DIR || { echo "Error: Project directory not found!"; exit 1; }

# Verify we are in the Git repository
# if [ ! -d ".git" ]; then
#     echo "Error: Not a Git repository. Aborting."
#     exit 1
# fi

# Pull the latest code
# echo "Pulling code from GitHub..."
# git pull || { echo "Git pull failed!"; exit 1; }

# Activate the virtual environment
# echo "Activating the virtual environment..."
# source $VENV_PATH/bin/activate || { echo "Virtual environment activation failed!"; exit 1; }

# Install dependencies
# echo "Installing dependencies..."
# pip install --upgrade -r requirements.txt || { echo "Dependency installation failed!"; exit 1; }

# Restart the web server
# echo "Restarting the web server..."
# touch $WSGI_PATH || { echo "Failed to restart web server!"; exit 1; }

# echo "Rebuild finished successfully."

PROJECT_DIR="/home/ktn3138/kdnc_swe_journal"
VENV_PATH="$PROJECT_DIR/venv"

touch rebuild

cd $PROJECT_DIR || { echo "Error: Project directory not found!"; exit 1; }

echo "Pulling code from master"
git pull origin master || { echo "Git pull failed!"; exit 1; }

echo "Activate the virtual env $VENV for user $PA_USER"
# source /home/$PA_USER/.virtualenvs/$VENV/bin/activate
source $VENV_PATH/bin/activate || { echo "Virtual environment activation failed!"; exit 1; }

echo "Install packages"
pip install --upgrade -r requirements.txt

export API_TOKEN="$API_TOKEN"
echo "Going to reboot the webserver using $API_TOKEN"
pa_reload_webapp.py $PA_DOMAIN

touch reboot
echo "Finished rebuild."
