# docker-flask-redis-celery
Skeleton code of distributed system for computational experiments on horizontal scalability.
- Celery is used to implement a MapReduce like workflow.
- Redis is used as broker, backend, and database.
- Gunicorn is used as web server for the Flask application.
## Install
[docker](https://docs.docker.com/install/linux/linux-postinstall/)
```bash
sudo apt-get update
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
sudo usermod -aG docker $USER
newgrp docker
```
[docker-compose](https://docs.docker.com/compose/install/)
```bash
curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
## Run
```bash
docker-compose build
docker-compose up --scale worker=3
curl -i http://localhost:5000/mapreduce/10
docker-compose down
```