"""
Extract ARC-GEN Archive

Simple script to extract the ARC-GEN dataset from downloaded archive.
"""

import zipfile
import os
from pathlib import Path

def extract_arc_gen(archive_path: str, extract_to: str = "."):
    """Extract ARC-GEN archive."""
    
    archive_path = Path(archive_path)
    extract_path = Path(extract_to)
    
    print(f"Extracting: {archive_path}")
    print(f"To: {extract_path.absolute()}")
    print()
    
    if not archive_path.exists():
        print(f"ERROR: Archive not found: {archive_path}")
        return False
    
    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            print("Extracting files...")
            zip_ref.extractall(extract_path)
            
            # List extracted files
            extracted = zip_ref.namelist()
            print(f"\nExtracted {len(extracted)} files")
            
            # Show first few files
            print("\nSample files:")
            for filename in extracted[:5]:
                print(f"  {filename}")
            
            if len(extracted) > 5:
                print(f"  ... and {len(extracted) - 5} more files")
        
        print("\nExtraction complete!")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    # Extract archive
    success = extract_arc_gen(
        r"C:\Users\prajw\Downloads\archive.zip",
        r"C:\Users\prajw\OneDrive\Desktop\google golf"
    )
    
    if success:
        print("\nNext step: Run prepare_dataset.py to merge with existing data")
        print("  python prepare_dataset.py")
