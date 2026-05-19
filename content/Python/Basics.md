# Python Programming Basics

#programming #python #data-science #web-development #automation

## Overview

**Python** is a high-level, interpreted programming language known for its simplicity, readability, and versatility. Created by Guido van Rossum in 1991, it has become one of the most popular programming languages worldwide.

> [!quote] Python Philosophy (The Zen of Python) "Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex. Readability counts."

**Key Characteristics:**

- **Easy to learn**: Clean, readable syntax
- **Interpreted**: No compilation step needed
- **Cross-platform**: Runs on Windows, Mac, Linux
- **Extensive libraries**: Rich ecosystem of packages
- **Multi-paradigm**: Supports OOP, functional, procedural programming

## Why Learn Python?

### Career Opportunities

- **[[Data Science]]**: NumPy, pandas, scikit-learn
- **[[Web Development]]**: Django, Flask, FastAPI
- **[[Machine Learning]]**: TensorFlow, PyTorch, Keras
- **[[Automation]]**: Selenium, Beautiful Soup, Requests
- **[[DevOps]]**: Docker, Kubernetes, Ansible scripting
- **[[Game Development]]**: Pygame, Panda3D

### Industry Usage

- **Google**: YouTube, Google Search internals
- **Netflix**: Recommendation algorithms, automation
- **Instagram**: Backend services (Django)
- **Spotify**: Data analysis, backend services
- **Dropbox**: Desktop client, server infrastructure

---

## Installation & Setup

#python/installation

### Installing Python

bash

```bash
# Check if Python is installed
python --version
python3 --version

# Windows (using Python.org installer)
# Download from: https://python.org/downloads/

# macOS (using Homebrew)
brew install python

# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip
```

### Development Environment Setup

#### Option 1: [[IDLE]] (Built-in)

- Comes with Python installation
- Good for beginners and simple scripts

#### Option 2: [[VS Code]] (Recommended)

json

```json
// VS Code Python extensions
{
    "recommendations": [
        "ms-python.python",
        "ms-python.pylint",
        "ms-python.flake8"
    ]
}
```

#### Option 3: [[PyCharm]]

- Professional IDE for Python
- Excellent debugging and project management

#### Option 4: [[Jupyter Notebook]]

bash

```bash
pip install jupyter
jupyter notebook
```

### Package Management with [[pip]]

bash

```bash
# Install packages
pip install package_name
pip install requests pandas numpy

# Install specific version
pip install django==3.2.0

# Install from requirements.txt
pip install -r requirements.txt

# Create requirements.txt
pip freeze > requirements.txt

# Upgrade packages
pip install --upgrade package_name

# Uninstall packages
pip uninstall package_name
```

### Virtual Environments

bash

```bash
# Create virtual environment
python -m venv myenv

# Activate (Windows)
myenv\Scripts\activate

# Activate (macOS/Linux)
source myenv/bin/activate

# Deactivate
deactivate

# Install packages in virtual environment
pip install requests pandas
```

---

## Python Syntax Basics

#python/syntax

### Running Python Code

python

```python
# Interactive Python (REPL)
python
>>> print("Hello, World!")
Hello, World!

# Run Python file
python script.py

# Run module as script
python -m module_name
```

### Comments

python

```python
# Single line comment
print("Hello")  # End of line comment

"""
Multi-line comment
or docstring
"""

'''
Alternative multi-line
comment syntax
'''
```

### Basic Output

python

```python
# Print function
print("Hello, World!")
print("Hello", "World", sep=" ", end="\n")

# Formatted output
name = "Alice"
age = 25
print(f"My name is {name} and I'm {age} years old")  # f-strings (Python 3.6+)
print("My name is {} and I'm {} years old".format(name, age))  # .format()
print("My name is %s and I'm %d years old" % (name, age))  # % formatting
```

### Basic Input

python

```python
# Get user input (always returns string)
name = input("Enter your name: ")
age = int(input("Enter your age: "))  # Convert to integer

# Input validation
while True:
    try:
        age = int(input("Enter your age: "))
        break
    except ValueError:
        print("Please enter a valid number")
```

---

## Variables & Data Types

#python/variables #python/data-types

### Variable Assignment

python

```python
# Basic assignment
name = "Alice"
age = 25
height = 5.6
is_student = True

# Multiple assignment
x, y, z = 1, 2, 3
a = b = c = 0

# Swapping variables
x, y = y, x

# Unpacking
coordinates = (10, 20)
x, y = coordinates
```

### Variable Naming Rules

python

```python
# Valid names
my_variable = 1
myVariable = 2  # camelCase (less common in Python)
my_variable2 = 3
_private_var = 4
__very_private = 5

# Invalid names (will cause SyntaxError)
# 2variable = 6      # Can't start with number
# my-variable = 7    # Hyphens not allowed
# class = 8          # Reserved keyword
# my variable = 9    # Spaces not allowed
```

### Data Types Overview

#### 1. Numbers

python

```python
# Integers
age = 25
big_number = 1_000_000  # Underscores for readability

# Floats
height = 5.75
scientific = 2.5e6  # 2,500,000

# Complex numbers
complex_num = 3 + 4j

# Type checking
print(type(age))        # <class 'int'>
print(isinstance(age, int))  # True

# Type conversion
str_num = "123"
int_num = int(str_num)     # 123
float_num = float(str_num)  # 123.0
```

