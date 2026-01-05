# This function detects non-empty directories in the 'data' folder, 
# in order to identify which restaurants were already scraped. 

from pathlib import Path

data = Path("data")

non_empty_dirs = [
    d for d in data.iterdir()
    if d.is_dir() and any(d.iterdir())
]

print("NON EMPTY DIRS:", non_empty_dirs)