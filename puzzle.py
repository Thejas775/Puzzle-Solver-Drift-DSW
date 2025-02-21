import copy

# ------------------------------------------------------------------
# 1. Define the board layout
#    Suppose we have a 7x7 grid (indices 0..6), but only 43 squares
#    are "valid" puzzle squares. We’ll store each square’s label:
#    - A month label ("Jan", "Feb", ..., "Dec") for 12 squares
#    - A day label ("1", "2", ..., "31") for 31 squares
#    - Or None / "X" if that cell is not used at all
# ------------------------------------------------------------------

BOARD_LAYOUT = [
    ["Jan",   "Feb",   "Mar",   "Apr",   "May",   "Jun",   "X"],
    ["Jul",   "Aug",   "Sep",   "Oct",   "Nov",   "Dec",   "X"],
    ["1",     "2",     "3",     "4",     "5",     "6",     "7"],
    ["8",     "9",     "10",    "11",    "12",    "13",    "14"],
    ["15",    "16",    "17",    "18",    "19",    "20",    "21"],
    ["22",    "23",    "24",    "25",    "26",    "27",    "28"],
    ["29",    "30",    "31",    "X",     "X",     "X",     "X"],
]

ROWS = len(BOARD_LAYOUT)
COLS = len(BOARD_LAYOUT[0])

# ------------------------------------------------------------------
# 2. Define the puzzle pieces
#    Each piece is a list of (row, col) tuples relative to some
#    "origin".  For example, a T-shaped piece covering 5 squares.
#    NOTE: Replace these with the ACTUAL shapes of your puzzle pieces!
# ------------------------------------------------------------------

PIECES = {
    "Red":    [(0,0), (1,0), (1,1), (1,2), (0,2)],   # correct
    "Blue":   [(0,0), (0,1), (0,2), (1,2),(1,3)],           # correct
    "Green":  [(0,0), (1,0), (0,1), (0,2),(0,3)],           # correct
    "Yellow": [(0,0), (0,1), (0,2), (0,3),(1,2)],           # correct
    "LightBlue": [(0,0), (0,1), (0,2), (1,0), (1,1)],    # Correct...
    "Purple": [(0,0), (1,0), (2,0), (2,1),(2,2)],           # Correct
    "Pink":   [(0,0), (1,0), (1,1),(1,2),(2,2)],   #correct
    "Box": [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)]              #Correct
}

# ------------------------------------------------------------------
# Helper: generate all transformations (rotations + flips)
# for a given piece shape
# ------------------------------------------------------------------
def generate_transformations(coords):
    """
    Given a list of (r, c) offsets for a piece, return all
    unique transformations (rotations & flips).
    """
    transformations = set()

    def normalize(shape):
        # shift shape so the top-left is (0,0)
        min_r = min(r for (r,c) in shape)
        min_c = min(c for (r,c) in shape)
        return tuple(sorted((r - min_r, c - min_c) for (r,c) in shape))

    def rotate_90(shape):
        # rotate (r,c) -> (c, -r)
        return [(c, -r) for (r,c) in shape]

    def flip(shape):
        # flip horizontally (r,c) -> (r, -c)
        return [(r, -c) for (r,c) in shape]

    # Start with original
    base = coords
    for _ in range(4):
        # rotate 4 times
        norm = normalize(base)
        transformations.add(norm)
        # also flip
        f = flip(base)
        transformations.add(normalize(f))
        # rotate base
        base = rotate_90(base)

    return list(transformations)

# Precompute transformations for each piece
ALL_PIECES = {}
for color, shape in PIECES.items():
    ALL_PIECES[color] = generate_transformations(shape)


# ------------------------------------------------------------------
# 3. Backtracking solver
# ------------------------------------------------------------------

