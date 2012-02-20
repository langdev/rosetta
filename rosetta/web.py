import functools
import hashlib, hmac
import json
from flask import (Flask, request, render_template, redirect,
                   url_for, session, abort)
from .model import db, Topic
import requests

app = Flask(__name__)
app.config.from_pyfile('../default.cfg')
db.init_app(app)


def login_required(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_form'))
        else:
            return f(*args, **kwargs)
    return wrapped


def valid_login(username, password):
    url = 'http://langdev.org/apps/{0}/sso/{1}?error=ignore' \
        .format(app.config['LANGDEV_APP_KEY'], username)
    hashed_password = hashlib.md5(password).hexdigest()
    payload = hmac.new(app.config['LANGDEV_SECRET_KEY'], hashed_password,
                       digestmod=hashlib.sha1).hexdigest()
    result = requests.post(url, data={'password': payload},
                                headers={'Accept': 'application/json'})
    if result.status_code == requests.codes.ok:
        return json.loads(result.content)
    else:
        return False


@app.route('/')
def root():
    topics = Topic.query.all()
    return render_template('index.html', topics=topics)


@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    return render_template('topic.html', topic=topic)


@app.route('/topic/new')
@login_required
def write_topic():
    return render_template('write.html')


@app.route('/login')
def login_form():
    if 'username' in session:
        return redirect(url_for('root'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def sso_login():
    username = request.form['username']
    password = request.form.get('password')
    if valid_login(username, password):
        session['username'] = username
        return redirect(url_for('root'))
    else:
        error = 'Invalid username/password'
        return render_template('login.html', username=username, error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('root'))
