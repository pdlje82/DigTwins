Preparation
This script assumes that the installation is done on a host (like runpod.io) with into 
the dir`/workspace/` (permanent volume). 

## Set up the runpod account
Use this description prepare your computer for runpod, in case you have not done it.
https://volateq.atlassian.net/wiki/spaces/STARTVOLAT/pages/3172007945/Set-up+Runpod

## Create a new runpod instance (if non exists)
```
runpodctl create pod --name 'TrainTestAPI' \
--imageName 'runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04' \
--gpuType 'NVIDIA GeForce RTX 3070' \
--communityCloud \
--ports 22/tcp \
--ports 8000/tcp \
--containerDiskSize 5 \
--volumePath '/workspace' \
--volumeSize 25 \
--gpuCount 1
```

### Set the GIT user credentials as secrets in the container
- ```GIT_USERNAME```    
  - if using an email address, make sure ti replace '@' with '%40', ie max.muster%40gmail.com
- ```GIT_TOKEN```

### Set the NGROK credentials as secrets in the container
- ```ngrok_auth_token```
- ```ngrok_static_domain```
 
```bash
git clone https://$GIT_USERNAME:$GIT_TOKEN@github.com/VolaTeQ/volateq_mlapi.git /workspace/volateq_mlapi/
```

### Run the script
```bash
cd /workspace/volateq_mlapi/scripts/
source setup.sh
```

## If the container was just restarted, use the the init script:
```bash
cd /workspace/volateq_mlapi/scripts/
source init.sh
```
## To just start the API, use
```bash
conda activate inference_api
cd /workspace/volateq_mlapi/source
# uvicorn ML_api:app --host 0.0.0.0 --port 8000 --reload
```

## Example for a Container Start Command
```
bash -c "apt update;apt install -y wget;DEBIAN_FRONTEND=noninteractive apt-get install openssh-server -y;mkdir -p ~/.ssh;cd $_;chmod 700 ~/.ssh;echo AAAAC3NzaC1lZDI1NTE5AAAAIAOYq9DxqWS8aySfTVW3zKXHBgKQURkZUc8JzaVf00UJ > authorized_keys;chmod 700 authorized_keys;service ssh start;sleep infinity"
```
