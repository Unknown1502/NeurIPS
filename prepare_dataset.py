"""
Dataset Preparation Script

This script combines the ARC-AGI training/evaluation data with ARC-GEN-100K data
to create the complete competition dataset format with train, test, and arc-gen fields.

Usage:
    python prepare_dataset.py

Requirements:
    1. ARC-AGI repository cloned (contains train and test data)
    2. ARC-GEN-100K dataset downloaded (optional - will use train/test only if not available)

Author: Competition Framework
Date: October 24, 2025
"""

import json
import os
from pathlib import Path
import shutil


def prepare_competition_dataset(
    arc_agi_dir: str = "./ARC-AGI",
    arc_gen_dir: str = "./ARC-GEN-100K",
    output_dir: str = "./data"
):
    """
    Prepare competition dataset by merging ARC-AGI and ARC-GEN data.
    
    Args:
        arc_agi_dir: Path to cloned ARC-AGI repository
        arc_gen_dir: Path to ARC-GEN-100K dataset (optional)
        output_dir: Output directory for combined task files
    """
    
    arc_agi_path = Path(arc_agi_dir)
    arc_gen_path = Path(arc_gen_dir)
    output_path = Path(output_dir)
    
    # Ensure output directory exists
    output_path.mkdir(exist_ok=True)
    
    print("=" * 80)
    print("DATASET PREPARATION")
    print("=" * 80)
    print()
    
    # Check ARC-AGI directory
    training_dir = arc_agi_path / "data" / "training"
    evaluation_dir = arc_agi_path / "data" / "evaluation"
    
    if not training_dir.exists():
        print(f"ERROR: ARC-AGI training directory not found: {training_dir}")
        print("Please ensure ARC-AGI repository is cloned correctly.")
        return False
    
    print(f"Found ARC-AGI training data: {training_dir}")
    print(f"Found ARC-AGI evaluation data: {evaluation_dir}")
    
    # Check ARC-GEN directory (optional)
    arc_gen_available = arc_gen_path.exists()
    if arc_gen_available:
        print(f"Found ARC-GEN-100K data: {arc_gen_path}")
    else:
        print(f"ARC-GEN-100K not found at: {arc_gen_path}")
        print("Will create dataset with train and test examples only.")
    
    print()
    
    # Process training tasks
    training_files = sorted(training_dir.glob("*.json"))
    print(f"Processing {len(training_files)} training tasks...")
    
    processed_count = 0
    
    for task_file in training_files:
        try:
            # Load training data
            with open(task_file, 'r', encoding='utf-8') as f:
                task_data = json.load(f)
            
            # Create combined task format
            combined_task = {
                'train': task_data.get('train', []),
                'test': task_data.get('test', []),
                'arc-gen': []  # Will be populated if ARC-GEN data available
            }
            
            # Try to load corresponding ARC-GEN data if available
            if arc_gen_available:
                arc_gen_file = arc_gen_path / task_file.name
                if arc_gen_file.exists():
                    try:
                        with open(arc_gen_file, 'r', encoding='utf-8') as f:
                            arc_gen_data = json.load(f)
                        
                        # Add arc-gen examples
                        combined_task['arc-gen'] = arc_gen_data.get('examples', [])
                    except Exception as e:
                        print(f"  Warning: Could not load ARC-GEN data for {task_file.name}: {e}")
            
            # Generate task number from filename
            task_name = task_file.stem
            task_number = processed_count + 1
            
            # Save combined task
            output_file = output_path / f"task{task_number:03d}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(combined_task, f, indent=2)
            
            processed_count += 1
            
            if processed_count % 50 == 0:
                print(f"  Processed {processed_count} tasks...")
        
        except Exception as e:
            print(f"  ERROR processing {task_file.name}: {e}")
    
    print()
    print("=" * 80)
    print("DATASET PREPARATION COMPLETE")
    print("=" * 80)
    print(f"Total tasks processed: {processed_count}")
    print(f"Output directory: {output_path.absolute()}")
    print()
    
    # Verify a sample task
    if processed_count > 0:
        sample_file = output_path / "task001.json"
        with open(sample_file, 'r', encoding='utf-8') as f:
            sample = json.load(f)
        
        print("Sample task (task001.json):")
        print(f"  Train examples: {len(sample['train'])}")
        print(f"  Test examples: {len(sample['test'])}")
        print(f"  Arc-gen examples: {len(sample['arc-gen'])}")
    
    print()
    print("Dataset is ready for use with the ARC solver framework!")
    
    return True


def verify_dataset(data_dir: str = "./data"):
    """
    Verify the prepared dataset.
    
    Args:
        data_dir: Directory containing task files
    """
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"ERROR: Data directory not found: {data_path}")
        return False
    
    task_files = sorted(data_path.glob("task*.json"))
    
    print("=" * 80)
    print("DATASET VERIFICATION")
    print("=" * 80)
    print()
    print(f"Found {len(task_files)} task files")
    print()
    
    # Check first few tasks
    for task_file in task_files[:5]:
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                task = json.load(f)
            
            train_count = len(task.get('train', []))
            test_count = len(task.get('test', []))
            arc_gen_count = len(task.get('arc-gen', []))
            total = train_count + test_count + arc_gen_count
            
            print(f"{task_file.name}:")
            print(f"  Train: {train_count}, Test: {test_count}, Arc-gen: {arc_gen_count}")
            print(f"  Total: {total} examples")
        
        except Exception as e:
            print(f"ERROR: {task_file.name}: {e}")
    
    if len(task_files) > 5:
        print(f"... and {len(task_files) - 5} more tasks")
    
    print()
    print("Verification complete!")
    
    return True


def main():
    """Main entry point."""
    import sys
    
    print("ARC-AGI Dataset Preparation Tool")
    print()
    
    # Check if ARC-AGI exists
    if not Path("./ARC-AGI").exists():
        print("ERROR: ARC-AGI repository not found!")
        print()
        print("Please clone the repository first:")
        print("  git clone https://github.com/fchollet/ARC-AGI.git")
        print()
        sys.exit(1)
    
    # Prepare dataset
    success = prepare_competition_dataset(
        arc_agi_dir="./ARC-AGI",
        arc_gen_dir="./ARC-GEN-100K",
        output_dir="./data"
    )
    
    if success:
        # Verify dataset
        verify_dataset("./data")
        
        print()
        print("=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print()
        print("1. (Optional) Download ARC-GEN-100K dataset from Kaggle:")
        print("   https://www.kaggle.com/datasets/arcgen100k/the-arc-gen-100k-dataset")
        print()
        print("2. If you have ARC-GEN data, place it in ./ARC-GEN-100K/ and run this script again")
        print()
        print("3. Start solving tasks:")
        print("   python arc_solver.py")
        print("   python interactive_analyzer.py")
        print()
    else:
        print("Dataset preparation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
