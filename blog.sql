-- $ sqlite3 blog.db < blog.sql

--PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS followers;
DROP TABLE IF EXISTS posts;

CREATE TABLE users (
  username VARCHAR PRIMARY KEY,
  email VARCHAR NOT NULL,
  password VARCHAR NOT NULL
);

CREATE TABLE followers (
  username VARCHAR REFERENCES users(username),
  usernameToFollow VARCHAR REFERENCES users(username),
  PRIMARY KEY (username, usernameToFollow)
);

CREATE TABLE posts (
  post_id INTEGER PRIMARY KEY,
  username VARCHAR REFERENCES users(username),
	text VARCHAR,
  post_time VARCHAR
);

INSERT INTO users(username, email, password) VALUES('JohnDoe','johndoe@gmail.com','password');
INSERT INTO users(username, email, password) VALUES('JaneDoe','janedoe@gmail.com','password');

INSERT INTO posts(username, text, post_time) VALUES('JohnDoe', 'John Doe is a cool dude!', "0000002");
INSERT INTO posts(username, text, post_time) VALUES('JaneDoe', 'Jane Doe is a sick chick!', "0000001");

COMMIT;
