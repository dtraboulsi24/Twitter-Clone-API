-- :name public_timeline :many
SELECT username, post, post_time
FROM posts
INNER JOIN users ON (posts.user_id  = users.user_id)
LIMIT 25;