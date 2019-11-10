from flask import Flask, redirect, url_for
from tasks import app_celery

app_flask = Flask(__name__)

@app_flask.route('/')
def index():
    return 'hello world'

@app_flask.route('/test/<int:n>')
def test(n):
    result = app_celery.send_task('tasks.test', args=[n])
    return redirect(url_for('status', task_id=result.id))

@app_flask.route('/status/<string:task_id>')
def status(task_id):
    result = app_celery.AsyncResult(task_id)
    if result.successful():
        return result.get()
    else:
        return result.state

if __name__ == "__main__":
    app_flask.run(host='0.0.0.0', debug=True)