#!/bin/bash
# filepath: /home/pi/git/TFLuna-Pi/update_tfluna.sh

# Define variables
SERVICE_NAME="tfluna.service"
REPO_DIR="/home/pi/git/TFLuna-Pi"

# Navigate to the repository directory
cd "$REPO_DIR" || { echo "Failed to navigate to $REPO_DIR"; exit 1; }

# Pull the latest changes from the repository
echo "Pulling latest changes from Git..."
git pull || { echo "Git pull failed"; exit 1; }

# Reload and restart the systemd service
echo "Reloading and restarting the $SERVICE_NAME service..."
sudo systemctl daemon-reload
sudo systemctl restart "$SERVICE_NAME" || { echo "Failed to restart $SERVICE_NAME"; exit 1; }

echo "Update and service restart completed successfully."