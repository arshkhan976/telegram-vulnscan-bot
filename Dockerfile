FROM python:3.10-slim

# Install system packages
RUN apt update && apt install -y \
    nmap \
    curl \
    openjdk-11-jre-headless \
    weasyprint \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    && apt clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run bot
CMD ["python", "bot.py"]
