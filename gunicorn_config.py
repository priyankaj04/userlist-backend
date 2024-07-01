# Gunicorn configuration file: `backend/gunicorn_config_read.py`

# The address (IP and port) on which the application will listen.
# In this case, it's localhost (127.0.0.1) on port 8000.
bind = "127.0.0.1:8000"

# The number of worker processes for handling requests.
# A larger number might be needed for handling a high number of requests.
workers = 3

# The number of threads to use for each worker process.
# This is only relevant for certain types of worker classes, like 'gthread'.
threads = 3

# The type of worker processes to run.
# 'gthread' is a threaded worker type provided by gunicorn.
worker_class = "gthread"

# The maximum amount of time a worker can take to respond to a request.
# If a worker takes longer than this, it will be killed and replaced.
timeout = 30

# The maximum number of requests a worker will process before restarting.
# This can help prevent memory leaks from affecting the application.
max_requests = 1000

# The maximum jitter added to the `max_requests` setting.
# This can help prevent all workers from restarting at the same time.
max_requests_jitter = 50