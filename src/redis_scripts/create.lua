local key = KEYS[1]

local token_quota_left = tonumber(ARGV[1])
local initial_tokens = tonumber(ARGV[2])
local ttl_seconds = tonumber(ARGV[3])

local time_now = tonumber(redis.call("TIME")[1])

redis.call("HSET", key,
    "token_quota", token_quota_left,
    "tokens_left", initial_tokens,
    "last_refill", time_now
)

redis.call("EXPIRE", key, ttl_seconds)
