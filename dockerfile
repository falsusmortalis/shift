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

# Установите Buildozer
RUN pip3 install --upgrade buildozer cython virtualenv

# Создайте не-root пользователя
RUN useradd -m -u 1000 builder && \
    echo "builder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Переключитесь на не-root пользователя
USER builder
WORKDIR /app

CMD ["buildozer", "--version"]
