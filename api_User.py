# Microblog Microservice - User
# <https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask>.
#
# What's new:
#
#  * Switched from Flask to Flask API
#    <https://www.flaskapi.org>
#
#  * Switched to PugSQL for database access
#    <https://pugsql.org>
#
#  * SQLAlchemy Database URL specified in app config file
#
#  * Adds CLI command to create initial schema from "Using SQLite 3 with Flask"
#    <https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/>
#
#  * New API calls:
#    - GET /api/v1/resources/books/{id} to retrieve a specific book
#    - POST /api/v1/resources/books to create a new book
#

import flask_api
from flask import request
from flask_api import status, exceptions
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
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    try:
        app.logger.debug(username)
        user = queries.create_user(username, email, password)
        return user #, status.HTTP_201_CREATED, {
     #'Location': #f'/users/{user["id"]}'
     #}
    except Exception as e:
        return {'error': str(e)}, status.HTTP_409_CONFLICT

    

@app.route('/users/auth', methods=['POST'])
def authenticate_user(query_parameters):
    id = query_parameters.get('id')
    username = query_parameters.get('username')
    hashed_password = query_parameters.get('hashed_password')

    query = "SELECT * FROM users WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if username:
        query += ' username=? AND'
        to_filter.append(username)
    if hashed_password:
        query += ' hashed_password=? AND'
        to_filter.append(hashed_password)
    if not (id or username or hashed_password):
        raise exceptions.NotFound()

    query = query[:-4] + ';'

    results = queries.engine.execute(query, to_filter).fetchall()

    return list(map(dict, results))

@app.route('/users/<username>/follow', methods=['PUT', 'DELETE'])
def users():
    if request.method == 'PUT':
        return add_follower(request.args)
    elif request.method == 'DELETE':
        return remove_follower(request.data)


def add_follower(query_parameters):
    id = query_parameters.get('id')
    username = query_parameters.get('username')
    username_to_follow = query_parameters.get('usernameToFollow')

    query = "SELECT * FROM users WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if username:
        query += ' username=? AND'
        to_filter.append(username)
    if username_to_follow:
        query += ' usernameToFollow=? AND'
        to_filter.append(username_to_follow)
    if not (id or username or username_to_follow):
        raise exceptions.NotFound()

    query = query[:-4] + ';'

    results = queries.engine.execute(query, to_filter).fetchall()

    return list(map(dict, results))


def remove_follower(query_parameters):
    id = query_parameters.get('id')
    username = query_parameters.get('username')
    remove_follower = query_parameters.get('removeFollower')

    query = "SELECT * FROM users WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if username:
        query += ' username=? AND'
        to_filter.append(username)
    if remove_follower:
        query += ' removeFollower=? AND'
        to_filter.append(remove_follower)
    if not (id or username or remove_follower):
        raise exceptions.NotFound()

    query = query[:-4] + ';'

    results = queries.engine.execute(query, to_filter).fetchall()

    return list(map(dict, results))
