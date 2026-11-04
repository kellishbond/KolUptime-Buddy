
import sqlite3
import math

from database import DATABASE_FILE


website_url = "http://127.0.0.1:8000"


def calculate_percentile(values, percentile):

    if not values:
        return None

    rank = math.ceil((percentile / 100) * len(values))

    return values[rank - 1]


def get_metrics(url):

    with sqlite3.connect(DATABASE_FILE) as connection:

        result = connection.execute("""
            SELECT
                COUNT(*) AS total_checks,

                SUM(CASE WHEN status = 'UP' THEN 1 ELSE 0 END),

                SUM(CASE WHEN status = 'DOWN' THEN 1 ELSE 0 END),

                AVG(
                    CASE
                        WHEN http_status_code IS NOT NULL
                        THEN response_time
                    END
                )

            FROM check_history
            WHERE website_url = ?
        """, (url,)).fetchone()

        response_times = connection.execute("""
            SELECT response_time
            FROM check_history
            WHERE website_url = ?
            AND http_status_code IS NOT NULL
            AND response_time IS NOT NULL
            ORDER BY response_time ASC
        """, (url,)).fetchall()

    total = result[0]
    successful = result[1] or 0
    failed = result[2] or 0
    average_response_time = result[3]

    uptime = (successful / total * 100) if total > 0 else 0

    # Extract actual HTTP response times.
    times = [row[0] for row in response_times]

    p95 = calculate_percentile(times, 95)
    p99 = calculate_percentile(times, 99)

    return {
        "total_checks": total,
        "successful_checks": successful,
        "failed_checks": failed,
        "http_responses": len(times),
        "uptime_percentage": uptime,
        "average_response_time": average_response_time,
        "p95_latency": p95,
        "p99_latency": p99
    }


metrics = get_metrics(website_url)

print(f"\nMonitoring report for: {website_url}")
print("--------------------------------------")

print(f"Total checks: {metrics['total_checks']}")
print(f"Successful checks: {metrics['successful_checks']}")
print(f"Failed checks: {metrics['failed_checks']}")
print(f"HTTP responses received: {metrics['http_responses']}")

print(f"Uptime: {metrics['uptime_percentage']:.2f}%")

if metrics["average_response_time"] is not None:
    print(
        f"Average response time: "
        f"{metrics['average_response_time']:.2f} seconds"
    )

if metrics["p95_latency"] is not None:
    print(f"P95 latency: {metrics['p95_latency']:.2f} seconds")

if metrics["p99_latency"] is not None:
    print(f"P99 latency: {metrics['p99_latency']:.2f} seconds")
