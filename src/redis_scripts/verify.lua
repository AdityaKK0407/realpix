local key = KEYS[1]

local bucket_size = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])

local token_quota = tonumber(redis.call("HGET", key, "token_quota"))
local token_count = tonumber(redis.call("HGET", key, "tokens_left"))
local last_refill = tonumber(redis.call("HGET", key, "last_refill"))

if not token_quota or token_quota <= 0 then
    redis.call("DEL", key)
    return 0
end

local time_now = tonumber(redis.call("TIME")[1])
local elapsed = time_now - last_refill

token_count = math.min(
    bucket_size,
    token_count + elapsed * rate
)

if token_count < 1 then
    redis.call("HSET", key, "last_refill", time_now)
    return 0
end

token_quota = token_quota - 1
token_count = token_count - 1

redis.call("HSET", key, "token_quota", token_quota)
redis.call("HSET", key, "tokens_left", token_count)
redis.call("HSET", key, "last_refill", time_now)

return 1