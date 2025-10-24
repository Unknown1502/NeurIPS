"""
Pattern Detection Utility Module

This module provides functions for detecting common patterns in ARC-AGI tasks.
Use these to analyze task characteristics and guide solution development.

Author: Competition Framework
Date: October 24, 2025
"""

from typing import List, Tuple, Dict, Set
from collections import Counter


Grid = List[List[int]]


def detect_transformation_type(
    input_grids: List[Grid],
    output_grids: List[Grid]
) -> Dict[str, bool]:
    """
    Detect likely transformation types based on input/output pairs.
    
    Args:
        input_grids: List of input grids
        output_grids: List of output grids
        
    Returns:
        Dictionary of transformation characteristics
    """
    characteristics = {
        'preserves_dimensions': True,
        'changes_dimensions': False,
        'increases_size': False,
        'decreases_size': False,
        'preserves_colors': True,
        'adds_colors': False,
        'removes_colors': False,
        'constant_output_size': True,
    }
    
    if not input_grids or not output_grids:
        return characteristics
    
    # Check dimension changes
    input_dims = [get_dimensions(g) for g in input_grids]
    output_dims = [get_dimensions(g) for g in output_grids]
    
    for inp_dim, out_dim in zip(input_dims, output_dims):
        if inp_dim != out_dim:
            characteristics['preserves_dimensions'] = False
            characteristics['changes_dimensions'] = True
            
            inp_size = inp_dim[0] * inp_dim[1]
            out_size = out_dim[0] * out_dim[1]
            
            if out_size > inp_size:
                characteristics['increases_size'] = True
            elif out_size < inp_size:
                characteristics['decreases_size'] = True
    
    # Check if output size is constant
    if len(set(output_dims)) > 1:
        characteristics['constant_output_size'] = False
    
    # Check color changes
    for inp, out in zip(input_grids, output_grids):
        inp_colors = set(flatten_grid(inp))
        out_colors = set(flatten_grid(out))
        
        if inp_colors != out_colors:
            characteristics['preserves_colors'] = False
            
            if out_colors - inp_colors:
                characteristics['adds_colors'] = True
            
            if inp_colors - out_colors:
                characteristics['removes_colors'] = True
    
    return characteristics


def get_dimensions(grid: Grid) -> Tuple[int, int]:
    """Get grid dimensions."""
    if not grid:
        return (0, 0)
    return (len(grid), len(grid[0]) if grid[0] else 0)


def flatten_grid(grid: Grid) -> List[int]:
    """Flatten grid to 1D list."""
    return [cell for row in grid for cell in row]


def analyze_color_distribution(grid: Grid) -> Dict[int, int]:
    """
    Analyze color distribution in grid.
    
    Args:
        grid: Input grid
        
    Returns:
        Dictionary mapping color values to counts
    """
    flat = flatten_grid(grid)
    return dict(Counter(flat))


def detect_objects(grid: Grid, background: int = 0) -> List[Set[Tuple[int, int]]]:
    """
    Detect connected objects in grid (4-connectivity).
    
    Args:
        grid: Input grid
        background: Background color value
        
    Returns:
        List of sets, each containing (row, col) positions of an object
    """
    rows, cols = get_dimensions(grid)
    visited = set()
    objects = []
    
    def flood_fill(start_row: int, start_col: int, color: int) -> Set[Tuple[int, int]]:
        """Flood fill to find connected object."""
        obj = set()
        stack = [(start_row, start_col)]
        
        while stack:
            r, c = stack.pop()
            
            if (r, c) in visited:
                continue
            
            if r < 0 or r >= rows or c < 0 or c >= cols:
                continue
            
            if grid[r][c] != color:
                continue
            
            visited.add((r, c))
            obj.add((r, c))
            
            # Add 4 neighbors
            stack.extend([(r-1, c), (r+1, c), (r, c-1), (r, c+1)])
        
        return obj
    
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in visited and grid[i][j] != background:
                obj = flood_fill(i, j, grid[i][j])
                if obj:
                    objects.append(obj)
    
    return objects


