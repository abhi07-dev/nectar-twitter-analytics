#!/usr/bin/env bash
# INSTALL DOCKER
sudo apt-get remove docker docker-engine docker.io
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce
#sudo docker run hello-world

# INSTALL NODEJS
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
#sudo apt-get install -y build-essential

# INSTALL GRUNT
#sudo npm update -g npm
sudo npm install -g grunt
#npm install

# INSTALL JQ
sudo apt-get install jq