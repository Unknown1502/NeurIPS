"""
Merge ARC-AGI and ARC-GEN Datasets

This script merges the training data from ARC-AGI with the additional
examples from ARC-GEN-100K to create the complete competition format.

Author: Competition Framework
Date: October 24, 2025
"""

import json
import os
from pathlib import Path


def find_matching_arc_gen_file(task_id_hash: str, arc_gen_dir: Path):
    """
    Find ARC-GEN file matching the task.
    
    ARC-AGI uses hashed filenames, ARC-GEN should have matching files.
    """
    arc_gen_file = arc_gen_dir / f"{task_id_hash}.json"
    if arc_gen_file.exists():
        return arc_gen_file
    return None


def merge_datasets(
    arc_agi_dir: str = "./ARC-AGI",
    arc_gen_dir: str = "./ARC-GEN-100K",
    output_dir: str = "./data"
):
    """
    Merge ARC-AGI training data with ARC-GEN examples.
    
    Args:
        arc_agi_dir: Path to ARC-AGI repository
        arc_gen_dir: Path to ARC-GEN-100K dataset
        output_dir: Output directory for merged task files
    """
    
    arc_agi_path = Path(arc_agi_dir)
    arc_gen_path = Path(arc_gen_dir)
    output_path = Path(output_dir)
    
    # Create backup of existing data
    backup_dir = output_path.parent / "data_backup"
    if output_path.exists():
        print(f"Creating backup: {backup_dir}")
        import shutil
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(output_path, backup_dir)
    
    output_path.mkdir(exist_ok=True)
    
    print("=" * 80)
    print("MERGING ARC-AGI AND ARC-GEN DATASETS")
    print("=" * 80)
    print()
    
    # Check directories
    training_dir = arc_agi_path / "data" / "training"
    
    if not training_dir.exists():
        print(f"ERROR: Training directory not found: {training_dir}")
        return False
    
    print(f"ARC-AGI training: {training_dir}")
    
    arc_gen_available = arc_gen_path.exists()
    if arc_gen_available:
        arc_gen_files = list(arc_gen_path.glob("*.json"))
        print(f"ARC-GEN dataset: {arc_gen_path} ({len(arc_gen_files)} files)")
    else:
        print(f"ARC-GEN not found: {arc_gen_path}")
        print("Will create dataset with train and test only.")
    
    print()
    
    # Process all training files
    training_files = sorted(training_dir.glob("*.json"))
    print(f"Processing {len(training_files)} tasks...")
    print()
    
    processed = 0
    with_arc_gen = 0
    total_train = 0
    total_test = 0
    total_arc_gen = 0
    
    for idx, task_file in enumerate(training_files, 1):
        try:
            # Load ARC-AGI training data
            with open(task_file, 'r', encoding='utf-8') as f:
                task_data = json.load(f)
            
            # Get task ID hash from filename
            task_hash = task_file.stem
            
            # Create combined format
            combined = {
                'train': task_data.get('train', []),
                'test': task_data.get('test', []),
                'arc-gen': []
            }
            
            # Try to find and load ARC-GEN data
            if arc_gen_available:
                arc_gen_file = find_matching_arc_gen_file(task_hash, arc_gen_path)
                
                if arc_gen_file:
                    try:
                        with open(arc_gen_file, 'r', encoding='utf-8') as f:
                            arc_gen_data = json.load(f)
                        
                        # ARC-GEN files are lists of {input, output} pairs
                        if isinstance(arc_gen_data, list):
                            combined['arc-gen'] = arc_gen_data
                            with_arc_gen += 1
                    
                    except Exception as e:
                        print(f"  Warning: Could not load {arc_gen_file.name}: {e}")
            
            # Count examples
            train_count = len(combined['train'])
            test_count = len(combined['test'])
            arc_gen_count = len(combined['arc-gen'])
            
            total_train += train_count
            total_test += test_count
            total_arc_gen += arc_gen_count
            
            # Save merged task
            output_file = output_path / f"task{idx:03d}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(combined, f, indent=2)
            
            processed += 1
            
            # Progress update
            if processed % 50 == 0:
                print(f"  Processed {processed}/{len(training_files)} tasks...")
        
        except Exception as e:
            print(f"  ERROR processing {task_file.name}: {e}")
    
    print()
    print("=" * 80)
    print("MERGE COMPLETE")
    print("=" * 80)
    print(f"Tasks processed: {processed}")
    print(f"Tasks with ARC-GEN: {with_arc_gen}")
    print()
    print("Example counts:")
    print(f"  Total train examples: {total_train}")
    print(f"  Total test examples: {total_test}")
    print(f"  Total arc-gen examples: {total_arc_gen}")
    print(f"  Average arc-gen per task: {total_arc_gen / processed:.1f}")
    print()
    print(f"Output directory: {output_path.absolute()}")
    print()
    
    # Verify sample
    if processed > 0:
        sample_file = output_path / "task001.json"
        with open(sample_file, 'r', encoding='utf-8') as f:
            sample = json.load(f)
        
        print("Sample verification (task001.json):")
        print(f"  Train examples: {len(sample['train'])}")
        print(f"  Test examples: {len(sample['test'])}")
        print(f"  Arc-gen examples: {len(sample['arc-gen'])}")
    
    print()
    
    if with_arc_gen > 0:
        print("SUCCESS: Dataset now includes ARC-GEN examples!")
    else:
        print("Note: No ARC-GEN examples found. Dataset has train+test only.")
    
    print()
    print("Ready to use with: python arc_solver.py")
    
    return True


