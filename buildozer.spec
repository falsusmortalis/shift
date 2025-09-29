FROM python:3.8-bullseye

# Установите зависимости
RUN apt-get update && apt-get install -y \
    git zip unzip openjdk-8-jdk \
    autoconf libtool pkg-config zlib1g-dev \
    libncurses5-dev libncursesw5-dev libtinfo5 \
    cmake libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Установите Buildozer
RUN pip install buildozer==1.4.0 cython==0.29.33

WORKDIR /app

# Создайте не-root пользователя
RUN useradd -m -u 1000 builder && chown -R builder:builder /app
USER builder

CMD ["buildozer", "--version"]
