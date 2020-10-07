-- :name home_timeline :many
SELECT followers.usernameToFollow, text, post_time
FROM posts
INNER JOIN followers ON (followers.username = posts.username)
WHERE followers.username = :username
ORDER BY post_time DESC
LIMIT 25;