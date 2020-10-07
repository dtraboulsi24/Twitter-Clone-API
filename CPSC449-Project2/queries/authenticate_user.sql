-- :name authenticate_user :one
SELECT password FROM users WHERE username = :username