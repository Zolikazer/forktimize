import statistics
import time
from concurrent.futures import ThreadPoolExecutor

import requests

CREATE_MENU_URL = "https://forktimize.xyz/api/menu"
NUM_THREADS = 5
NUM_REQUESTS = 500

PAYLOAD = {
    "date": "2025-03-18",
    "nutritionalConstraints": {
        "minCalories": 2300,
        "maxCalories": 2700,
        "minProtein": 180,
        "maxFat": 100,
    },
    "foodBlacklist": ["hal", "uborka"]
}

response_times = []


def send_request():
    """Function to send a single request and measure response time."""
    start_time = time.perf_counter()
    response = requests.post(CREATE_MENU_URL, json=PAYLOAD)
    end_time = time.perf_counter()

    duration = end_time - start_time
    response_times.append(duration)

    return response.status_code, duration


def run_load_test(num_threads, num_requests):
    """Runs the load test with the given number of threads."""
    print(f"🚀 Starting load test with {num_threads} threads and {num_requests} total requests...\n")

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(lambda _: send_request(), range(num_requests)))

    # Extract status codes & print stats
    status_codes = [result[0] for result in results]

    print(f"\n✅ Load test completed! Stats:")
    print(f"  - Total Requests: {num_requests}")
    print(f"  - Success Responses (200s): {status_codes.count(200)}")
    print(f"  - Errors: {len([s for s in status_codes if s != 200])}")

    if response_times:
        print(f"📊 Response Time Stats:")
        print(f"  - Fastest: {min(response_times):.4f}s")
        print(f"  - Slowest: {max(response_times):.4f}s")
        print(f"  - Average: {statistics.mean(response_times):.4f}s")
        print(f"  - Median: {statistics.median(response_times):.4f}s")
        print(f"  - Std Dev: {statistics.stdev(response_times):.4f}s" if len(response_times) > 1 else "")


if __name__ == "__main__":
    run_load_test(NUM_THREADS, NUM_REQUESTS)
