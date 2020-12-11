import celery
import time
import os


app = celery.Celery()
app.conf.update(BROKER_URL=os.getenv('REDISTOGO_URL', 'redis://redis:6379/0'),
                CELERY_ROUTES={
                    'predict': {'queue': 'predict'}
                },
                CELERY_RESULT_BACKEND=os.getenv('REDIS_URL', 'redis://redis:6379/0'),
                BROKER_POOL_LIMIT=None)


@app.task(name='predict')
def predict():
    print('starting predict')
    time.sleep(5)
    print('ending predict')
    return 'result'
