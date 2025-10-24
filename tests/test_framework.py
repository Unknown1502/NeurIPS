"""
Test Suite for ARC Solver Framework

This module contains comprehensive tests for the ARC solver framework
and utility functions.

Run tests: python -m pytest test_framework.py -v

Author: Competition Framework
Date: October 24, 2025
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arc_solver import ARCTaskSolver
from utils import grid_operations as go
from utils import pattern_detection as pd


def test_grid_operations():
    """Test basic grid operations."""
    print("Testing grid operations...")
    
    # Test rotation
    grid = [[1, 2], [3, 4]]
    rotated = go.rotate_90_clockwise(grid)
    expected = [[3, 1], [4, 2]]
    assert rotated == expected, f"Rotation failed: {rotated} != {expected}"
    print("  Rotation: PASS")
    
    # Test flip
    flipped = go.flip_horizontal(grid)
    expected = [[2, 1], [4, 3]]
    assert flipped == expected, f"Flip failed: {flipped} != {expected}"
    print("  Flip: PASS")
    
    # Test transpose
    transposed = go.transpose(grid)
    expected = [[1, 3], [2, 4]]
    assert transposed == expected, f"Transpose failed: {transposed} != {expected}"
    print("  Transpose: PASS")
    
    # Test dimensions
    dims = go.get_dimensions(grid)
    assert dims == (2, 2), f"Dimensions failed: {dims} != (2, 2)"
    print("  Dimensions: PASS")
    
    # Test flatten
    flat = go.flatten(grid)
    expected = [1, 2, 3, 4]
    assert flat == expected, f"Flatten failed: {flat} != {expected}"
    print("  Flatten: PASS")
    
    # Test count
    count = go.count_value(grid, 1)
    assert count == 1, f"Count failed: {count} != 1"
    print("  Count: PASS")
    
    # Test replace
    replaced = go.replace_value(grid, 1, 5)
    expected = [[5, 2], [3, 4]]
    assert replaced == expected, f"Replace failed: {replaced} != {expected}"
    print("  Replace: PASS")
    
    print("Grid operations: ALL TESTS PASSED\n")


def test_pattern_detection():
    """Test pattern detection functions."""
    print("Testing pattern detection...")
    
    # Test symmetry
    symmetric_grid = [[1, 2, 1], [3, 4, 3], [1, 2, 1]]
    symmetry = pd.detect_symmetry(symmetric_grid)
    assert symmetry['horizontal'], "Horizontal symmetry not detected"
    print("  Symmetry detection: PASS")
    
    # Test color distribution
    grid = [[1, 1, 2], [2, 3, 3]]
    dist = pd.analyze_color_distribution(grid)
    assert dist[1] == 2, f"Color distribution failed: {dist}"
    assert dist[2] == 2, f"Color distribution failed: {dist}"
    assert dist[3] == 2, f"Color distribution failed: {dist}"
    print("  Color distribution: PASS")
    
    # Test object detection
    grid = [[0, 0, 0], [0, 1, 1], [0, 1, 0]]
    objects = pd.detect_objects(grid, background=0)
    assert len(objects) == 1, f"Object detection failed: found {len(objects)} objects"
    print("  Object detection: PASS")
    
    print("Pattern detection: ALL TESTS PASSED\n")


def test_solver_initialization():
    """Test solver initialization."""
    print("Testing solver initialization...")
    
    try:
        solver = ARCTaskSolver(data_dir="./data", solutions_dir="./solutions")
        print("  Initialization: PASS")
        return solver
    except Exception as e:
        print(f"  Initialization: FAILED - {e}")
        return None


def test_solution_processing():
    """Test solution processing with a simple example."""
    print("Testing solution processing...")
    
    # Create a simple test solution (identity function)
    test_solution = """
def solve(grid):
    return grid
"""
    
    # Create mock task data
    mock_task = {
        'train': [
            {'input': [[1, 2], [3, 4]], 'output': [[1, 2], [3, 4]]},
            {'input': [[5, 6]], 'output': [[5, 6]]},
        ],
        'test': [
            {'input': [[7, 8]], 'output': [[7, 8]]},
        ],
        'arc-gen': [
            {'input': [[9, 0]], 'output': [[9, 0]]},
        ]
    }
    
    solver = ARCTaskSolver(data_dir="./data", solutions_dir="./solutions")
    
    # Extract and test the function
    namespace = {}
    exec(test_solution, namespace)
    solve_func = namespace['solve']
    
    is_correct, message, stats = solver.test_solution(solve_func, mock_task, verbose=False)
    
    assert is_correct, f"Solution test failed: {message}"
    assert stats['train']['passed'] == 2, "Train examples failed"
    assert stats['test']['passed'] == 1, "Test examples failed"
    assert stats['arc-gen']['passed'] == 1, "Arc-gen examples failed"
    
    print("  Solution processing: PASS")


def test_scoring():
    """Test scoring calculation."""
    print("Testing scoring...")
    
    solver = ARCTaskSolver(data_dir="./data", solutions_dir="./solutions")
    
    # Test correct solution scoring
    score = solver.calculate_score(True, 100)
    expected = 2400
    assert score == expected, f"Scoring failed: {score} != {expected}"
    print("  Correct solution scoring: PASS")
    
    # Test incorrect solution scoring
    score = solver.calculate_score(False, 100)
    expected = 0.001
    assert score == expected, f"Scoring failed: {score} != {expected}"
    print("  Incorrect solution scoring: PASS")
    
    # Test minimum score
    score = solver.calculate_score(True, 3000)
    expected = 1
    assert score == expected, f"Minimum scoring failed: {score} != {expected}"
    print("  Minimum score: PASS")
    
    print("Scoring: ALL TESTS PASSED\n")


def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("ARC SOLVER FRAMEWORK TEST SUITE")
    print("=" * 80)
    print()
    
    try:
        test_grid_operations()
        test_pattern_detection()
        test_solver_initialization()
        test_solution_processing()
        test_scoring()
        
        print("=" * 80)
        print("ALL TESTS PASSED")
        print("=" * 80)
        return True
        
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
