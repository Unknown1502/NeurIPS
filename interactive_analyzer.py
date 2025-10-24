"""
Interactive Task Analyzer

This script provides an interactive interface for analyzing and solving ARC tasks.

Usage:
    python interactive_analyzer.py

Author: Competition Framework
Date: October 24, 2025
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from arc_solver import ARCTaskSolver
from utils import grid_operations as go
from utils import pattern_detection as pd


class InteractiveAnalyzer:
    """Interactive interface for analyzing ARC tasks."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.solver = ARCTaskSolver(data_dir="./data", solutions_dir="./solutions")
        self.current_task_id = None
        self.current_task_data = None
    
    def print_menu(self):
        """Print main menu."""
        print("\n" + "=" * 80)
        print("ARC TASK INTERACTIVE ANALYZER")
        print("=" * 80)
        print()
        print("Commands:")
        print("  load <task_id>       - Load and analyze a task (1-400)")
        print("  analyze              - Detailed analysis of current task")
        print("  suggest              - Get suggested approaches for current task")
        print("  show <set> <n>       - Show example from set (train/test/arc-gen)")
        print("  test <code_file>     - Test solution from file")
        print("  prompt               - Generate Claude prompt for current task")
        print("  progress             - Show overall progress")
        print("  batch <start> <end>  - Batch analyze tasks")
        print("  help                 - Show this menu")
        print("  quit                 - Exit")
        print()
    
    def load_task(self, task_id: int):
        """Load a task for analysis."""
        try:
            self.current_task_id = task_id
            self.current_task_data = self.solver.load_task(task_id)
            print(f"\nLoaded task {task_id:03d}")
            self.solver.print_task_analysis(task_id)
        except Exception as e:
            print(f"Error loading task: {e}")
    
    def analyze_current_task(self):
        """Perform detailed analysis of current task."""
        if not self.current_task_data:
            print("No task loaded. Use 'load <task_id>' first.")
            return
        
        print("\n" + "=" * 80)
        print(f"DETAILED ANALYSIS - TASK {self.current_task_id:03d}")
        print("=" * 80)
        
        # Gather all grids
        all_inputs = []
        all_outputs = []
        
        for pair in self.current_task_data.get('train', []):
            all_inputs.append(pair['input'])
            all_outputs.append(pair['output'])
        
        for pair in self.current_task_data.get('test', []):
            all_inputs.append(pair['input'])
            all_outputs.append(pair['output'])
        
        # Analyze transformation type
        print("\nTransformation Characteristics:")
        trans_type = pd.detect_transformation_type(all_inputs, all_outputs)
        for key, value in trans_type.items():
            if value:
                print(f"  - {key.replace('_', ' ').title()}")
        
        # Analyze complexity
        print("\nComplexity Metrics:")
        complexity = pd.analyze_task_complexity(all_inputs, all_outputs)
        for key, value in complexity.items():
            print(f"  {key}: {value}")
        
        # Check for common patterns in first example
        if all_inputs:
            print("\nFirst Example Analysis:")
            first_in = all_inputs[0]
            first_out = all_outputs[0]
            
            print(f"  Input dimensions: {go.get_dimensions(first_in)}")
            print(f"  Output dimensions: {go.get_dimensions(first_out)}")
            print(f"  Input colors: {go.get_unique_values(first_in)}")
            print(f"  Output colors: {go.get_unique_values(first_out)}")
            
            # Check symmetry
            symmetry_in = pd.detect_symmetry(first_in)
            symmetry_out = pd.detect_symmetry(first_out)
            
            print("\n  Input symmetries:")
            for sym_type, has_sym in symmetry_in.items():
                if has_sym:
                    print(f"    - {sym_type}")
            
            print("\n  Output symmetries:")
            for sym_type, has_sym in symmetry_out.items():
                if has_sym:
                    print(f"    - {sym_type}")
            
            # Check for repetition
            repetition = pd.detect_repetition(first_in)
            if any(repetition.values()):
                print("\n  Input repetition patterns:")
                for rep_type, has_rep in repetition.items():
                    if has_rep:
                        print(f"    - {rep_type}")
        
        print()
    
    def suggest_approaches(self):
        """Suggest approaches for current task."""
        if not self.current_task_data:
            print("No task loaded. Use 'load <task_id>' first.")
            return
        
        all_inputs = []
        all_outputs = []
        
        for set_name in ['train', 'test']:
            for pair in self.current_task_data.get(set_name, []):
                all_inputs.append(pair['input'])
                all_outputs.append(pair['output'])
        
        print("\n" + "=" * 80)
        print(f"SUGGESTED APPROACHES - TASK {self.current_task_id:03d}")
        print("=" * 80)
        
        suggestions = pd.suggest_approach(all_inputs, all_outputs)
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. {suggestion}")
        
        print()
    
    def show_example(self, set_name: str, index: int):
        """Show specific example."""
        if not self.current_task_data:
            print("No task loaded. Use 'load <task_id>' first.")
            return
        
        examples = self.current_task_data.get(set_name, [])
        
        if index < 0 or index >= len(examples):
            print(f"Invalid index. {set_name} has {len(examples)} examples (0-{len(examples)-1})")
            return
        
        pair = examples[index]
        inp = pair['input']
        out = pair['output']
        
        print("\n" + "=" * 80)
        print(f"EXAMPLE: {set_name.upper()} [{index}]")
        print("=" * 80)
        
        print(f"\nInput ({len(inp)}x{len(inp[0]) if inp else 0}):")
        for row in inp:
            print(f"  {row}")
        
        print(f"\nOutput ({len(out)}x{len(out[0]) if out else 0}):")
        for row in out:
            print(f"  {row}")
        
        print()
    
    def test_solution(self, code_file: str):
        """Test solution from file."""
        if not self.current_task_data:
            print("No task loaded. Use 'load <task_id>' first.")
            return
        
        try:
            with open(code_file, 'r') as f:
                code = f.read()
            
            result = self.solver.process_solution(
                self.current_task_id,
                code,
                verbose=True
            )
            
            if result['success']:
                print(f"\nSUCCESS! Score: {result['score']:.2f} points")
            else:
                print(f"\nFAILED: {result['message']}")
        
        except FileNotFoundError:
            print(f"File not found: {code_file}")
        except Exception as e:
            print(f"Error: {e}")
    
    def generate_prompt(self):
        """Generate Claude prompt."""
        if not self.current_task_id:
            print("No task loaded. Use 'load <task_id>' first.")
            return
        
        prompt = self.solver.generate_claude_prompt(self.current_task_id)
        
        print("\n" + "=" * 80)
        print("CLAUDE PROMPT")
        print("=" * 80)
        print(prompt)
        print("=" * 80)
    
    def run(self):
        """Run interactive loop."""
        print("Welcome to ARC Task Interactive Analyzer")
        self.print_menu()
        
        while True:
            try:
                command = input("analyzer> ").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd == 'quit' or cmd == 'exit':
                    print("Goodbye!")
                    break
                
                elif cmd == 'help':
                    self.print_menu()
                
                elif cmd == 'load':
                    if len(parts) < 2:
                        print("Usage: load <task_id>")
                    else:
                        task_id = int(parts[1])
                        self.load_task(task_id)
                
                elif cmd == 'analyze':
                    self.analyze_current_task()
                
                elif cmd == 'suggest':
                    self.suggest_approaches()
                
                elif cmd == 'show':
                    if len(parts) < 3:
                        print("Usage: show <set> <index>")
                        print("Example: show train 0")
                    else:
                        set_name = parts[1]
                        index = int(parts[2])
                        self.show_example(set_name, index)
                
                elif cmd == 'test':
                    if len(parts) < 2:
                        print("Usage: test <code_file>")
                    else:
                        self.test_solution(parts[1])
                
                elif cmd == 'prompt':
                    self.generate_prompt()
                
                elif cmd == 'progress':
                    self.solver.report_progress()
                
                elif cmd == 'batch':
                    if len(parts) < 3:
                        print("Usage: batch <start> <end>")
                    else:
                        start = int(parts[1])
                        end = int(parts[2])
                        self.solver.batch_analyze_tasks(start, end)
                
                else:
                    print(f"Unknown command: {cmd}")
                    print("Type 'help' for available commands")
            
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    analyzer = InteractiveAnalyzer()
    analyzer.run()
