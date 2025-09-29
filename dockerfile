FROM ubuntu:22.04

# Установите переменные окружения
ENV DEBIAN_FRONTEND=noninteractive

# Обновите и установите все зависимости
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
    && rm -rf /var/lib/apt/lists/*

# Установите Buildozer
RUN pip3 install --upgrade buildozer cython virtualenv

# Создайте рабочую директорию
WORKDIR /app

# Установите команду по умолчанию
CMD ["buildozer", "--version"]
