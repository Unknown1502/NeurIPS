"""
Advanced ARC Task Solver with Pattern Recognition and Auto-Solution Generation

This module provides enhanced pattern recognition and automatic solution generation
for ARC-AGI tasks to achieve 100% success rate.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple, Callable, Optional
from collections import Counter
import itertools

class AdvancedARCSolver:
    """Advanced solver with pattern recognition and auto-generation capabilities."""
    
    def __init__(self, data_dir: str = "./data", solutions_dir: str = "./solutions"):
        self.data_dir = Path(data_dir)
        self.solutions_dir = Path(solutions_dir)
        self.solutions_dir.mkdir(exist_ok=True)
        self.solved_tasks = {}
        
    def load_task(self, task_id: int) -> Dict[str, Any]:
        """Load task data from JSON file."""
        task_file = self.data_dir / f"task{task_id:03d}.json"
        with open(task_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_pattern(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the transformation pattern in the task."""
        train_pairs = task_data['train']
        
        if not train_pairs:
            return {"pattern_type": "unknown"}
        
        # Get dimensions
        input_dims = [(len(pair['input']), len(pair['input'][0])) for pair in train_pairs]
        output_dims = [(len(pair['output']), len(pair['output'][0])) for pair in train_pairs]
        
        # Check for consistent scaling
        if len(set(input_dims)) == 1 and len(set(output_dims)) == 1:
            in_h, in_w = input_dims[0]
            out_h, out_w = output_dims[0]
            
            # Check for 3x3 to 9x9 tiling pattern (like Task 1)
            if in_h == 3 and in_w == 3 and out_h == 9 and out_w == 9:
                return self._analyze_tiling_pattern(train_pairs)
            
            # Check for other scaling patterns
            if out_h == in_h * 2 and out_w == in_w * 2:
                return {"pattern_type": "scale_2x"}
            elif out_h == in_h * 3 and out_w == in_w * 3:
                return {"pattern_type": "scale_3x"}
        
        # Check for rotation/flip patterns
        if input_dims == output_dims:
            return self._analyze_geometric_pattern(train_pairs)
        
        return {"pattern_type": "complex"}
    
    def _analyze_tiling_pattern(self, train_pairs: List[Dict]) -> Dict[str, Any]:
        """Analyze 3x3 to 9x9 tiling pattern."""
        # Check if it's the conditional tiling pattern from Task 1
        for pair in train_pairs:
            inp = pair['input']
            out = pair['output']
            
            # Test if this matches Task 1 pattern
            if self._test_task1_pattern(inp, out):
                return {
                    "pattern_type": "conditional_tiling_3x3",
                    "rule": "tile_based_on_input_values"
                }
        
        return {"pattern_type": "simple_tiling_3x3"}
    
    def _test_task1_pattern(self, inp: List[List[int]], out: List[List[int]]) -> bool:
        """Test if input/output matches Task 1 conditional tiling pattern."""
        if len(inp) != 3 or len(inp[0]) != 3 or len(out) != 9 or len(out[0]) != 9:
            return False
        
        # Generate expected output using Task 1 rule
        expected = self._generate_task1_output(inp)
        return expected == out
    
    def _generate_task1_output(self, inp: List[List[int]]) -> List[List[int]]:
        """Generate output using Task 1 conditional tiling rule."""
        result = []
        n = len(inp)
        
        for i in range(n):
            for sub_row in range(n):
                row = []
                for j in range(n):
                    if inp[i][j] == 0:
                        # Place zeros
                        row.extend([0] * n)
                    else:
                        # Place the input grid row
                        row.extend(inp[sub_row])
                result.append(row)
        
        return result
    
    def _analyze_geometric_pattern(self, train_pairs: List[Dict]) -> Dict[str, Any]:
        """Analyze geometric transformation patterns."""
        # Test common geometric transformations
        for pair in train_pairs:
            inp = pair['input']
            out = pair['output']
            
            if self._rotate_90(inp) == out:
                return {"pattern_type": "rotate_90"}
            elif self._rotate_180(inp) == out:
                return {"pattern_type": "rotate_180"}
            elif self._flip_horizontal(inp) == out:
                return {"pattern_type": "flip_horizontal"}
            elif self._flip_vertical(inp) == out:
                return {"pattern_type": "flip_vertical"}
        
        return {"pattern_type": "other_geometric"}
    
    def _rotate_90(self, grid: List[List[int]]) -> List[List[int]]:
        """Rotate grid 90 degrees clockwise."""
        return [list(row) for row in zip(*grid[::-1])]
    
    def _rotate_180(self, grid: List[List[int]]) -> List[List[int]]:
        """Rotate grid 180 degrees."""
        return [row[::-1] for row in grid[::-1]]
    
    def _flip_horizontal(self, grid: List[List[int]]) -> List[List[int]]:
        """Flip grid horizontally."""
        return [row[::-1] for row in grid]
    
    def _flip_vertical(self, grid: List[List[int]]) -> List[List[int]]:
        """Flip grid vertically."""
        return grid[::-1]
    
    def generate_solution(self, task_id: int) -> Optional[str]:
        """Generate solution code for a task."""
        task_data = self.load_task(task_id)
        pattern = self.analyze_pattern(task_data)
        
        if pattern["pattern_type"] == "conditional_tiling_3x3":
            return self._generate_task1_solution()
        elif pattern["pattern_type"] == "rotate_90":
            return "solve=lambda g:[list(r)for r in zip(*g[::-1])]"
        elif pattern["pattern_type"] == "rotate_180":
            return "solve=lambda g:[r[::-1]for r in g[::-1]]"
        elif pattern["pattern_type"] == "flip_horizontal":
            return "solve=lambda g:[r[::-1]for r in g]"
        elif pattern["pattern_type"] == "flip_vertical":
            return "solve=lambda g:g[::-1]"
        
        return None
    
    def _generate_task1_solution(self) -> str:
        """Generate optimized solution for Task 1 pattern."""
        return """solve=lambda g:[[x for j in range(len(g))for x in(g[s]if g[i][j]else[0]*len(g))]for i in range(len(g))for s in range(len(g))]"""
    
    def test_solution(self, solution_code: str, task_data: Dict[str, Any]) -> Tuple[bool, int, int]:
        """Test solution against all examples."""
        namespace = {}
        try:
            exec(solution_code, namespace)
            solve_func = namespace.get('solve')
            if not solve_func:
                return False, 0, 0
        except:
            return False, 0, 0
        
        total_tests = 0
        passed_tests = 0
        
        for set_name in ['train', 'test', 'arc-gen']:
            examples = task_data.get(set_name, [])
            for pair in examples:
                total_tests += 1
                try:
                    result = solve_func(pair['input'])
                    if result == pair['output']:
                        passed_tests += 1
                except:
                    pass
        
        return passed_tests == total_tests, passed_tests, total_tests
    
    def solve_task(self, task_id: int) -> Dict[str, Any]:
        """Attempt to solve a task automatically."""
        task_data = self.load_task(task_id)
        solution_code = self.generate_solution(task_id)
        
        if not solution_code:
            return {
                "task_id": task_id,
                "success": False,
                "message": "No pattern recognized"
            }
        
        is_correct, passed, total = self.test_solution(solution_code, task_data)
        
        if is_correct:
            # Save solution
            byte_count = len(solution_code.encode('utf-8'))
            score = max(1, 2500 - byte_count)
            
            solution_file = self.solutions_dir / f"task{task_id:03d}.py"
            with open(solution_file, 'w') as f:
                f.write(solution_code)
            
            self.solved_tasks[task_id] = {
                "code": solution_code,
                "byte_count": byte_count,
                "score": score
            }
            
            return {
                "task_id": task_id,
                "success": True,
                "byte_count": byte_count,
                "score": score,
                "passed": passed,
                "total": total
            }
        
        return {
            "task_id": task_id,
            "success": False,
            "passed": passed,
            "total": total,
            "message": f"Solution failed: {passed}/{total} tests passed"
        }
    
    def solve_all_tasks(self, start_task: int = 1, end_task: int = 400) -> Dict[str, Any]:
        """Attempt to solve all tasks in range."""
        results = {}
        successful = 0
        total_score = 0
        
        print(f"Solving tasks {start_task} to {end_task}...")
        
        for task_id in range(start_task, end_task + 1):
            try:
                result = self.solve_task(task_id)
                results[task_id] = result
                
                if result["success"]:
                    successful += 1
                    total_score += result["score"]
                    print(f"✓ Task {task_id:03d}: {result['score']} points ({result['byte_count']} bytes)")
                else:
                    print(f"✗ Task {task_id:03d}: {result.get('message', 'Failed')}")
                
                # Progress update every 50 tasks
                if task_id % 50 == 0:
                    print(f"Progress: {successful}/{task_id - start_task + 1} solved, {total_score:,} points")
                    
            except Exception as e:
                print(f"✗ Task {task_id:03d}: Error - {e}")
                results[task_id] = {
                    "task_id": task_id,
                    "success": False,
                    "message": f"Error: {e}"
                }
        
        return {
            "total_tasks": end_task - start_task + 1,
            "successful": successful,
            "success_rate": successful / (end_task - start_task + 1) * 100,
            "total_score": total_score,
            "average_score": total_score / successful if successful > 0 else 0,
            "results": results
        }

def main():
    """Main function to run the advanced solver."""
    print("Advanced ARC Task Solver")
    print("=" * 50)
    
    solver = AdvancedARCSolver(
        data_dir="./data",
        solutions_dir="./solutions"
    )
    
    # Test on first 10 tasks
    results = solver.solve_all_tasks(1, 10)
    
    print("\n" + "=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)
    print(f"Tasks solved: {results['successful']}/{results['total_tasks']}")
    print(f"Success rate: {results['success_rate']:.1f}%")
    print(f"Total score: {results['total_score']:,} points")
    if results['successful'] > 0:
        print(f"Average score: {results['average_score']:.1f} points/task")

if __name__ == "__main__":
    main()