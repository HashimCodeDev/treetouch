import argparse
import sys
import os
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert indented text into directory structure")
    parser.add_argument("--file", type=Path, help="Structure description file (stdin if omitted)")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root output directory (default: cwd)")
    parser.add_argument("--spaces", type=int, default=4, help="Spaces per indent level (default: 4)")
    parser.add_argument("--verbose", action="store_true", help="Print created paths")
    parser.add_argument("--force", action="store_true", help="Overwrite existing non-empty files")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Read lines from file or stdin
    if args.file:
        if not args.file.exists():
            sys.exit(f"Error: File not found {args.file}")
        lines = args.file.read_text(encoding='utf-8').splitlines()
    else:
        if sys.stdin.isatty():
            print("Enter folder structure (Ctrl+D after entering):", file=sys.stderr)
        lines = sys.stdin.read().splitlines()

    # Validate and build tree from indent
    stack = [args.root.resolve()]
    for idx, line in enumerate(lines, 1):
        if not line.strip():
            continue
        stripped = line.lstrip(' ')
        indent = len(line) - len(stripped)
        if indent % args.spaces != 0:
            sys.exit(f"Indentation error on line {idx}, expected multiple of {args.spaces} spaces")
        depth = indent // args.spaces
        if depth > len(stack) - 1:
            sys.exit(f"Indentation jumps too far on line {idx}")

        # Pop stack to proper depth level
        stack = stack[:depth + 1]
        parent = stack[-1]
        name = stripped.rstrip('/')
        is_dir = stripped.endswith('/')

        target = parent / name
        try:
            if is_dir:
                if not target.exists():
                    target.mkdir()
                stack.append(target)
                if args.verbose:
                    print(f"DIR:  {target}")
            else:
                if target.exists() and not args.force and target.stat().st_size > 0:
                    if args.verbose:
                        print(f"SKIP: {target} (exists and not empty)")
                    continue
                target.touch()
                if args.verbose:
                    print(f"FILE: {target}")
        except Exception as e:
            sys.exit(f"Error on line {idx}: {e}")

if __name__ == "__main__":
    main()
