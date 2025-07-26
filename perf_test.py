import requests
import time
import concurrent.futures
import statistics

URL = "http://34.66.9.111/predict"
HEADERS = {"Content-Type": "application/json"}
DATA = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}

NUM_THREADS = 4
NUM_CONNECTIONS = 100
DURATION = 30  # seconds

def send_request():
    start = time.time()
    try:
        response = requests.post(URL, json=DATA, headers=HEADERS, timeout=10)
        latency = (time.time() - start) * 1000  # ms
        return latency, response.status_code
    except Exception:
        return None, None

def worker(stop_time, latencies, statuses):
    while time.time() < stop_time:
        latency, status = send_request()
        if latency is not None:
            latencies.append(latency)
            statuses.append(status)

def main():
    print("🚀 Starting Python performance test...")
    stop_time = time.time() + DURATION
    latencies = []
    statuses = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for _ in range(NUM_CONNECTIONS):
            futures.append(executor.submit(worker, stop_time, latencies, statuses))
        concurrent.futures.wait(futures)

    if latencies:
        print(f"Total requests: {len(latencies)}")
        print(f"Success responses: {statuses.count(200)}")
        print(f"Mean latency: {statistics.mean(latencies):.2f} ms")
        print(f"Median latency: {statistics.median(latencies):.2f} ms")
        print(f"Min latency: {min(latencies):.2f} ms")
        print(f"Max latency: {max(latencies):.2f} ms")
        print(f"99th percentile latency: {statistics.quantiles(latencies, n=100)[98]:.2f} ms")
    else:
        print("No successful requests.")

if __name__ == "__main__":
    main() 