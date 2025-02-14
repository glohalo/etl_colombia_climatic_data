FROM seleniarm/standalone-chromium:latest

# Switch to root user to install dependencies
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg2 \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libgdk-pixbuf2.0-0 \
    libxcomposite1 \
    libasound2 \
    libxrandr2 \
    libatk1.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install a compatible version of Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /src

# Copy requirements 
COPY requirements.txt .

# Create a virtual environment 
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Set the PATH to include the virtual environment
ENV PATH="/src/venv/bin:$PATH"

# Create necessary directories
RUN mkdir -p /data/bronze /data/silver /data/gold/

# Copy application code
COPY src/ /src/
COPY data/ /data/
COPY notebooks/ /src/notebooks/
COPY tests/ /src/tests/

# Switch back to the default user (selenium)
USER 1200

# Set the default command
CMD ["python3", "orchestrator.py"]