def detect_symmetry(grid: Grid) -> Dict[str, bool]:
    """
    Detect various types of symmetry in grid.
    
    Args:
        grid: Input grid
        
    Returns:
        Dictionary indicating presence of different symmetries
    """
    return {
        'horizontal': is_symmetric_horizontal(grid),
        'vertical': is_symmetric_vertical(grid),
        'diagonal_main': is_symmetric_diagonal_main(grid),
        'diagonal_anti': is_symmetric_diagonal_anti(grid),
        'rotational_90': is_rotational_symmetric(grid, 90),
        'rotational_180': is_rotational_symmetric(grid, 180),
    }


def is_symmetric_horizontal(grid: Grid) -> bool:
    """Check horizontal symmetry (left-right mirror)."""
    return all(row == row[::-1] for row in grid)


def is_symmetric_vertical(grid: Grid) -> bool:
    """Check vertical symmetry (top-bottom mirror)."""
    return grid == grid[::-1]


def is_symmetric_diagonal_main(grid: Grid) -> bool:
    """Check main diagonal symmetry."""
    rows, cols = get_dimensions(grid)
    if rows != cols:
        return False
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != grid[j][i]:
                return False
    return True


def is_symmetric_diagonal_anti(grid: Grid) -> bool:
    """Check anti-diagonal symmetry."""
    rows, cols = get_dimensions(grid)
    if rows != cols:
        return False
    
    n = rows
    for i in range(n):
        for j in range(n):
            if grid[i][j] != grid[n-1-j][n-1-i]:
                return False
    return True


def is_rotational_symmetric(grid: Grid, degrees: int) -> bool:
    """Check rotational symmetry."""
    from .grid_operations import rotate_90_clockwise, rotate_180
    
    if degrees == 90:
        rotated = rotate_90_clockwise(grid)
    elif degrees == 180:
        rotated = rotate_180(grid)
    else:
        return False
    
    return grid == rotated


def detect_repetition(grid: Grid) -> Dict[str, bool]:
    """
    Detect if grid contains repeated patterns.
    
    Args:
        grid: Input grid
        
    Returns:
        Dictionary indicating types of repetition found
    """
    rows, cols = get_dimensions(grid)
    
    result = {
        'horizontal_repetition': False,
        'vertical_repetition': False,
        'tile_repetition': False,
    }
    
    # Check horizontal repetition
    for divisor in range(2, cols + 1):
        if cols % divisor == 0:
            segment_size = cols // divisor
            if all(
                row[i:i+segment_size] == row[0:segment_size]
                for row in grid
                for i in range(0, cols, segment_size)
            ):
                result['horizontal_repetition'] = True
                break
    
    # Check vertical repetition
    for divisor in range(2, rows + 1):
        if rows % divisor == 0:
            segment_size = rows // divisor
            segments = [grid[i:i+segment_size] for i in range(0, rows, segment_size)]
            if all(seg == segments[0] for seg in segments):
                result['vertical_repetition'] = True
                break
    
    # Check 2D tile repetition
    for row_div in range(2, rows + 1):
        for col_div in range(2, cols + 1):
            if rows % row_div == 0 and cols % col_div == 0:
                tile_h = rows // row_div
                tile_w = cols // col_div
                
                first_tile = [row[0:tile_w] for row in grid[0:tile_h]]
                
                all_match = True
                for i in range(0, rows, tile_h):
                    for j in range(0, cols, tile_w):
                        tile = [row[j:j+tile_w] for row in grid[i:i+tile_h]]
                        if tile != first_tile:
                            all_match = False
                            break
                    if not all_match:
                        break
                
                if all_match:
                    result['tile_repetition'] = True
                    return result
    
    return result


