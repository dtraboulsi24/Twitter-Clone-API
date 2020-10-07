-- :name public_timeline :many
SELECT username, post, post_time
FROM posts
ORDER BY post_time DESC
LIMIT 25;