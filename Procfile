web: flask db upgrade; gunicorn testovac:app
worker: rq worker -u $REDIS_URL testovac-judge