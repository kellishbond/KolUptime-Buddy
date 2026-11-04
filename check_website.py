
import time
from datetime import datetime, timezone

import httpx

from database import create_table, save_check
from circuit_breaker import CircuitBreaker


url = "http://127.0.0.1:8000"

max_attempts = 3
check_interval = 60

# Create one circuit breaker for the monitor.
breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=60
)


def check_website():

    print(f"\nChecking website: {url}")
    print(f"Check started at: {time.strftime('%H:%M:%S')}")

    # Ask the circuit breaker whether a request is allowed.
    if not breaker.allow_request():
        print("Website check skipped because the circuit is OPEN.")
        return

    final_status = "DOWN"
    response_time = None
    http_status_code = None
    attempts_used = 0

    # In HALF-OPEN, allow only one attempt as a recovery probe.
    if breaker.state == "HALF-OPEN":
        attempts_limit = 1
        print("Recovery probe: retries disabled.")
    else:
        attempts_limit = max_attempts

    for attempt in range(1, attempts_limit + 1):

        attempts_used = attempt

        print(f"\nAttempt {attempt} of {attempts_limit}")

        start_time = time.time()

        try:
            response = httpx.get(
                url,
                timeout=5.0,
                trust_env=False
            )

            end_time = time.time()
            response_time = end_time - start_time

            http_status_code = response.status_code

            is_healthy = 200 <= response.status_code < 400

            print(f"HTTP status code: {http_status_code}")
            print(f"Response time: {response_time:.2f} seconds")
            print("Reachability: REACHABLE")

            if is_healthy:
                final_status = "UP"
                print("Health: HEALTHY")
            else:
                final_status = "DOWN"
                print("Health: UNHEALTHY")

            break

        except (httpx.TimeoutException, httpx.ConnectError) as error:

            end_time = time.time()
            response_time = end_time - start_time

            print(f"Request failed: {type(error).__name__}")
            print(f"Time spent: {response_time:.2f} seconds")

            if attempt == attempts_limit:
                print("Reachability: UNREACHABLE")
                print("All attempts failed.")
                break

            wait_time = 2 ** attempt

            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    # Record one result for the entire monitoring cycle.
    if final_status == "UP":
        breaker.record_success()
    else:
        breaker.record_failure()

    checked_at = datetime.now(timezone.utc).isoformat()

    save_check(
        website_url=url,
        checked_at=checked_at,
        status=final_status,
        response_time=response_time,
        http_status_code=http_status_code,
        attempts=attempts_used
    )

    print(f"\nFinal status: {final_status}")
    print("Monitoring result saved to database.")
    print(f"Circuit breaker state: {breaker.state}")


create_table()

while True:

    check_website()

    print(f"\nNext check in {check_interval} seconds.")

    time.sleep(check_interval)
