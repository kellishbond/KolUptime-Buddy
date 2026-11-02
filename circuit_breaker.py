import time


class CircuitBreaker:

    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failure_count = 0
        self.state = "CLOSED"
        self.opened_at = None

    def allow_request(self):

        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":

            elapsed_time = time.time() - self.opened_at

            if elapsed_time >= self.recovery_timeout:
                self.state = "HALF-OPEN"
                print("Circuit breaker: HALF-OPEN")
                return True

            print("Circuit breaker: OPEN - Request blocked")
            return False

        if self.state == "HALF-OPEN":
            return True

    def record_success(self):

        self.failure_count = 0
        self.state = "CLOSED"
        self.opened_at = None

        print("Circuit breaker: CLOSED - Website recovered")

    def record_failure(self):

        self.failure_count += 1

        print(f"Consecutive failures: {self.failure_count}")

        if self.state == "HALF-OPEN":
            self.open_circuit()

        elif self.failure_count >= self.failure_threshold:
            self.open_circuit()

    def open_circuit(self):

        self.state = "OPEN"
        self.opened_at = time.time()

        print("Circuit breaker: OPEN - Too many failures")