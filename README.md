# Django Nginx Gunicorn Project

## Overview

This repository contains the code for a Django web application configured to run with Nginx and Gunicorn. The following instructions will guide you through the setup, installation, and running of the application both locally and via Docker.

## Requirements

- Python 3.x
- Django 3.x
- Gunicorn
- Nginx
- Postgresql

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/priyankaj04/userlist-backend.git
cd userlist-backend
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirement.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Collect Static Files
```bash
python manage.py collectstatic
```

### 6. Run the Application with Gunicorn
```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

## Running through Docker

### Build and Run the Docker Containers
```bash
docker-compose up --build
```

### Database Model: 
<img width="527" alt="Screenshot 2024-07-01 at 5 20 20 AM" src="https://github.com/priyankaj04/userlist-backend/assets/103273242/b64220b4-e151-4afb-981f-3e6505f1b5a8">

### Thankyou