def verify_merged_dataset(data_dir: str = "./data"):
    """Verify the merged dataset."""
    
    data_path = Path(data_dir)
    task_files = sorted(data_path.glob("task*.json"))
    
    print()
    print("=" * 80)
    print("DATASET VERIFICATION")
    print("=" * 80)
    print()
    print(f"Total task files: {len(task_files)}")
    print()
    
    # Statistics
    with_arc_gen = 0
    min_arc_gen = float('inf')
    max_arc_gen = 0
    total_arc_gen = 0
    
    for task_file in task_files:
        with open(task_file, 'r') as f:
            task = json.load(f)
        
        arc_gen_count = len(task.get('arc-gen', []))
        
        if arc_gen_count > 0:
            with_arc_gen += 1
            min_arc_gen = min(min_arc_gen, arc_gen_count)
            max_arc_gen = max(max_arc_gen, arc_gen_count)
            total_arc_gen += arc_gen_count
    
    print(f"Tasks with arc-gen data: {with_arc_gen}/{len(task_files)}")
    
    if with_arc_gen > 0:
        print(f"Arc-gen examples per task:")
        print(f"  Minimum: {min_arc_gen}")
        print(f"  Maximum: {max_arc_gen}")
        print(f"  Average: {total_arc_gen / with_arc_gen:.1f}")
        print(f"  Total: {total_arc_gen:,}")
    
    print()
    
    # Show sample tasks
    print("Sample tasks:")
    for task_file in task_files[:5]:
        with open(task_file, 'r') as f:
            task = json.load(f)
        
        train = len(task.get('train', []))
        test = len(task.get('test', []))
        arc_gen = len(task.get('arc-gen', []))
        total = train + test + arc_gen
        
        status = "COMPLETE" if arc_gen > 0 else "BASIC"
        print(f"  {task_file.name}: train={train}, test={test}, arc-gen={arc_gen}, total={total} [{status}]")
    
    if len(task_files) > 5:
        print(f"  ... and {len(task_files) - 5} more")
    
    print()
    print("Verification complete!")
    
    return True


def main():
    """Main entry point."""
    import sys
    
    print()
    print("ARC Dataset Merger")
    print()
    
    # Check requirements
    arc_agi = Path("./ARC-AGI")
    arc_gen = Path("./ARC-GEN-100K")
    
    if not arc_agi.exists():
        print("ERROR: ARC-AGI directory not found!")
        print("Please clone: git clone https://github.com/fchollet/ARC-AGI.git")
        sys.exit(1)
    
    if not arc_gen.exists():
        print("WARNING: ARC-GEN-100K directory not found!")
        print("Dataset will be created with train+test only.")
        print()
        response = input("Continue without ARC-GEN? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Merge datasets
    success = merge_datasets(
        arc_agi_dir="./ARC-AGI",
        arc_gen_dir="./ARC-GEN-100K",
        output_dir="./data"
    )
    
    if success:
        verify_merged_dataset("./data")
    else:
        print("Merge failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
