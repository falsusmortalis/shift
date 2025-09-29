FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Установите зависимости
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    wget \
    curl \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Создайте пользователя с таким же UID как на хосте
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g $GROUP_ID builder && \
    useradd -m -u $USER_ID -g $GROUP_ID builder && \
    mkdir -p /app && \
    chown -R builder:builder /app

# Установите Buildozer
RUN pip3 install --upgrade buildozer cython virtualenv

# Переключитесь на пользователя
USER builder
WORKDIR /app

CMD ["buildozer", "--version"]