#### 2. Strings

python

```python
# String creation
single_quote = 'Hello'
double_quote = "World"
multi_line = """This is a
multi-line string"""

# String concatenation
full_name = "John" + " " + "Doe"
greeting = f"Hello, {full_name}!"

# String methods
text = "Python Programming"
print(text.lower())        # python programming
print(text.upper())        # PYTHON PROGRAMMING
print(text.title())        # Python Programming
print(text.replace("Python", "Java"))  # Java Programming
print(text.split())        # ['Python', 'Programming']
print(len(text))          # 18

# String indexing and slicing
text = "Python"
print(text[0])    # P (first character)
print(text[-1])   # n (last character)
print(text[0:3])  # Pyt (characters 0, 1, 2)
print(text[:3])   # Pyt (from beginning to index 3)
print(text[3:])   # hon (from index 3 to end)
print(text[::-1]) # nohtyP (reverse string)
```

#### 3. Booleans

python

```python
# Boolean values
is_active = True
is_complete = False

# Boolean operations
print(True and False)  # False
print(True or False)   # True
print(not True)        # False

# Truthiness in Python
# Falsy values: False, 0, 0.0, '', [], {}, None
print(bool(0))         # False
print(bool(""))        # False
print(bool([]))        # False
print(bool("Hello"))   # True
print(bool([1, 2, 3])) # True
```

### Type Conversion

python

```python
# Explicit type conversion
num_str = "123"
num_int = int(num_str)      # 123
num_float = float(num_str)  # 123.0

age = 25
age_str = str(age)          # "25"

# Implicit type conversion
result = 10 + 3.5           # 13.5 (int + float = float)
```

---

## Operators

#python/operators

### Arithmetic Operators

python

```python
x = 10
y = 3

print(x + y)    # Addition: 13
print(x - y)    # Subtraction: 7
print(x * y)    # Multiplication: 30
print(x / y)    # Division: 3.3333...
print(x // y)   # Floor division: 3
print(x % y)    # Modulus (remainder): 1
print(x ** y)   # Exponentiation: 1000

# Compound assignment operators
x += 5    # x = x + 5
x -= 3    # x = x - 3
x *= 2    # x = x * 2
x /= 4    # x = x / 4
```

### Comparison Operators

python

```python
a = 10
b = 20

print(a == b)   # Equal to: False
print(a != b)   # Not equal to: True
print(a < b)    # Less than: True
print(a > b)    # Greater than: False
print(a <= b)   # Less than or equal: True
print(a >= b)   # Greater than or equal: False

# String comparison (lexicographic)
print("apple" < "banana")  # True
print("Python" == "python")  # False (case sensitive)
```

### Logical Operators

python

```python
# and, or, not
age = 25
income = 50000

print(age >= 18 and income > 30000)  # True
print(age < 18 or income > 100000)   # False
print(not (age < 18))                # True

# Short-circuit evaluation
def expensive_operation():
    print("This function was called!")
    return True

# This won't call expensive_operation() because first condition is False
result = False and expensive_operation()
```

### Membership Operators

python

```python
# in and not in
fruits = ["apple", "banana", "orange"]
print("apple" in fruits)        # True
print("grape" not in fruits)    # True

text = "Python Programming"
print("Python" in text)         # True
print("Java" not in text)       # True
```

### Identity Operators

python

```python
# is and is not
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)    # True (same content)
print(a is b)    # False (different objects)
print(a is c)    # True (same object)

# Common use with None
value = None
if value is None:
    print("Value is None")

# Don't use == with None
if value == None:  # Works but not recommended
    print("Value is None")
```

---

## Data Structures

#python/data-structures

### Lists

python

```python
# Creating lists
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, True, 3.14]
empty_list = []

# List methods
fruits = ["apple", "banana"]
fruits.append("orange")           # Add to end
fruits.insert(1, "grape")         # Insert at index
fruits.remove("banana")           # Remove first occurrence
popped = fruits.pop()             # Remove and return last item
fruits.extend(["kiwi", "mango"])  # Add multiple items

# List indexing and slicing
numbers = [0, 1, 2, 3, 4, 5]
print(numbers[0])      # 0 (first item)
print(numbers[-1])     # 5 (last item)
print(numbers[1:4])    # [1, 2, 3] (slice)
print(numbers[:3])     # [0, 1, 2] (first 3)
print(numbers[3:])     # [3, 4, 5] (from index 3)
print(numbers[::2])    # [0, 2, 4] (every 2nd item)

# List comprehensions (advanced)
squares = [x**2 for x in range(10)]           # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
evens = [x for x in range(20) if x % 2 == 0] # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Common list operations
numbers = [3, 1, 4, 1, 5, 9, 2]
print(len(numbers))        # 7 (length)
print(max(numbers))        # 9 (maximum)
print(min(numbers))        # 1 (minimum)
print(sum(numbers))        # 25 (sum)
print(numbers.count(1))    # 2 (count occurrences)
numbers.sort()             # Sort in place
print(numbers)             # [1, 1, 2, 3, 4, 5, 9]
```

### Tuples

python

