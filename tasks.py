from celery import Celery
import time

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
app_celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app_celery.conf.worker_prefetch_multiplier = 1

@app_celery.task()
def test(n):
    time.sleep(n)
    return 'hello'

if __name__ == "__main__":
    app_celery.start(['celery', 'worker', '-l', 'info'])