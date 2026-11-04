
import time

from circuit_breaker import CircuitBreaker


breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=2
)

print("\n--- Triggering circuit breaker ---")

for attempt in range(5):
    breaker.record_failure()

print(f"State: {breaker.state}")
print(f"Failure count: {breaker.failure_count}")


print("\n--- Waiting for recovery ---")

time.sleep(2)

allowed = breaker.allow_request()
print(f"Recovery request allowed: {allowed}")


print("\n--- Simulating failed recovery ---")

breaker.record_failure()

print(f"State: {breaker.state}")
print(f"Failure count: {breaker.failure_count}")


print("\n--- Waiting for another recovery attempt ---")

time.sleep(2)

allowed = breaker.allow_request()
print(f"Recovery request allowed: {allowed}")


print("\n--- Simulating successful recovery ---")

breaker.record_success()

print(f"State: {breaker.state}")
print(f"Failure count: {breaker.failure_count}")
