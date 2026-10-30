import sqlite3

from database import DATABASE_FILE

website_url = "http://127.0.0.1:8000"


def get_metrics(url):

    with sqlite3.connect(DATABASE_FILE) as connection:

        result = connection.execute("""
            SELECT
                COUNT(*) AS total_checks,

                COALESCE(
                    SUM(CASE WHEN status = 'UP' THEN 1 ELSE 0 END),
                    0
                ) AS successful_checks,

                COALESCE(
                    SUM(CASE WHEN status = 'DOWN' THEN 1 ELSE 0 END),
                    0
                ) AS failed_checks,

                AVG(response_time) AS average_response_time

            FROM check_history
            WHERE website_url = ?
        """, (url,)).fetchone()

    total = result[0]
    successful = result[1]
    failed = result[2]
    average_response_time = result[3]

    uptime = (successful / total * 100) if total > 0 else 0

    return {
        "total_checks": total,
        "successful_checks": successful,
        "failed_checks": failed,
        "uptime_percentage": uptime,
        "average_response_time": average_response_time
    }


metrics = get_metrics(website_url)

print(f"\nMonitoring report for: {website_url}")
print("--------------------------------------")

print(f"Total checks: {metrics['total_checks']}")
print(f"Successful checks: {metrics['successful_checks']}")
print(f"Failed checks: {metrics['failed_checks']}")
print(f"Uptime: {metrics['uptime_percentage']:.2f}%")

if metrics["average_response_time"] is not None:
    print(
        f"Average response time: "
        f"{metrics['average_response_time']:.2f} seconds"
    )
else:
    print("Average response time: No data available")