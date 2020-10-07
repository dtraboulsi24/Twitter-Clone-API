# Microblog Microservice - User

import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
from werkzeug.security import generate_password_hash, check_password_hash
import pugsql


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
    return '''<h1>Microblog User API</h1>
<p>A prototype User API for microservice architecture</p>'''


@app.route('/api/v1/test/users', methods=['GET'])
def all_users():
    app.logger.debug("GOT HERE")
    users = queries.all_users()
    app.logger.debug("Ran Query")
    return list(users)


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.data
    posted_fields = {*user_data.keys()}
    required_fields = {'username', 'email', 'password'}
    if not required_fields <= posted_fields:
        message = f'Missing fields: {required_fields - posted_fields}'
        raise exceptions.ParseError(message)
    user_data["password"] = generate_password_hash(user_data['password'], "sha256")
    try:
        app.logger.info("*********************")
        app.logger.info(user_data)
        user = queries.create_user(**user_data)
        return jsonify(user) #, status.HTTP_201_CREATED, {
        #'Location': #f'/users/{user["id"]}'
        #}
    except Exception as e:
        return {'error': str(e)}, status.HTTP_409_CONFLICT

    

@app.route('/auth', methods=['POST'])
def authenticate_user():
    user_data = request.data
    posted_fields = {*user_data.keys()}
    required_fields = {'username', 'password'}
    if not required_fields <= posted_fields:
        message = f'Missing fields: {required_fields - posted_fields}'
        raise exceptions.ParseError(message)
    try:
        password = queries.authenticate_user(**user_data)
        app.logger.info(user_data["password"])
        app.logger.info(password["password"])
        return jsonify(check_password_hash(password["password"], user_data["password"]))
    except Exception as e:
        return {'error': str(e)}, status.HTTP_409_CONFLICT


@app.route('/follow', methods=['PUT'])
def add_follower():
    user_data = request.data
    posted_fields = {*user_data.keys()}
    required_fields = {'username', 'usernameToFollow'}
    if not required_fields <= posted_fields:
        message = f'Missing fields: {required_fields - posted_fields}'
        raise exceptions.ParseError(message)
    try:
        follow = queries.add_follower(**user_data)
        return jsonify(follow)
    except Exception as e:
        return {'error': str(e)}, status.HTTP_409_CONFLICT
    

@app.route('/unfollow', methods=['DELETE'])
def remove_follower():
    user_data = request.data
    posted_fields = {*user_data.keys()}
    required_fields = {'username', 'usernameToFollow'}
    if not required_fields <= posted_fields:
        message = f'Missing fields: {required_fields - posted_fields}'
        raise exceptions.ParseError(message)
    try:
        follow = queries.remove_follower(**user_data)
        return jsonify(follow)
    except Exception as e:
        return {'error': str(e)}, status.HTTP_409_CONFLICT
