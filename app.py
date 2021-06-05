from flask import Flask, redirect, url_for, render_template
from celery import Celery
import logging

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
app_celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app_flask = Flask(__name__)

@app_flask.route('/')
def index():
    return 'hello world'

@app_flask.route('/test/<int:n>')
def test(n):
    result = app_celery.send_task('tasks.test', args=[n])
    return redirect(url_for('status', task_id=result.id))

@app_flask.route('/mapreduce/<int:n>')
def mapreduce(n):
    result = app_celery.send_task('tasks.map_reduce', args=[n])
    return redirect(url_for('mapreduce_status', task_id=result.id))

@app_flask.route('/status/<string:task_id>')
def status(task_id):
    res = app_celery.AsyncResult(task_id)
    successful=res.successful()
    if successful:
        result = res.get()
    else:
        result = None
    return render_template('status.html', result=result, successful=successful, state=res.state)

@app_flask.route('/mapreduce_status/<string:task_id>')
def mapreduce_status(task_id):
    chord_result = app_celery.AsyncResult(task_id)
    if chord_result.successful():
        reducer_id = chord_result.get()[0][0]
        return redirect(url_for('status', task_id=reducer_id))
    else:
        return render_template('status.html', result=None, successful=False, state=chord_result.state)

if __name__ == "__main__":
    app_flask.run(host='0.0.0.0', debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    for hdlr in gunicorn_logger.handlers:
        app_flask.logger.addHandler(hdlr)
    app_flask.logger.setLevel(gunicorn_logger.level)