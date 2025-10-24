"""
Quick fix script to test the improved solver.
"""

import sys
from pathlib import Path

# Add project directory to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from arc_solver import ARCTaskSolver

def test_fixed_solver():
    """Test the fixed solver on first 10 tasks."""
    print("Testing fixed solver...")
    
    solver = ARCTaskSolver(data_dir="./data", solutions_dir="./solutions")
    
    # Test first 10 tasks
    results = solver.batch_auto_solve(1, 10)
    
    print(f"\nFixed Results:")
    print(f"Success Rate: {results['success_rate']:.1f}%")
    print(f"Tasks Solved: {results['successful']}/{results['total_tasks']}")
    print(f"Total Score: {results['total_score']:,} points")
    
    return results

if __name__ == "__main__":
    test_fixed_solver()