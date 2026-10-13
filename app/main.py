"""System resource monitor: exposes current CPU, RAM and disk usage over HTTP."""

import os
import socket
from datetime import datetime, timezone

import psutil
from fastapi import FastAPI

# Path whose filesystem is measured. Inside Docker this points to the host's
# root filesystem mounted read-only (see docker-compose.yml).
DISK_PATH = os.getenv("DISK_PATH", "/")

app = FastAPI(title="System Monitor", version="1.0.0")


def _gb(value: int) -> float:
    return round(value / 1024**3, 2)


@app.get("/")
def usage():
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage(DISK_PATH)
    return {
        "hostname": socket.gethostname(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu": {
            "percent": psutil.cpu_percent(interval=0.5),
            "cores": psutil.cpu_count(),
            "load_avg": [round(x, 2) for x in psutil.getloadavg()],
        },
        "ram": {
            "percent": mem.percent,
            "used_gb": _gb(mem.total - mem.available),
            "total_gb": _gb(mem.total),
        },
        "disk": {
            "path": DISK_PATH,
            "percent": disk.percent,
            "used_gb": _gb(disk.used),
            "total_gb": _gb(disk.total),
        },
    }


@app.get("/health")
def health():
    return {"status": "ok"}
