# TreeTouch

Folder-structure to folder-converter. Generates a real directory tree from a text-based structure definition. Operates through a single command: `treetouch`.

## Purpose

Eliminate manual folder creation. Accept a structured specification and materialize it directly into nested directories and files.

## Features

* Converts a text tree into actual folders and empty files.
* Supports nested structures of arbitrary depth.
* Minimal command surface: `treetouch <spec-file>` or piped input.
* Safe operation with overwrite checks.

## Installation

```bash
npm install -g treetouch
```

## Usage

### Basic

```bash
treetouch structure.txt
```

### Piped

```bash
cat structure.txt | treetouch
```

### Inline

```bash
treetouch <<EOF
src/
  components/
    Header.js
    Footer.js
  utils/
    helpers.js
README.md
EOF
```

## Input Format

Indentation defines hierarchy.
A line ending with `/` becomes a folder.
A line without `/` becomes an empty file.

Example:

```
project/
  src/
    index.js
    api/
      client.js
  test/
    sample.test.js
README.md
```

## Output

Actual filesystem:

```
project
├── src
│   ├── index.js
│   └── api
│       └── client.js
├── test
│   └── sample.test.js
└── README.md
```

## Error Handling

* Rejects malformed indentation.
* Reports collisions with existing paths.
* Rejects invalid characters.

## Notes

TreeTouch creates only the structure. File contents remain empty.
