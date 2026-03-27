# backend

# Table of Contents

- [About](#about)
- [How to Run](#how-to-run)
- [Additional Commands](#additional-commands)
- [Source Code Description](#source-code-description)
- [API Endpoints](#api-endpoints)

---

# About

This is a FastAPI server with celery for background processing. It uses redis for the broker and
backend task processing.

---

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

SERVER=development
#SERVER=production
```

---

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
mypy ./src
```

## Format

```bash
# Format code
ruff format
# Format imports
ruff check --select I --fix .
```

## Fix code

```bash
ruff check
# Apply fixes
ruff check --fix
# Apply unsafe fixes
ruff check --unsafe-fixes
```

---

# Source Code Description

### pyproject.toml

Handles all the packages and versions

### uv.lock

Records exact versions of direct and transitive versions

### Procfile.dev

Commands to run server in development mode

### Procfile.prod

Commands to run server in production mode

### .python-version

Contains the exact python version used

## src

### middleware/rate_limiter.py

Handles the middleware for rate limiting

### redis_client/ip_rate_limiter.py

Redis operations for ip rate limiting

### redis_client/rate_limiter.py

Redis operations for server generated rate limiter token

### redis_scripts

Lua files for redis operations

### routers/model.py

Holds the endpoints for image, video model inference and checking task_status along with image/video validation

### routers/verfication.py

Handles Cloudflare Turnstile verification endpoint

### tasks/app.py

Holds the celery task queue object

### tasks/model.py

Performs the model inference for image and video

### dependencies.py

Records the necessary dependencies (eg. redis client and redis sha scripts)

### helpers.py

Performs the basic initializing before server starts

### main.py

The entry point of the program and holds the fastapi object

## tests

### mocks

Contains mock objects for testing

### redis_client

Tests redis operation logic and return values

### routers/test_root.py

Tests the health check endpoint

### routers/test_routers_model.py

Tests if the image/video validation and endpoints function correctly and tests the task polling endpoint

### routers/test_verification.py

Tests the CloudFlare Turnstile verification endpoint

### tasks

Tests the model inference endpoints

### conftest.py

Contains all the necessary dependencies, env variables, mock objects for testing endpoints

### test_helpers.py

Tests the helper functions that run before server starts

---

# API Endpoints

## Local Development

**Base URL**:  http://localhost:8000

## Render Production

**Base URL**: https://realpix.onrender.com

---

## Default

### HEAD /

**Health check for server**

---

## Verification

### POST /verify/captcha

**Validate Cloudflare Turnstile token and issue a server token**

### Request

**Headers**

- `Content-Type: application/json`
- `X-Client-Ip: <client_ip>`
- `X-RateLimit-Token: <rate-limiter-token>` (optional)

**Body**

```json
{
  "token": "<cloudflare-turnstile-token>"
}
 ```

### Response

- `200` - Token validated successfully

```json
{
  "status": "success",
  "user_token": "<rate-limiter-token>"
}
```

- `400` - Missing Cloudflare Turnstile token from body or Client IP from header

```json lines
// Missing Cloudflare Turnstile token
{
  "status": "error",
  "detail": "Missing CAPTCHA token"
}
// Missing Client IP
{
  "status": "error",
  "detail": "Missing Client IP"
}
```

- `403` - Cloudflare Turnstile provided is invalid

```json
{
  "status": "error",
  "detail": "Invalid CAPTCHA token"
}
```

- `429` - Rate limit exceeded. Rate limit computed based on IP address

```json
{
  "status": "error",
  "detail": "Rate limit exceeded"
}
```

- `500` - Unexpected server error

```json
{
  "status": "error",
  "detail": "Unexpected server error"
}
```

- `502` - Cloudflare server is down and turnstile token cannot be verified

```json
{
  "status": "error",
  "detail": "Unable to verify request at this time. Please try again later"
}
```

- `503` - Server services are unavailable

```json
{
  "status": "error",
  "detail": "Service temporarily unavailable"
}
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
{
  "status": "success",
  "task_id": "<task_id>"
}
```

- `400` - Missing rate limiter token or bad request error

```json lines
{
  "status": "error",
  "detail": "Missing rate limiter token"
}
// Received no images
{
  "status": "error",
  "detail": "At least one image must be provided"
}
// Received more images than acceptable
{
  "status": "error",
  "detail": "Max limit of <image_limit> images exceeded"
}
// Image exceeds memory limit
{
  "status": "error",
  "detail": "Image too large"
}
// Unsupported image type
{
  "status": "error",
  "detail": "Unsupported image format"
}
// Invalid file
{
  "status": "error",
  "detail": "Invalid image file"
}
// Potential image bomb
{
  "status": "error",
  "detail": "Dangerous image file"
}
// Corrupted file
{
  "status": "error",
  "detail": "Corrupted or unreadable image file"
}
```

- `401` - Rate limit token expired, CAPTCHA required

```json
{
  "status": "error",
  "detail": "Invalid rate limiter token"
}
```

- `403` - Rate limit token expired, CAPTCHA required with inactive token as header

```json
{
  "status": "error",
  "detail": "Rate limiter token inactive"
}
```

- `429` - Rate limit exceeded. Token is inactive, activate token using CAPTCHA

```json
{
  "status": "error",
  "detail": "Rate limit exceeded"
}
```

- `500` - Failed to read image. Or server error, something unexpected happened

```json lines
// Video stream failed to convert to bytes
{
  "status": "error",
  "detail": "Failed to process image"
}
// Unreachable error
{
  "status": "error",
  "detail": "Unexpected server error"
}
```

- `503` - Server services are unavailable

```json
{
  "status": "error",
  "detail": "Service temporarily unavailable"
}
```

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
{
  "status": "success",
  "task_ids": "<task_id>"
}
```

- `400` - Missing rate limiter token or bad request

```json lines
// Rate limit token missing
{
  "status": "error",
  "detail": "Missing rate limiter token"
}
// Client provided no videos
{
  "status": "error",
  "detail": "At least one video must be provided"
}
// Client provided too many videos
{
  "status": "error",
  "detail": "Max limit of <video_limit> videos exceeded"
}
// Too large video
{
  "status": "error",
  "detail": "Video too large"
}
// Invalid filename
{
  "status": "error",
  "detail": "Unsupported video format"
}
// Invalid or corrupt video
{
  "status": "error",
  "detail": "Invalid or corrupted video"
}
// Invalid video stream
{
  "status": "error",
  "detail": "No video stream found"
}
// Video file container unsupported
{
  "status": "error",
  "detail": "Unsupported video format"
}
// Unsupported codec
{
  "status": "error",
  "detail": "Unsupported codec"
}
// Resolution too large
{
  "status": "error",
  "detail": "Resolution too high"
}
// Video duration too long
{
  "status": "error",
  "detail": "Video duration of <duration> exceeds max limit of 30 seconds"
}
```

- `401` - Rate limit token expired, CAPTCHA required

```json
{
  "status": "error",
  "detail": "Invalid rate limiter token"
}
```

- `403` - Rate limit token expired, CAPTCHA required with inactive token as header

```json
{
  "status": "error",
  "detail": "Rate limiter token inactive"
}
```

- `429` - Rate limit exceeded. Token is inactive, activate token using CAPTCHA

```json
{
  "status": "error",
  "detail": "Rate limit exceeded"
}
```

- `500` - Failed to read video. Or server error, something unexpected happened

```json lines
// Video stream failed to convert to bytes
{
  "status": "error",
  "detail": "Failed to process video"
}
// Unreachable error
{
  "status": "error",
  "detail": "Unexpected server error"
}
```

- `503` - Server services are unavailable

```json
{
  "status": "error",
  "detail": "Service temporarily unavailable"
}
```

### GET /model/status/{task_id}

**Get the status of model inference given a task id**

### Request

**Headers**

- `X-RateLimit-Token: <rate-limiter-token>`

### Response

- `200` - Request is processed correctly.

```json lines
// Task succeeded and result generated
{
  "status": "success",
  "result": "completed",
  "data": "<data>"
}
// Task failed
{
  "status": "success",
  "result": "failed",
}
// Task is still pending
{
  "status": "success",
  "result": "pending",
}
```

- `400` - Missing rate limiter token

```json
{
  "status": "error",
  "detail": "Missing rate limiter token"
}
```

- `401` - Rate limit token expired, CAPTCHA required

```json
{
  "status": "error",
  "detail": "Invalid rate limiter token"
}
```

- `403` - Rate limit token inactive, CAPTCHA required with inactive token as header to reactivate it

```json
{
  "status": "error",
  "detail": "Rate limiter token inactive"
}
```

- `429` - Rate limit exceeded. Token is inactive, activate token using CAPTCHA

```json
{
  "status": "error",
  "detail": "Rate limit exceeded"
}
```

- `500` - Server error, something unexpected happened

```json
{
  "status": "error",
  "detail": "Unexpected server error"
}
```

- `503` - Server services are unavailable

```json
{
  "status": "error",
  "detail": "Service temporarily unavailable"
}
```