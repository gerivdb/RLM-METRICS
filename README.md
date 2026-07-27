# RLM-METRICS

Metrics collector and aggregator for the RLM ecosystem.

- Port: `8802`
- Role: phi-CPS, benchmarks, health aggregation
- Stack: Flask + SQLite (future state persistence)

## Endpoints

| Method | Path       | Purpose                       |
|--------|------------|-------------------------------|
| GET    | /health    | Liveness check                |
| GET    | /metrics   | Aggregated metrics snapshot   |
| POST   | /vote      | Record a vote                 |
| POST   | /collect   | Accept a metric payload       |
| GET    | /status    | Service status                |

## Run

```powershell
python src/app.py
```

## Test

```powershell
pytest tests/test_app.py -q
```

## Archi notes

- MVP: in-memory collect and static aggregated view
- Next: time-series persistence, phi-CPS computation, KIX integration
