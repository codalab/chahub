# ChaHub

Under construction!


## Installation locally

1. `git clone git@github.com:codalab/chahub.git`
1. `cd chahub`
1. Make a virtual environment and source into it
1. `pip install -r requirements.dev.txt`
1. `npm install -g npm-watch riot stylus`
1. `brew install elasticsearch` (defaults should work)


## Running it locally


`elasticsearch` in a different terminal tab to start running elasticsearch before running the server. On Mac you can `brew install elasticsearch`.

`python manage.py runserver` to start django which will automatically start `npm-watch` to compile riot (javascript components) and stylus (css preprocessor)


## Heroku installation

_NOTE: Todo!_

Add this buildpack:

https://github.com/heroku/heroku-buildpack-pgbouncer

Set these ENV vars:

```
WHITENOISE_ROOT=
```

# Production settings


```bash
# This environment variable passes arguments to gunicorn, tweak worker count here
export GUNICORN_CMD_ARGS="--workers=10"
```

To setup ElasticSearch data directory:
```bash
sudo chown 1000:1000 var/data/elasticsearch/
```