def solve_calendar(date_month, date_day):
    """
    Solve the puzzle so that the square with label = date_month
    and the square with label = date_day are left uncovered.
    Returns a dictionary mapping (row, col) -> piece_color if solved,
    or None if no solution.
    """

    # A) Identify which squares must remain uncovered
    #    We skip them entirely during coverage
    uncovered_squares = set()
    for r in range(ROWS):
        for c in range(COLS):
            label = BOARD_LAYOUT[r][c]
            if label == date_month or label == date_day:
                uncovered_squares.add((r, c))

    # B) Create a list of all valid squares that must be covered
    valid_squares = []
    for r in range(ROWS):
        for c in range(COLS):
            label = BOARD_LAYOUT[r][c]
            if label != "X" and (r,c) not in uncovered_squares:
                valid_squares.append((r,c))

    # We will try to cover these squares with our 7 pieces
    solution = {}  # (r, c) -> color
    used_pieces = set()

    def backtrack(idx):
        # If idx == len(valid_squares), we've covered them all
        if idx == len(valid_squares):
            return True

        row, col = valid_squares[idx]

        # If already covered, skip to next square
        if (row, col) in solution:
            return backtrack(idx + 1)

        # Try each piece that is not used yet
        for color in ALL_PIECES:
            if color in used_pieces:
                continue
            # Try each transformation
            for shape in ALL_PIECES[color]:
                # shape is a list of offsets, but we want to anchor
                # the "first" cell at (row, col)
                if can_place(shape, row, col, color):
                    # place piece
                    place_piece(shape, row, col, color)
                    used_pieces.add(color)

                    if backtrack(idx + 1):
                        return True

                    # undo
                    remove_piece(shape, row, col)
                    used_pieces.remove(color)

        return False

    def can_place(shape, anchor_r, anchor_c, color):
        """
        Check if placing this piece shape at anchor (anchor_r, anchor_c)
        would fit entirely on valid squares, none of which are already covered.
        """
        for (dr, dc) in shape:
            r = anchor_r + dr
            c = anchor_c + dc
            # check bounds
            if not (0 <= r < ROWS and 0 <= c < COLS):
                return False
            # check if valid square
            if BOARD_LAYOUT[r][c] == "X":
                return False
            # check if uncovered square
            if (r,c) in uncovered_squares:
                # This is the month/day we must leave uncovered
                return False
            # check if already covered by another piece
            if (r,c) in solution:
                return False
        return True

    def place_piece(shape, anchor_r, anchor_c, color):
        """
        Mark squares as covered by 'color'.
        """
        for (dr, dc) in shape:
            r = anchor_r + dr
            c = anchor_c + dc
            solution[(r,c)] = color

    def remove_piece(shape, anchor_r, anchor_c):
        """
        Remove coverage for squares.
        """
        for (dr, dc) in shape:
            r = anchor_r + dr
            c = anchor_c + dc
            if (r,c) in solution:
                del solution[(r,c)]

    # Start backtracking
    if backtrack(0):
        return solution
    else:
        return None

# ------------------------------------------------------------------
# 4. Example usage: Solve for "Mar" and "1"
# ------------------------------------------------------------------

if __name__ == "__main__":
    desired_month = "Feb"
    desired_day   = "30"

    sol = solve_calendar(desired_month, desired_day)
    if sol is None:
        print(f"No solution found for {desired_month} {desired_day}.")
    else:
        print(f"Solution for {desired_month} {desired_day}:")
        # Print out a grid showing which piece covers each square
        # (or 'XX' if uncovered, or '.' if not part of puzzle)
        grid_display = []
        for r in range(ROWS):
            row_str = []
            for c in range(COLS):
                label = BOARD_LAYOUT[r][c]
                if label == "X":
                    row_str.append("..")
                elif (r,c) not in sol and label != "X":
                    # either uncovered because it's month/day
                    # or not used
                    row_str.append("UN")  # uncovered
                else:
                    row_str.append(sol.get((r,c), "..")[:2])
            grid_display.append(" ".join(row_str))

        print("\n".join(grid_display))
