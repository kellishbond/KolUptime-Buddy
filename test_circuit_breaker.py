import time

from circuit_breaker import CircuitBreaker


breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=5
)

print("\n--- Testing consecutive failures ---")

for attempt in range(5):
    breaker.record_failure()

print(f"\nCurrent state: {breaker.state}")

print("\n--- Testing request blocking ---")

allowed = breaker.allow_request()

print(f"Request allowed: {allowed}")

print("\n--- Waiting for recovery period ---")

time.sleep(5)

print("\n--- Testing recovery ---")

allowed = breaker.allow_request()

print(f"Request allowed: {allowed}")
print(f"Current state: {breaker.state}")

print("\n--- Simulating successful recovery ---")

breaker.record_success()

print(f"Final state: {breaker.state}")