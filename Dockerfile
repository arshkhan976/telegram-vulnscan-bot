FROM python:3.10-slim

# System dependencies required for WeasyPrint (for PDF generation)
RUN apt update && apt install -y \
    nmap \
    curl \
    openjdk-11-jre-headless \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    libffi-dev \
    build-essential \
    libssl-dev \
    && apt clean

# Create app directory
WORKDIR /app

# Copy your project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port (optional, if using ZAP or webhook)
EXPOSE 8080

# Run the bot
CMD ["python", "bot.py"]
