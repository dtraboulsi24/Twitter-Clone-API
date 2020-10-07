-- :name add_follower :insert
INSERT INTO followers(username, usernameToFollow)
VALUES(:username, :usernameToFollow)