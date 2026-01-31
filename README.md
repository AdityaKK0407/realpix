# backend

# Table of Contents

- [About](#about)
- [Todo](#todo)
- [How to Run](#how-to-run)

# About

This is a FastAPI server with celery for background processing. The current program uses redis for the broker and backend task processing.

# Todo

- Configure FastAPI and celery and script runner using Make [Done]
- Create FastAPI endpoint for receiving image/video data [Done]
- Create Celery async task queue [Done]
- Create endpoint for checking status of task [Done]
- Rate Limiting [Done]
- Add model [Pending]

# How to Run

- Start the redis server
- Run the make script

To run Make needs to be installed.

> [!NOTE]
> For Windows, it is better to install and use it via git bash.
> That can be done by installing Make using PowerShell Administrator

```bash
    make run
```

This will start the celery worker and the api server.
They can also be executed individually

```bash
    make worker
    make api
```

For production use the following commands:-

```bash
    // Single command
    make run_prod
    
    // Individual commands
    make worker
    make api_prod
```