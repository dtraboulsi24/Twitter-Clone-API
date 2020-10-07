# Microblog Microservice - Timeline

import flask_api
from flask import request, jsonify
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


@app.route('/users/public', methods=['GET'])
def get_public_timeline():
    public = queries.public_timeline()
    if public:
        #app.logger.debug(type(public))
        return list(public)
    else:
        raise exceptions.NotFound()


@app.route('/users/<string:username>/home', methods=['GET'])
def get_home_timeline(username):
    app.logger.debug(username)
    home = queries.home_timeline(username=username)
    app.logger.debug("***************")
    app.logger.debug(type(home))

    if home:
        return list(home) # list(home)
    else:
        raise exceptions.NotFound()

#working
@app.route('/users/<string:username>', methods=['GET', 'POST'])
def users(username):
    if request.method == 'GET':
        app.logger.debug(username)
        return get_user_timeline(username)
    elif request.method == 'POST':
        app.logger.debug(username)
        return post_tweet(username)

#working
def get_user_timeline(username):
    app.logger.debug(username)
    home = queries.user_timeline(username=username)
    app.logger.debug("***************")
    app.logger.debug(type(home))
    if home:
        return list(home) # list(home)
    else:
        raise exceptions.NotFound()

#Fix user username to user_ID
def post_tweet(username):
    post_time = str(datetime.datetime.now())
    user_data = request.data
    posted_fields = {*user_data.keys()}
    required_fields = {'text'}
    if not required_fields <= posted_fields:
        message = f'Missing fields: {required_fields - posted_fields}'
        raise exceptions.ParseError(message)
    try:
        post = str(queries.post(username=username, text=user_data["text"], post_time=post_time))
        app.logger.debug(post)
        if post:
            return post, status.HTTP_201_CREATED
        else:
            raise exceptions.NotFound()
    except Exception as e:
        return {'error': str(e)}, status.HTTP_409_CONFLICT