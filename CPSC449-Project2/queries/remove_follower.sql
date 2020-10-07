-- :name remove_follower :insert
DELETE FROM followers 
WHERE username=:username AND usernameToFollow=:usernameToFollow;