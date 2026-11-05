# KolUptime Buddy — Website Monitor

KolUptime Buddy is a Python-based website monitoring tool that checks whether a website is reachable and healthy. It tracks response times, handles temporary failures, records monitoring history and detects website recovery.

## Features

- **HTTP monitoring:** Checks website availability using HTTP requests.
- **Timeout handling:** Prevents requests from waiting indefinitely.
- **Retries:** Retries failed requests before declaring a monitoring cycle unsuccessful.
- **Exponential backoff:** Increases the waiting time between retries.
- **Circuit breaker:** Uses CLOSED, OPEN and HALF-OPEN states to manage repeated failures.
- **Automatic monitoring:** Runs checks at configurable intervals.
- **Persistent history:** Stores monitoring results in SQLite.
- **Metrics:** Calculates check-based uptime, average response time, P95 and P99 latency.
- **Alert detection:** Detects when a website goes DOWN or recovers.
- **Duplicate alert prevention:** Avoids repeatedly reporting the same status.

## Technologies

- Python
- HTTPX
- SQLite
- Standard Python libraries

## Project structure

```text
KolUptime-Buddy/
│
├── check_website.py
├── circuit_breaker.py
├── database.py
├── metrics.py
├── view_history.py
├── test_circuit_breaker.py
├── retry_server.py
├── uptime.db
└── README.md
```

`uptime.db` is generated automatically when monitoring begins. It stores monitoring history.

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd KolUptime-Buddy
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

Install the dependency:

```bash
python -m pip install httpx
```

## Running the monitor

Start monitoring:

```bash
python check_website.py
```

The default monitoring target is:

```text
http://127.0.0.1:8000
```

The monitoring interval is 60 seconds.

Stop monitoring with `Ctrl + C`.

## Viewing monitoring history

```bash
python view_history.py
```

## Viewing monitoring metrics

```bash
python metrics.py
```

## Testing the circuit breaker

```bash
python test_circuit_breaker.py
```

## Core reliability concepts learned

1. HTTP requests and response status codes.
2. Request timeouts.
3. Retries and exponential backoff.
4. Website reachability versus application health.
5. Sequential monitoring and scheduling.
6. Persistent storage using SQLite.
7. SQL aggregation and monitoring metrics.
8. Average latency, P95 and P99.
9. Circuit breaker patterns.
10. State-transition alerts and recovery detection.

## Limitations

- Alerts are currently printed in the terminal; external notifications are not implemented.
- Monitoring runs while the Python process is running.
- Circuit breaker state is held in memory and resets when the process restarts.
- Uptime percentage is based on successful checks, not exact elapsed availability time.
- P95 and P99 estimates become more meaningful with larger datasets.
- This is a learning project, not yet a production-grade monitoring service.

## Purpose

The goal of KolUptime Buddy was to understand how backend systems handle unreliable services, temporary failures, latency and recovery.

Built as a practical Python backend engineering learning project.