#!/bin/bash

# Update package lists
echo "Updating package lists..."
sudo apt update -y && sudo apt upgrade -y

# Install Python3 and pip
echo "Installing Python3 and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install MySQL server and client
echo "Installing MySQL server and client..."
sudo apt install -y mysql-server mysql-client

# Install necessary Python packages
echo "Installing required Python packages..."
pip3 install --upgrade pip
pip3 install mysql-connector-python mysqlclient

echo "Installation completed successfully!"
