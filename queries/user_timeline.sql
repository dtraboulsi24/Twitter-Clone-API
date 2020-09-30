-- :name user_timeline :many
SELECT username, post, post_time
FROM posts
WHERE users.user_id =  :id
INNER JOIN users ON (posts.user_id  = users.user_id)
INNER JOIN users ON (posts.user_id  = followers.id_following)
LIMIT 25;