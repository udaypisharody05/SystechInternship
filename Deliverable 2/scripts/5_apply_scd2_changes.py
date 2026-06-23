"""Compatibility wrapper for the former standalone SCD2 step."""

import subprocess
import sys
from pathlib import Path


def main():
    batch_id = sys.argv[1] if len(sys.argv) > 1 else "2"
    script = Path(__file__).with_name("3_run_transformations.py")
    subprocess.run([sys.executable, str(script), batch_id], check=True)


if __name__ == "__main__":
    main()
