"""
Demonstration of the improved ARC solver with automatic pattern recognition.
This script shows how to achieve 100% success rate on ARC tasks.
"""

import sys
from pathlib import Path

# Add project directory to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from arc_solver import ARCTaskSolver
from pattern_solutions import OptimizedSolutions

def main():
    """Main demonstration function."""
    print("IMPROVED ARC SOLVER DEMONSTRATION")
    print("=" * 80)
    print("Goal: Achieve 100% success rate on ARC tasks")
    print("=" * 80)
    
    # Initialize solver
    solver = ARCTaskSolver(data_dir="./data", solutions_dir="./solutions")
    
    print("\n1. TESTING CORRECTED TASK 1 SOLUTION")
    print("-" * 50)
    
    # Test the corrected Task 1 solution
    task1_solution = OptimizedSolutions.TASK1
    print(f"Solution: {task1_solution}")
    print(f"Bytes: {len(task1_solution.encode('utf-8'))}")
    print(f"Score: {max(1, 2500 - len(task1_solution.encode('utf-8')))}")
    
    result = solver.process_solution(1, task1_solution, verbose=False)
    print(f"Task 1 Result: {'✓ SUCCESS' if result['success'] else '✗ FAILED'}")
    
    if result['success']:
        print(f"  - Passed: {sum(s['passed'] for s in result['stats'].values())}/{sum(s['total'] for s in result['stats'].values())} tests")
        print(f"  - Score: {result['score']} points")
    
    print("\n2. AUTO-SOLVING FIRST 20 TASKS")
    print("-" * 50)
    
    # Auto-solve first 20 tasks to demonstrate capability
    batch_results = solver.batch_auto_solve(1, 20)
    
    print("\n3. DETAILED RESULTS")
    print("-" * 50)
    
    successful_tasks = []
    failed_tasks = []
    
    for task_id, result in batch_results['results'].items():
        if result['success']:
            successful_tasks.append((task_id, result['score'], result['byte_count']))
        else:
            failed_tasks.append((task_id, result.get('message', 'Unknown error')))
    
    print(f"\nSuccessful tasks ({len(successful_tasks)}):")
    for task_id, score, bytes_count in successful_tasks:
        print(f"  Task {task_id:03d}: {score:4.0f} points ({bytes_count:2d} bytes)")
    
    if failed_tasks:
        print(f"\nFailed tasks ({len(failed_tasks)}):")
        for task_id, message in failed_tasks[:5]:  # Show first 5 failures
            print(f"  Task {task_id:03d}: {message}")
        if len(failed_tasks) > 5:
            print(f"  ... and {len(failed_tasks) - 5} more")
    
    print("\n4. PERFORMANCE ANALYSIS")
    print("-" * 50)
    
    success_rate = batch_results['success_rate']
    total_score = batch_results['total_score']
    avg_score = batch_results['average_score']
    
    print(f"Success Rate: {success_rate:.1f}%")
    print(f"Total Score: {total_score:,} points")
    print(f"Average Score: {avg_score:.1f} points/task")
    
    # Project to full competition
    if success_rate > 0:
        projected_successful = int(400 * success_rate / 100)
        projected_total_score = avg_score * projected_successful
        print(f"\nProjected for 400 tasks:")
        print(f"  - Successful tasks: {projected_successful}")
        print(f"  - Total score: {projected_total_score:,.0f} points")
        
        # Competition ranking estimate
        if projected_total_score > 800000:
            rank_estimate = "Top 10"
        elif projected_total_score > 600000:
            rank_estimate = "Top 50"
        elif projected_total_score > 400000:
            rank_estimate = "Top 100"
        else:
            rank_estimate = "Needs improvement"
        
        print(f"  - Estimated ranking: {rank_estimate}")
    
    print("\n5. NEXT STEPS FOR 100% SUCCESS")
    print("-" * 50)
    
    if success_rate < 100:
        print("To achieve 100% success rate:")
        print("1. Analyze failed tasks to identify missing patterns")
        print("2. Implement additional pattern recognition algorithms")
        print("3. Add more optimized solutions to the pattern library")
        print("4. Use machine learning for complex pattern detection")
        print("5. Implement brute-force search for remaining tasks")
    else:
        print("🎉 CONGRATULATIONS! 100% success rate achieved!")
        print("Ready for competition submission!")
    
    print("\n6. SOLUTION OPTIMIZATION")
    print("-" * 50)
    
    if successful_tasks:
        # Show byte count distribution
        byte_counts = [bc for _, _, bc in successful_tasks]
        min_bytes = min(byte_counts)
        max_bytes = max(byte_counts)
        avg_bytes = sum(byte_counts) / len(byte_counts)
        
        print(f"Byte count statistics:")
        print(f"  - Minimum: {min_bytes} bytes")
        print(f"  - Maximum: {max_bytes} bytes")
        print(f"  - Average: {avg_bytes:.1f} bytes")
        
        # Show most efficient solutions
        efficient_solutions = sorted(successful_tasks, key=lambda x: x[2])[:3]
        print(f"\nMost efficient solutions:")
        for task_id, score, bytes_count in efficient_solutions:
            print(f"  Task {task_id:03d}: {bytes_count} bytes → {score} points")
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    
    return batch_results

if __name__ == "__main__":
    # Check if data directory exists
    data_dir = Path("./data")
    if not data_dir.exists():
        print("ERROR: Data directory not found!")
        print("Please ensure task JSON files are in ./data/ directory")
        print("\nTo get the data:")
        print("1. Download from: https://www.kaggle.com/competitions/google-code-golf-2025")
        print("2. Extract task files to ./data/ directory")
        sys.exit(1)
    
    # Run demonstration
    try:
        results = main()
        
        # Success message
        if results['success_rate'] > 50:
            print(f"\n✓ Demonstration successful! {results['success_rate']:.1f}% success rate achieved.")
        else:
            print(f"\n⚠ Demonstration completed with {results['success_rate']:.1f}% success rate.")
            print("Consider implementing additional patterns for better performance.")
            
    except Exception as e:
        print(f"\n✗ Demonstration failed with error: {e}")
        sys.exit(1)