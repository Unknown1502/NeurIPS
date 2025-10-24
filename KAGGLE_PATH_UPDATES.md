# Kaggle Notebook Path Updates Guide

## Overview

When running the ARC_AGI_Competition_Notebook.ipynb on Kaggle, you need to update several paths to match Kaggle's directory structure.

## Critical Path Updates Required

### 1. Repository Path (Cell 3)
**Local Path:**
```python
repo_path = 'c:\Users\prajw\OneDrive\Desktop\google golf'
```

**Kaggle Path:**
```python
repo_path = '/kaggle/working/NeurIPS-2025'
```

**Explanation:** 
- On Kaggle, you'll need to clone your GitHub repo to `/kaggle/working/`
- Your repo is: `Unknown1502/NeurIPS-2025`
- Command to clone: `!git clone https://github.com/Unknown1502/NeurIPS-2025.git /kaggle/working/NeurIPS-2025`

---

### 2. Data Directory Path (Cell 3)
**Local Path:**
```python
DATA_DIR = "./data"
```

**Kaggle Path Options:**

**Option A - ARC Prize 2024 (Official Competition Dataset):**
```python
DATA_DIR = "/kaggle/input/arc-prize-2024"
```

**Option B - Custom Uploaded Dataset (If you upload your merged data):**
```python
DATA_DIR = "/kaggle/input/arc-agi-complete-dataset/data"
```

**Option C - ARC-AGI Training Dataset:**
```python
DATA_DIR = "/kaggle/input/abstraction-and-reasoning-challenge/training"
```

**Explanation:**
- Kaggle datasets are mounted at `/kaggle/input/<dataset-name>/`
- You need to add the dataset to your notebook first
- Use Cell 4 to discover which datasets are available
- Then update `DATA_DIR` accordingly

---

### 3. Solutions Directory Path (Cell 3)
**Local Path:**
```python
SOLUTIONS_DIR = "./solutions"
```

**Kaggle Path:**
```python
SOLUTIONS_DIR = "/kaggle/working/solutions"
```

**Explanation:**
- `/kaggle/working/` is the writable directory on Kaggle
- This is where your generated solutions will be saved
- The directory will be created automatically

---

### 4. ARC-GEN Dataset Path (If using merged dataset)
**Local Path:**
```python
# In prepare_dataset.py or merge_datasets.py
arc_gen_dir = "./ARC-GEN-100K"
```

**Kaggle Path:**
```python
arc_gen_dir = "/kaggle/input/arc-gen-100k-dataset"
```

**Explanation:**
- If you upload the ARC-GEN-100K dataset separately
- Or include it in your custom dataset upload
- Update the path to match Kaggle's input directory

---

## Complete Updated Cell 3 for Kaggle

```python
import json
import sys
from pathlib import Path

# Add your cloned repo to Python path
repo_path = '/kaggle/working/NeurIPS-2025'
sys.path.insert(0, repo_path)

# Import the ARC solver framework
from arc_solver import ARCTaskSolver

# Import utility modules
from utils import grid_operations as go
from utils import pattern_detection as pd

# Import standard libraries
from collections import Counter
from typing import List, Tuple, Dict

# Setup paths for Kaggle
# UPDATE THIS after adding a dataset and checking cell 4!
DATA_DIR = "/kaggle/input/arc-prize-2024"  # <-- UPDATE based on cell 4 output
SOLUTIONS_DIR = "/kaggle/working/solutions"

# Create solutions directory if it doesn't exist
Path(SOLUTIONS_DIR).mkdir(exist_ok=True, parents=True)

print("Imports successful!")
print(f"Repo path: {repo_path}")
print(f"Data directory: {DATA_DIR}")
print(f"Solutions directory: {Path(SOLUTIONS_DIR).absolute()}")
print("\nIMPORTANT: If you see 'FileNotFoundError' below, run cell 4 first!")
print("Then add a dataset and update DATA_DIR above.")
```

---

## Step-by-Step Kaggle Setup

### Step 1: Create New Kaggle Notebook
1. Go to Kaggle.com
2. Click "Create" → "New Notebook"
3. Upload your `ARC_AGI_Competition_Notebook.ipynb`

### Step 2: Add GitHub Repo
**Option A - Clone via notebook (Recommended):**
Add a new cell at the beginning:
```python
!git clone https://github.com/Unknown1502/NeurIPS-2025.git /kaggle/working/NeurIPS-2025
!ls /kaggle/working/NeurIPS-2025
```

**Option B - Upload as dataset:**
1. Zip your entire repo
2. Upload as Kaggle dataset
3. Add dataset to notebook
4. Update `repo_path = "/kaggle/input/neurips-2025-repo/"`

### Step 3: Add ARC Dataset
1. Click "Add Data" in right sidebar
2. Search for "ARC Prize 2024" or "ARC-AGI"
3. Add to notebook
4. Run Cell 4 to discover the exact path
5. Update `DATA_DIR` in Cell 3

### Step 4: (Optional) Upload Your Merged Dataset
If you want to use your complete merged dataset with ARC-GEN:

1. **Prepare dataset locally:**
   ```cmd
   # On your local machine
   cd "c:\Users\prajw\OneDrive\Desktop\google golf"
   
   # Create a zip of your data folder
   powershell Compress-Archive -Path data -DestinationPath arc-complete-dataset.zip
   ```

