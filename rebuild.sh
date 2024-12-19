#!/bin/bash
# This runs on PythonAnywhere servers: fetches new code,
# installs needed packages, and restarts the server.

PROJECT_DIR="/home/$PA_USER/$PROJ_DIR"
VENV_PATH="$PROJECT_DIR/$VENV"
WSGI_PATH="/var/www/$PA_DOMAIN_wsgi.py"

touch rebuild
echo "Rebuilding $PA_DOMAIN"

cd $PROJECT_DIR || { echo "Project directory not found!"; exit 1; }

echo "Pulling code from master"
git pull origin master || { echo "Git pull failed!"; exit 1; }

echo "Activate the virtual env $VENV for user $PA_USER"
source $VENV_PATH/bin/activate || { echo "Virtual environment activation failed!"; exit 1; }

echo "Install packages"
pip install --upgrade -r requirements.txt

echo "Restarting the web server"
touch $WSGI_PATH || { echo "Failed to restart web server!"; exit 1; }

touch reboot
echo "Finished rebuild."
