import time
import multiprocessing as mp
import requests

URL = "http://localhost:5000/data"

# How many different keys and how many requests per worker
NUM_KEYS = 20
REQUESTS_PER_WORKER = 50

def worker(worker_id: int, use_unique_keys: bool):
    """
    Each worker sends many requests to the service.
    If use_unique_keys is False, workers will share keys (good to show cache benefit).
    """
    session = requests.Session()
    slow_count = 0
    fast_count = 0

    for i in range(REQUESTS_PER_WORKER):
        if use_unique_keys:
            # Each worker mostly hits different keys (less cache benefit)
            key = f"key_worker{worker_id}_{i % NUM_KEYS}"
        else:
            # All workers hit from the same small set of keys (max cache benefit)
            key = f"key_shared_{i % NUM_KEYS}"

        start = time.time()
        resp = session.get(URL, params={"key": key})
        elapsed = time.time() - start

        data = resp.json()
        source = data.get("source", "unknown")

        if source == "expensive_operation":
            slow_count += 1
        else:
            fast_count += 1

    return worker_id, slow_count, fast_count


def run_test(num_workers: int, use_unique_keys: bool):
    print(f"Running with {num_workers} worker processes...")
    print(f"use_unique_keys = {use_unique_keys}")
    start = time.time()

    with mp.Pool(processes=num_workers) as pool:
        results = pool.starmap(worker, [(wid, use_unique_keys) for wid in range(num_workers)])

    total_slow = sum(r[1] for r in results)
    total_fast = sum(r[2] for r in results)
    duration = time.time() - start

    print("=== Load Test Results ===")
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Total slow (expensive_operation) calls: {total_slow}")
    print(f"Total fast (cache) calls: {total_fast}")
    print("=========================")


if __name__ == "__main__":
    # Tune these for demo
    num_workers = 8  # adjust based on your CPU cores
    run_test(num_workers=num_workers, use_unique_keys=False)