2. **Upload to Kaggle:**
   - Go to Kaggle.com → Datasets → New Dataset
   - Upload `arc-complete-dataset.zip`
   - Name it: "ARC-AGI Complete Dataset with ARC-GEN"
   - Make it public or private

3. **Add to notebook:**
   - In your notebook, click "Add Data"
   - Search for your uploaded dataset
   - Add it
   - Update path: `DATA_DIR = "/kaggle/input/arc-agi-complete-dataset-with-arc-gen/data"`

### Step 5: Verify Paths
Run Cell 4 in the notebook to see all available datasets and their paths.

---

## Common Kaggle Dataset Paths

| Dataset | Kaggle Path |
|---------|-------------|
| ARC Prize 2024 | `/kaggle/input/arc-prize-2024` |
| ARC Challenge (Training) | `/kaggle/input/abstraction-and-reasoning-challenge/training` |
| ARC Challenge (Evaluation) | `/kaggle/input/abstraction-and-reasoning-challenge/evaluation` |
| ARC Challenge (Test) | `/kaggle/input/abstraction-and-reasoning-challenge/test` |
| ARC-GEN-100K | `/kaggle/input/arc-gen-100k` (if uploaded separately) |
| Your Custom Dataset | `/kaggle/input/<your-dataset-name>/` |

---

## Path Verification Checklist

Before running your notebook on Kaggle:

- [ ] **Cell 3**: Updated `repo_path` to `/kaggle/working/NeurIPS-2025`
- [ ] **Cell 3**: Updated `DATA_DIR` to correct Kaggle input path
- [ ] **Cell 3**: Updated `SOLUTIONS_DIR` to `/kaggle/working/solutions`
- [ ] **Pre-cell**: Added Git clone command if using GitHub approach
- [ ] **Datasets**: Added required datasets to notebook via Kaggle UI
- [ ] **Cell 4**: Run to verify all paths are correct
- [ ] **Cell 6**: Verify solver initializes without errors

---

## Testing on Kaggle

After updating paths, run these cells in order:

1. **Git Clone Cell** (if using GitHub method)
2. **Cell 3** - Setup and imports
3. **Cell 4** - Discover datasets
4. **Update Cell 3** - Fix DATA_DIR based on Cell 4 output
5. **Cell 6** - Initialize solver
6. **Cell 8** - Load and analyze first task

If all cells run successfully, your paths are correct!

---

## Troubleshooting

### Error: "No module named 'arc_solver'"
**Problem:** Repository not found
**Solution:** 
- Verify git clone worked: `!ls /kaggle/working/`
- Check repo_path is correct
- Ensure all files are in the repo

### Error: "FileNotFoundError: [Errno 2] No such file or directory"
**Problem:** DATA_DIR path is wrong
**Solution:**
- Run Cell 4 to see available datasets
- Update DATA_DIR to match actual path
- Ensure dataset is added to notebook

### Error: "No task files found"
**Problem:** Dataset doesn't contain expected files
**Solution:**
- Check dataset structure: `!ls /kaggle/input/<dataset-name>/`
- Verify JSON files exist
- May need different dataset or upload your own

### Error: "Permission denied" when saving solutions
**Problem:** Trying to write to read-only directory
**Solution:**
- Only `/kaggle/working/` is writable
- Update SOLUTIONS_DIR to `/kaggle/working/solutions`

---

## Summary

### Local Paths → Kaggle Paths

| Component | Local Path | Kaggle Path |
|-----------|------------|-------------|
| Repo | `c:\Users\prajw\OneDrive\Desktop\google golf` | `/kaggle/working/NeurIPS-2025` |
| Data | `./data` | `/kaggle/input/arc-prize-2024` |
| Solutions | `./solutions` | `/kaggle/working/solutions` |
| ARC-GEN | `./ARC-GEN-100K` | `/kaggle/input/arc-gen-100k` |

### Key Differences

1. **Read-only inputs:** `/kaggle/input/` (datasets you add)
2. **Writable workspace:** `/kaggle/working/` (your code and outputs)
3. **Absolute paths:** Always use absolute paths on Kaggle
4. **Linux filesystem:** Use forward slashes `/` not backslashes `\`

---

## Quick Reference Card

```python
# KAGGLE NOTEBOOK PATHS QUICK REFERENCE

# 1. Clone repo (add as first cell)
!git clone https://github.com/Unknown1502/NeurIPS-2025.git /kaggle/working/NeurIPS-2025

# 2. Update Cell 3 paths
repo_path = '/kaggle/working/NeurIPS-2025'
DATA_DIR = "/kaggle/input/arc-prize-2024"  # Update after Cell 4
SOLUTIONS_DIR = "/kaggle/working/solutions"

# 3. Verify (run in a cell)
!ls /kaggle/working/NeurIPS-2025  # Check repo files
!ls /kaggle/input/  # Check available datasets
!ls {DATA_DIR}  # Check data files

# 4. Test import
import sys
sys.path.insert(0, '/kaggle/working/NeurIPS-2025')
from arc_solver import ARCTaskSolver  # Should work
```

---

**Ready to run on Kaggle! Just update the paths and you're good to go.**
