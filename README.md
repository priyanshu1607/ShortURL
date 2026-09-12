# Tiny URL

## Overview
Tiny URL is a production‑ready URL shortener built with **FastAPI**, **MongoDB**, **Redis**, and a **React (Vite)** frontend. An **Nginx** gateway sits in front of the services handling routing, static asset serving, and basic rate‑limiting. All components are containerised and orchestrated with **Docker Compose**, making the whole stack easy to spin up on any machine that has Docker.

---

## Tech Stack
| Layer | Technology |
|-------|------------|
| API   | FastAPI (Python 3.12) |
| DB    | MongoDB 8 |
| Cache | Redis 7 |
| Frontend | React 19 + Vite 8 |
| Proxy / Rate‑limit | Nginx (alpine) |
| Containerisation | Docker & Docker‑Compose |

---

## Project Structure
```
.
├─ Core/                     # FastAPI backend source
│   ├─ Dockerfile            # Builds the API container
│   ├─ requirements.txt      # Python dependencies
│   ├─ main.py               # Entry point & route definitions
│   └─ ...
├─ React/                    # React (Vite) application
│   ├─ Dockerfile            # Multi‑stage build → static files served by Nginx
│   ├─ package.json          # Node dependencies & scripts
│   └─ src/ …                # React source code (not shown)
├─ nginx/                    # Nginx configuration
│   ├─ Dockerfile            # Copies nginx.conf & URLshortner.conf
│   ├─ nginx.conf            # Global Nginx settings
│   └─ URLshortner.conf      # Rate‑limiting & routing rules
├─ docker-compose.yml        # Orchestrates the 5 containers
└─ README.md                 # ← you are here
```

---

## Configuration
The services are configured via the **docker‑compose.yml** file. Key environment variables are:

| Service | Variable | Description |
|---------|----------|-------------|
| `api`   | `MONGO_URL` | Connection string for MongoDB (`mongodb://mongo:27017`). |
| `api`   | `REDIS_URL` | Connection string for Redis (`redis://redis:6379`). |
| `api`   | `Secret_Key` | Simple secret used by the API (replace with a strong value for production). |

The Nginx container exposes port **80** on the host, so `http://localhost` points to the gateway. The API itself listens on **8000** inside its container, but it is never exposed directly – all traffic goes through Nginx.

---

## Quick Start
> **Prerequisites**
> - Docker (Desktop or Engine) with Compose support
> - Port 80 free on the host machine

```bash
# Clone the repository (if you haven't already)
git clone <repo‑url>
cd <repo‑directory>

# Build and start every service
docker compose up --build -d
```

The command spins up five containers:

| Container | Service | Purpose |
|-----------|---------|---------|
| `tinyurl_api_nginx` | `nginx` | Routing, static file serving, rate‑limiting (port 80) |
| `tinyurl_api_frontend` | `frontend` | React app compiled to static assets |
| `tinyurl_api` | `api` | FastAPI backend (exposed only to Nginx) |
| `tinyurl_mongo` | `mongo` | Persistent MongoDB instance |
| `tinyurl_redis` | `redis` | In‑memory cache for fast look‑ups |

### Verify the stack
```bash
# Health check – should return "server is Running"
curl http://localhost/health
```
Open a browser and navigate to **http://localhost** – you will see the React UI where you can create short URLs.

---

## Using the API
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Simple health‑check (returns 200 when the API is up). |
| `POST` | `/api/v1/urls` | Create a new short URL. Body example: |
| | | ```json
{ "url": "https://example.com", "alies": "myalias", "Expires_at": "2025-12-31 23:59:59" }
``` |
| | | * `url` – required, the long URL to shorten. <br> * `alies` – optional custom slug. <br> * `Expires_at` – optional expiration timestamp (`YYYY-MM-DD HH:MM:SS`). |
| `GET` | `/<short_code>` | Redirects to the original URL (handled by Nginx → FastAPI). |

All CORS headers are pre‑configured for the development frontend (`http://localhost:5173`).

---

## Key Dependencies
### Python (backend)
- **fastapi==0.141.1** – API framework
- **uvicorn==0.52.4** – ASGI server
- **motor==3.7.1** – Async MongoDB driver
- **redis==8.1.0** – Redis client
- **pydantic==2.13.5** – Data validation & settings
- **annotated-doc**, **annotated-types**, **starlette**, etc.

### Node (frontend)
- **react@19.2.8**, **react‑dom@19.2.8**, **react‑router‑dom@7.18.2**
- **vite@8.2.0** – Build tool & dev server
- **@vitejs/plugin-react** – Vite React integration
- **eslint** & related plugins for linting

---

## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository and clone your fork.
2. Create a feature branch (`git checkout -b feat/awesome-feature`).
3. Make your changes – keep the existing coding style (Pydantic models, type hints, ESLint rules).
4. Run the test suite (if any) and ensure the app builds:
   ```bash
   # Backend
   cd Core && pip install -r requirements.txt && python -m pyright
   # Frontend
   cd React && npm ci && npm run lint
   ```
5. Commit with a clear message and push to your fork.
6. Open a Pull Request describing the change.

Please keep the Docker configuration functional; if you add new environment variables, document them in the **Configuration** section above.
