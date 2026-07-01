

**Purpose:** Prepared environments for tests.

- Fixtures = context setup functions.
    
- Example analogy: picnic → prepare food/friends (setup), have fun (test), clean up (teardown).
    
- Responsible for preparation step before test execution.
    

## 🗂 Why Use Fixtures

**Purpose:** Benefits.

- Divide and conquer approach.
    
- Isolate environment preparation from test logic.
    
- Reusable setup code across multiple tests.
    
- Makes tests modular and maintainable.
    

## 🗂 Fixture Example

**Purpose:** Demonstrate usage.

- Data list with 9 elements, including “five” and “twenty‑one.”
    
- Initialization separated into fixture function.
    
- Test function consumes fixture as variable, not function.
    
- Pytest automatically calls fixture → passes output into test.
    

## 🗂 Fixture Syntax

**Purpose:** How to declare.

- Import pytest.
    
- Use `@pytest.fixture` decorator above fixture function.
    
- Pass fixture name into test function signature.
    
- Inside test, use fixture output directly.
    

## 🗂 Fixture Output

**Purpose:** CLI results.

- Output shows package versions, number of tests collected, scripts analyzed, results.
    
- Example: one test function in one script → one test passed.
    

## 🗂 Steps to Use Fixtures

**Purpose:** Workflow.

1. Prepare software/tests.
    
2. Identify environment preparation parts (e.g., data preprocessing, global variables).
    
3. Create fixture functions with `@pytest.fixture`.
    
4. Declare test functions consuming fixtures.
    
5. Run tests via CLI.
    

## 🗂 Fixtures Summary

**Purpose:** Recap.

- Fixtures = prepared environments for test execution.
    
- Make setup modular and reusable.
    
- Defined with `@pytest.fixture`.
    
- Fixture names treated as variables inside tests.