FROM python:3.10-slim
RUN apt update && apt install -y nmap curl openjdk-11-jre-headless weasyprint
RUN curl -sL https://github.com/zaproxy/zaproxy/releases/download/v2.14.0/ZAP_2.14.0_Linux.tar.gz \
    | tar xz -C /opt && ln -s /opt/ZAP_2.14.0/zap.sh /usr/bin/zap.sh
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "bot.py"]
