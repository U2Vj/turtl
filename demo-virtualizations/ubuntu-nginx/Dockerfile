FROM ubuntu:latest

RUN apt update
RUN apt install -y openssh-server && systemctl enable ssh
RUN apt install telnetd -y

EXPOSE 22
EXPOSE 23

CMD tail -F /dev/null