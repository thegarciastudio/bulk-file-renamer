import argparse
import logging
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bulk rename files in a folder.")
    parser.add_argument("--folder", required=True, help="Path to the folder with files to rename.")
    parser.add_argument("--prefix", default="", help="Prefix to add to each file.")
    parser.add_argument("--extension", default="", help="Only rename files with this extension.")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying them.")
    parser.add_argument("--log", action="store_true", help="Enable logging to a text file.")
    parser.add_argument("--pad", type=int, default=0, help="Zero-padding width for numbering (e.g., 3 → 001, 002).")
    return parser.parse_args()


def setup_logging():
    logging.basicConfig(
        filename='bulk_rename.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def main():
    args = parse_arguments()
    folder = Path(args.folder)

    if not folder.is_dir():
        print(f"Error: '{folder}' is not a valid directory.")
        return

    if args.log:
        setup_logging()

    files = sorted([f for f in folder.iterdir() if f.is_file()])

    counter = 1
    for file in files:
        if args.extension and file.suffix.lower() != args.extension.lower():
            continue

        number = str(counter).zfill(args.pad) if args.pad > 0 else str(counter)
        new_name = f"{args.prefix}{number}{file.suffix}"
        new_path = folder / new_name

        if new_path.exists():
            print(f"Skipped: {new_path.name} already exists.")
            continue

        if args.dry_run:
            print(f"[DRY-RUN] Would rename: {file.name} -> {new_name}")
        else:
            file.rename(new_path)
            print(f"Renamed: {file.name} -> {new_name}")
            if args.log:
                logging.info(f"Renamed: {file.name} -> {new_name}")

        counter += 1


if __name__ == "__main__":
    main()