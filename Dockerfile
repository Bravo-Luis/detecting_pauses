# Use netunicorn/chromium as the base image
FROM netunicorn/chromium:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN apt-get update && \
    apt-get install -y tshark && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt
