# Test Data Requirements & Validation Gates

## 🚨 The 100-App Validation Gate

### The Issue

The `DataExtractor` has a **production safety gate** that requires:

- **Minimum 100 apps** in the extracted data
- This prevents accidentally processing incomplete/corrupt data files

python

```python
# In src/extract.py
def validate_apps_extraction(self, df: pd.DataFrame) -> None:
    if len(df) < 100:
        raise ValueError(f"Insufficient data: got {len(df)} apps")
```

### The Conflict

Original test fixtures had only 4 rows:

python

```python
# ❌ This would FAIL validation
@pytest.fixture
def sample_apps_data():
    return pd.DataFrame({
        'App': ['App1', 'App2', 'App3', 'App1'],  # Only 4 rows!
        ...
    })
```

When tests call `extractor.extract_all()`, validation runs and **fails**:

```
ValueError: Insufficient data: got 4 apps, expected at least 100
```

## ✅ The Solution

### Strategy 1: Use 100+ Records in Integration Test Fixtures

For tests that go through the **complete pipeline** (extract → transform → load):

python

```python
@pytest.fixture
def sample_apps_data():
    """Fixture with 120 apps to pass validation."""
    apps_list = []
    for i in range(120):
        apps_list.append({
            'App': f'App{i}',
            'Rating': 4.5,
            # ... other fields
        })
    return pd.DataFrame(apps_list)
```

**Benefits:**

- ✅ Passes validation
- ✅ Tests real-world data volumes
- ✅ Catches performance issues

### Strategy 2: Use Small Data for Unit Tests

For tests of **individual functions** (without validation):

python

```python
@pytest.fixture
def small_apps_data():
    """Small fixture for unit tests - bypasses validation."""
    return pd.DataFrame({
        'App': ['App1', 'App2', 'App3'],  # Only 3 rows OK here
        ...
    })

def test_clean_size_column(transformer):
    """Unit test - doesn't call validation."""
    df = pd.DataFrame({'Size': ['10M', '500k']})  # 2 rows OK
    result = transformer.clean_size_column(df)
    assert result['Size'].iloc[0] == 10.0
```

**When to use:**

- ✅ Testing `transformer.clean_X_column()` functions
- ✅ Testing data cleaning logic
- ✅ Testing edge cases with specific values
- ✅ Performance (faster tests)

### Strategy 3: Use Test Factories with Proper Defaults

Factories now default to 120 apps:

python

```python
# ✅ Passes validation
df = AppDataFactory.create()  # Default: 120 apps

# ✅ For unit tests, explicitly use fewer
df = AppDataFactory.create(num_apps=5)  # OK for unit tests
```

## 📊 Test Type Decision Matrix

| Test Type            | Data Size  | Passes Validation? | Use                                                    |
| -------------------- | ---------- | ------------------ | ------------------------------------------------------ |
| **Integration Test** | 100+ apps  | ✅ Yes              | `sample_apps_data`, `AppDataFactory.create()`          |
| **Unit Test**        | Any size   | N/A (bypasses)     | `small_apps_data`, `AppDataFactory.create(num_apps=5)` |
| **Performance Test** | 1000+ apps | ✅ Yes              | `AppDataFactory.create(num_apps=10000)`                |

## 🔧 Updated Fixtures

### For Integration Tests (with validation)

python

```python
@pytest.fixture
def sample_apps_data():
    """120 apps - passes validation ✓"""
    # Implementation creates 120 apps
    ...

@pytest.fixture  
def sample_reviews_data():
    """60 reviews - safety margin ✓"""
    # Implementation creates 60 reviews
    ...
```

### For Unit Tests (without validation)

python

```python
@pytest.fixture
def small_apps_data():
    """4 apps - for unit tests only"""
    return pd.DataFrame({
        'App': ['App1', 'App2', 'App3', 'App1'],
        ...
    })
```

Or create inline:

python

```python
def test_something(transformer):
    df = pd.DataFrame({'Rating': [19.0, 4.5]})  # Minimal test data
    result = transformer.clean_rating_column(df)
    ...
```