```python
# Creating tuples (immutable)
coordinates = (10, 20)
rgb_color = (255, 0, 128)
single_item = (42,)  # Note the comma for single-item tuple
empty_tuple = ()

# Tuple unpacking
point = (3, 4)
x, y = point
print(f"x: {x}, y: {y}")  # x: 3, y: 4

# Named tuples (from collections module)
from collections import namedtuple
Person = namedtuple('Person', ['name', 'age', 'city'])
alice = Person('Alice', 30, 'New York')
print(alice.name)     # Alice
print(alice.age)      # 30
```

### Dictionaries

python

```python
# Creating dictionaries
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "is_student": False
}

# Alternative creation methods
person2 = dict(name="Bob", age=25, city="Boston")
person3 = dict([("name", "Charlie"), ("age", 35)])

# Dictionary operations
print(person["name"])          # Alice
print(person.get("age"))       # 30
print(person.get("salary", 0)) # 0 (default value)

person["salary"] = 50000       # Add new key-value pair
person["age"] = 31             # Update existing value
del person["is_student"]       # Remove key-value pair

# Dictionary methods
print(person.keys())           # dict_keys(['name', 'age', 'city', 'salary'])
print(person.values())         # dict_values(['Alice', 31, 'New York', 50000])
print(person.items())          # dict_items([('name', 'Alice'), ...])

# Dictionary comprehensions
numbers = [1, 2, 3, 4, 5]
squares_dict = {x: x**2 for x in numbers}  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

### Sets

python

```python
# Creating sets (unique elements only)
fruits = {"apple", "banana", "orange"}
numbers = {1, 2, 3, 4, 5}
empty_set = set()  # Note: {} creates empty dict, not set

# Set operations
fruits.add("grape")            # Add element
fruits.remove("banana")        # Remove element (raises error if not found)
fruits.discard("kiwi")         # Remove element (no error if not found)

# Set mathematics
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print(set1 | set2)       # Union: {1, 2, 3, 4, 5, 6}
print(set1 & set2)       # Intersection: {3, 4}
print(set1 - set2)       # Difference: {1, 2}
print(set1 ^ set2)       # Symmetric difference: {1, 2, 5, 6}
```

---

## Control Flow

#python/control-flow

### Conditional Statements

#### if/elif/else

python

```python
# Basic if statement
age = 18
if age >= 18:
    print("You are an adult")

# if-else
score = 85
if score >= 60:
    print("Pass")
else:
    print("Fail")

# if-elif-else chain
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade is: {grade}")

# Ternary operator (conditional expression)
age = 20
status = "adult" if age >= 18 else "minor"
```

#### Advanced Conditionals

python

```python
# Multiple conditions
age = 25
income = 50000
if age >= 18 and income > 30000:
    print("Eligible for loan")

# Checking membership
valid_users = ["alice", "bob", "charlie"]
username = "alice"
if username in valid_users:
    print("Access granted")

# Checking for None
value = None
if value is not None:
    print(f"Value is: {value}")
else:
    print("No value provided")
```

### Loops

#### for loops

python

```python
# Iterating over sequences
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"I like {fruit}")

# Using range()
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):       # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8
    print(i)

# Iterating with index using enumerate()
fruits = ["apple", "banana", "orange"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Iterating over dictionary
person = {"name": "Alice", "age": 30, "city": "NYC"}
for key in person:
    print(f"{key}: {person[key]}")

for key, value in person.items():
    print(f"{key}: {value}")

# Nested loops
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})")
```

#### while loops

python

```python
# Basic while loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# Input validation with while
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input.lower() == 'quit':
        break
    print(f"You entered: {user_input}")

# While with else (executes if loop completes normally)
count = 0
while count < 3:
    print(count)
    count += 1
else:
    print("Loop completed normally")
```

#### Loop Control

python

```python
# break - exit loop immediately
for i in range(10):
    if i == 5:
        break
    print(i)  # Prints 0, 1, 2, 3, 4

# continue - skip to next iteration
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)  # Prints 1, 3, 5, 7, 9

# pass - do nothing (placeholder)
for i in range(5):
    if i == 2:
        pass  # TODO: implement special case
    else:
        print(i)
```

---

## Functions

#python/functions

### Basic Function Definition

python

```python
# Simple function
def greet():
    print("Hello, World!")

greet()  # Call the function

# Function with parameters
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")

# Function with return value
def add_numbers(a, b):
    result = a + b
    return result

sum_result = add_numbers(5, 3)
print(sum_result)  # 8

# Multiple return values
def get_name_parts(full_name):
    parts = full_name.split()
    first_name = parts[0]
    last_name = parts[-1]
    return first_name, last_name

first, last = get_name_parts("John Doe")
```

### Function Parameters

#### Default Parameters

python

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Bob", "Hi")         # Hi, Bob!
greet("Charlie", greeting="Hey")  # Hey, Charlie!
```

#### Keyword Arguments

python

```python
def create_profile(name, age, city="Unknown", occupation="Unknown"):
    return {
        "name": name,
        "age": age,
        "city": city,
        "occupation": occupation
    }

# Positional arguments
profile1 = create_profile("Alice", 30)

# Keyword arguments
profile2 = create_profile(name="Bob", age=25, city="Boston")

# Mixed (positional must come before keyword)
profile3 = create_profile("Charlie", 35, occupation="Engineer")
```

#### Variable Arguments

python

