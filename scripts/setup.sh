#!/bin/bash

# Install helper programms
echo "Installing helper programms..."
apt-get update && \
apt-get install -y htop nload nano && \
apt-get install -y git-lfs && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

# Install NGROK
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -O /workspace/ngrok-v3-stable-linux-amd64.tgz
mkdir /workspace/ngrok
tar xvzf /workspace/ngrok-v3-stable-linux-amd64.tgz -C /workspace/ngrok
export PATH=$PATH:/workspace/ngrok

# Set up git
git lfs install
git config --global user.email "$GIT_USERNAME$"  # suppose you use the email address as your username
cd /workspace/volateq_mlapi/
git lfs pull

# Install Miniforge and Mamba
echo "Installing Miniforge..."
cd /workspace/
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O /workspace/Miniforge3.sh
bash /workspace/Miniforge3.sh -b -p /workspace/miniforge3
rm /workspace/Miniforge3.sh
echo 'export PATH="/workspace/miniforge3/bin:$PATH"' >> ~/.bashrc

source /workspace/miniforge3/bin/activate # required so the rest of the script works as intended

# Create and activate the virtual environment
echo "Creating Mamba environment..."
mamba env create -f /workspace/volateq_mlapi/conda_env_s3.yml
conda activate inference_api

# Add Virtual Environment to Jupyter Notebook
python -m ipykernel install --user --name=inference_api

# Clone the YOLOv5 Repository
echo "Cloning repositories..."
git clone https://github.com/ultralytics/yolov5.git /workspace/yolov5
cd /workspace/yolov5
git checkout tags/v7.0

# Install YOLOv5 Python dependencies
cd /workspace/yolov5
pip install --cache-dir=/workspace/.pip-cache -r requirements.txt

# Correct erroneous yolo wandb logger init
chmod +x /workspace/volateq_mlapi/scripts/modify_yolo_logger_init.sh
. /workspace/volateq_mlapi/scripts/modify_yolo_logger_init.sh

# # Start NGROK
# ngrok config add-authtoken $ngrok_auth_token
# # start ngrok in the background and point it at the API
# # nohup ngrok http --domain=$ngrok_static_domain 8000 &  # start with static domain
# nohup ngrok http 8000 &  # Start with ephemeral domain

# Start app
conda activate inference_api
# cd /workspace/volateq_mlapi/source
# uvicorn ML_api:app --host 0.0.0.0 --port 8000 --reload

# Initialize Conda for bash
conda init bash
source ~/.bashrc
