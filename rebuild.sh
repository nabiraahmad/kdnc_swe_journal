#!/bin/bash
# This runs on PythonAnywhere servers: fetches new code,
# installs needed packages, and restarts the server.

touch rebuild
echo "Rebuilding $PA_DOMAIN"

echo "Pulling code from master"
git pull origin master

echo "Activate the virtual env $VENV for user $PA_USER"
source /home/$PA_USER/kdnc_swe_journal/$VENV/bin/activate

echo "Install packages"
pip install --upgrade -r requirements.txt

echo "Going to reboot the webserver using $API_TOKEN"
touch /var/www/$PA_DOMAIN_wsgi.py

touch reboot
echo "Finished rebuild."
