# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirement.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirement.txt

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Copy project files
COPY . /app/

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the ports
EXPOSE 8000 80

# Collect static files
RUN python manage.py collectstatic --noinput

# Create entrypoint script
RUN echo '#!/bin/bash\n\
gunicorn --bind 0.0.0.0:8000 backend.wsgi:application &\n\
nginx -g "daemon off;"' > /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Run the entrypoint script
CMD ["/entrypoint.sh"]
