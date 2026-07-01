

**Purpose:** Why testing matters.

- Tackles bugs, errors, hardware failures, unexpected behavior.
    
- Saves costs by catching issues early.
    
- Ensures systems meet requirements.
    

## 🗂 What is Testing

**Purpose:** Define the process.

- Evaluates system against requirements.
    
- Uses **tests** → procedures verifying correctness and quality.
    
- Goal: discover errors before deployment.
    

## 🗂 Course Prerequisites

**Purpose:** Skills needed.

- Solid Python knowledge.
    
- Familiarity with **assert statements**, **decorators**, and **basic OOP concepts**.
    

## 🗂 Testing in Real Life

**Purpose:** Analogy for importance.

- Airplane pre‑flight checks → visual inspection, electronics, fuel, passengers, weather, ATC permission.
    
- Each is a test → ensures safety.
    
- Same principle applies to software reliability.
    

## 🗂 Assert in Python

**Purpose:** Quick built‑in test.

- Keyword `assert` checks condition returns True.
    
- If False → raises **AssertionError**.
    

## 🗂 Pytest Framework

**Purpose:** Popular testing tool.

- Simple way to write tests.
    
- Test function names start with `test_` → recognized by pytest.
    
- Example: `test_squared` verifies function works for both `-2` and `2`.
    
- Not exhaustive but a good start.
    

## 🗂 Context Managers Recap

**Purpose:** Manage temporary context.

- Declared with `with` statement.
    
- Useful for setup/teardown in tests.
    
- Example: ensure no division by zero occurs.
    

## 🗂 Pytest Raises

**Purpose:** Test exceptions.

- `pytest.raises` ensures expected exception is raised.
    
- Example: division function → raises **ZeroDivisionError** if denominator = 0.
    

## 🗂 Summary of Tools

**Purpose:** Key takeaways.

- Testing ensures correctness and safety.
    
- Use **assert** for quick checks.
    
- Use **pytest** for structured tests.
    
- Use **pytest.raises** for exception handling.