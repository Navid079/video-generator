FROM python:3.11

# Install ffmpeg and any missing video/image dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 libgl1 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your app code
COPY video_server.py .

# Install Python dependencies
RUN pip install --no-cache-dir moviepy

# Expose the port your server listens on
EXPOSE 4444

# Run the server
CMD ["python", "video_server.py"]
