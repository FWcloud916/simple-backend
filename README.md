# Simple Backend

## Description

Fastapi skeleton for a simple backend with JWT authentication and PostgreSQL database.

## Requirements

Python >= 3.12.2
Poetry >= 1.3.1 (for dependency management)
PostgreSQL >= 15 (for database)

## Installation

Poetry is used for dependency management.
To install dependencies, run:

```bash
poetry install
```

## Usage

To run the server, run:

```bash
poetry run uvicorn app.main:app --reload
```

## Docker Compose Usage

To run the server with Docker Compose, run:

```bash
docker-compose up -d
```

## Environment Variables

### Project
- SECRET_KEY: Secret key for JWT authentication
- ALGORITHM: Algorithm for JWT authentication, default is HS256
- ACCESS_TOKEN_EXPIRE_MINUTES: Expiration time for JWT authentication, default is 30 minutes

#### Generate a secret key
```bash
openssl rand -hex 32
```

### Database
- POSTGRES_SERVER: The url of the postgres server
- POSTGRES_USER: The username of the postgres user
- POSTGRES_PASSWORD: The password of the postgres user
- POSTGRES_DB: The name of the postgres database