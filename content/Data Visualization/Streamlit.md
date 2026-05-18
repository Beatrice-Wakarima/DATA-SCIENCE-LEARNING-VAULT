# Streamlit

## Table of Contents

- [[#Getting Started]]
- [[#Core Components]]
- [[#Layout and Containers]]
- [[#User Input Widgets]]
- [[#Data Display]]
- [[#Charts and Visualizations]]
- [[#Session State]]
- [[#Caching and Performance]]
- [[#Deployment]]
- [[#Advanced Features]]

## Getting Started

### Installation

bash

```bash
pip install streamlit
```

### Basic App Structure

python

```python
import streamlit as st

# App title
st.title("My Streamlit App")

# Simple text
st.write("Hello, World!")

# Run with: streamlit run app.py
```

> [!tip] Use `streamlit run app.py` to launch your app locally on port 8501.

### Page Configuration

python

```python
st.set_page_config(
    page_title="My App",
    page_icon="🚀",
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded"
)
```

## Core Components

### Text Elements

python

```python
# Headers
st.title("Main Title")
st.header("Header")
st.subheader("Subheader")

# Text formatting
st.text("Fixed-width text")
st.markdown("**Bold** and *italic* text")
st.write("Universal display function")
st.caption("Small caption text")
```

### Code Display

python

```python
# Code blocks
st.code("print('Hello')", language="python")

# Inline code
st.markdown("Use `st.write()` function")
```

## Layout and Containers

### Columns

python

```python
col1, col2, col3 = st.columns([2, 1, 1])  # Ratio-based widths

with col1:
    st.write("Wide column")

with col2:
    st.write("Narrow column")

# Alternative syntax
col1.metric("Sales", "1000", "10%")
```

### Containers

python

```python
# Container for grouping elements
container = st.container()
container.write("Content in container")

# Empty placeholder
placeholder = st.empty()
placeholder.text("This will be replaced")
```

### Sidebar

python

```python
# Sidebar elements
st.sidebar.title("Navigation")
st.sidebar.selectbox("Choose option", ["A", "B", "C"])

# Using with statement
with st.sidebar:
    st.write("Sidebar content")
```

### Expander

python

```python
with st.expander("Click to expand"):
    st.write("Hidden content revealed!")
```

## User Input Widgets

### Basic Inputs

python

```python
# Text input
name = st.text_input("Enter your name")
message = st.text_area("Enter message", height=100)

# Number inputs
age = st.number_input("Age", min_value=0, max_value=120, value=25)
price = st.slider("Price", 0.0, 100.0, 50.0, step=0.1)
```

### Selection Widgets

python

```python
# Single selection
option = st.selectbox("Choose option", ["Option 1", "Option 2"])
radio = st.radio("Pick one", ["A", "B", "C"])

# Multiple selection
multiselect = st.multiselect("Choose multiple", ["X", "Y", "Z"])
```

### Boolean and Dates

python

```python
# Checkbox
agree = st.checkbox("I agree to terms")

# Date/time inputs
date = st.date_input("Select date")
time = st.time_input("Select time")
```

### Buttons

python

```python
if st.button("Click me"):
    st.write("Button clicked!")

# Download button
st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="data.csv",
    mime="text/csv"
)
```

## Data Display

### DataFrames and Tables

python

```python
import pandas as pd

df = pd.DataFrame({
    'Column 1': [1, 2, 3],
    'Column 2': ['A', 'B', 'C']
})

# Interactive dataframe
st.dataframe(df)

# Static table
st.table(df)

# Data editor (editable dataframe)
edited_df = st.data_editor(df)
```

### Metrics

python

```python
st.metric(
    label="Sales", 
    value=1000, 
    delta=50,
    delta_color="normal"  # or "inverse"
)
```

### JSON and Dictionaries

python

```python
data = {"key": "value", "number": 42}
st.json(data)
```

## Charts and Visualizations

### Built-in Charts

python

```python
import numpy as np

# Line chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(chart_data)

# Bar chart
st.bar_chart(chart_data)

# Area chart
st.area_chart(chart_data)
```

### Plotly Integration

python

```python
import plotly.express as px

fig = px.scatter(df, x="x", y="y", color="category")
st.plotly_chart(fig, use_container_width=True)
```

### Maps

python

```python
# Simple map
map_data = pd.DataFrame({
    'lat': [37.76, 37.77],
    'lon': [-122.4, -122.41]
})
st.map(map_data)
```

## Session State

### Basic Usage

python

```python
# Initialize session state
if 'count' not in st.session_state:
    st.session_state.count = 0

# Update session state
if st.button("Increment"):
    st.session_state.count += 1

st.write(f"Count: {st.session_state.count}")
```

### Form Handling

python

```python
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age")
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state.user_data = {"name": name, "age": age}
```

> [!note] Session state persists data across reruns and user interactions.

## Caching and Performance

### Data Caching

python

```python
@st.cache_data
def load_data():
    # Expensive data loading operation
    return pd.read_csv("large_file.csv")

data = load_data()  # Cached result
```

### Resource Caching

python

```python
@st.cache_resource
def init_model():
    # Initialize ML model (resource-heavy)
    return load_model("model.pkl")

model = init_model()  # Cached resource
```

> [!warning] Use `st.cache_data` for data, `st.cache_resource` for global resources like ML models.

### Cache Control

python

```python
# Clear specific cache
load_data.clear()

# Clear all cache
st.cache_data.clear()
```

## Deployment

### Streamlit Cloud

python

```python
# Requirements.txt needed
# Push to GitHub, connect to Streamlit Cloud
# streamlit.io/cloud
```

### Docker Deployment

dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Configuration

toml

```toml
# .streamlit/config.toml
[server]
port = 8501
address = "0.0.0.0"

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
```

## Advanced Features

### File Upload

python

```python
uploaded_file = st.file_uploader("Choose file", type=['csv', 'xlsx'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
```

### Progress Indicators

python

```python
# Progress bar
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)

# Spinner
with st.spinner("Processing..."):
    time.sleep(3)
    st.success("Done!")
```

### Custom Components

python

```python
# HTML components
st.components.v1.html("""
<div style="background-color: lightblue; padding: 10px;">
    <h3>Custom HTML Component</h3>
</div>
""", height=100)
```

### Multipage Apps

python

```python
# pages/page1.py
import streamlit as st

st.title("Page 1")

# pages/page2.py  
import streamlit as st

st.title("Page 2")

# Main app automatically detects pages/ folder
```

### Error Handling

python

```python
try:
    result = risky_operation()
    st.success("Operation successful!")
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()  # Stop execution
```

> [!tip] Use `st.stop()` to halt execution and prevent cascading errors.

### Secrets Management

python

```python
# .streamlit/secrets.toml
# api_key = "your-secret-key"

api_key = st.secrets["api_key"]
```

---

**Related Notes:** [[Python]], [[Data Visualization]], [[Web Development]], [[Dashboard Design]], [[Plotly]], [[Pandas]]

#python #streamlit #dashboard #web-development #data-visualization #interactive #ui


