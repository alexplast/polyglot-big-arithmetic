# Используем последнюю LTS версию Ubuntu (24.04 Noble Numbat)
FROM ubuntu:24.04

# Отключаем интерактивные запросы
ENV DEBIAN_FRONTEND=noninteractive

# 1. Системные зависимости и компиляторы
# Добавляем libgmp-dev для C++ GMP бенчмарков
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgmp-dev \
    gfortran \
    python3 \
    python3-pip \
    python3-matplotlib \
    openjdk-21-jdk \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Установка Node.js (v22 - Latest Current)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# 3. Установка Golang (1.23.4 - Latest Stable)
ENV GO_VERSION=1.23.4
RUN curl -OL https://golang.org/dl/go${GO_VERSION}.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz && \
    rm go${GO_VERSION}.linux-amd64.tar.gz

ENV PATH=$PATH:/usr/local/go/bin

# 4. Установка Rust (Latest Stable)
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH

# Используем profile minimal для ускорения (без docs и rustfmt)
RUN curl --proto '=https' --tlsv1.2 -fL https://sh.rustup.rs -o rustup-init.sh && \
    chmod +x rustup-init.sh && \
    ./rustup-init.sh -y --no-modify-path --profile minimal --default-toolchain stable && \
    rm rustup-init.sh && \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME

# Настройка рабочей директории
WORKDIR /app

# По умолчанию выводим справку
CMD ["make", "help"]
