"""
ComfyUI Output Watcher & Auto-Renamer
--------------------------------------
Watches the ComfyUI output folder and renames generated images from UUID filenames
to a readable YYYYMMDD_HHMMSS_seed format.

Usage: python watch_and_rename.py --watch "C:/ComfyUI/output"
"""

import time
import re
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


class ImageRenamer(FileSystemEventHandler):
    def __init__(self, watch_dir: Path):
        self.watch_dir = watch_dir
        self.seen = set()

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return
        if path.name in self.seen:
            return
        self.seen.add(path.name)

        # Brief wait to ensure file is fully written
        time.sleep(1.5)
        self.rename(path)

    def rename(self, path: Path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Extract seed from filename if ComfyUI includes it (e.g. ComfyUI_01234_...)
        seed_match = re.search(r"_(\d{5,})_", path.stem)
        seed_part = f"_{seed_match.group(1)}" if seed_match else ""
        new_name = f"{timestamp}{seed_part}{path.suffix}"
        new_path = path.parent / new_name

        # Avoid collision
        counter = 1
        while new_path.exists():
            new_name = f"{timestamp}{seed_part}_{counter}{path.suffix}"
            new_path = path.parent / new_name
            counter += 1

        shutil.move(str(path), str(new_path))
        print(f"Renamed: {path.name} → {new_name}")


def watch(folder: str):
    watch_path = Path(folder)
    if not watch_path.exists():
        print(f"Folder not found: {folder}")
        return

    handler = ImageRenamer(watch_path)
    observer = Observer()
    observer.schedule(handler, str(watch_path), recursive=False)
    observer.start()
    print(f"Watching: {watch_path}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Watch ComfyUI output and auto-rename images")
    parser.add_argument("--watch", default="./output", help="ComfyUI output folder to watch")
    args = parser.parse_args()
    watch(args.watch)
