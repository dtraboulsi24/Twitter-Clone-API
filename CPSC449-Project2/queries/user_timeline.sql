-- :name user_timeline :many
SELECT username, text, post_time
FROM posts
WHERE username = :username
ORDER BY post_time DESC
LIMIT 25;