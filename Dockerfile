# Use official Python slim image (Debian-based)
FROM python:3.11-slim

# Install ffmpeg (moviepy needs ffmpeg binary)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy server script
COPY video_server.py /app/video_server.py

# Install Python dependencies
RUN pip install --no-cache-dir moviepy

# Expose port 8080
EXPOSE 8080

# Run the server
CMD ["python", "video_server.py"]
