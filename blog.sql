-- $ sqlite3 blog.db < blog.sql

--PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS followers;
DROP TABLE IF EXISTS posts;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  username VARCHAR NOT NULL,
  passhash VARCHAR NOT NULL,
  email VARCHAR NOT NULL
);

CREATE TABLE followers (
  id_user INTEGER NOT NULL REFERENCES users (user_id),
  id_following INTEGER NOT NULL REFERENCES users (user_id),
  PRIMARY KEY (id_user, id_following)
);

CREATE TABLE posts (
  post_id INTEGER PRIMARY KEY,
  user_id INTEGER REFERENCES users(user_id),
  post VARCHAR NOT NULL,
  post_time VARCHAR NOT NULL
);

INSERT INTO users(username, passhash, email) VALUES('JohnDoe','password','johndoe@gmail.com');
INSERT INTO users(username, passhash, email) VALUES('JaneDoe','password','janedoe@gmail.com');

INSERT INTO posts(user_id, post, post_time) VALUES(1,'John Doe is a cool dude!', "Yesterday");
INSERT INTO posts(user_id, post, post_time) VALUES(2,'Jane Doe is a sick chick!', "Today");

COMMIT;
