import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "0_generate_raw_data.py",
    "1_create_raw_tables.py",
    "2_load_raw_data.py",
    "3_run_transformations.py",
    "4_generate_reports.py"
]


def run_script(script_name):
    script_path = BASE_DIR / script_name

    print(f"\nRunning {script_name}...")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"{script_name} failed.")


def main():
    print("Starting Sports Goods Store ELT Pipeline...")

    for script in SCRIPTS:
        run_script(script)

    print("\nELT Pipeline completed successfully.")


if __name__ == "__main__":
    main()