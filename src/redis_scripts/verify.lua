local key = KEYS[1]
local key_exists = redis.call("EXISTS", key)

if key_exists == 0 then
    return -1
end

local bucket_size = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])

local token_quota = tonumber(redis.call("HGET", key, "token_quota"))
local token_count = tonumber(redis.call("HGET", key, "tokens_left"))
local last_refill = tonumber(redis.call("HGET", key, "last_refill"))
local active_token = tonumber(redis.call("HGET", key, "active_token"))

if token_quota <= 0 then
    redis.call("DEL", key)
    return -1
end

if active_token == 0 then
    return 2
end

local time_now = tonumber(redis.call("TIME")[1])
local elapsed = time_now - last_refill

token_count = math.min(
    bucket_size,
    token_count + elapsed * rate
)

if token_count < 1 then
    redis.call("HSET", key, "active_token", 0)
    return 0
end

token_quota = token_quota - 1
token_count = token_count - 1

redis.call("HSET", key, "token_quota", token_quota)
redis.call("HSET", key, "tokens_left", token_count)
redis.call("HSET", key, "last_refill", time_now)

return 1