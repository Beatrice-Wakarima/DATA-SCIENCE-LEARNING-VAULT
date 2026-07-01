**`glob`** is a built-in Python module used to search for files and folders on your computer whose names match a specific pattern.

The name comes from the term **"globbing,"** which is old computer slang for matching wildcard patterns (like finding all files that end in `.xlsx`).

Instead of writing complex code to manually loop through folders, check file extensions, and filter out hidden system files, `glob` lets you find exactly what you are looking for in a single line of code using **wildcard characters**.

###  The Core Wildcard Characters

There are three main symbols you use to build patterns in `glob`:

#### 1. The Asterisk (`*`) – Matches _Everything_

The `*` matches any number of characters, including letters, numbers, or symbols.

- **Example:** `*.xlsx` means _"I don't care what the file name is, as long as it ends with `.xlsx`."_
    
- This is exactly how your Python ETL container found your 4 financial spreadsheets inside the `/app/data` folder!
    

#### 2. The Question Mark (`?`) – Matches a _Single_ Character

The `?` acts as a placeholder for exactly one character.

- **Example:** `sales_202?.csv` will find `sales_2024.csv`, `sales_2025.csv`, and `sales_2026.csv`.
    
- It will _not_ match `sales_202.csv` (too short) or `sales_2026_final.csv` (too long).
    

#### 3. Square Brackets (`[ ]`) – Matches a _Range_ of Characters

Brackets let you specify a specific list or range of acceptable characters for a single slot.

- **Example:** `target_[Q13].xlsx` will only look for `target_Q1.xlsx` and `target_Q3.xlsx`.
    
- **Example:** `v[1-3]_data.csv` will find versions 1, 2, and 3, but ignore version 4.
    

### How it Looks in Action (Python)

Here is a quick look at how you use it in a script. It always returns a clean Python **list** containing the full path strings of every matching file it uncovers:

Python

```
import glob

# 1. Find all Excel files in the data folder
excel_files = glob.glob("data/*.xlsx")
print(excel_files)
# Output: ['data/Capital_Budgeting.xlsx', 'data/Employee_Fact.xlsx', 'data/revenue_targets.xlsx', 'data/spaero_sales.xlsx']

# 2. Find only sales files that have a single-digit version number
versioned_sales = glob.glob("data/sales_v?.xlsx")
print(versioned_sales)
# Output: ['data/sales_v1.xlsx', 'data/sales_v2.xlsx']
```

### Going Deep: Recursive Searching ()

By default, `glob` only looks inside the single folder you point it at. If your data folder has nested subfolders (like `data/2025/` and `data/2026/`), a regular search will miss them.

To search through an entire directory tree, you use a **recursive** search with a double asterisk ():

Python

```
# Look inside the data folder, ANY subfolders, and find ALL Excel sheets
all_nested_files = glob.glob("data/**/*.xlsx", recursive=True)
```

In short, `glob` is the file-system scout for your automation pipelines. It goes out, scans the target directories using your wildcard pattern rules, and hands a clean list of file paths back to engines like Pandas or OpenPyXL so they can begin processing data.