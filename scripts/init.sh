#!/bin/bash

# Step 1: Install helper programms
echo "Installing helper programs..."
apt-get update && \
apt-get install -y htop nload nano && \
apt-get install -y git-lfs && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

# Set up git
git lfs install
git config --global user.email "$GIT_USERNAME$"  # suppose you use the email address as your username
cd /workspace/DigTwins/
git lfs pull

# Activate conda base environment
echo 'export PATH="/workspace/miniforge3/bin:$PATH"' >> ~/.bashrc
source /workspace/miniforge3/bin/activate

# Initialize the YOLO environment
conda activate venv_DT
python -m ipykernel install --user --name=venv_DT

# Start app
cd /workspace/DigTwins/source
# uvicorn ML_api:app --host 0.0.0.0 --port 8000 --reload


# Initialize Conda for bash shell
conda init bash
source ~/.bashrc