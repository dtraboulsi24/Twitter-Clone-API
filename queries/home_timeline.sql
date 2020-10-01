-- :name home_timeline :many
SELECT * FROM users 
INNER JOIN followers ON (users.users_id = followers.id_user) 
WHERE followers.id_following = :username