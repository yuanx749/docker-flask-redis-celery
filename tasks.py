import time
from celery import Celery, chord, group, chain

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
app_celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app_celery.conf.worker_prefetch_multiplier = 1

@app_celery.task()
def test(n):
    time.sleep(n)
    return 'hello'

@app_celery.task()
def mapper(n):
    return n ** 2

@app_celery.task()
def reducer(numbers):
    return sum(numbers)

@app_celery.task()
def map_reduce(n):
    callback = reducer.s()
    header = [mapper.s(i) for i in range(n)]
    return chord(header)(callback)
    # return chain(group(header), callback).apply_async()

if __name__ == "__main__":
    app_celery.start(['celery', 'worker', '-l', 'info'])
