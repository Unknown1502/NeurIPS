import json

# Check task001
with open('data/task001.json', 'r') as f:
    data = json.load(f)

print(f"Task 001:")
print(f"  Train examples: {len(data['train'])}")
print(f"  Test examples: {len(data['test'])}")  
print(f"  Arc-gen examples: {len(data['arc-gen'])}")
print(f"  Total: {len(data['train']) + len(data['test']) + len(data['arc-gen'])}")
