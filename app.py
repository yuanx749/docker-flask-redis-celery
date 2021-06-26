import logging
import redis
from flask import Flask, redirect, url_for, render_template
from celery import Celery

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
app_celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app_flask = Flask(__name__)
db = redis.Redis(host='redis', port=6379, db=1, decode_responses=True)

@app_flask.route('/')
def index():
    return 'hello world'

@app_flask.route('/test/<int:n>')
def test(n):
    result = app_celery.send_task('tasks.test', args=[n])
    return redirect(url_for('status', task_id=result.id))

def check_task(task_id):
    """
    Checks Celry task, returns AsyncResult and its result value.
    """
    async_result = app_celery.AsyncResult(task_id)
    if async_result.successful():
        result = async_result.get()
    else:
        result = None
    return async_result, result

@app_flask.route('/status/<string:task_id>')
def status(task_id):
    async_result, result = check_task(task_id)
    return render_template('status.html', result=result, successful=async_result.successful(), state=async_result.state)

@app_flask.route('/mapreduce/<int:n>')
def mapreduce(n):
    cache = db.get(str(n))
    if cache:
        return render_template('status.html', result=cache, successful=True, state='SUCCESS')
    else:
        result = app_celery.send_task('tasks.map_reduce', args=[n])
        return redirect(url_for('mapreduce_status', key=str(n), task_id=result.id))

@app_flask.route('/mapreduce_status/<string:key>/<string:task_id>')
def mapreduce_status(key, task_id):
    chord_result = app_celery.AsyncResult(task_id)
    if chord_result.successful():
        reducer_id = chord_result.get()[0][0]
        return redirect(url_for('reducer_status', key=key, task_id=reducer_id))
    else:
        return render_template('status.html', result=None, successful=False, state=chord_result.state)

@app_flask.route('/reducer_status/<string:key>/<string:task_id>')
def reducer_status(key, task_id):
    async_result, result = check_task(task_id)
    if result:
        db.set(key, result, ex=86400)
    return render_template('status.html', result=result, successful=async_result.successful(), state=async_result.state)

if __name__ == "__main__":
    app_flask.run(host='0.0.0.0', debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    for hdlr in gunicorn_logger.handlers:
        app_flask.logger.addHandler(hdlr)
    app_flask.logger.setLevel(gunicorn_logger.level)
