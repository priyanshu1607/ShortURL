# Tiny URL

A Production ready URL shortener built with FastAPI, MongoDB, Redis, and a React (Vite) frontend, fronted by an Nginx gateway that handles routing and rate limiting.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose (bundled with Docker Desktop)
- Port 80 free on your machine — if something else is already listening on it (another local web server, a WSL service, IIS, etc.), stop that first or the `nginx` container won't be reachable at `http://localhost`

## Running the project

From the project root:

 - docker compose up --build

This builds and starts 5 containers:

| Container | Service | Purpose |
|---|---|---|
| `tinyurl_api_nginx` | `nginx` |  routing + rate limiting (port `80`) |
| `tinyurl_api_frontend` | `frontend` | React app |
| `tinyurl_api` | `api` | FastAPI backend |
| `tinyurl_mongo` | `mongo` | MongoDB |
| `tinyurl_redis` | `redis` | Redis |

Confirm everything is up:


## Using the app

- Open **http://localhost** — the React frontend to create short URLs.
- `GET http://localhost/health` —  health check.
- `POST http://localhost/api/v1/urls` — create a short URL. Body:
  ```json
  { "url": "https://example.com" }
  ```
  Optional fields: `alies` (custom alias), `Expires_at` (`YYYY-MM-DD HH:MM:SS`).
- `GET http://localhost/<short_code>` — redirects to the original URL.

## Rate limiting

The gateway (`nginx/URLshortner.conf`) limits requests to 10 requests/second per client IP, with a burst allowance of 20. 
