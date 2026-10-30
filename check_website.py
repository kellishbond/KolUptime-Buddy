import time
import httpx

url = "http://127.0.0.1:8000"

max_attempts = 3
check_interval = 60


def check_website():
    print(f"\nChecking website: {url}")
    print(f"Check started at: {time.strftime('%H:%M:%S')}")

    for attempt in range(1, max_attempts + 1):

        print(f"\nAttempt {attempt} of {max_attempts}")

        start_time = time.time()

        try:
            response = httpx.get(
                url,
                timeout=5.0,
                trust_env=False
            )

            end_time = time.time()
            response_time = end_time - start_time

            is_healthy = 200 <= response.status_code < 400

            print(f"HTTP status code: {response.status_code}")
            print(f"Response time: {response_time:.2f} seconds")
            print("Reachability: REACHABLE")

            if is_healthy:
                print("Health: HEALTHY")
                print("Final status: UP")
            else:
                print("Health: UNHEALTHY")
                print("Final status: DOWN")

            return

        except (httpx.TimeoutException, httpx.ConnectError) as error:

            end_time = time.time()
            response_time = end_time - start_time

            print(f"Request failed: {type(error).__name__}")
            print(f"Time spent: {response_time:.2f} seconds")

            if attempt == max_attempts:
                print("Reachability: UNREACHABLE")
                print("Final status: DOWN")
                print("All attempts failed.")
                return

            wait_time = 2 ** attempt

            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)


while True:
    check_website()

    print(f"\nNext check in {check_interval} seconds.")
    time.sleep(check_interval)