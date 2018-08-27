# NOTE: We want to start in the `src/` directory for all of our Python paths
#web: bin/start-pgbouncer sh -c 'cd src/ && exec uvicorn asgi:application --port $PORT --host 0.0.0.0 -v2'
web: bin/start-pgbouncer sh -c 'cd src/ && exec gunicorn asgi:application -k uvicorn.workers.UvicornWorker --threads 2 --max-requests 100 --bind 0.0.0.0:$PORT'
