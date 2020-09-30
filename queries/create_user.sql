-- :name create_user :insert
INSERT INTO users(username, passhash, email)
VALUES(:username, :password, :email)
