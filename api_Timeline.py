# Microblog Microservice - Timeline

import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import datetime


app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries.engine.raw_connection()
        with app.open_resource('blog.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Microblog Timeline API</h1>
<p>A prototype Timeline API for microservice architecture</p>'''


@app.route('/public', methods=['GET'])
def get_public_timeline():
    app.logger.debug("public")
    public = queries.public_timeline()
    if public:
        return list(public)
    else:
        raise exceptions.NotFound()


@app.route('/users/<string:username>/home', methods=['GET'])
def get_home_timeline(username):
    app.logger.debug(username)
    home = queries.home_timeline(name=username)
    if home:
        return home # list(home)
    else:
        raise exceptions.NotFound()


@app.route('/users/<string:username>', methods=['GET', 'POST'])
def users(username):
    if request.method == 'GET':
        return get_user_timeline(username)
    elif request.method == 'POST':
        return post_tweet(username)


def get_user_timeline(username):
    app.logger.debug(username)
    user = queries.user_timeline()
    if user:
        return user
    else:
        raise exceptions.NotFound()


def post_tweet(username):
    #request.form.get('')
    text = request.args.get('text')
    time = datetime.now()
    post = queries.post(username, text, time)
    if post:
        return post
    else:
        raise exceptions.NotFound()
