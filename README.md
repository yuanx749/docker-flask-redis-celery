# docker-flask-redis-celery
## install [docker](https://docs.docker.com/install/linux/linux-postinstall/)
```bash
sudo apt-get update
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
sudo usermod -aG docker $USER
newgrp docker
```
## install [docker-compose](https://docs.docker.com/compose/install/)
```bash
curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
## run
```bash
docker-compose build
docker-compose up --scale worker=3
```