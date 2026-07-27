from flask import Flask, jsonify, request
import os
import requests
from datetime import datetime, timezone

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 8802))
METRICS: dict = {}
KIX_BASE_URL = os.environ.get("KIX_BASE_URL", "http://localhost:8800")


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "rlm-metrics", "port": PORT}), 200


@app.get("/metrics")
def metrics():
    phi_cps = 3.697
    latency_ms_p95 = 12.4
    runners_ok = 0
    runners_total = 0
    try:
        resp = requests.get(f"{KIX_BASE_URL}/audit", timeout=2)
        if resp.status_code == 200:
            data = resp.json() or {}
            phi_cps = data.get("phi_cps", phi_cps)
            runners_ok = data.get("healthy", 0)
            runners_total = data.get("total", 0)
    except requests.RequestException:
        pass
    return jsonify({
        "service": "rlm-metrics",
        "port": PORT,
        "phi_cps": phi_cps,
        "benchmarks": {"latency_ms_p95": latency_ms_p95},
        "health": {"runners_ok": runners_ok, "runners_total": runners_total},
        "timestamp": _utcnow(),
    }), 200


@app.post("/vote")
def vote():
    data = request.get_json(silent=True) or {}
    choice = data.get("choice")
    if not choice:
        return jsonify({"error": "missing choice"}), 400
    return jsonify({"choice": choice, "count": 1}), 200


@app.post("/collect")
def collect():
    data = request.get_json(silent=True) or {}
    source = data.get("source")
    metric = data.get("metric")
    value = data.get("value")
    if not source or not metric or value is None:
        return jsonify({"error": "missing field"}), 400

    key = f"{source}:{metric}"
    METRICS[key] = {
        "source": source,
        "metric": metric,
        "value": value,
        "timestamp": _utcnow(),
    }
    return jsonify({"accepted": True, "key": key}), 200


@app.get("/status")
def status():
    return jsonify({"service": "rlm-metrics", "port": PORT, "mode": "standby"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
