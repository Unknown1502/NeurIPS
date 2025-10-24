"""
Grid Operations Utility Module

This module provides common grid transformation operations useful for
solving ARC-AGI tasks. These functions can be imported and used as
building blocks for solutions.

Author: Competition Framework
Date: October 24, 2025
"""

from typing import List, Tuple, Callable, Any

Grid = List[List[int]]


def rotate_90_clockwise(grid: Grid) -> Grid:
    """
    Rotate grid 90 degrees clockwise.
    
    Args:
        grid: Input grid
        
    Returns:
        Rotated grid
    """
    return [list(row) for row in zip(*grid[::-1])]


def rotate_90_counterclockwise(grid: Grid) -> Grid:
    """
    Rotate grid 90 degrees counter-clockwise.
    
    Args:
        grid: Input grid
        
    Returns:
        Rotated grid
    """
    return [list(row) for row in zip(*grid)][::-1]


def rotate_180(grid: Grid) -> Grid:
    """
    Rotate grid 180 degrees.
    
    Args:
        grid: Input grid
        
    Returns:
        Rotated grid
    """
    return [row[::-1] for row in grid[::-1]]


def flip_horizontal(grid: Grid) -> Grid:
    """
    Flip grid horizontally (mirror left-right).
    
    Args:
        grid: Input grid
        
    Returns:
        Flipped grid
    """
    return [row[::-1] for row in grid]


def flip_vertical(grid: Grid) -> Grid:
    """
    Flip grid vertically (mirror top-bottom).
    
    Args:
        grid: Input grid
        
    Returns:
        Flipped grid
    """
    return grid[::-1]


def transpose(grid: Grid) -> Grid:
    """
    Transpose grid (swap rows and columns).
    
    Args:
        grid: Input grid
        
    Returns:
        Transposed grid
    """
    return [list(row) for row in zip(*grid)]


def get_dimensions(grid: Grid) -> Tuple[int, int]:
    """
    Get dimensions of grid.
    
    Args:
        grid: Input grid
        
    Returns:
        Tuple of (rows, columns)
    """
    if not grid:
        return (0, 0)
    return (len(grid), len(grid[0]) if grid[0] else 0)


def create_grid(rows: int, cols: int, fill_value: int = 0) -> Grid:
    """
    Create new grid with specified dimensions.
    
    Args:
        rows: Number of rows
        cols: Number of columns
        fill_value: Value to fill grid with
        
    Returns:
        New grid filled with fill_value
    """
    return [[fill_value] * cols for _ in range(rows)]


def copy_grid(grid: Grid) -> Grid:
    """
    Create deep copy of grid.
    
    Args:
        grid: Input grid
        
    Returns:
        Copy of grid
    """
    return [row[:] for row in grid]


def extract_subgrid(
    grid: Grid,
    row_start: int,
    col_start: int,
    row_end: int,
    col_end: int
) -> Grid:
    """
    Extract rectangular subgrid.
    
    Args:
        grid: Input grid
        row_start: Starting row (inclusive)
        col_start: Starting column (inclusive)
        row_end: Ending row (exclusive)
        col_end: Ending column (exclusive)
        
    Returns:
        Extracted subgrid
    """
    return [row[col_start:col_end] for row in grid[row_start:row_end]]


def flatten(grid: Grid) -> List[int]:
    """
    Flatten grid to 1D list.
    
    Args:
        grid: Input grid
        
    Returns:
        Flattened list of all values
    """
    return [cell for row in grid for cell in row]


def count_value(grid: Grid, value: int) -> int:
    """
    Count occurrences of a value in grid.
    
    Args:
        grid: Input grid
        value: Value to count
        
    Returns:
        Number of occurrences
    """
    return sum(cell == value for row in grid for cell in row)


def find_positions(grid: Grid, value: int) -> List[Tuple[int, int]]:
    """
    Find all positions of a value in grid.
    
    Args:
        grid: Input grid
        value: Value to find
        
    Returns:
        List of (row, col) tuples
    """
    return [
        (i, j)
        for i, row in enumerate(grid)
        for j, cell in enumerate(row)
        if cell == value
    ]


def replace_value(grid: Grid, old_value: int, new_value: int) -> Grid:
    """
    Replace all occurrences of one value with another.
    
    Args:
        grid: Input grid
        old_value: Value to replace
        new_value: Replacement value
        
    Returns:
        Grid with values replaced
    """
    return [
        [new_value if cell == old_value else cell for cell in row]
        for row in grid
    ]


def map_values(grid: Grid, mapping: dict) -> Grid:
    """
    Map values according to dictionary.
    
    Args:
        grid: Input grid
        mapping: Dictionary mapping old values to new values
        
    Returns:
        Grid with mapped values
    """
    return [
        [mapping.get(cell, cell) for cell in row]
        for row in grid
    ]


def apply_function(grid: Grid, func: Callable[[int], int]) -> Grid:
    """
    Apply function to each cell.
    
    Args:
        grid: Input grid
        func: Function to apply to each cell value
        
    Returns:
        Grid with function applied
    """
    return [[func(cell) for cell in row] for row in grid]


