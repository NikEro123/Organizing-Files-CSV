# Organizing-Files-CSV

A small Python script that walks a folder of categorized subfolders and writes a CSV
listing every file alongside the category it came from.

This is one of my first data-processing scripts. It's deliberately simple — the point
was to get comfortable with reading a directory tree, handling paths, and writing
structured output instead of printing to the screen.

## What it does

Given a folder laid out like this:

```
products/
├── dairy/
│   ├── milk.jpg
│   └── cheese.jpg
├── bakery/
│   └── bread.jpg
└── produce/
    └── apples.jpg
```

It produces `output.csv`:

```
File Name,Category
milk.jpg,dairy
cheese.jpg,dairy
bread.jpg,bakery
apples.jpg,produce
```

## How it works

1. `collect_files()` loops through each subfolder of the base path, treating the folder
   name as the category
2. For each item, it checks `os.path.isfile()` so subfolders and stray directories are
   skipped rather than crashing the run
3. `save_to_csv()` writes the rows with a header, using `newline=""` and UTF-8 so the
   file opens cleanly in Excel and doesn't mangle non-Latin filenames

## Run it

No dependencies beyond the standard library.

```bash
python forfiles.py
```

Set `base_path` at the top of the file to the folder you want to scan.

## What I learned

- Walking a directory tree with `os.listdir()` and `os.path.join()` instead of building
  paths by hand with string concatenation
- Why `os.path.isfile()` matters — without it, nested folders end up in the output as if
  they were files
- The `newline=""` argument to `open()`, and what happens to a CSV on Windows without it
- That writing to a file is a different discipline from printing: encoding and headers
  are decisions, not defaults

## Known limitations

- The folder path is hardcoded rather than passed as an argument
- Only scans one level deep — files directly inside `products/` are ignored
- Captures only filename and category; size, extension and modified date would be more
  useful in an inventory
- No error message if the base path doesn't exist — it just raises

## Next

Replace the hardcoded path with `argparse`, add file size and modified date as columns,
and add a `--recursive` flag for nested folders.
