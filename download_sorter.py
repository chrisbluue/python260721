from pathlib import Path
import shutil
import sys


def unique_destination(path: Path) -> Path:
    if not path.exists():
        return path

    counter = 1
    stem = path.stem
    suffix = path.suffix
    while True:
        candidate = path.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize_downloads(download_dir: Path) -> None:
    download_dir.mkdir(parents=True, exist_ok=True)

    target_dirs = {
        "images": [".jpg", ".jpeg", ".png"],
        "data": [".csv", ".xlsx"],
        "docs": [".txt", ".doc", ".pdf"],
        "archive": [".zip"],
    }

    for folder_name in target_dirs:
        (download_dir / folder_name).mkdir(parents=True, exist_ok=True)

    for file_path in download_dir.iterdir():
        if not file_path.is_file():
            continue

        lower_suffix = file_path.suffix.lower()
        target_folder = None

        for folder_name, extensions in target_dirs.items():
            if lower_suffix in extensions:
                target_folder = folder_name
                break

        if target_folder is None:
            continue

        destination_dir = download_dir / target_folder
        destination_path = destination_dir / file_path.name

        if destination_path.exists() and destination_path.resolve() != file_path.resolve():
            destination_path = unique_destination(destination_path)

        shutil.move(str(file_path), str(destination_path))
        print(f"Moved: {file_path.name} -> {destination_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_dir = Path(sys.argv[1]).expanduser()
    else:
        base_dir = Path(r"C:\Users\student\Downloads")

    organize_downloads(base_dir)