def overlay_grids(base: Grid, overlay: Grid, transparent: int = 0) -> Grid:
    """
    Overlay one grid on another. Non-transparent values in overlay take precedence.
    
    Args:
        base: Base grid
        overlay: Overlay grid
        transparent: Value considered transparent in overlay
        
    Returns:
        Combined grid
    """
    rows = len(base)
    cols = len(base[0]) if base else 0
    
    result = copy_grid(base)
    
    for i in range(min(rows, len(overlay))):
        for j in range(min(cols, len(overlay[i]) if i < len(overlay) else 0)):
            if overlay[i][j] != transparent:
                result[i][j] = overlay[i][j]
    
    return result


def tile_grid(grid: Grid, times_horizontal: int, times_vertical: int) -> Grid:
    """
    Tile grid by repeating it horizontally and vertically.
    
    Args:
        grid: Input grid
        times_horizontal: Number of horizontal repetitions
        times_vertical: Number of vertical repetitions
        
    Returns:
        Tiled grid
    """
    # Tile horizontally first
    tiled_rows = [row * times_horizontal for row in grid]
    # Then tile vertically
    return tiled_rows * times_vertical


def scale_grid(grid: Grid, scale: int) -> Grid:
    """
    Scale grid by repeating each cell scale x scale times.
    
    Args:
        grid: Input grid
        scale: Scaling factor
        
    Returns:
        Scaled grid
    """
    result = []
    for row in grid:
        scaled_row = []
        for cell in row:
            scaled_row.extend([cell] * scale)
        for _ in range(scale):
            result.append(scaled_row[:])
    return result


def find_bounding_box(grid: Grid, value: int = None) -> Tuple[int, int, int, int]:
    """
    Find bounding box of non-zero (or specific value) cells.
    
    Args:
        grid: Input grid
        value: Specific value to find (None = any non-zero)
        
    Returns:
        Tuple of (min_row, min_col, max_row, max_col) or None if not found
    """
    positions = []
    
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if value is None:
                if cell != 0:
                    positions.append((i, j))
            else:
                if cell == value:
                    positions.append((i, j))
    
    if not positions:
        return None
    
    rows, cols = zip(*positions)
    return (min(rows), min(cols), max(rows), max(cols))


def extract_object(grid: Grid, value: int = None) -> Grid:
    """
    Extract minimal bounding box containing all instances of value.
    
    Args:
        grid: Input grid
        value: Value to extract (None = any non-zero)
        
    Returns:
        Extracted subgrid
    """
    bbox = find_bounding_box(grid, value)
    if bbox is None:
        return [[]]
    
    min_row, min_col, max_row, max_col = bbox
    return extract_subgrid(grid, min_row, min_col, max_row + 1, max_col + 1)


def pad_grid(
    grid: Grid,
    pad_top: int,
    pad_bottom: int,
    pad_left: int,
    pad_right: int,
    pad_value: int = 0
) -> Grid:
    """
    Add padding around grid.
    
    Args:
        grid: Input grid
        pad_top: Rows to add at top
        pad_bottom: Rows to add at bottom
        pad_left: Columns to add at left
        pad_right: Columns to add at right
        pad_value: Value to use for padding
        
    Returns:
        Padded grid
    """
    rows, cols = get_dimensions(grid)
    new_cols = cols + pad_left + pad_right
    
    result = []
    
    # Top padding
    for _ in range(pad_top):
        result.append([pad_value] * new_cols)
    
    # Original rows with side padding
    for row in grid:
        new_row = [pad_value] * pad_left + row + [pad_value] * pad_right
        result.append(new_row)
    
    # Bottom padding
    for _ in range(pad_bottom):
        result.append([pad_value] * new_cols)
    
    return result


def get_neighbors(
    grid: Grid,
    row: int,
    col: int,
    diagonal: bool = False
) -> List[Tuple[int, int, int]]:
    """
    Get neighboring cells (value and position).
    
    Args:
        grid: Input grid
        row: Row index
        col: Column index
        diagonal: Whether to include diagonal neighbors
        
    Returns:
        List of (row, col, value) tuples for neighbors
    """
    rows, cols = get_dimensions(grid)
    neighbors = []
    
    # Orthogonal neighbors
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Add diagonal if requested
    if diagonal:
        directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col, grid[new_row][new_col]))
    
    return neighbors


def is_symmetric_horizontal(grid: Grid) -> bool:
    """
    Check if grid is symmetric horizontally.
    
    Args:
        grid: Input grid
        
    Returns:
        True if symmetric
    """
    return all(row == row[::-1] for row in grid)


def is_symmetric_vertical(grid: Grid) -> bool:
    """
    Check if grid is symmetric vertically.
    
    Args:
        grid: Input grid
        
    Returns:
        True if symmetric
    """
    return grid == grid[::-1]


def get_unique_values(grid: Grid) -> List[int]:
    """
    Get list of unique values in grid.
    
    Args:
        grid: Input grid
        
    Returns:
        Sorted list of unique values
    """
    return sorted(set(flatten(grid)))


def crop_to_content(grid: Grid, background: int = 0) -> Grid:
    """
    Crop grid to minimal bounding box of non-background content.
    
    Args:
        grid: Input grid
        background: Background value to crop
        
    Returns:
        Cropped grid
    """
    bbox = find_bounding_box(grid, value=None)
    if bbox is None:
        return [[background]]
    
    min_row, min_col, max_row, max_col = bbox
    return extract_subgrid(grid, min_row, min_col, max_row + 1, max_col + 1)
