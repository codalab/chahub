# ChaHub

Under construction!


## Installation locally

1. `git clone git@github.com:codalab/chahub.git`
1. `cd chahub`
1. Make a virtual environment and source into it
1. `pip install -r requirements.dev.txt`


## Running it locally


`python manage.py runserver` to start django and `npm-watch` to compile riot (javascript components) and stylus (css preprocessor)


## Heroku installation

_NOTE: Todo!_

Add this buildpack:

https://github.com/heroku/heroku-buildpack-pgbouncer

Set these ENV vars:

```
WHITENOISE_ROOT=
```