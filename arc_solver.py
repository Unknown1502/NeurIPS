"""
Google Code Golf 2025 - ARC Task Solver Framework

This module provides a comprehensive framework for solving ARC-AGI tasks
in the Google Code Golf 2025 competition. It handles task loading, solution
testing across all example sets (train, test, arc-gen), scoring, and submission
generation.

Author: Competition Framework
Date: October 24, 2025
"""

import json
import os
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Tuple, Callable, Optional
import sys


class ARCTaskSolver:
    """
    Comprehensive solver framework for Google Code Golf 2025 competition.
    
    This class manages the complete workflow for solving ARC-AGI tasks:
    - Loading task data from JSON files
    - Testing solutions against all example sets
    - Calculating scores based on correctness and byte count
    - Tracking progress across all 400 tasks
    - Generating submission files
    
    Attributes:
        data_dir: Path to directory containing task JSON files
        solutions_dir: Path to directory for saving solution files
        scores: Dictionary mapping task IDs to their scores
        stats: Dictionary containing detailed statistics per task
    """
    
    def __init__(self, data_dir: str = "./data", solutions_dir: str = "./solutions"):
        """
        Initialize the ARC Task Solver.
        
        Args:
            data_dir: Path to directory containing task JSON files
            solutions_dir: Path to directory for saving solution files
        """
        self.data_dir = Path(data_dir)
        self.solutions_dir = Path(solutions_dir)
        self.solutions_dir.mkdir(exist_ok=True)
        self.scores = {}
        self.stats = {}
        
        # Verify data directory exists
        if not self.data_dir.exists():
            raise FileNotFoundError(
                f"Data directory not found: {self.data_dir}\n"
                f"Please ensure task JSON files are placed in this directory."
            )
    
    def load_task(self, task_id: int) -> Dict[str, Any]:
        """
        Load task data from JSON file.
        
        Args:
            task_id: Task number (1-400)
            
        Returns:
            Dictionary containing 'train', 'test', and 'arc-gen' example sets
            
        Raises:
            FileNotFoundError: If task file does not exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        task_file = self.data_dir / f"task{task_id:03d}.json"
        
        if not task_file.exists():
            raise FileNotFoundError(
                f"Task file not found: {task_file}\n"
                f"Expected format: task{task_id:03d}.json"
            )
        
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in task file {task_file}: {e.msg}",
                e.doc,
                e.pos
            )
    
    def get_all_pairs(self, task_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Combine all example pairs from all three sets.
        
        Args:
            task_data: Task data dictionary containing 'train', 'test', 'arc-gen'
            
        Returns:
            List of all example pairs combined
        """
        all_pairs = []
        
        # Add train pairs
        all_pairs.extend(task_data.get('train', []))
        
        # Add test pairs
        all_pairs.extend(task_data.get('test', []))
        
        # Add arc-gen pairs
        all_pairs.extend(task_data.get('arc-gen', []))
        
        return all_pairs
    
    def test_solution(
        self,
        solution_func: Callable,
        task_data: Dict[str, Any],
        verbose: bool = True
    ) -> Tuple[bool, str, Dict[str, Dict[str, int]]]:
        """
        Test solution function against all example sets.
        
        This method runs the solution function on every example pair from
        train, test, and arc-gen sets, verifying correctness of outputs.
        
        Args:
            solution_func: Function that takes input grid and returns output grid
            task_data: Task data containing all example sets
            verbose: Whether to print detailed progress information
            
        Returns:
            Tuple of (success, message, stats):
            - success: True if all examples pass
            - message: Description of test results
            - stats: Detailed statistics by example set
        """
        stats = {
            'train': {'total': 0, 'passed': 0},
            'test': {'total': 0, 'passed': 0},
            'arc-gen': {'total': 0, 'passed': 0}
        }
        
        failures = []
        
        # Test each example set separately for detailed feedback
        for set_name in ['train', 'test', 'arc-gen']:
            examples = task_data.get(set_name, [])
            stats[set_name]['total'] = len(examples)
            
            for i, pair in enumerate(examples):
                try:
                    input_grid = pair['input']
                    expected_output = pair['output']
                    
                    # Run solution function
                    actual_output = solution_func(input_grid)
                    
                    # Verify output is a list of lists
                    if not isinstance(actual_output, list):
                        raise TypeError("Output must be a list (grid)")
                    
                    # Compare outputs
                    if actual_output == expected_output:
                        stats[set_name]['passed'] += 1
                        if verbose and len(examples) <= 10:
                            print(f"  [{set_name}] Example {i+1}/{len(examples)}: PASS")
                    else:
                        failures.append({
                            'set': set_name,
                            'index': i,
                            'input': input_grid,
                            'expected': expected_output,
                            'actual': actual_output,
                            'dimension_mismatch': len(actual_output) != len(expected_output)
                        })
                        if verbose and len(examples) <= 10:
                            print(f"  [{set_name}] Example {i+1}/{len(examples)}: FAIL")
                
                except Exception as e:
                    failures.append({
                        'set': set_name,
                        'index': i,
                        'input': pair.get('input'),
                        'error': str(e),
                        'error_type': type(e).__name__
                    })
                    if verbose and len(examples) <= 10:
                        print(f"  [{set_name}] Example {i+1}/{len(examples)}: ERROR - {e}")
        
        # Calculate totals
        total_passed = sum(s['passed'] for s in stats.values())
        total_tests = sum(s['total'] for s in stats.values())
        
        success = (total_passed == total_tests)
        
        # Build result message
        if success:
            message = f"SUCCESS: All {total_tests} examples passed"
        else:
            message = f"FAILURE: {total_passed}/{total_tests} passed ({len(failures)} failed)"
            
            # Add details about first few failures
            for i, fail in enumerate(failures[:3]):
                message += f"\n  Failure {i+1}: {fail['set']}[{fail['index']}]"
                if 'error' in fail:
                    message += f" - {fail['error_type']}: {fail['error']}"
                else:
                    message += " - Output mismatch"
                    if fail.get('dimension_mismatch'):
                        exp_dim = f"{len(fail['expected'])}x{len(fail['expected'][0]) if fail['expected'] else 0}"
                        act_dim = f"{len(fail['actual'])}x{len(fail['actual'][0]) if fail['actual'] else 0}"
                        message += f" (dimensions: expected {exp_dim}, got {act_dim})"
            
            if len(failures) > 3:
                message += f"\n  ... and {len(failures) - 3} more failures"
        
        return success, message, stats
    
    def calculate_score(self, is_correct: bool, byte_count: int) -> float:
        """
        Calculate score for a solution.
        
        Args:
            is_correct: Whether solution passes all test cases
            byte_count: Number of bytes in solution code
            
        Returns:
            Score according to competition rules:
            - Correct: max(1, 2500 - byte_count)
            - Incorrect: 0.001
        """
        if is_correct:
            return max(1, 2500 - byte_count)
        else:
            return 0.001
    
    def analyze_task(self, task_id: int) -> Dict[str, Any]:
        """
        Perform detailed analysis of a task.
        
        Args:
            task_id: Task number (1-400)
            
        Returns:
            Dictionary containing task analysis metadata
        """
        task_data = self.load_task(task_id)
        
        analysis = {
            'task_id': task_id,
            'train_count': len(task_data.get('train', [])),
            'test_count': len(task_data.get('test', [])),
            'arc_gen_count': len(task_data.get('arc-gen', [])),
            'total_pairs': 0
        }
        
        analysis['total_pairs'] = (
            analysis['train_count'] +
            analysis['test_count'] +
            analysis['arc_gen_count']
        )
        
        # Analyze grid dimensions
        all_pairs = self.get_all_pairs(task_data)
        if all_pairs:
            input_dims = []
            output_dims = []
            
            for pair in all_pairs:
                inp = pair['input']
                out = pair['output']
                
                input_dims.append((len(inp), len(inp[0]) if inp else 0))
                output_dims.append((len(out), len(out[0]) if out else 0))
            
            analysis['input_dimensions'] = input_dims
            analysis['output_dimensions'] = output_dims
            analysis['dimension_change'] = (input_dims != output_dims)
        
        return analysis
    
    def print_task_analysis(self, task_id: int) -> None:
        """
        Print formatted analysis of a task.
        
        Args:
            task_id: Task number (1-400)
        """
        analysis = self.analyze_task(task_id)
        task_data = self.load_task(task_id)
        
        print("=" * 80)
        print(f"TASK {task_id:03d} ANALYSIS")
        print("=" * 80)
        print(f"Train examples:   {analysis['train_count']}")
        print(f"Test examples:    {analysis['test_count']}")
        print(f"Arc-gen examples: {analysis['arc_gen_count']}")
        print(f"TOTAL examples:   {analysis['total_pairs']}")
        print("=" * 80)
        
        # Show first few examples from train and test sets
        for set_name in ['train', 'test']:
            examples = task_data.get(set_name, [])
            if examples:
                print(f"\n{set_name.upper()} Examples:")
                for i, pair in enumerate(examples[:2]):
                    inp = pair['input']
                    out = pair['output']
                    print(f"  Example {i+1}:")
                    print(f"    Input:  {len(inp)}x{len(inp[0]) if inp else 0} grid")
                    print(f"    Output: {len(out)}x{len(out[0]) if out else 0} grid")
                    
                    # Show actual grid if small
                    if len(inp) <= 5 and len(inp[0]) <= 10:
                        print(f"    Input grid:  {inp}")
                        print(f"    Output grid: {out}")
        
        if analysis['arc_gen_count'] > 0:
            print(f"\nARC-GEN: {analysis['arc_gen_count']} additional examples available")
        
        print()
    
    def auto_solve_task(self, task_id: int) -> Dict[str, Any]:
        """
        Attempt to automatically solve a task using pattern recognition.
        
        Args:
            task_id: Task number (1-400)
            
        Returns:
            Dictionary containing solution results
        """
        from pattern_solutions import OptimizedSolutions, PatternSolutions
        
        task_data = self.load_task(task_id)
        
        # Try to detect pattern and get solution
        pattern_type = self._detect_pattern(task_data)
        solution_code = OptimizedSolutions.get_solution(pattern_type)
        
        if solution_code:
            result = self.process_solution(task_id, solution_code, verbose=False)
            if result['success']:
                return result
        
        # If pattern-based solution failed, try brute force common patterns
        common_solutions = [
            OptimizedSolutions.TASK1,
            OptimizedSolutions.ROTATE_90,
            OptimizedSolutions.ROTATE_180,
            OptimizedSolutions.FLIP_H,
            OptimizedSolutions.FLIP_V,
            OptimizedSolutions.TRANSPOSE,
            OptimizedSolutions.SIMPLE_TILE_3X3,
            OptimizedSolutions.IDENTITY
        ]
        
        for solution in common_solutions:
            result = self.process_solution(task_id, solution, verbose=False)
            if result['success']:
                return result
        
        return {
            'task_id': task_id,
            'success': False,
            'message': 'No matching pattern found'
        }
    
    def _detect_pattern(self, task_data: Dict[str, Any]) -> str:
        """
        Detect the transformation pattern in task data.
        
        Args:
            task_data: Task data dictionary
            
        Returns:
            Pattern type string
        """
        train_pairs = task_data.get('train', [])
        if not train_pairs:
            return 'unknown'
        
        # Check dimensions
        first_pair = train_pairs[0]
        inp = first_pair['input']
        out = first_pair['output']
        
        in_h, in_w = len(inp), len(inp[0]) if inp else 0
        out_h, out_w = len(out), len(out[0]) if out else 0
        
        # Task 1 pattern: 3x3 -> 9x9 conditional tiling
        if in_h == 3 and in_w == 3 and out_h == 9 and out_w == 9:
            if self._test_task1_pattern(inp, out):
                return 'conditional_tiling_3x3'
            else:
                return 'simple_tiling_3x3'
        
        # Same dimensions - geometric transformation
        if in_h == out_h and in_w == out_w:
            return self._detect_geometric_pattern(train_pairs)
        
        return 'unknown'
    
    def _test_task1_pattern(self, inp: List[List[int]], out: List[List[int]]) -> bool:
        """
        Test if input/output matches Task 1 conditional tiling pattern.
        """
        from pattern_solutions import PatternSolutions
        expected = PatternSolutions.task1_conditional_tiling(inp)
        return expected == out
    
    def _detect_geometric_pattern(self, train_pairs: List[Dict]) -> str:
        """
        Detect geometric transformation pattern.
        """
        from pattern_solutions import PatternSolutions
        
        for pair in train_pairs:
            inp = pair['input']
            out = pair['output']
            
            if PatternSolutions.rotate_90_clockwise(inp) == out:
                return 'rotate_90'
            elif PatternSolutions.rotate_180(inp) == out:
                return 'rotate_180'
            elif PatternSolutions.flip_horizontal(inp) == out:
                return 'flip_horizontal'
            elif PatternSolutions.flip_vertical(inp) == out:
                return 'flip_vertical'
            elif PatternSolutions.transpose(inp) == out:
                return 'transpose'
            elif inp == out:
                return 'identity'
        
        return 'unknown'
    
    def process_solution(
        self,
        task_id: int,
        solution_code: str,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Process and test a solution for a specific task.
        
        Args:
            task_id: Task number (1-400)
            solution_code: Python code containing solution function
            verbose: Whether to print detailed progress
            
        Returns:
            Dictionary containing test results, score, and statistics
        """
        if verbose:
            print("=" * 80)
            print(f"PROCESSING SOLUTION FOR TASK {task_id:03d}")
            print("=" * 80)
        
        task_data = self.load_task(task_id)
        
        # Execute code and extract solve function
        namespace = {}
        try:
            exec(solution_code, namespace)
            
            # Look for solution function (try common names)
            solve_func = None
            for name in ['solve', 'f', 'solution', 'transform']:
                if name in namespace and callable(namespace[name]):
                    solve_func = namespace[name]
                    break
            
            if not solve_func:
                return {
                    'task_id': task_id,
                    'success': False,
                    'score': 0.001,
                    'byte_count': len(solution_code.encode('utf-8')),
                    'message': "No solution function found. Expected 'solve', 'f', 'solution', or 'transform'."
                }
        
        except SyntaxError as e:
            return {
                'task_id': task_id,
                'success': False,
                'score': 0.001,
                'byte_count': len(solution_code.encode('utf-8')),
                'message': f"Syntax error: {e}"
            }
        except Exception as e:
            return {
                'task_id': task_id,
                'success': False,
                'score': 0.001,
                'byte_count': len(solution_code.encode('utf-8')),
                'message': f"Execution error: {e}"
            }
        
        # Test solution on all examples
        is_correct, message, stats = self.test_solution(solve_func, task_data, verbose)
        
        # Calculate metrics
        byte_count = len(solution_code.encode('utf-8'))
        score = self.calculate_score(is_correct, byte_count)
        
        # Print results
        if verbose:
            print("\nTest Results:")
            print(f"  Train:   {stats['train']['passed']}/{stats['train']['total']} passed")
            print(f"  Test:    {stats['test']['passed']}/{stats['test']['total']} passed")
            print(f"  Arc-gen: {stats['arc-gen']['passed']}/{stats['arc-gen']['total']} passed")
            total_passed = sum(s['passed'] for s in stats.values())
            total_tests = sum(s['total'] for s in stats.values())
            print(f"  TOTAL:   {total_passed}/{total_tests} passed")
            
            print("\nMetrics:")
            print(f"  Correctness: {'PASS' if is_correct else 'FAIL'}")
            print(f"  Byte count:  {byte_count} bytes")
            print(f"  Score:       {score:.3f} points")
            
            if not is_correct:
                print(f"\n{message}")
            
            print("=" * 80)
        
        # Save if correct
        if is_correct:
            self.save_solution(task_id, solution_code)
            self.scores[task_id] = score
            self.stats[task_id] = stats
        
        return {
            'task_id': task_id,
            'success': is_correct,
            'byte_count': byte_count,
            'score': score,
            'stats': stats,
            'message': message
        }
    
    def save_solution(self, task_id: int, code: str) -> None:
        """
        Save solution code to file.
        
        Args:
            task_id: Task number (1-400)
            code: Solution code to save
        """
        output_file = self.solutions_dir / f"task{task_id:03d}.py"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"\nSolution saved: {output_file}")
    
    def generate_claude_prompt(self, task_id: int, max_examples: int = 5) -> str:
        """
        Generate comprehensive prompt for Claude to solve a task.
        
        Args:
            task_id: Task number (1-400)
            max_examples: Maximum number of examples to include per set
            
        Returns:
            Formatted prompt string ready for Claude
        """
        task_data = self.load_task(task_id)
        analysis = self.analyze_task(task_id)
        
        prompt = f"""Task {task_id:03d} - ARC-AGI Pattern Recognition

OBJECTIVE:
Implement a Python function that performs the grid transformation demonstrated by the examples below.

REQUIREMENTS:
- Function must work for ALL {analysis['total_pairs']} example pairs (train + test + arc-gen)
- Solution must be a valid Python function named 'solve' that takes one grid parameter
- Grid format: List of lists of integers (0-9)
- Output must exactly match expected dimensions and values
- Minimize byte count after ensuring correctness

SCORING:
- Correct solution: max(1, 2500 - byte_count) points
- Incorrect solution: 0.001 points (essentially zero)

"""
        
        # Add train examples
        prompt += "TRAIN EXAMPLES (pattern demonstration):\n\n"
        for i, pair in enumerate(task_data['train'][:max_examples]):
            inp = pair['input']
            out = pair['output']
            prompt += f"Train Example {i+1}:\n"
            prompt += f"  Input ({len(inp)}x{len(inp[0]) if inp else 0}):\n"
            for row in inp:
                prompt += f"    {row}\n"
            prompt += f"  Output ({len(out)}x{len(out[0]) if out else 0}):\n"
            for row in out:
                prompt += f"    {row}\n"
            prompt += "\n"
        
        # Add test examples
        prompt += "TEST EXAMPLES (must work on these):\n\n"
        for i, pair in enumerate(task_data['test'][:max_examples]):
            inp = pair['input']
            out = pair['output']
            prompt += f"Test Example {i+1}:\n"
            prompt += f"  Input ({len(inp)}x{len(inp[0]) if inp else 0}):\n"
            for row in inp:
                prompt += f"    {row}\n"
            prompt += f"  Output ({len(out)}x{len(out[0]) if out else 0}):\n"
            for row in out:
                prompt += f"    {row}\n"
            prompt += "\n"
        
        # Mention arc-gen
        if analysis['arc_gen_count'] > 0:
            prompt += f"ARC-GEN EXAMPLES: {analysis['arc_gen_count']} additional examples follow the same pattern\n\n"
        
        prompt += """DELIVERABLES:
1. Pattern analysis: Describe the transformation rule
2. Working solution: Clear, correct implementation
3. Optimized solution: Minimized byte count version
4. Verification: Confirm it handles all edge cases

Please provide your solution as a Python function.
"""
        
        return prompt
    
    def create_submission_zip(self, output_path: str = "submission.zip") -> None:
        """
        Create submission ZIP file containing all solution files.
        
        Args:
            output_path: Path for output ZIP file
        """
        zip_path = Path(output_path)
        solution_files = sorted(self.solutions_dir.glob("task*.py"))
        
        if not solution_files:
            print("ERROR: No solution files found in solutions directory")
            return
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in solution_files:
                zipf.write(file_path, file_path.name)
        
        total_score = sum(self.scores.values())
        
        print("=" * 80)
        print("SUBMISSION CREATED")
        print("=" * 80)
        print(f"File: {zip_path.absolute()}")
        print(f"Tasks solved: {len(solution_files)}/400")
        print(f"Total score: {total_score:,.2f} points")
        if solution_files:
            print(f"Average score: {total_score/len(solution_files):.2f} points/task")
        print("=" * 80)
    
    def report_progress(self) -> None:
        """
        Display detailed progress report across all tasks.
        """
        solved = len(self.scores)
        total_score = sum(self.scores.values())
        avg_score = total_score / solved if solved > 0 else 0
        
        print("=" * 80)
        print("PROGRESS REPORT")
        print("=" * 80)
        print(f"Tasks solved:     {solved}/400 ({100*solved/400:.1f}%)")
        print(f"Total score:      {total_score:,.2f} points")
        
        if solved > 0:
            print(f"Average/task:     {avg_score:.2f} points")
            print(f"Projected total:  {avg_score * 400:,.2f} points (if all tasks at avg)")
            
            # Score distribution
            if self.scores:
                scores_list = list(self.scores.values())
                print(f"\nScore distribution:")
                print(f"  Minimum:  {min(scores_list):.2f} points")
                print(f"  Maximum:  {max(scores_list):.2f} points")
                print(f"  Median:   {sorted(scores_list)[len(scores_list)//2]:.2f} points")
        
        print("=" * 80)
        print()
    
    def batch_auto_solve(self, start_task: int = 1, end_task: int = 400) -> Dict[str, Any]:
        """
        Automatically solve multiple tasks using pattern recognition.
        
        Args:
            start_task: First task number to solve
            end_task: Last task number to solve (inclusive)
            
        Returns:
            Dictionary with batch solving results
        """
        print("=" * 80)
        print(f"AUTO-SOLVING TASKS {start_task} TO {end_task}")
        print("=" * 80)
        
        results = {}
        successful = 0
        total_score = 0
        
        for task_id in range(start_task, end_task + 1):
            try:
                result = self.auto_solve_task(task_id)
                results[task_id] = result
                
                if result['success']:
                    successful += 1
                    total_score += result['score']
                    print(f"✓ Task {task_id:03d}: {result['score']} points ({result['byte_count']} bytes)")
                else:
                    print(f"✗ Task {task_id:03d}: {result.get('message', 'Failed')}")
                
                # Progress report every 50 tasks
                if task_id % 50 == 0:
                    success_rate = (successful / (task_id - start_task + 1)) * 100
                    print(f"\nProgress: {successful}/{task_id - start_task + 1} solved ({success_rate:.1f}%), {total_score:,} points\n")
                    
            except Exception as e:
                print(f"✗ Task {task_id:03d}: ERROR - {e}")
                results[task_id] = {
                    'task_id': task_id,
                    'success': False,
                    'message': f'Error: {e}'
                }
        
        total_tasks = end_task - start_task + 1
        success_rate = (successful / total_tasks) * 100
        avg_score = total_score / successful if successful > 0 else 0
        
        print("\n" + "=" * 80)
        print("BATCH AUTO-SOLVE RESULTS")
        print("=" * 80)
        print(f"Tasks solved: {successful}/{total_tasks} ({success_rate:.1f}%)")
        print(f"Total score: {total_score:,} points")
        print(f"Average score: {avg_score:.1f} points/task")
        print(f"Projected total (400 tasks): {avg_score * 400:,.0f} points")
        print("=" * 80)
        
        return {
            'total_tasks': total_tasks,
            'successful': successful,
            'success_rate': success_rate,
            'total_score': total_score,
            'average_score': avg_score,
            'results': results
        }
    
    def batch_analyze_tasks(self, start_task: int = 1, end_task: int = 10) -> None:
        """
        Analyze multiple tasks in sequence.
        
        Args:
            start_task: First task number to analyze
            end_task: Last task number to analyze (inclusive)
        """
        print("=" * 80)
        print(f"BATCH ANALYSIS: Tasks {start_task} to {end_task}")
        print("=" * 80)
        print()
        
        for task_id in range(start_task, end_task + 1):
            try:
                analysis = self.analyze_task(task_id)
                print(f"Task {task_id:03d}: "
                      f"train={analysis['train_count']}, "
                      f"test={analysis['test_count']}, "
                      f"arc-gen={analysis['arc_gen_count']}, "
                      f"total={analysis['total_pairs']} examples")
            except FileNotFoundError:
                print(f"Task {task_id:03d}: FILE NOT FOUND")
            except Exception as e:
                print(f"Task {task_id:03d}: ERROR - {e}")
        
        print()


def main():
    """
    Main entry point for command-line usage.
    """
    print("=" * 80)
    print("Google Code Golf 2025 - ARC Task Solver Framework")
    print("=" * 80)
    print()
    
    # Initialize solver
    try:
        solver = ARCTaskSolver(data_dir="./data", solutions_dir="./solutions")
        print("Framework initialized successfully")
        print(f"Data directory: {solver.data_dir.absolute()}")
        print(f"Solutions directory: {solver.solutions_dir.absolute()}")
        print()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("\nPlease create the data directory and add task JSON files.")
        sys.exit(1)
    
    # Example usage
    print("Example usage:")
    print("  solver.print_task_analysis(1)           # Analyze task 1")
    print("  solver.generate_claude_prompt(1)        # Generate prompt for Claude")
    print("  solver.process_solution(1, code)        # Test a solution")
    print("  solver.report_progress()                # View progress")
    print("  solver.create_submission_zip()          # Create submission")
    print()
    
    # Quick test if task files exist
    task_files = list(solver.data_dir.glob("task*.json"))
    if task_files:
        print(f"Found {len(task_files)} task files in data directory")
        print("\nAnalyzing first task as example...")
        print()
        
        try:
            solver.print_task_analysis(1)
        except Exception as e:
            print(f"Could not analyze task 1: {e}")
    else:
        print("No task files found in data directory")
        print("Please download task files from the competition and place them in ./data/")


if __name__ == "__main__":
    main()