## 🎯 Real Examples

### ✅ CORRECT: Integration Test

python

```python
def test_full_pipeline_integration(
    extractor,      # Uses temp CSV with 120+ apps
    transformer, 
    loader, 
    temp_csv_files  # Contains sample_apps_data (120 apps)
):
    # Extract - will run validation
    apps_df, reviews_df = extractor.extract_all()  # ✓ Passes (120 apps)
    
    # Transform
    apps_transformed = transformer.transform_apps_data(apps_df)
    
    # Load
    loader.load_apps_data(apps_transformed)
```

### ✅ CORRECT: Unit Test

python

```python
def test_clean_rating_column_decimal_error(transformer):
    """Unit test - no validation involved."""
    df = pd.DataFrame({'Rating': [19.0, 4.5, 3.8]})  # Only 3 rows OK
    
    result = transformer.clean_rating_column(df)
    
    assert result['Rating'].iloc[0] == 1.9  # 19.0 → 1.9
```

### ❌ WRONG: Integration Test with Small Data

python

```python
def test_full_pipeline(extractor, transformer, loader):
    # This would FAIL!
    df = pd.DataFrame({'App': ['App1', 'App2']})  # Only 2 apps
    
    # Save to CSV...
    # extractor.extract_all() → ValidationError: got 2 apps!
```

## 🏭 Factory Usage

### Default (for Integration Tests)

python

```python
def test_with_factory(app_factory, transformer):
    df = app_factory.create()  # Creates 120 apps by default
    result = transformer.transform_apps_data(df)
    # Passes validation ✓
```

### Explicit Small (for Unit Tests)

python

```python
def test_unit_with_factory(app_factory, transformer):
    df = app_factory.create(num_apps=5)  # Explicitly small
    result = transformer.clean_size_column(df)
    # No validation, so size doesn't matter ✓
```

## 📝 Best Practices

### 1. **Know Your Test Type**

python

```python
# Integration test → Use 100+ apps
def test_full_etl(sample_apps_data, ...):
    ...

# Unit test → Use any size
def test_clean_function(transformer):
    df = pd.DataFrame({...})  # Small is fine
    ...
```

### 2. **Document Data Size Requirements**

python

```python
@pytest.fixture
def sample_apps_data():
    """
    Fixture with 120 apps.
    
    NOTE: Must have 100+ apps to pass DataExtractor validation.
    For unit tests without validation, use small_apps_data instead.
    """
    ...
```

### 3. **Use Factories for Flexibility**

python

```python
# Good: Explicit about what you need
def test_something(app_factory):
    # Integration test - need 100+
    df = app_factory.create(num_apps=120)
    
    # Unit test - small is fine
    df_small = app_factory.create(num_apps=3)
```

## 🐛 Debugging Validation Failures

If you see:

```
ValueError: Insufficient data: got 50 apps, expected at least 100
```

**Fix options:**

1. **Increase fixture data:**

python

```python
   df = AppDataFactory.create(num_apps=120)  # Instead of default
```

2. **Skip validation for unit tests:**

python

```python
   # Don't call extractor.extract_all()
   # Call transformer functions directly
```

3. **Mock validation (advanced):**

python

```python
   @pytest.fixture
   def extractor_no_validation(temp_data_dir, monkeypatch):
       extractor = DataExtractor(data_dir=str(temp_data_dir))
       monkeypatch.setattr(extractor, 'validate_apps_extraction', lambda df: None)
       return extractor
```

## ✨ Summary

**The Rule:**

- **Integration tests** (E→T→L) → Use 100+ apps (sample_apps_data, factory defaults)
- **Unit tests** (individual functions) → Use any size (small_apps_data, explicit factory params)

**Why This Matters:**

- ✅ Tests match production behavior
- ✅ Catches real validation issues
- ✅ Prevents false positives
- ✅ Maintains data quality gates

All fixtures and factories have been updated to respect this requirement! 🎉