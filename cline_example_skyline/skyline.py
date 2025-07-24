def get_skyline(buildings):
    """
    buildings: List of [left, right, height] triples.
    Returns the skyline as a list of [x, height] key points.
    """
    # Collect and sort all unique edge coordinates
    xs = sorted({x for left, right, height in buildings for x in (left, right)})
    result = []
    prev_height = 0

    # Sweep through each x-coordinate
    for x in xs:
        # Determine the current max height at this x
        curr_height = 0
        for left, right, height in buildings:
            if left <= x < right and height > curr_height:
                curr_height = height

        # Record a key point if the height changes
        if curr_height != prev_height:
            result.append([x, curr_height])
            prev_height = curr_height

    return result
