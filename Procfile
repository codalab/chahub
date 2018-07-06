# NOTE: We have to move pgbouncer files properly
web: cp -rn bin src/bin && cd src && bin/start-pgbouncer-stunnel daphne asgi:application --port $PORT --bind 0.0.0.0 -v2
