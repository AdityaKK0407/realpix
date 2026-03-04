# backend

# Table of Contents

- [About](#about)
- [How to Run](#how-to-run)
- [Additional Commands](#additional-commands)
- [API Endpoints](#api-endpoints)

# About

This is a FastAPI server with celery for background processing. It uses redis for the broker and
backend task processing.

# How to Run

- Install all the required packages using uv

```bash
uv sync 
```
- Start the redis server
- Run the make script

```bash
# Development mode
honcho start -f ./Procfile.dev
    
# Production mode
honcho start -f ./Procfile.prod
```

## Environment Variables

```dotenv
CLOUDFLARE_URL=https://challenges.cloudflare.com/turnstile/v0/siteverify
CLOUDFLARE_SECRET_KEY=<cloudflare-secret-key>

REDIS_HOST=localhost
REDIS_PORT=6379
```

# Additional Commands

## Tests

```bash
# Run all tests
pytest ./tests
# Or specify filepath to run particular tests
```

## Static Type Checker

```bash
# Performs typing checking on project
mypy ./src/main.py
```

## Format

```bash
ruff format
```

## Fix code

```bash
ruff check
# Apply fixes
ruff check --fix
# Apply unsafe fixes
ruff check --unsafe-fixes
```

# API Endpoints

## Local Development
**Base URL**:  http://localhost:8000

## Render Production
**Base URL**: https://realpix.onrender.com

---

## Default

### HEAD /

**Health check for server**

### Response

- `200` - success
```json
{
  "status": "running"
}
```
- `429` - Rate limit exceeded. Rate limit computed based on IP address
```json
    {"detail":  "Rate limit exceeded"}
```
- `500` - Client doesn't exist or unexpected server error
```json lines
    // Client doesn't exist
    {"detail": "Client not available"}
    // Unexpected error
    {"detail": "Unexpected server error"}
```
---

## Verification

### POST /verify/captcha

**Validate Cloudflare Turnstile token and issue a server token**

### Request

**Headers**
- `Content-Type: application/json`
- `X-RateLimit-Token: <rate-limiter-token>` (optional)

**Body**
```json
    {"token":  "<cloudflare-turnstile-token>"}
 ```

### Response

- `200` - Token validated successfully
```json
    {"user_token": "<rate-limiter-token>"}
```
- `400` - Missing Cloudflare Turnstile token from body
```json
    {"detail":  "Missing CAPTCHA token"}
```
- `403` - Cloudflare Turnstile provided is invalid
```json
    {"detail":  "Invalid CAPTCHA token"}
```
- `429` - Rate limit exceeded. Rate limit computed based on IP address
```json
    {"detail":  "Rate limit exceeded"}
```
- `500` - Client doesn't exist or unexpected server error
```json lines
    // Client doesn't exist
    {"detail": "Client not available"}
    // Unexpected error
    {"detail": "Unexpected server error"}
```
- `502` - Cloudflare server is down and turnstile token cannot be verified
```json
    {"detail":  "Unable to verify request at this time. Please try again later"}
```
- `503` - Server services are unavailable
```json
    {"detail":  "Service temporarily unavailable"}
```

---

## Model

### POST /model/images

**Provide input images data to start model inference**

### Request

**Headers**
- `Content-Type: multipart/form-data`
- `X-RateLimit-Token: <rate-limiter-token>`

**Body**
```bash
--boundary
Content-Disposition: form-data; name="fieldName"; filename="filename.extension"
Content-Type: image/extension

<file data>
--boundary
Content-Disposition: form-data; name="fieldName"; filename="filename.extension"
Content-Type: image/extension

<file data>
--boundary--
```

### Response

- `200` - Request is processed correctly.
```json lines
    {"task_ids":  ["<task_id1>", "<task_id2>", ...]}
```
- `400` - Missing rate limiter token or bad request error
```json lines
    {"detail": "Missing rate limiter token"}
    // Received more images than accepted
    {"detail": "Max limit of <image_limit> images exceeded"}
    // Unsupported image type
    {"detail": "Unsupported image format"}
    // Invalid file
    {"detail": "Invalid image file"}
    // Potential image bomb
    {"detail": "Image too large or suspicious"}
    // Corrupted file
    {"detail": "Corrupted or unreadable image file"}
```
- `401` - Rate limit token expired, CAPTCHA required
```json
    {"detail":  "Invalid rate limiter token"}
```
- `403` - Rate limit token expired, CAPTCHA required with inactive token as header
```json
    {"detail":  "Rate limiter token inactive"}
```
- `429` - Rate limit exceeded. Token is inactive, activate token using CAPTCHA
```json
    {"detail":  "Rate limit exceeded"}
```
- `500` - Failed to read image. Or server error, something unexpected happened
```json lines
    // Video stream failed to convert to bytes
    {"detail":  "Failed to read image"}
    // Unreachable error
    {"detail": "Unexpected server error"}
```
- `503` - Server services are unavailable
```json
    {"detail": "Service temporarily unavailable"}
```

> [!WARNING]
> This API endpoint is currently unavailable

### POST /model/videos

**Provide input videos data to start model inference**

### Request

**Headers**
- `Content-Type: multipart/form-data`
- `X-RateLimit-Token: <rate-limiter-token>`

**Body**
```bash
--boundary
Content-Disposition: form-data; name="fieldName"; filename="filename.extension"
Content-Type: video/extension

<file data>
--boundary
Content-Disposition: form-data; name="fieldName"; filename="filename.extension"
Content-Type: video/extension

<file data>
--boundary--
```

### Response

- `200` - Request is processed correctly.
```json lines
    {"task_ids":  ["<task_id1>", "<task_id2>", ...]}
```
- `400` - Missing rate limiter token
```json
    {"detail": "Missing rate limiter token"}
```
- `401` - Rate limit token expired, CAPTCHA required
```json
    {"detail":  "Invalid rate limiter token"}
```
- `403` - Rate limit token expired, CAPTCHA required with inactive token as header
```json
    {"detail":  "Rate limiter token inactive"}
```
- `429` - Rate limit exceeded. Token is inactive, activate token using CAPTCHA
```json
    {"detail":  "Rate limit exceeded"}
```
- `500` - Failed to read video. Or server error, something unexpected happened
```json lines
    // Video stream failed to convert to bytes
    {"detail":  "Failed to read video"}
    // Unreachable error
    {"detail": "Unexpected server error"}
```
- `503` - Server services are unavailable
```json
    {"detail": "Service temporarily unavailable"}
```

### GET /status/{task_id}

**Get the status of model inference given a task id**

### Request

**Headers**
- `X-RateLimit-Token: <rate-limiter-token>`

### Response

- `200` - Request is processed correctly.
```json lines
    // task succeeded and result generated
    {"status":  "completed", "result":  "<result>"}
    // task failed
    {"status":  "failed"}
    // task is still pending
    {"status":  "pending"}
```
- `400` - Missing rate limiter token
```json
    {"detail": "Missing rate limiter token"}
```
- `401` - Rate limit token expired, CAPTCHA required
```json
    {"detail":  "Invalid rate limiter token"}
```
- `403` - Rate limit token inactive, CAPTCHA required with inactive token as header to reactivate it
```json
    {"detail":  "Rate limiter token inactive"}
```
- `429` - Rate limit exceeded. Token is inactive, activate token using CAPTCHA
```json
    {"detail":  "Rate limit exceeded"}
```
- `500` - Server error, something unexpected happened
```json
    {"detail": "Unexpected server error"}
```
- `503` - Server services are unavailable
```json
    {"detail": "Service temporarily unavailable"}
```