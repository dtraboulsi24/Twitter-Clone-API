Assignment: Project 2

Name:	Daniel Traboulsi
email:	DTraboulsi@csu.fullerton.edu

Name:	Nicole Traboulsi
email:	NTraboulsi@csu.fullerton.edu

Documention:
The goal of this project was to impliment the basics of a twitter like API service.

1. In order to initialize the database you can use ethier of the commands below after changing your directory to where these api are:
FLASK_APP=api_User flask init
FLASK_APP=api_Timeline flask init

2. Then start both services using foreman with the command below:
foreman start

3. Now that the API is up an running you can hit any of the endpoints listed here:

*** USER API ***
Endpoint:	/users
Type:		POST - createUser(username, email, password)
Description: 	Registers a new user account.
Example:	http POST http://127.0.0.1:5100/users email=test1@gmail.com password=password username=test1

Endpoint:	/users/auth
Type:		POST ● authenticateUser(username, hashed_password)
Description: 	Returns true if the password matches the username.
Example:	http POST http://127.0.0.1:5100/auth password=password username=test1

Endpoint:	/users/<username>/follow
Type:		PUT ● addFollower(username, usernameToFollow)
Description: Start following a new user.
Example:	http PUT http://127.0.0.1:5100/follow username=test1 usernameToFollow=JaneDoe

Endpoint:	/users/<username>/unfollow
Type:		DELETE ● removeFollower(username, usernameToRemove)
Description: 	Stop following a user.
Example:	http DELETE http://127.0.0.1:5100/unfollow username=test1 usernameToFollow=JaneDoe

*** TIMELINE API ***
Endpoint:	/users/<username>
Type:		GET - getUserTimeline(username)
Description:	Returns recent tweets from a user.
Example:	http GET http://127.0.0.1:5000/users/test1

Endpoint:	/users/<username>
Type:		POST ● postTweet(username, text)
Description: 	Post a new tweet.
Example:	http POST http://127.0.0.1:5000/users/test1 text="This is another post"

Endpoint:	/public
Type:		GET ● getPublicTimeline()
Description: 	Returns recent tweets from all users.
Example:	http GET http://127.0.0.1:5000/users/public

Endpoint:	/users/<username>/home
Type:		GET ● getHomeTimeline(username)
Description: 	Returns recent tweets from all users that this user follows.
Example:	http GET http://127.0.0.1:5000/users/test1/home


