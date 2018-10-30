web: bin/start-pgbouncer sh -c 'cd src/ && exec gunicorn asgi:application -k uvicorn.workers.UvicornWorker --max-requests 100 --bind 0.0.0.0:$PORT'
