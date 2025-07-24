import random
import json

def generate_cases():
    """
    Generates a random list of building triples.
    Each triple is [left, right, height] with:
      0 ≤ left < right ≤ 1000
      1 ≤ height ≤ 1000
    The number of buildings is a random integer between 1 and 100.
    """
    n = random.randint(1, 100)
    buildings = []
    for _ in range(n):
        left = random.randint(0, 999)
        right = random.randint(left + 1, 1000)
        height = random.randint(1, 1000)
        buildings.append([left, right, height])
    return buildings

if __name__ == "__main__":
    with open("test_cases.ndjson", "w") as f:
        for _ in range(1000):
            case = generate_cases()
            f.write(json.dumps(case) + "\n")
