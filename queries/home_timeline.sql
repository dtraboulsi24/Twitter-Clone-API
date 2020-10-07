-- :name home_timeline :many
SELECT *
FROM posts
INNER JOIN followers ON (followers.username = posts.username)
WHERE followers.username = :username
ORDER BY post_time DESC
LIMIT 25;