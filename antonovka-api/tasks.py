import celery
import time
import os
import run_inference


app = celery.Celery()
app.conf.update(BROKER_URL=os.getenv('REDISTOGO_URL', 'redis://redis:6379/0'),
                CELERY_ROUTES={
                    'predict': {'queue': 'predict'}
                },
                CELERY_RESULT_BACKEND=os.getenv('REDIS_URL', 'redis://redis:6379/0'),
                BROKER_POOL_LIMIT=None)

storage_folder = 'storage'
if not os.path.exists(storage_folder):
    os.mkdir(storage_folder)


class PredictTask(celery.Task):
    model_object = None

    @property
    def model(self):
        if self.model_object is None:
            print('loading model')
            self.model_object = run_inference.init_model('models/fold0.ckpt')
            print('finish loading model')
        return self.model_object


@app.task(base=PredictTask, name='predict')
def predict(filepath):
    start_pred = time.time()
    print('inference started')
    result = run_inference.predict(predict.model, filepath)
    end_pred = time.time()
    print('Run time:', end_pred - start_pred, 'seconds')
    return result