```python
# *args - variable positional arguments
def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3))        # 6
print(sum_all(1, 2, 3, 4, 5))  # 15

# **kwargs - variable keyword arguments
def create_person(**kwargs):
    person = {}
    for key, value in kwargs.items():
        person[key] = value
    return person

person = create_person(name="Alice", age=30, city="NYC", job="Engineer")

# Combining all parameter types
def complex_function(required, *args, default="value", **kwargs):
    print(f"Required: {required}")
    print(f"Args: {args}")
    print(f"Default: {default}")
    print(f"Kwargs: {kwargs}")

complex_function("test", 1, 2, 3, default="changed", extra="info")
```

### Function Scope

python

```python
# Global vs Local scope
global_var = "I'm global"

def my_function():
    local_var = "I'm local"
    print(global_var)   # Can access global
    print(local_var)    # Can access local

def modify_global():
    global global_var
    global_var = "Modified global"

# Nested functions and closures
def outer_function(x):
    def inner_function(y):
        return x + y  # Can access outer function's parameters
    return inner_function

add_ten = outer_function(10)
result = add_ten(5)  # 15
```

### Lambda Functions

python

```python
# Lambda (anonymous) functions
square = lambda x: x**2
print(square(5))  # 25

add = lambda x, y: x + y
print(add(3, 4))  # 7

# Using lambda with built-in functions
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))  # [1, 4, 9, 16, 25]
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]

# Sorting with lambda
students = [("Alice", 85), ("Bob", 90), ("Charlie", 78)]
students.sort(key=lambda student: student[1])  # Sort by grade
```

### Decorators (Basic)

python

```python
# Simple decorator example
def timer_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer_decorator
def slow_function():
    import time
    time.sleep(1)
    return "Done"

result = slow_function()  # Will print execution time
```

---

## Error Handling

#python/error-handling #python/exceptions

### Common Exception Types

python

```python
# Common built-in exceptions
try:
    # ZeroDivisionError
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

try:
    # ValueError
    number = int("not a number")
except ValueError:
    print("Invalid number format")

try:
    # IndexError
    my_list = [1, 2, 3]
    item = my_list[10]
except IndexError:
    print("Index out of range")

try:
    # KeyError
    my_dict = {"a": 1, "b": 2}
    value = my_dict["c"]
except KeyError:
    print("Key not found")

try:
    # FileNotFoundError
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("File not found")
```

### Exception Handling Syntax

python

```python
# Basic try-except
try:
    risky_operation()
except Exception as e:
    print(f"An error occurred: {e}")

# Multiple exceptions
try:
    user_input = input("Enter a number: ")
    number = int(user_input)
    result = 10 / number
except ValueError:
    print("That's not a valid number")
except ZeroDivisionError:
    print("Cannot divide by zero")

# Multiple exceptions with same handler
try:
    risky_operation()
except (ValueError, TypeError) as e:
    print(f"Value or Type error: {e}")

# Generic exception handler
try:
    risky_operation()
except ValueError:
    print("Specific value error")
except Exception as e:
    print(f"Something else went wrong: {e}")

# else clause (runs if no exception)
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Division by zero")
else:
    print(f"Result: {result}")

# finally clause (always runs)
try:
    file = open("data.txt", "r")
    data = file.read()
except FileNotFoundError:
    print("File not found")
finally:
    # This runs regardless of exception
    try:
        file.close()
    except:
        pass
```

### Raising Exceptions

python

```python
# Raising built-in exceptions
def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")

# Custom exceptions
class CustomError(Exception):
    pass

class ValidationError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

def validate_email(email):
    if "@" not in email:
        raise ValidationError("Email must contain @", code="INVALID_FORMAT")

try:
    validate_email("invalid-email")
except ValidationError as e:
    print(f"Validation failed: {e}")
    print(f"Error code: {e.code}")
```

---

## File Operations

#python/file-io #python/files

### Reading Files

python

```python
# Basic file reading
with open("data.txt", "r") as file:
    content = file.read()
    print(content)

# Reading line by line
with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())  # strip() removes newline characters

# Reading all lines into a list
with open("data.txt", "r") as file:
    lines = file.readlines()

# Reading with error handling
try:
    with open("data.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Permission denied")

# Different encodings
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()
```

### Writing Files

python

```python
# Writing to file (overwrites existing content)
with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is a new line.")

# Appending to file
with open("output.txt", "a") as file:
    file.write("\nThis line was appended.")

# Writing multiple lines
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w") as file:
    file.writelines(lines)

# Writing data structures
import json
data = {"name": "Alice", "age": 30, "city": "NYC"}
with open("data.json", "w") as file:
    json.dump(data, file, indent=2)
```

### Working with CSV Files

python

```python
import csv

# Reading CSV
with open("data.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)

# Reading CSV with headers
with open("data.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        print(row["name"], row["age"])

# Writing CSV
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "NYC"],
    ["Bob", 25, "Boston"]
]

with open("output.csv", "w", newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)

# Writing CSV with dictionary
fieldnames = ["name", "age", "city"]
data = [
    {"name": "Alice", "age": 30, "city": "NYC"},
    {"name": "Bob", "age": 25, "city": "Boston"}
]

with open("output.csv", "w", newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(data)
```

### File System Operations

python

