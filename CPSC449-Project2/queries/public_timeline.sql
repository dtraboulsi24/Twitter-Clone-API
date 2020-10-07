-- :name public_timeline :many
SELECT username, text, post_time
FROM posts
ORDER BY post_time DESC
LIMIT 25;