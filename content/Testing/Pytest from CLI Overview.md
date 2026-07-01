

**Purpose:** Run tests directly from terminal.

- CLI = Command‑Line Interface → interact with programs via text commands.
    
- Pytest keyword runs tests using pytest framework, not just as a Python script.
    

## 🗂 Example CLI Run

**Purpose:** Syntax basics.

- Command: `pytest slides.py`
    
- `pytest` → run with pytest framework.
    
- `slides.py` → module argument (specific test script).
    

## 🗂 CLI Output

**Purpose:** Understand results.

- Shows module versions.
    
- Number of collected tests.
    
- Names of test scripts.
    
- Test results → passed, failed, skipped.
    
- “Collected” = test functions pytest found.
    

## 🗂 IDE Exercises

**Purpose:** Practice environment.

- Instructions on left, scripts on right, console at bottom.
    
- Lets you write code and run CLI commands inside IDE.
    

## 🗂 Directory Argument

**Purpose:** Run multiple scripts.

- Save tests in folder (e.g., `tests_dir`).
    
- Command: `pytest tests_dir`
    
- Output shows collected tests across scripts.
    
- Trailing slash optional but improves readability.
    

## 🗂 Keyword Argument -k

**Purpose:** Filter tests by name.

- Use `-k` flag followed by expression.
    
- Example: `pytest -k squared` → runs only tests with “squared” in name.
    
- Output: collected items, deselected items, selected items.
    

## 🗂 Summary of CLI Usage

**Purpose:** Recap.

- CLI pytest command starts with `pytest`.
    
- Run one script → pass script name.
    
- Run multiple scripts → pass directory name.
    
- Filter tests → `-k` keyword expression.
    
- IDE exercises integrate CLI practice.