```python
import os

# Current directory
current_dir = os.getcwd()
print(current_dir)

# Change directory
os.chdir("/path/to/directory")

# List directory contents
files = os.listdir(".")
for file in files:
    print(file)

# Check if file/directory exists
if os.path.exists("data.txt"):
    print("File exists")

if os.path.isfile("data.txt"):
    print("It's a file")

if os.path.isdir("my_folder"):
    print("It's a directory")

# Create directory
os.mkdir("new_folder")
os.makedirs("path/to/nested/folder")  # Create nested directories

# File operations
os.rename("old_name.txt", "new_name.txt")
os.remove("file_to_delete.txt")

# Path operations (use pathlib for modern Python)
from pathlib import Path

# Create Path objects
file_path = Path("data/input/file.txt")
print(file_path.parent)        # data/input
print(file_path.name)          # file.txt
print(file_path.stem)          # file
print(file_path.suffix)        # .txt

# Check existence
if file_path.exists():
    print("File exists")

# Create directories
file_path.parent.mkdir(parents=True, exist_ok=True)

# Read/write with pathlib
content = file_path.read_text()
file_path.write_text("New content")
```

---

## Modules and Packages

#python/modules #python/packages

### Importing Modules

python

```python
# Import entire module
import math
print(math.pi)         # 3.141592653589793
print(math.sqrt(16))   # 4.0

# Import specific functions
from math import pi, sqrt
print(pi)             # 3.141592653589793
print(sqrt(16))       # 4.0

# Import with alias
import math as m
print(m.pi)

from math import sqrt as square_root
print(square_root(16))

# Import all (not recommended)
from math import *
print(pi, e, sqrt(16))
```

### Standard Library Modules

#### [[datetime]] Module

python

```python
from datetime import datetime, date, timedelta

# Current date and time
now = datetime.now()
today = date.today()

# Creating specific dates
birthday = date(1990, 5, 15)
meeting_time = datetime(2024, 12, 25, 14, 30)

# Date arithmetic
tomorrow = today + timedelta(days=1)
next_week = now + timedelta(weeks=1)
three_hours_ago = now - timedelta(hours=3)

# Formatting dates
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted_date)  # 2024-01-15 14:30:45

# Parsing strings to dates
date_string = "2024-01-15"
parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
```

#### [[random]] Module

python

```python
import random

# Random numbers
random_int = random.randint(1, 10)        # Random integer 1-10
random_float = random.random()            # Random float 0.0-1.0
random_range = random.uniform(1.5, 10.5)  # Random float in range

# Random choices
fruits = ["apple", "banana", "orange"]
chosen_fruit = random.choice(fruits)
sample_fruits = random.sample(fruits, 2)  # Sample 2 without replacement

# Shuffle list in place
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)

# Set seed for reproducible results
random.seed(42)
print(random.randint(1, 100))  # Always produces same result with seed 42
```

#### [[json]] Module

python

```python
import json

# Python dict to JSON string
data = {
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "swimming"],
    "married": False
}

json_string = json.dumps(data, indent=2)
print(json_string)

# JSON string to Python dict
json_data = '{"name": "Bob", "age": 25}'
python_data = json.loads(json_data)
print(python_data["name"])  # Bob

# Read JSON from file
with open("data.json", "r") as file:
    data = json.load(file)

# Write JSON to file
with open("output.json", "w") as file:
    json.dump(data, file, indent=2)
```

#### [[requests]] Module (Third-party)

python

```python
# First install: pip install requests
import requests

# GET request
response = requests.get("https://api.github.com/users/octocat")
if response.status_code == 200:
    user_data = response.json()
    print(user_data["login"])  # octocat

# POST request with data
data = {"name": "John", "email": "john@example.com"}
response = requests.post("https://httpbin.org/post", json=data)

# Request with headers
headers = {"User-Agent": "My Python App"}
response = requests.get("https://httpbin.org/headers", headers=headers)

# Error handling
try:
    response = requests.get("https://httpbin.org/status/404")
    response.raise_for_status()  # Raises exception for bad status codes
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### Creating Custom Modules

python

```python
# Create a file called my_utils.py
def greet(name):
    return f"Hello, {name}!"

def calculate_area(length, width):
    return length * width

PI = 3.14159

class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

# Using your custom module
# In another file:
import my_utils

print(my_utils.greet("Alice"))
area = my_utils.calculate_area(5, 3)
calc = my_utils.Calculator()
result = calc.add(10, 5)
```

### Package Structure

```
my_package/
    __init__.py          # Makes it a package
    module1.py
    module2.py
    subpackage/
        __init__.py
        submodule.py
```

python

```python
# __init__.py contents
from .module1 import function1
from .module2 import function2

# Usage
from my_package import function1, function2
```

---

## Object-Oriented Programming

#python/oop #python/classes

### Basic Class Definition

python

```python
# Simple class
class Person:
    # Class variable (shared by all instances)
    species = "Homo sapiens"
    
    # Constructor method
    def __init__(self, name, age):
        # Instance variables (unique to each instance)
        self.name = name
        self.age = age
    
    # Instance method
    def introduce(self):
        return f"Hi, I'm {self.name} and I'm {self.age} years old"
    
    # Another method
    def have_birthday(self):
        self.age += 1
        return f"Happy birthday! {self.name} is now {self.age}"

# Creating objects (instances)
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

# Using methods
print(person1.introduce())     # Hi, I'm Alice and I'm 25 years old
print(person1.have_birthday()) # Happy birthday! Alice is now 26

