local key = KEYS[1]
local key_exists = redis.call("EXISTS", key)

if key_exists == 0 then
    return 0
end

local now = redis.call("TIME")[1]
redis.call("HSET", key, "last_refill", now)
redis.call("HSET", key, "active_token", 1)
return 1
