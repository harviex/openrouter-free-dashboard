#!/usr/bin/env python3
"""Update OpenRouter Free Models Dashboard data (without scoring).

This script runs fetch_models.py and add_parameters.py to update
the data/models.json file. Scoring has been removed.
"""

import subprocess
import sys

def run_script(script_name):
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True, text=True, cwd='/home/c1/openrouter-free-dashboard'
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode

if __name__ == "__main__":
    print("=" * 50)
    print("Updating OpenRouter Free Models Dashboard")
    print("=" * 50)

    # Step 1: Fetch models from OpenRouter API
    print("\n>>> Step 1: Fetching models from OpenRouter API...")
    code = run_script('fetch_models.py')
    if code != 0:
        print(f"ERROR: fetch_models.py failed with code {code}")
        sys.exit(1)

    # Step 2: Add parameters
    print("\n>>> Step 2: Adding parameters to models.json...")
    code = run_script('add_parameters.py')
    if code != 0:
        print(f"ERROR: add_parameters.py failed with code {code}")
        sys.exit(1)

    # Step 3: Copy to root directory
    print("\n>>> Step 3: Copying models.json to root directory...")
    import shutil
    shutil.copy('data/models.json', 'models.json')
    print("  ✅ Copied data/models.json → models.json")

    print("\n" + "=" * 50)
    print("✅ Update complete!")
    print("=" * 50)