-- :name user_timeline :many
SELECT username, post, post_time
FROM posts
INNER JOIN users ON (posts.user_id  = users.user_id)
WHERE username = :username
ORDER BY post_time DESC
LIMIT 25;