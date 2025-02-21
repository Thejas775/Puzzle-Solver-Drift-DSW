import copy

# ------------------------------------------------------------------
# 1. Define the board layout
#    A 7x7 grid with 43 valid squares (12 month labels and 31 day labels).
#    Cells that are not used are marked as "X".
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
# 2. Define the puzzle pieces with their relative coordinates.
#    (Each list should accurately represent the physical piece.)
#    In this example, we have 8 pieces.
# ------------------------------------------------------------------

PIECES = {
    "Red":       [(0,0), (1,0), (1,1), (1,2), (0,2)],    # correct
    "Blue":      [(0,0), (0,1), (0,2), (1,2), (1,3)],      # correct
    "Green":     [(0,0), (1,0), (0,1), (0,2), (0,3)],      # correct
    "Yellow":    [(0,0), (0,1), (0,2), (0,3), (1,2)],      # correct
    "LightBlue": [(0,0), (0,1), (0,2), (1,0), (1,1)],       # correct
    "Purple":    [(0,0), (1,0), (2,0), (2,1), (2,2)],       # correct
    "Pink":      [(0,0), (1,0), (1,1), (1,2), (2,2)],       # correct
    "Box":       [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1)]   # correct
}

# ------------------------------------------------------------------
# Helper: generate all transformations (rotations + flips)
# for a given piece shape.
# ------------------------------------------------------------------
def generate_transformations(coords):
    """
    Given a list of (r, c) offsets for a piece, return all unique
    transformations (rotations and horizontal flips).
    """
    transformations = set()

    def normalize(shape):
        # Shift shape so that its top-left is at (0,0)
        min_r = min(r for (r, c) in shape)
        min_c = min(c for (r, c) in shape)
        return tuple(sorted((r - min_r, c - min_c) for (r, c) in shape))

    def rotate_90(shape):
        # Rotate (r,c) -> (c, -r)
        return [(c, -r) for (r, c) in shape]

    def flip(shape):
        # Flip horizontally: (r,c) -> (r, -c)
        return [(r, -c) for (r, c) in shape]

    base = coords
    for _ in range(4):
        norm = normalize(base)
        transformations.add(norm)
        # Also add the flipped version.
        flipped = flip(base)
        transformations.add(normalize(flipped))
        # Rotate base for next iteration.
        base = rotate_90(base)

    return list(transformations)

# Precompute transformations for each piece.
ALL_PIECES = {}
for color, shape in PIECES.items():
    ALL_PIECES[color] = generate_transformations(shape)

# ------------------------------------------------------------------
# 3. Backtracking solver using the "minimum remaining values" heuristic.
# ------------------------------------------------------------------

def solve_calendar(date_month, date_day):
    """
    Solve the puzzle so that the squares labeled date_month and date_day
    remain uncovered. Returns a dictionary mapping (row, col) -> piece_color
    if a solution is found, or None otherwise.
    """
    # A) Identify squares that must remain uncovered.
    uncovered_squares = set()
    for r in range(ROWS):
        for c in range(COLS):
            label = BOARD_LAYOUT[r][c]
            if label == date_month or label == date_day:
                uncovered_squares.add((r, c))
    
    # B) List all valid squares that must be covered (exclude "X" and uncovered).
    valid_squares = []
    for r in range(ROWS):
        for c in range(COLS):
            if BOARD_LAYOUT[r][c] != "X" and (r, c) not in uncovered_squares:
                valid_squares.append((r, c))
    
    solution = {}   # mapping: (r, c) -> piece_color
    used_pieces = set()

    def all_covered():
        """Return True if every valid square is covered."""
        return all(cell in solution for cell in valid_squares)

    def backtrack():
        if all_covered():
            return True

        # Choose an uncovered cell from valid_squares that has the fewest placement options.
        best_cell = None
        best_options = None
        for cell in valid_squares:
            if cell in solution:
                continue
            options = []
            # For each unused piece and for each transformation, try to see if
            # you can place the piece such that one of its squares covers this cell.
            for color in ALL_PIECES:
                if color in used_pieces:
                    continue
                for shape in ALL_PIECES[color]:
                    for (dr, dc) in shape:
                        anchor_r = cell[0] - dr
                        anchor_c = cell[1] - dc
                        if can_place(shape, anchor_r, anchor_c):
                            options.append((color, shape, anchor_r, anchor_c))
            if len(options) == 0:
                # No possible placements for this cell → backtrack.
                return False
            if best_options is None or len(options) < len(best_options):
                best_options = options
                best_cell = cell

        # Try each possible placement for the best_cell.
        for (color, shape, anchor_r, anchor_c) in best_options:
            place_piece(shape, anchor_r, anchor_c, color)
            used_pieces.add(color)
            if backtrack():
                return True
            # Undo placement.
            remove_piece(shape, anchor_r, anchor_c)
            used_pieces.remove(color)
        return False

    def can_place(shape, anchor_r, anchor_c):
        """
        Check if placing the piece (given by shape and anchored at (anchor_r, anchor_c))
        fits entirely on valid squares that are not already covered or marked as uncovered.
        """
        for (dr, dc) in shape:
            r = anchor_r + dr
            c = anchor_c + dc
            if not (0 <= r < ROWS and 0 <= c < COLS):
                return False
            if BOARD_LAYOUT[r][c] == "X":
                return False
            if (r, c) in uncovered_squares:
                return False
            if (r, c) in solution:
                return False
        return True

    def place_piece(shape, anchor_r, anchor_c, color):
        """
        Mark the squares covered by the piece with the given color.
        """
        for (dr, dc) in shape:
            r = anchor_r + dr
            c = anchor_c + dc
            solution[(r, c)] = color

    def remove_piece(shape, anchor_r, anchor_c):
        """
        Remove the piece from the solution.
        """
        for (dr, dc) in shape:
            r = anchor_r + dr
            c = anchor_c + dc
            if (r, c) in solution:
                del solution[(r, c)]

    if backtrack():
        return solution
    else:
        return None

# ------------------------------------------------------------------
# 4. Example usage.
#    Change the desired_month and desired_day to a date that is known
#    to work in your physical puzzle.
# ------------------------------------------------------------------

if __name__ == "__main__":
    # For example, try a date that is known to be solvable.
    desired_month = "Feb"
    desired_day   = "22"

    sol = solve_calendar(desired_month, desired_day)
    if sol is None:
        print(f"No solution found for {desired_month} {desired_day}.")
    else:
        print(f"Solution for {desired_month} {desired_day}:")
        # Print out a grid showing which piece covers each square.
        for r in range(ROWS):
            row_str = []
            for c in range(COLS):
                label = BOARD_LAYOUT[r][c]
                if label == "X":
                    row_str.append("..")
                elif (r, c) not in sol and label != "X":
                    # Uncovered (month/day cell).
                    row_str.append("UN")
                else:
                    row_str.append(sol.get((r, c), "..")[:2])
            print(" ".join(row_str))
