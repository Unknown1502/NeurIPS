"""
Test script to validate the improved ARC solver with pattern recognition.
"""

import sys
import os
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from arc_solver import ARCTaskSolver
from pattern_solutions import PatternSolutions, OptimizedSolutions

def test_task1_solution():
    """Test the corrected Task 1 solution."""
    print("=" * 60)
    print("TESTING TASK 1 SOLUTION")
    print("=" * 60)
    
    # Initialize solver
    solver = ARCTaskSolver(data_dir="./data", solutions_dir="./solutions")
    
    # Test the optimized Task 1 solution
    task1_solution = OptimizedSolutions.TASK1
    print(f"Solution code: {task1_solution}")
    print(f"Byte count: {len(task1_solution.encode('utf-8'))}")
    print(f"Potential score: {max(1, 2500 - len(task1_solution.encode('utf-8')))}")
    
    # Test it on Task 1
    result = solver.process_solution(1, task1_solution, verbose=True)
    
    return result['success']

def test_pattern_recognition():
    """Test pattern recognition on multiple tasks."""
    print("\n" + "=" * 60)
    print("TESTING PATTERN RECOGNITION")
    print("=" * 60)
    
    solver = ARCTaskSolver(data_dir="./data", solutions_dir="./solutions")
    
    # Test pattern detection on first 5 tasks
    for task_id in range(1, 6):
        try:
            task_data = solver.load_task(task_id)
            pattern = solver._detect_pattern(task_data)
            print(f"Task {task_id:03d}: Pattern detected = {pattern}")
        except Exception as e:
            print(f"Task {task_id:03d}: Error - {e}")

def test_auto_solve():
    """Test automatic solving on first 10 tasks."""
    print("\n" + "=" * 60)
    print("TESTING AUTO-SOLVE ON FIRST 10 TASKS")
    print("=" * 60)
    
    solver = ARCTaskSolver(data_dir="./data", solutions_dir="./solutions")
    
    # Auto-solve first 10 tasks
    results = solver.batch_auto_solve(1, 10)
    
    return results

def test_geometric_patterns():
    """Test geometric pattern solutions."""
    print("\n" + "=" * 60)
    print("TESTING GEOMETRIC PATTERNS")
    print("=" * 60)
    
    # Test data for geometric transformations
    test_grid = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    print("Original grid:")
    for row in test_grid:
        print(f"  {row}")
    
    # Test rotations
    print("\nRotate 90° clockwise:")
    rotated_90 = PatternSolutions.rotate_90_clockwise(test_grid)
    for row in rotated_90:
        print(f"  {row}")
    
    print("\nRotate 180°:")
    rotated_180 = PatternSolutions.rotate_180(test_grid)
    for row in rotated_180:
        print(f"  {row}")
    
    print("\nFlip horizontal:")
    flipped_h = PatternSolutions.flip_horizontal(test_grid)
    for row in flipped_h:
        print(f"  {row}")
    
    print("\nFlip vertical:")
    flipped_v = PatternSolutions.flip_vertical(test_grid)
    for row in flipped_v:
        print(f"  {row}")

def run_comprehensive_test():
    """Run comprehensive test of all improvements."""
    print("COMPREHENSIVE TEST OF ARC SOLVER IMPROVEMENTS")
    print("=" * 80)
    
    # Test 1: Task 1 solution
    task1_success = test_task1_solution()
    
    # Test 2: Pattern recognition
    test_pattern_recognition()
    
    # Test 3: Geometric patterns
    test_geometric_patterns()
    
    # Test 4: Auto-solve
    auto_solve_results = test_auto_solve()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Task 1 solution: {'✓ PASS' if task1_success else '✗ FAIL'}")
    print(f"Auto-solve results: {auto_solve_results['successful']}/{auto_solve_results['total_tasks']} tasks solved")
    print(f"Success rate: {auto_solve_results['success_rate']:.1f}%")
    print(f"Total score: {auto_solve_results['total_score']:,} points")
    
    if auto_solve_results['successful'] > 0:
        print(f"Average score: {auto_solve_results['average_score']:.1f} points/task")
        projected_total = auto_solve_results['average_score'] * 400
        print(f"Projected total (400 tasks): {projected_total:,.0f} points")
    
    print("=" * 80)
    
    return {
        'task1_success': task1_success,
        'auto_solve_results': auto_solve_results
    }

if __name__ == "__main__":
    # Check if data directory exists
    data_dir = Path("./data")
    if not data_dir.exists():
        print("ERROR: Data directory not found!")
        print("Please ensure task JSON files are in ./data/ directory")
        sys.exit(1)
    
    # Run tests
    results = run_comprehensive_test()
    
    # Exit with appropriate code
    if results['task1_success'] and results['auto_solve_results']['successful'] > 0:
        print("\n✓ Tests completed successfully!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)