def find_color_mappings(
    input_grids: List[Grid],
    output_grids: List[Grid]
) -> Dict[int, Set[int]]:
    """
    Find possible color mappings between input and output.
    
    Args:
        input_grids: List of input grids
        output_grids: List of output grids
        
    Returns:
        Dictionary mapping input colors to possible output colors
    """
    mappings = {}
    
    for inp, out in zip(input_grids, output_grids):
        inp_flat = flatten_grid(inp)
        out_flat = flatten_grid(out)
        
        if len(inp_flat) == len(out_flat):
            for inp_val, out_val in zip(inp_flat, out_flat):
                if inp_val not in mappings:
                    mappings[inp_val] = set()
                mappings[inp_val].add(out_val)
    
    return mappings


def analyze_task_complexity(
    input_grids: List[Grid],
    output_grids: List[Grid]
) -> Dict[str, any]:
    """
    Analyze overall task complexity.
    
    Args:
        input_grids: List of input grids
        output_grids: List of output grids
        
    Returns:
        Dictionary with complexity metrics
    """
    metrics = {
        'max_input_size': 0,
        'max_output_size': 0,
        'unique_colors_input': set(),
        'unique_colors_output': set(),
        'dimension_changes': False,
        'variable_output_size': False,
    }
    
    input_dims = []
    output_dims = []
    
    for inp in input_grids:
        rows, cols = get_dimensions(inp)
        size = rows * cols
        metrics['max_input_size'] = max(metrics['max_input_size'], size)
        metrics['unique_colors_input'].update(flatten_grid(inp))
        input_dims.append((rows, cols))
    
    for out in output_grids:
        rows, cols = get_dimensions(out)
        size = rows * cols
        metrics['max_output_size'] = max(metrics['max_output_size'], size)
        metrics['unique_colors_output'].update(flatten_grid(out))
        output_dims.append((rows, cols))
    
    # Check if dimensions change
    for inp_dim, out_dim in zip(input_dims, output_dims):
        if inp_dim != out_dim:
            metrics['dimension_changes'] = True
    
    # Check if output size varies
    if len(set(output_dims)) > 1:
        metrics['variable_output_size'] = True
    
    metrics['unique_colors_input'] = len(metrics['unique_colors_input'])
    metrics['unique_colors_output'] = len(metrics['unique_colors_output'])
    
    return metrics


def suggest_approach(
    input_grids: List[Grid],
    output_grids: List[Grid]
) -> List[str]:
    """
    Suggest possible approaches based on pattern analysis.
    
    Args:
        input_grids: List of input grids
        output_grids: List of output grids
        
    Returns:
        List of suggested approach descriptions
    """
    suggestions = []
    
    trans_type = detect_transformation_type(input_grids, output_grids)
    
    if trans_type['preserves_dimensions']:
        suggestions.append("Cell-by-cell transformation (same dimensions)")
    
    if trans_type['increases_size']:
        suggestions.append("Scaling or expansion operation")
    
    if trans_type['decreases_size']:
        suggestions.append("Filtering, cropping, or extraction operation")
    
    if trans_type['constant_output_size']:
        suggestions.append("Output size is constant - may be counting or aggregation")
    
    # Check for geometric transformations
    for inp, out in zip(input_grids, output_grids):
        from .grid_operations import (
            rotate_90_clockwise, rotate_180, 
            flip_horizontal, flip_vertical, transpose
        )
        
        if rotate_90_clockwise(inp) == out:
            suggestions.append("90° clockwise rotation")
            break
        elif rotate_180(inp) == out:
            suggestions.append("180° rotation")
            break
        elif flip_horizontal(inp) == out:
            suggestions.append("Horizontal flip")
            break
        elif flip_vertical(inp) == out:
            suggestions.append("Vertical flip")
            break
        elif transpose(inp) == out:
            suggestions.append("Transpose operation")
            break
    
    # Check for color operations
    color_mappings = find_color_mappings(input_grids, output_grids)
    if color_mappings:
        consistent_mapping = all(len(vals) == 1 for vals in color_mappings.values())
        if consistent_mapping:
            suggestions.append("Simple color replacement mapping")
    
    if not suggestions:
        suggestions.append("Complex custom transformation - requires detailed analysis")
    
    return suggestions
