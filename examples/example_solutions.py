"""
Example Solutions for Common ARC-AGI Patterns

This file contains reference implementations for common transformation patterns.
These can serve as templates for solving similar tasks.

Author: Competition Framework
Date: October 24, 2025
"""

from typing import List

Grid = List[List[int]]


# GEOMETRIC TRANSFORMATIONS

def rotate_90_cw(grid: Grid) -> Grid:
    """Rotate 90 degrees clockwise."""
    return [list(row) for row in zip(*grid[::-1])]


def rotate_180(grid: Grid) -> Grid:
    """Rotate 180 degrees."""
    return [row[::-1] for row in grid[::-1]]


def flip_horizontal(grid: Grid) -> Grid:
    """Flip horizontally (mirror left-right)."""
    return [row[::-1] for row in grid]


def flip_vertical(grid: Grid) -> Grid:
    """Flip vertically (mirror top-bottom)."""
    return grid[::-1]


def transpose_grid(grid: Grid) -> Grid:
    """Transpose (swap rows and columns)."""
    return [list(row) for row in zip(*grid)]


# COLOR OPERATIONS

def replace_color(grid: Grid, old: int, new: int) -> Grid:
    """Replace all instances of one color with another."""
    return [[new if c == old else c for c in r] for r in grid]


def invert_colors(grid: Grid, max_color: int = 9) -> Grid:
    """Invert colors (0->9, 1->8, etc.)."""
    return [[max_color - c for c in r] for r in grid]


def swap_colors(grid: Grid, color1: int, color2: int) -> Grid:
    """Swap two colors."""
    return [
        [color2 if c == color1 else color1 if c == color2 else c for c in r]
        for r in grid
    ]


# SCALING OPERATIONS

def scale_up_2x(grid: Grid) -> Grid:
    """Scale up by factor of 2."""
    result = []
    for row in grid:
        scaled_row = []
        for cell in row:
            scaled_row.extend([cell, cell])
        result.extend([scaled_row, scaled_row])
    return result


def scale_down_2x(grid: Grid) -> Grid:
    """Scale down by factor of 2 (sample every other cell)."""
    return [row[::2] for row in grid[::2]]


# TILING OPERATIONS

def tile_2x2(grid: Grid) -> Grid:
    """Tile pattern 2x2."""
    return [r + r for r in grid] + [r + r for r in grid]


def tile_horizontal(grid: Grid, times: int) -> Grid:
    """Tile horizontally."""
    return [r * times for r in grid]


def tile_vertical(grid: Grid, times: int) -> Grid:
    """Tile vertically."""
    return grid * times


# EXTRACTION OPERATIONS

def extract_color(grid: Grid, color: int, background: int = 0) -> Grid:
    """Keep only specific color, replace others with background."""
    return [[c if c == color else background for c in r] for r in grid]


def crop_to_nonzero(grid: Grid) -> Grid:
    """Crop to minimal bounding box of non-zero cells."""
    nonzero = [(i, j) for i, r in enumerate(grid) for j, c in enumerate(r) if c]
    if not nonzero:
        return [[0]]
    
    rows, cols = zip(*nonzero)
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    return [r[min_c:max_c+1] for r in grid[min_r:max_r+1]]


# OVERLAY OPERATIONS

def overlay_with_priority(base: Grid, overlay: Grid, transparent: int = 0) -> Grid:
    """Overlay grids, non-transparent overlay values take precedence."""
    result = [r[:] for r in base]
    for i in range(min(len(base), len(overlay))):
        for j in range(min(len(base[0]), len(overlay[0]))):
            if overlay[i][j] != transparent:
                result[i][j] = overlay[i][j]
    return result


# PATTERN COMPLETION

