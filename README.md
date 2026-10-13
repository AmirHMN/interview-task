# System Monitor

A small Python (FastAPI + psutil) service that reports the current CPU, RAM and disk usage on port **8000**.

## Endpoints

| Path      | Description                         |
|-----------|-------------------------------------|
| `/`       | Current CPU / RAM / disk usage (JSON) |
| `/health` | Health check                        |
| `/docs`   | Interactive API docs (Swagger)      |

Example response:

```json
{
  "hostname": "server-1",
  "timestamp": "2026-10-13T13:46:14+00:00",
  "cpu":  {"percent": 19.5, "cores": 8, "load_avg": [0.42, 0.37, 0.30]},
  "ram":  {"percent": 70.6, "used_gb": 11.24, "total_gb": 15.91},
  "disk": {"path": "/host", "percent": 45.1, "used_gb": 53.2, "total_gb": 118.0}
}
```

## Run with Docker on Ubuntu 24.04 (recommended)

```bash
# Install Docker (once)
sudo apt update && sudo apt install -y docker.io docker-compose-v2
sudo systemctl enable --now docker

# Build and start
sudo docker compose up -d --build

curl http://localhost:8000/
```

`docker-compose.yml` mounts the host root filesystem read-only at `/host` and shares the
host PID namespace, so the figures describe the **host** server, not just the container.

## Run without Docker

```bash
sudo apt update && sudo apt install -y python3-venv
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Configuration

| Variable    | Default | Description                         |
|-------------|---------|-------------------------------------|
| `DISK_PATH` | `/`     | Filesystem path whose usage is reported |

If a firewall is active: `sudo ufw allow 8000/tcp`
