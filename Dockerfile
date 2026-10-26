FROM ubuntu:latest

RUN apt-getupdate && apt-get install -y \ 
    python3.x \ 
    python3-pip \ 
    git

RUN pip3 install PyYAML 

COPY feed.py /usr/bin/feed.py 

COPY entrypoint.sh /entrypoint.sh 

ENTRYPOINT ["/entrypoint.sh"] 