def fill_horizontal_symmetry(grid: Grid) -> Grid:
    """Fill right half to mirror left half."""
    rows = len(grid)
    cols = len(grid[0])
    result = [r[:] for r in grid]
    
    for i in range(rows):
        for j in range(cols // 2):
            result[i][cols - 1 - j] = result[i][j]
    
    return result


def fill_vertical_symmetry(grid: Grid) -> Grid:
    """Fill bottom half to mirror top half."""
    rows = len(grid)
    result = [r[:] for r in grid]
    
    for i in range(rows // 2):
        result[rows - 1 - i] = result[i][:]
    
    return result


# COUNTING OPERATIONS

def count_colors_to_grid(grid: Grid) -> Grid:
    """Create 1x10 grid with counts of each color."""
    counts = [0] * 10
    for row in grid:
        for cell in row:
            counts[cell] += 1
    return [counts]


# NEIGHBOR OPERATIONS

def apply_majority_filter(grid: Grid) -> Grid:
    """Set each cell to majority color of its neighbors."""
    rows, cols = len(grid), len(grid[0])
    result = [r[:] for r in grid]
    
    for i in range(rows):
        for j in range(cols):
            neighbors = []
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighbors.append(grid[ni][nj])
            
            if neighbors:
                result[i][j] = max(set(neighbors), key=neighbors.count)
    
    return result


# CONDITIONAL OPERATIONS

def keep_if_color(grid: Grid, target: int, background: int = 0) -> Grid:
    """Keep cells matching target color, set others to background."""
    return [[c if c == target else background for c in r] for r in grid]


def apply_mask(grid: Grid, mask: Grid, on_value: int = 1) -> Grid:
    """Apply binary mask to grid."""
    return [
        [grid[i][j] if mask[i][j] == on_value else 0 for j in range(len(grid[0]))]
        for i in range(len(grid))
    ]


# DIMENSION CHANGE OPERATIONS

def flatten_to_row(grid: Grid) -> Grid:
    """Flatten grid to single row."""
    return [[c for r in grid for c in r]]


def reshape_to_square(grid: Grid) -> Grid:
    """Attempt to reshape flat grid to square."""
    flat = [c for r in grid for c in r]
    n = int(len(flat) ** 0.5)
    if n * n != len(flat):
        return grid  # Can't make square
    
    return [flat[i*n:(i+1)*n] for i in range(n)]


# CODE GOLF VERSIONS (minimal byte count)

# Rotate 90 CW (minimal)
solve_rotate_cw = lambda g: [list(r) for r in zip(*g[::-1])]

# Flip horizontal (minimal)
solve_flip_h = lambda g: [r[::-1] for r in g]

# Replace color (minimal)
solve_replace = lambda g, o, n: [[n if c == o else c for c in r] for r in g]

# Transpose (minimal)
solve_transpose = lambda g: [list(r) for r in zip(*g)]

# Scale 2x (minimal)
solve_scale_2x = lambda g: sum([[c for c in r for _ in range(2)] * 2 for r in g], [])


# EXAMPLE: Complete solution with analysis

def example_solution_with_analysis():
    """
    Example showing complete solution process.
    
    Task: Rotate grid 90 degrees clockwise
    
    Analysis:
    - Input: NxM grid
    - Output: MxN grid (dimensions swap)
    - Each input[i][j] maps to output[j][N-1-i]
    
    Clear solution:
    """
    def solve_clear(grid):
        rows = len(grid)
        cols = len(grid[0])
        result = []
        for j in range(cols):
            new_row = []
            for i in range(rows - 1, -1, -1):
                new_row.append(grid[i][j])
            result.append(new_row)
        return result
    
    """
    Optimized solution:
    """
    def solve_optimized(grid):
        return [list(row) for row in zip(*grid[::-1])]
    
    """
    Code golf solution (39 bytes):
    """
    solve = lambda g: [list(r) for r in zip(*g[::-1])]
    
    return solve


# TESTING UTILITIES

def test_solution(solve_func, test_cases):
    """
    Test solution against test cases.
    
    Args:
        solve_func: Solution function
        test_cases: List of (input, expected_output) tuples
        
    Returns:
        True if all tests pass
    """
    for i, (inp, expected) in enumerate(test_cases):
        result = solve_func(inp)
        if result != expected:
            print(f"Test {i+1} FAILED")
            print(f"  Input:    {inp}")
            print(f"  Expected: {expected}")
            print(f"  Got:      {result}")
            return False
    
    print(f"All {len(test_cases)} tests PASSED")
    return True


if __name__ == "__main__":
    print("Example Solutions Reference")
    print("=" * 80)
    print()
    print("This file contains reference implementations for common patterns.")
    print("Use these as templates for solving similar ARC-AGI tasks.")
    print()
    
    # Test a simple transformation
    test_grid = [[1, 2], [3, 4]]
    
    print("Example transformations on:", test_grid)
    print()
    print("Rotate 90 CW:", rotate_90_cw(test_grid))
    print("Flip horizontal:", flip_horizontal(test_grid))
    print("Transpose:", transpose_grid(test_grid))
    print("Scale 2x:", scale_up_2x(test_grid))
    print("Replace 1->5:", replace_color(test_grid, 1, 5))
