# Google Code Golf 2025 - Project Setup

## Project Structure

```
google golf/
├── arc_solver.py              # Main solver framework
├── interactive_analyzer.py     # Interactive analysis tool
├── todo.md                     # Competition guide and documentation
├── README.md                   # This file
│
├── data/                       # Task JSON files (download from competition)
│   ├── task001.json
│   ├── task002.json
│   └── ...
│
├── solutions/                  # Generated solution files
│   ├── task001.py
│   ├── task002.py
│   └── ...
│
├── tests/                      # Test suite
│   └── test_framework.py
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── grid_operations.py     # Grid transformation functions
│   └── pattern_detection.py   # Pattern analysis functions
│
└── examples/                   # Example solutions and templates
    └── example_solutions.py
```

## Quick Start

### 1. Download Task Data

Download the competition dataset from Kaggle:
- Visit: https://www.kaggle.com/competitions/google-code-golf-2025
- Download task files (task001.json - task400.json)
- Place all JSON files in the `data/` directory

### 2. Install Dependencies

This framework uses only Python standard library. No additional packages required.

Required: Python 3.7+

### 3. Run Tests

Verify the framework is working correctly:

```cmd
cd "c:\Users\prajw\OneDrive\Desktop\google golf"
python tests\test_framework.py
```

### 4. Analyze a Task

Using the main framework:

```python
from arc_solver import ARCTaskSolver

solver = ARCTaskSolver(data_dir="./data")
solver.print_task_analysis(1)
```

Or use the interactive analyzer:

```cmd
python interactive_analyzer.py
```

Then in the interactive shell:
```
analyzer> load 1
analyzer> analyze
analyzer> suggest
```

## Usage Examples

### Analyze a Task

```python
from arc_solver import ARCTaskSolver

solver = ARCTaskSolver(data_dir="./data")

# View task details
solver.print_task_analysis(1)

# Generate prompt for Claude
prompt = solver.generate_claude_prompt(1)
print(prompt)
```

### Test a Solution

```python
from arc_solver import ARCTaskSolver

solver = ARCTaskSolver(data_dir="./data")

# Your solution code
solution_code = """
def solve(grid):
    return [list(row) for row in zip(*grid[::-1])]
"""

# Test it
result = solver.process_solution(1, solution_code)
print(f"Score: {result['score']}")
```

### Use Utility Functions

```python
from utils import grid_operations as go

grid = [[1, 2], [3, 4]]

# Rotate 90 degrees clockwise
rotated = go.rotate_90_clockwise(grid)

# Flip horizontal
flipped = go.flip_horizontal(grid)

# Extract subgrid
subgrid = go.extract_subgrid(grid, 0, 0, 1, 2)
```

### Pattern Detection

```python
from utils import pattern_detection as pd

# Detect transformation type
characteristics = pd.detect_transformation_type(input_grids, output_grids)

# Detect symmetry
symmetry = pd.detect_symmetry(grid)

# Get suggestions
suggestions = pd.suggest_approach(input_grids, output_grids)
```

## Workflow

### For Each Task:

1. **Analyze the task**
   ```python
   solver.print_task_analysis(task_id)
   ```

2. **Generate Claude prompt**
   ```python
   prompt = solver.generate_claude_prompt(task_id)
   # Send to Claude Sonnet 4.5
   ```

3. **Implement solution** based on Claude's analysis

4. **Test solution**
   ```python
   result = solver.process_solution(task_id, solution_code)
   ```

5. **Iterate** until all examples pass

6. **Optimize** for byte count while maintaining correctness

### Batch Processing:

```python
for task_id in range(1, 401):
    solver.print_task_analysis(task_id)
    # Implement solution
    # solver.process_solution(task_id, code)
    
    if task_id % 10 == 0:
        solver.report_progress()
```

### Create Submission:

```python
solver.create_submission_zip("submission.zip")
```

## Key Components

### ARCTaskSolver

Main class for managing the solving workflow:
- `load_task(task_id)` - Load task data
- `test_solution(func, task_data)` - Test solution function
- `process_solution(task_id, code)` - Complete test and scoring
- `generate_claude_prompt(task_id)` - Generate AI prompt
- `create_submission_zip()` - Package solutions
- `report_progress()` - Show statistics

### Grid Operations

Common transformations in `utils/grid_operations.py`:
- Rotations (90°, 180°, 270°)
- Flips (horizontal, vertical)
- Transpose
- Scaling
- Tiling
- Cropping
- Overlay
- And many more...

### Pattern Detection

Analysis tools in `utils/pattern_detection.py`:
- Transformation type detection
- Symmetry detection
- Object detection
- Repetition detection
- Complexity analysis
- Approach suggestions

## Testing

Run the complete test suite:

```cmd
python tests\test_framework.py
```

Individual tests:
- Grid operations
- Pattern detection
- Solver initialization
- Solution processing
- Scoring calculation

## Best Practices

### 1. Always Verify First

Test solutions on ALL example sets before optimizing:
- train examples (3-4 pairs)
- test examples (1-2 pairs)
- arc-gen examples (50+ pairs)

### 2. Correctness Over Brevity

Wrong answer = 0.001 points (essentially zero)  
Correct answer = up to 2499 points

Always prioritize correctness.

### 3. Systematic Approach

- Analyze pattern thoroughly
- Implement clear solution first
- Verify on all examples
- Then optimize for bytes

### 4. Use Utilities

Leverage provided utility functions instead of reimplementing common operations.

### 5. Track Progress

```python
solver.report_progress()  # Every 10 tasks
solver.create_submission_zip()  # After each session
```

## Scoring Reference

- Correct solution: `max(1, 2500 - byte_count)` points
- Incorrect solution: `0.001` points

Examples:
- 50 bytes → 2450 points
- 100 bytes → 2400 points
- 500 bytes → 2000 points
- 1000 bytes → 1500 points
- 2500+ bytes → 1 point

## Troubleshooting

### Task files not found

Ensure JSON files are in `./data/` directory with correct naming:
- task001.json
- task002.json
- ...
- task400.json

### Import errors

Run from project root directory:
```cmd
cd "c:\Users\prajw\OneDrive\Desktop\google golf"
python arc_solver.py
```

### Solution fails on arc-gen examples

Arc-gen examples may reveal edge cases not obvious in train/test sets.
Carefully analyze failed examples to understand the complete pattern.

## Additional Resources

- Full guide: See `todo.md` for comprehensive documentation
- Example solutions: See `examples/example_solutions.py`
- Competition details: https://www.kaggle.com/competitions/google-code-golf-2025
- ARC-AGI repository: https://github.com/fchollet/ARC-AGI

## Contact

This framework is designed to support the Google Code Golf 2025 competition.
For questions about the competition, refer to the official Kaggle discussion forum.

## License

Competition framework for educational and competition purposes.

---

**Good luck in the competition!**

Target: 380+ correct solutions with optimal byte counts
Projected score: 880,000+ points
