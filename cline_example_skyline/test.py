import json
from skyline import get_skyline as slow_skyline
from skyline_fast import get_skyline as fast_skyline

def main():
    fail_count = 0
    total = 0
    with open("test_cases.ndjson", "r") as f:
        for line in f:
            buildings = json.loads(line)
            slow = slow_skyline(buildings)
            fast = fast_skyline(buildings)
            if slow != fast:
                fail_count += 1
            total += 1

    print(f"Total cases: {total}")
    print(f"Number of mismatches: {fail_count}")

if __name__ == "__main__":
    main()
