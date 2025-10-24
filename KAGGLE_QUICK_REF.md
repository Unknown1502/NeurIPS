# Kaggle Quick Reference

## One-Line Summary
Clone your GitHub repo (includes dataset) and run the notebook - no separate dataset upload needed.

## Kaggle Setup (3 Steps)

### 1. Upload Notebook
Upload `ARC_AGI_Competition_Notebook.ipynb` to Kaggle

### 2. Clone Repository (Cell 2)
Uncomment and run:
```python
!git clone https://github.com/Unknown1502/NeurIPS-2025.git /kaggle/working/NeurIPS-2025
```

### 3. Run Setup (Cell 5)
Already configured - just run it.

## Path Configuration

### Kaggle (Default in Notebook)
```python
repo_path = '/kaggle/working/NeurIPS-2025'
DATA_DIR = "/kaggle/working/NeurIPS-2025/data"
SOLUTIONS_DIR = "/kaggle/working/solutions"
```

### Local (Update Cell 5)
```python
repo_path = r'c:\Users\prajw\OneDrive\Desktop\google golf'
DATA_DIR = "./data"
SOLUTIONS_DIR = "./solutions"
```

## Key Points

1. **Dataset is in GitHub repo** - No separate upload needed
2. **Repository must be public** - Or accessible from Kaggle
3. **All paths pre-configured** - Notebook ready for Kaggle
4. **No emojis** - Professional formatting
5. **Clone once, use immediately** - Simple setup

## Quick Test

After cloning, run in a new cell:
```python
!ls -la /kaggle/working/NeurIPS-2025/data | head -10
```

Should show task001.json, task002.json, etc.

## Files You Need in GitHub

- `arc_solver.py`
- `utils/` folder
- `data/` folder (400 task files)

All other files are optional.

---

**That's it! Clone, run, solve.**
