import argparse
import shutil
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли з вихідної директорії в директорію "
                    "призначення, розкладаючи їх по піддиректоріях за розширенням."
    )
    parser.add_argument("source", type=Path, help="Шлях до вихідної директорії")
    parser.add_argument(
        "destination",
        type=Path,
        nargs="?",
        default=Path("dist"),
        help="Шлях до директорії призначення (за замовчуванням: dist)",
    )
    return parser.parse_args()


def copy_files(source: Path, destination: Path) -> None:
    try:
        entries = list(source.iterdir())
    except (PermissionError, OSError) as e:
        print(f"[!] Неможливо прочитати '{source}': {e}", file=sys.stderr)
        return

    for entry in entries:
        try:
            if entry.is_dir():
                copy_files(entry, destination)
            elif entry.is_file():
                extension = entry.suffix.lstrip(".").lower() or "no_extension"
                target_dir = destination / extension
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(entry, target_dir / entry.name)
                print(f"[+] {entry} -> {target_dir / entry.name}")
        except (PermissionError, OSError, shutil.Error) as e:
            print(f"[!] Помилка обробки '{entry}': {e}", file=sys.stderr)


def main():
    args = parse_args()
    source: Path = args.source
    destination: Path = args.destination

    if not source.exists():
        print(f"[!] Вихідна директорія не існує: {source}", file=sys.stderr)
        sys.exit(1)
    if not source.is_dir():
        print(f"[!] Шлях не є директорією: {source}", file=sys.stderr)
        sys.exit(1)

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"[!] Не вдалося створити '{destination}': {e}", file=sys.stderr)
        sys.exit(1)

    copy_files(source, destination)
    print(f"\nГотово. Файли скопійовано у '{destination}'.")


if __name__ == "__main__":
    main()
