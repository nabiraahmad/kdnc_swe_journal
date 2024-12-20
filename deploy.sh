#!/bin/bash
# This shell script deploys a new version to a server.

PROJ_DIR="kdnc_swe_journal"
VENV="venv"
PA_DOMAIN="ktn3138.pythonanywhere.com"
PA_USER="ktn3138"

echo "Project dir = $PROJ_DIR"
echo "PA domain = $PA_DOMAIN"
echo "Virtual env = $VENV"
echo "PA user = $PA_USER"
echo "Token = $API_TOKEN"

if [ -z "$DEMO_PA_PWD" ]; then
    echo "The PythonAnywhere password var (DEMO_PA_PWD) must be set in the env."
    exit 1
fi

echo "PA password = $DEMO_PA_PWD"

echo "SSHing to PythonAnywhere."
sshpass -p $DEMO_PA_PWD ssh -o "StrictHostKeyChecking no" $PA_USER@ssh.pythonanywhere.com << EOF
    export PA_DOMAIN=$PA_DOMAIN
    export API_TOKEN=$API_TOKEN
    export VENV=$VENV
    export PA_USER=$PA_USER
    cd /home/$PA_USER/$PROJ_DIR
    ./rebuild.sh
EOF

echo "Deployment completed successfully."
