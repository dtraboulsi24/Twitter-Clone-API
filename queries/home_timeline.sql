-- :name home_timeline :one
SELECT * FROM posts
WHERE user_id = :id
ORDER BY post_time
LIMIT 25;