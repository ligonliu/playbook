import heapq

def get_skyline(buildings):
    """
    High-performance skyline algorithm using a sweep line with a max-heap.
    buildings: List of [left, right, height] triples.
    Returns the skyline as a list of [x, height] key points.
    Time complexity: O(n log n)
    """
    # Create events: (x, neg_height, end_x)
    events = []
    for left, right, height in buildings:
        events.append((left, -height, right))  # building start
        events.append((right, 0, 0))           # building end

    # Sort events by x, then by height to ensure starts before ends
    events.sort()

    # Max-heap of active buildings: (neg_height, end_x)
    heap = [(0, float('inf'))]
    result = []
    prev_height = 0

    for x, neg_h, r in events:
        if neg_h < 0:
            # Insert new building
            heapq.heappush(heap, (neg_h, r))
        # Remove buildings that have ended
        while heap and heap[0][1] <= x:
            heapq.heappop(heap)
        # Current highest building
        curr_height = -heap[0][0]
        # If height changes, add a key point
        if curr_height != prev_height:
            result.append([x, curr_height])
            prev_height = curr_height

    return result
