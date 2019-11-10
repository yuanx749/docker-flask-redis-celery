FROM python:3
WORKDIR /home/user/app/
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["/bin/bash"]