# Accessing attributes
print(person1.name)            # Alice
print(person1.species)         # Homo sapiens
```

### Class Methods and Static Methods

python

```python
class MathUtils:
    pi = 3.14159
    
    def __init__(self, value):
        self.value = value
    
    # Instance method
    def square(self):
        return self.value ** 2
    
    # Class method (uses cls parameter, can access class variables)
    @classmethod
    def get_pi(cls):
        return cls.pi
    
    # Static method (no self or cls, like a regular function in the class)
    @staticmethod
    def add(a, b):
        return a + b

# Usage
math_obj = MathUtils(5)
print(math_obj.square())           # 25

# Calling class method
print(MathUtils.get_pi())          # 3.14159

# Calling static method
print(MathUtils.add(3, 4))         # 7
```

### Inheritance

python

```python
# Base class (parent)
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        return "Some generic animal sound"
    
    def info(self):
        return f"{self.name} is a {self.species}"

# Derived class (child)
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")  # Call parent constructor
        self.breed = breed
    
    # Method overriding
    def make_sound(self):
        return "Woof!"
    
    # Additional method
    def fetch(self):
        return f"{self.name} is fetching the ball!"

class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name, "Cat")
        self.indoor = indoor
    
    def make_sound(self):
        return "Meow!"

# Usage
dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Whiskers", indoor=True)

print(dog.info())         # Buddy is a Dog
print(dog.make_sound())   # Woof!
print(dog.fetch())        # Buddy is fetching the ball!

print(cat.make_sound())   # Meow!
```

### Encapsulation and Properties

python

```python
class BankAccount:
    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self._balance = initial_balance  # Protected attribute (convention)
        self.__pin = "0000"              # Private attribute (name mangling)
    
    # Property getter
    @property
    def balance(self):
        return self._balance
    
    # Property setter
    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount
    
    # Methods
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return f"Deposited ${amount}. New balance: ${self._balance}"
        else:
            return "Invalid deposit amount"
    
    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return f"Withdrew ${amount}. New balance: ${self._balance}"
        else:
            return "Invalid withdrawal amount"

# Usage
account = BankAccount("123456", 1000)
print(account.balance)        # 1000
print(account.deposit(500))   # Deposited $500. New balance: $1500
print(account.withdraw(200))  # Withdrew $200. New balance: $1300

# Using property setter
account.balance = 2000        # Uses the setter
print(account.balance)        # 2000
```

### Special Methods (Magic Methods)

python

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # String representation
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    # Addition
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    # Equality
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    # Length
    def __len__(self):
        return int((self.x**2 + self.y**2)**0.5)
    
    # Indexing
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector index out of range")

# Usage
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1)                # Vector(3, 4)
print(v1 + v2)          # Vector(4, 6)
print(v1 == v2)         # False
print(len(v1))          # 5
print(v1[0])            # 3
```

---

## Common Built-in Functions

#python/built-ins #python/functions

### Essential Built-ins

python

```python
# Type and conversion functions
print(type(42))           # <class 'int'>
print(isinstance(42, int)) # True

# Conversion functions
int("123")               # 123
float("3.14")            # 3.14
str(42)                  # "42"
list("hello")            # ['h', 'e', 'l', 'l', 'o']
tuple([1, 2, 3])         # (1, 2, 3)
set([1, 1, 2, 3])        # {1, 2, 3}

# Math functions
abs(-5)                  # 5
min(1, 2, 3)            # 1
max([1, 2, 3])          # 3
sum([1, 2, 3, 4])       # 10
round(3.14159, 2)       # 3.14
pow(2, 3)               # 8

# Sequence functions
len("hello")             # 5
len([1, 2, 3])          # 3

# Input/Output
print("Hello, World!")
name = input("Enter your name: ")
```

### Iteration Functions

python

```python
# range() - generates sequences
list(range(5))          # [0, 1, 2, 3, 4]
list(range(1, 6))       # [1, 2, 3, 4, 5]
list(range(0, 10, 2))   # [0, 2, 4, 6, 8]

# enumerate() - adds index to iteration
fruits = ["apple", "banana", "orange"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Start enumeration from different number
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")

# zip() - combines multiple iterables
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["NYC", "Boston", "Chicago"]

for name, age, city in zip(names, ages, cities):
    print(f"{name} is {age} years old and lives in {city}")

# zip with unequal lengths (stops at shortest)
numbers = [1, 2, 3, 4, 5]
letters = ['a', 'b', 'c']
print(list(zip(numbers, letters)))  # [(1, 'a'), (2, 'b'), (3, 'c')]
```

### Higher-Order Functions

python

```python
# map() - applies function to all items
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# map with multiple iterables
nums1 = [1, 2, 3]
nums2 = [4, 5, 6]
sums = list(map(lambda x, y: x + y, nums1, nums2))
print(sums)  # [5, 7, 9]

# filter() - filters items based on condition
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# reduce() - reduces sequence to single value (need to import)
from functools import reduce
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)
print(product)  # 120 (1*2*3*4*5)

# sorted() - returns sorted list
numbers = [3, 1, 4, 1, 5, 9, 2]
sorted_nums = sorted(numbers)
print(sorted_nums)  # [1, 1, 2, 3, 4, 5, 9]

# Sort with key function
students = [("Alice", 85), ("Bob", 90), ("Charlie", 78)]
sorted_by_grade = sorted(students, key=lambda x: x[1])
print(sorted_by_grade)  # [('Charlie', 78), ('Alice', 85), ('Bob', 90)]

# Reverse sort
sorted_desc = sorted(numbers, reverse=True)
print(sorted_desc)  # [9, 5, 4, 3, 2, 1, 1]
```

