

**Purpose:** Extend beyond built‑in tools.

- Custom tools = controlled, reusable logic.
    
- Bridge between agents and external resources.
    

## 🗂 Why Build Custom Tools?

**Advantages:**

- **Reliability** → test & validate logic.
    
- **Reusability** → use across projects.
    
- **Consistency** → predictable runs, easier debugging.
    
- **Controlled access** → limit agent scope to CSVs, APIs, DBs.
    
- Turn one‑off logic into reusable building blocks.
    

## 🗂 Retail Store Scenario

**Example:**

- Small retail store inventory in CSV.
    
- Agent doesn’t automatically access files.
    
- Wrap file‑reading logic in a custom tool → controlled access.
    

## 🗂 Anatomy of a Custom Tool

**Structure:**

- Use `@tool` decorator from smolagents.
    
- Define function (e.g., `check_inventory(product_name)`).
    
- Reads CSV, returns quantity in stock.
    
- Becomes callable by the agent.
    

## 🗂 Best Practices for Custom Tools

- Clear input parameters.
    
- Type hints for each parameter.
    
- Docstring explaining function purpose.
    
- Helps LLM understand usage correctly.
    

## 🗂 How the Agent Uses Your Tool

**Flow:**

1. Agent interprets query (“Do we have t‑shirts in stock?”).
    
2. Matches query to `check_inventory()`.
    
3. Executes with `"t-shirt"` as input.
    
4. Returns result → agent formulates response.
    

- Clear docstrings & type hints guide correct usage.
    

## 🗂 Registering a Custom Tool

**Setup:**

- Add tool to agent’s tools list.
    
- If tool uses external libraries (e.g., pandas), allow via `additional_authorized_imports`.
    
- If only built‑in Python → no need for extra imports.
    

## 🗂 Custom Tools in Production

**Beyond CSVs:**

- Connect to PostgreSQL databases.
    
- Access APIs.
    
- Integrate cloud storage.
    
- Same principles apply → tool bridges agent with external data.