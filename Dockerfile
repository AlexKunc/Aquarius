FROM jenkins/jenkins:lts-jdk17

# Установка системных зависимостей
USER root
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    qemu-system-arm \
    python3-venv \
    python3-pip \
    chromium \
    chromium-driver \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Создание виртуального окружения Python
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Установка Python-зависимостей
RUN /opt/venv/bin/pip install --no-cache-dir \
    requests \
    pytest \
    selenium \
    locust \
    pytest-html \
    webdriver-manager

# Возвращаемся к пользователю jenkins
USER jenkins

# Установка необходимых Jenkins плагинов
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow"
