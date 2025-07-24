import json
import time
from skyline import get_skyline as slow_skyline
from skyline_fast import get_skyline as fast_skyline

def main():
    # Load all test cases
    with open("test_cases.ndjson", "r") as f:
        cases = [json.loads(line) for line in f]

    # Measure slow algorithm
    start = time.perf_counter()
    for buildings in cases:
        slow_skyline(buildings)
    slow_time = time.perf_counter() - start

    # Measure fast algorithm
    start = time.perf_counter()
    for buildings in cases:
        fast_skyline(buildings)
    fast_time = time.perf_counter() - start

    # Report results
    print(f"Slow total time: {slow_time:.4f}s")
    print(f"Fast total time: {fast_time:.4f}s")
    if fast_time > 0:
        speedup = slow_time / fast_time
        print(f"Speedup: {speedup:.2f}×")
    else:
        print("Fast algorithm ran too quickly to measure speedup.")

if __name__ == "__main__":
    main()
