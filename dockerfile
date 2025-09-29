FROM ubuntu:22.04

# Установите зависимости
RUN apt update && apt install -y \
    python3 python3-pip git zip unzip openjdk-8-jdk \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
    && pip3 install buildozer

WORKDIR /app
