

**Purpose:** Handle lists of items.

- Examples: emails, SharePoint items, form responses.
    
- Loop through, filter, reshape, and combine results.
    

## 🗂 Apply to Each

**Purpose:** Process arrays.

- Runs actions once per item in list.
    
- Reference **Current item** for each iteration.
    
- Default: sequential runs.
    
- Concurrency control → parallel runs (faster, but risk of variable race conditions).
    

## 🗂 Current Item

**Purpose:** Value for specific iteration.

- First pass → item 1, second → item 2, etc.
    
- Access via Dynamic Content panel under Apply to Each.
    
- Mistake: referencing full array instead of Current item → returns whole list every time.
    

## 🗂 Filter Before Loop

**Purpose:** Reduce workload.

- Use **Filter Array** before Apply to Each.
    
- Example: 500 tickets/day → only 12 urgent tickets enter loop.
    
- Saves API calls and runtime cost.
    

## 🗂 Filter Array Action

**Purpose:** Narrow arrays.

- **From** → array to filter.
    
- **Filter Query** → condition row (like Condition action).
    
- Use `item()?['Status']` to read field.
    
- Output = **Body** (filtered array).
    

## 🗂 Body vs Body Item

**Purpose:** Correct output selection.

- **Body** → full filtered array (loop input).
    
- **Body Item** → single record (loop runs once, filtering lost).
    

## 🗂 Do Until

**Purpose:** Repeat until condition changes.

- Not for arrays → use Apply to Each for lists.
    
- Use for polling (wait for job finish) or retry (keep trying until success).
    
- Always set **count limit** → prevent infinite loops (default = 60 iterations).
    

## 🗂 Data Operations

**Purpose:** Transform arrays.

- **Select** → reshape items (extract needed fields).
    
- **Join** → combine items into single string (e.g., comma‑separated).
    
- **Create HTML table** → formatted table for email body.
    
- **Create CSV table** → CSV for Excel/exports.
    
- Common combo: **Select + Create HTML table** → clean, readable email report.