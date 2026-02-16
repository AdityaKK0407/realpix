local ip_key = KEYS[1]
local global_key = KEYS[2]

local ip_key_exists = redis.call("EXISTS", ip_key)
local global_key_exists = redis.call("EXISTS", global_key)

local ip_bucket_size = tonumber(ARGV[1])
local ip_rate = tonumber(ARGV[2])
local ip_ttl = tonumber(ARGV[3])
local global_bucket_size = tonumber(ARGV[4])
local global_rate = tonumber(ARGV[5])
local global_ttl = tonumber(ARGV[6])

local time_now = tonumber(redis.call("TIME")[1])

if ip_key_exists == 0 then
    redis.call("HSET", ip_key,
        "token_count", ip_bucket_size,
        "last_refill", time_now
    )
end

if global_key_exists == 0 then
    redis.call("HSET", global_key,
        "token_count", global_bucket_size,
        "last_refill", time_now
    )
end

local ip_token_count = tonumber(redis.call("HGET", ip_key, "token_count"))
local ip_last_refill = tonumber(redis.call("HGET", ip_key, "last_refill"))

local global_token_count = tonumber(redis.call("HGET", global_key, "token_count"))
local global_last_refill = tonumber(redis.call("HGET", global_key, "last_refill"))

local ip_elapsed = time_now - ip_last_refill
ip_token_count = math.min(
    ip_bucket_size,
    ip_token_count + ip_elapsed * ip_rate
)

local global_elapsed = time_now - global_last_refill
global_token_count = math.min(
    global_bucket_size,
    global_token_count + global_elapsed * global_rate
)

if ip_token_count < 1 or global_token_count < 1 then
    return 0
end

ip_token_count = ip_token_count - 1
global_token_count = global_token_count - 1

redis.call("HSET", ip_key,
    "token_count", ip_token_count,
    "last_refill", time_now
)

redis.call("HSET", global_key,
    "token_count", global_token_count,
    "last_refill", time_now
)

redis.call("EXPIRE", ip_key, ip_ttl)
redis.call("EXPIRE", global_key, global_ttl)

return 1
