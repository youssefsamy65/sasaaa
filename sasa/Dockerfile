# Use an official Python runtime as a parent image
FROM python:3.10-slim



# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install build dependencies and necessary libraries
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libasound-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    tk \
    libglib2.0-0 \
    libasound2 \
    pulseaudio \
    pulseaudio-utils \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*
# Add a non-root user


# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run application
CMD ["python", "GeminiArabic.py"]

