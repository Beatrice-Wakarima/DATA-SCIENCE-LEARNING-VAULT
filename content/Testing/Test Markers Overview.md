

**Purpose:** Control test behavior.

- Markers = tags for test functions.
    
- Specify behavior (skip, expected fail, conditional run).
    
- Any test can have one or more markers.
    

## 🗂 Markers Syntax

**Purpose:** How to apply.

- Based on **decorators**.
    
- Syntax: `@pytest.mark.<marker_name>` above test function.
    
- Example: `@pytest.mark.skip` → skips test.
    

## 🗂 Skip Marker

**Purpose:** Skip tests unconditionally.

- Useful when test not needed right now.
    
- Output: test found but marked skipped.
    

## 🗂 Skipif Marker

**Purpose:** Skip tests conditionally.

- Syntax: `@pytest.mark.skipif(<condition>, reason="...")`.
    
- Example: `@pytest.mark.skipif(2*2==5, reason="always false")`.
    
- Can use variables (e.g., module version checks).
    

## 🗂 Xfail Marker

**Purpose:** Expected failure.

- Marks test that is _supposed_ to fail.
    
- Useful for known bugs → confirms bug still exists.
    
- Output: test “xfailed” → failed as expected.
    

## 🗂 Markers Summary

**Purpose:** Recap.

- Markers = tags to control test execution.
    
- Syntax: `@pytest.mark.<marker>`.
    
- Built‑in markers: **skip**, **skipif**, **xfail**.
    
- Use to manage test runs responsibly.