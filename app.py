from flask import Flask, redirect, url_for, render_template
from celery import Celery

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
# CELERY_BROKER_URL = 'redis://localhost'
# CELERY_RESULT_BACKEND = 'redis://localhost'
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
    return redirect(url_for('chord_status', task_id=result.id))

@app_flask.route('/status/<string:task_id>')
def status(task_id):
    result = app_celery.AsyncResult(task_id)
    if result.successful():
        return render_template('status.html', result=result.get())
    else:
        return render_template('status.html', result=result.state)

@app_flask.route('/chord_status/<string:task_id>')
def chord_status(task_id):
    chord_result = app_celery.AsyncResult(task_id)
    result = app_celery.AsyncResult(chord_result.get()[0][0])
    if result.successful():
        return render_template('status.html', result=result.get())
    else:
        return render_template('status.html', result=result.state)

if __name__ == "__main__":
    app_flask.run(host='0.0.0.0', debug=True)