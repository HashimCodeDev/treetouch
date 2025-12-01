import argparse
import sys
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert indented text into directory structure")
    parser.add_argument("--file", type=Path, help="Structure description file (stdin if omitted)")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root output directory (default: cwd)")
    parser.add_argument("--spaces", type=int, default=4, help="Spaces per indent level (default: 4)")
    parser.add_argument("--verbose", action="store_true", help="Print created paths")
    parser.add_argument("--force", action="store_true", help="Overwrite existing non-empty files")
    return parser.parse_args()


def normalize_parts(entry: str):
    entry = entry.replace("\\", "/")
    return [part for part in entry.split("/") if part]


def main():
    args = parse_arguments()

    # Load lines
    if args.file:
        if not args.file.exists():
            sys.exit(f"Error: File not found {args.file}")
        lines = args.file.read_text(encoding='utf-8').splitlines()
    else:
        if sys.stdin.isatty():
            print("Enter folder structure (Ctrl+D to finish (on Linux) and Ctrl+Z+Enter to finish (on Windows)):", file=sys.stderr)
        lines = sys.stdin.read().splitlines()

    stack = [args.root.resolve()]
    
    for idx, line in enumerate(lines, 1):
        if not line.strip():
            continue

        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)

        # Indent validation
        if indent % args.spaces != 0:
            sys.exit(f"Indentation error on line {idx}, expected multiple of {args.spaces} spaces")

        depth = indent // args.spaces
        if depth > len(stack) - 1:
            sys.exit(f"Indentation jumps too far on line {idx}")

        stack = stack[:depth + 1]
        parent = stack[-1]

        # Directory detection
        is_dir = stripped.endswith(("/", "\\"))

        raw = stripped.rstrip("/\\")
        parts = normalize_parts(raw)

        target = parent
        for part in parts:
            target = target / part

        try:
            if is_dir:
                target.mkdir(parents=True, exist_ok=True)
                stack.append(target)
                if args.verbose:
                    print(f"DIR:  {target}")
            else:
                # File creation
                if target.exists() and not args.force and target.stat().st_size > 0:
                    if args.verbose:
                        print(f"SKIP: {target} (exists and not empty)")
                    continue

                target.parent.mkdir(parents=True, exist_ok=True)
                target.touch()
                if args.verbose:
                    print(f"FILE: {target}")

        except Exception as e:
            sys.exit(f"Error on line {idx}: {e}")


if __name__ == "__main__":
    main()