### Other Useful Built-ins

python

```python
# all() and any()
print(all([True, True, True]))   # True
print(all([True, False, True]))  # False
print(any([False, False, True])) # True
print(any([False, False, False])) # False

# Practical use
numbers = [2, 4, 6, 8]
print(all(x % 2 == 0 for x in numbers))  # True (all even)

# reversed() - reverse iterator
numbers = [1, 2, 3, 4, 5]
print(list(reversed(numbers)))  # [5, 4, 3, 2, 1]

# vars() and dir() - introspection
class Person:
    def __init__(self, name):
        self.name = name

person = Person("Alice")
print(vars(person))  # {'name': 'Alice'}
print(dir(person))   # List of all attributes and methods

# hasattr(), getattr(), setattr()
print(hasattr(person, 'name'))     # True
print(getattr(person, 'name'))     # Alice
setattr(person, 'age', 30)
print(person.age)                  # 30
```

---

## List Comprehensions & Generators

#python/comprehensions #python/generators

### List Comprehensions

python

```python
# Basic list comprehension
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(squares)  # [1, 4, 9, 16, 25]

# With condition (filter)
evens = [x for x in numbers if x % 2 == 0]
print(evens)  # [2, 4]

# With condition and transformation
even_squares = [x**2 for x in numbers if x % 2 == 0]
print(even_squares)  # [4, 16]

# Nested comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [item for row in matrix for item in row]
print(flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Complex transformations
words = ["hello", "world", "python"]
lengths = [len(word) for word in words]
print(lengths)  # [5, 5, 6]

# Conditional expressions in comprehension
numbers = [1, 2, 3, 4, 5]
result = ["even" if x % 2 == 0 else "odd" for x in numbers]
print(result)  # ['odd', 'even', 'odd', 'even', 'odd']
```

### Dictionary Comprehensions

python

```python
# Basic dictionary comprehension
numbers = [1, 2, 3, 4, 5]
squares_dict = {x: x**2 for x in numbers}
print(squares_dict)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# From two lists
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
people = {name: age for name, age in zip(names, ages)}
print(people)  # {'Alice': 25, 'Bob': 30, 'Charlie': 35}

# With condition
even_squares = {x: x**2 for x in numbers if x % 2 == 0}
print(even_squares)  # {2: 4, 4: 16}

# Transform existing dictionary
original = {"a": 1, "b": 2, "c": 3}
doubled = {k: v * 2 for k, v in original.items()}
print(doubled)  # {'a': 2, 'b': 4, 'c': 6}
```

### Set Comprehensions

python

```python
# Basic set comprehension
numbers = [1, 2, 2, 3, 3, 4, 5]
unique_squares = {x**2 for x in numbers}
print(unique_squares)  # {1, 4, 9, 16, 25}

# With condition
even_set = {x for x in numbers if x % 2 == 0}
print(even_set)  # {2, 4}
```

### Generator Expressions

python

```python
# Generator expression (lazy evaluation)
squares_gen = (x**2 for x in range(1000000))
print(type(squares_gen))  # <class 'generator'>

# Use only what you need - memory efficient
first_five = [next(squares_gen) for _ in range(5)]
print(first_five)  # [0, 1, 4, 9, 16]

# Generator for large data processing
def process_large_file(filename):
    with open(filename) as file:
        return (line.strip().upper() for line in file if line.strip())

# Use generator in loops
large_numbers = (x for x in range(1000000) if x % 1000 == 0)
for num in large_numbers:
    if num > 10000:
        break
    print(num)
```

### Generator Functions

python

```python
# Generator function with yield
def fibonacci_generator(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Using generator function
fib_gen = fibonacci_generator(10)
print(list(fib_gen))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Infinite generator
def infinite_counter(start=0):
    while True:
        yield start
        start += 1

counter = infinite_counter(10)
print(next(counter))  # 10
print(next(counter))  # 11
print(next(counter))  # 12

# Generator with send() method
def echo_generator():
    while True:
        received = yield
        if received is not None:
            print(f"Received: {received}")

gen = echo_generator()
next(gen)  # Prime the generator
gen.send("Hello")    # Received: Hello
gen.send("World")    # Received: World
```

---

## Best Practices & Style Guide

#python/best-practices #python/pep8

### PEP 8 Style Guidelines

#### Naming Conventions

python

```python
# Variables and functions: snake_case
user_name = "alice"
def calculate_total_price():
    pass

# Constants: UPPER_CASE
MAX_RETRY_COUNT = 3
PI = 3.14159

# Classes: PascalCase
class CustomerAccount:
    pass

# Private attributes: leading underscore
class MyClass:
    def __init__(self):
        self._protected_var = "protected"
        self.__private_var = "private"

# Avoid single letter names (except for loops)
# Good
for index in range(10):
    pass

# Acceptable for short loops
for i in range(3):
    for j in range(3):
        print(i, j)
```

#### Code Layout

python

