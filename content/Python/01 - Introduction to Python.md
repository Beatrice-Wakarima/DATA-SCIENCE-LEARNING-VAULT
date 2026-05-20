---
title: Introduction to Python
tags: [python, basics]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🐍 Introduction to Python

> Python is a high-level, beginner-friendly programming language used in data science, automation, web development, and AI.

---

## Why Python?

- Easy to read and write — reads almost like English
- Huge library ecosystem (pandas, numpy, scikit-learn)
- Used by Google, Netflix, NASA, and most data teams
- Free and open source

---

## Running Python

### Option 1 — Interactive Mode (REPL)
Open terminal and type:
```python
python
```
You can now type Python directly:
```python
>>> print("Hello Beatrice!")
Hello Beatrice!
```

### Option 2 — Script File
Save a file as `hello.py` and run:
```bash
python hello.py
```

### Option 3 — Jupyter Notebook
Best for data science — run cells one at a time.

---

## Your First Python Program

```python
# This is a comment — Python ignores it
print("Hello, World!")
print("My name is Beatrice")
print("I am a Full-Stack Data Scientist")
```

**Output:**
```
Hello, World!
My name is Beatrice
I am a Full-Stack Data Scientist
```

---

## Python Indentation

Python uses **indentation** (spaces) instead of brackets. This is critical!

```python
# ✅ Correct
if True:
    print("This is indented correctly")

# ❌ Wrong — will give an error
if True:
print("This will break")
```

---

## Comments

```python
# Single line comment

"""
This is a 
multi-line comment
"""

# Good habit — always comment your code!
```

---

## Key Takeaways

- Python files end in `.py`
- Indentation is not optional — it defines code blocks
- `print()` displays output to the screen
- `#` starts a comment

---

## Practice Exercise

Write a program that prints:
1. Your name
2. Your job title
3. Your favourite tool

```python
# Try it yourself!
print("Beatrice Wakarima")
print("Full-Stack Data Scientist")
print("Power BI")
```

---

## Next Note
→ [[02 - Variables and Data Types]]
