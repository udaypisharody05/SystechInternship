import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def run(script_name, *args):
    command = [sys.executable, str(BASE_DIR / script_name), *map(str, args)]
    subprocess.run(command, check=True)


def main():
    run("0_generate_raw_data.py")
    run("1_create_raw_tables.py")
    run("2_load_raw_data.py", 1)
    run("3_run_transformations.py", 1)
    run("4_generate_reports.py")
    print("Batch 1 pipeline completed. Use demo_incremental_load.py for both batches.")


if __name__ == "__main__":
    main()