```python
# Imports at top, grouped by type
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports
import requests
import pandas as pd

# 3. Local imports
from myproject.utils import helper_function
from myproject.models import User

# Line length: max 79 characters
# Break long lines sensibly
result = some_function_with_long_name(
    parameter_one="value_one",
    parameter_two="value_two",
    parameter_three="value_three"
)

# Or using backslash (less preferred)
long_calculation = first_variable + second_variable + \
                  third_variable + fourth_variable

# Blank lines
# 2 blank lines around top-level functions and classes
class MyClass:
    pass


def my_function():
    pass


# 1 blank line around method definitions
class MyClass:
    def method_one(self):
        pass
    
    def method_two(self):
        pass
```

#### Spacing and Operators

python

```python
# Operators: spaces around binary operators
result = a + b
result = a * b + c * d
result = (a + b) * (c + d)

# No spaces around = in keyword arguments
function_call(param1=value1, param2=value2)

# No spaces around = in annotated function arguments
def function(param1: int = 0, param2: str = "default"):
    pass

# Commas: space after, not before
my_list = [1, 2, 3, 4]
my_dict = {"key1": "value1", "key2": "value2"}

# Colons: space after, not before (except slicing)
my_dict = {"key": "value"}
my_list[1:3]  # No space in slicing
```

### Type Hints (Python 3.5+)

python

```python
from typing import List, Dict, Optional, Union, Tuple, Callable

# Basic type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add_numbers(a: int, b: int) -> int:
    return a + b

# Complex types
def process_data(data: List[Dict[str, Union[str, int]]]) -> Dict[str, int]:
    result = {}
    for item in data:
        if isinstance(item.get("value"), int):
            result[item["name"]] = item["value"]
    return result

# Optional types (can be None)
def find_user(user_id: int) -> Optional[Dict[str, str]]:
    # Returns user dict or None if not found
    pass

# Variable annotations
name: str = "Alice"
numbers: List[int] = [1, 2, 3, 4, 5]
coordinates: Tuple[int, int] = (10, 20)

# Function type hints
def apply_operation(numbers: List[int], operation: Callable[[int], int]) -> List[int]:
    return [operation(num) for num in numbers]

# Class with type hints
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    
    def get_info(self) -> Dict[str, Union[str, int]]:
        return {"name": self.name, "age": self.age}
```

### Documentation and Comments

python

```python
"""
Module-level docstring explaining the purpose of this module.
"""

def calculate_compound_interest(principal: float, rate: float, 
                              time: float, compound_frequency: int = 1) -> float:
    """
    Calculate compound interest.
    
    Args:
        principal: Initial amount of money
        rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        time: Time in years
        compound_frequency: Number of times interest is compounded per year
    
    Returns:
        Final amount after compound interest
    
    Raises:
        ValueError: If any parameter is negative
    
    Example:
        >>> calculate_compound_interest(1000, 0.05, 2, 12)
        1104.89
    """
    if any(param < 0 for param in [principal, rate, time, compound_frequency]):
        raise ValueError("All parameters must be non-negative")
    
    # A = P(1 + r/n)^(nt)
    amount = principal * (1 + rate / compound_frequency) ** (compound_frequency * time)
    return round(amount, 2)

class BankAccount:
    """
    A simple bank account class.
    
    Attributes:
        account_number: Unique identifier for the account
        balance: Current balance in the account
    """
    
    def __init__(self, account_number: str, initial_balance: float = 0):
        """Initialize a new bank account."""
        self.account_number = account_number
        self._balance = initial_balance
    
    @property
    def balance(self) -> float:
        """Get current account balance."""
        return self._balance
```

### Error Handling Best Practices

python

```python
# Be specific with exception types
try:
    value = int(user_input)
except ValueError:  # Specific exception
    print("Please enter a valid number")

# Don't catch everything
try:
    risky_operation()
except Exception:  # Too broad - avoid unless necessary
    pass

# Use finally for cleanup
file = None
try:
    file = open("data.txt", "r")
    data = file.read()
except FileNotFoundError:
    print("File not found")
finally:
    if file:
        file.close()

# Better: use context managers
try:
    with open("data.txt", "r") as file:
        data = file.read()
except FileNotFoundError:
    print("File not found")

# Custom exceptions for specific domains
class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

def validate_email(email: str) -> None:
    if "@" not in email:
        raise ValidationError(f"Invalid email format: {email}")
```

### Code Organization

python

```python
# Use main guard
def main():
    """Main program entry point."""
    print("This is the main program")
    
    # Your main program logic here
    user_name = input("Enter your name: ")
    greet_user(user_name)

def greet_user(name: str) -> None:
    """Greet a user by name."""
    print(f"Hello, {name}!")

if __name__ == "__main__":
    main()

# Constants at module level
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
CONFIG_FILE = "config.json"

# Helper functions before main functions
def _helper_function():
    """Private helper function (indicated by leading underscore)."""
    pass

def public_function():
    """Public function that uses helper."""
    return _helper_function()
```

---

## Testing Basics

#python/testing #python/unittest

### Unit Testing with unittest

python

```python
import unittest
from mymodule import Calculator  # Assume we're testing a Calculator class

class TestCalculator(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()
    
    def tearDown(self):
        """Clean up after each test method."""
        # Usually not needed, but available if required
        pass
    
    def test_addition(self):
        """Test addition functionality."""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_division(self):
        """Test division functionality."""
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5.0)
    
    def test_division_by_zero(self):
        """Test that division by zero raises appropriate exception."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)
    
    def test_multiple_assertions(self):
        """Test multiple conditions
```

up:: [[Python MOC]]
