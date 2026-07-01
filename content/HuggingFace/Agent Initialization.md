

**Purpose:** Set up the agent and load expense data.

python

```
# Initialize expense data
expense_data = {
    "groceries": [120, 95, 110, 140],
    "utilities": [85, 92, 78, 88],
    "entertainment": [45, 0, 75, 30],
    "transportation": [60, 55, 70, 65]
}

# Example: Initialize agent (conceptual)
agent = CodeAgent(expense_data)
```

## 🗂 Weekly Expense Analysis

**Step 1: Compute averages per category**

- Groceries → mean = (120+95+110+140)/4=116.25
    
- Utilities → mean = 85.75
    
- Entertainment → mean = 37.5
    
- Transportation → mean = 62.5
    

**Step 2: Identify variability**

- Groceries: relatively stable, moderate variance.
    
- Utilities: consistent, low variance.
    
- Entertainment: highly variable (0 → 75).
    
- Transportation: stable, mid‑range.
    

## 🗂 Spending Habits

- **Groceries**: largest recurring expense, predictable.
    
- **Utilities**: steady baseline, unavoidable.
    
- **Entertainment**: discretionary, fluctuates widely.
    
- **Transportation**: consistent, mid‑tier cost.
    

## 🗂 Budget Plan

**Suggested allocation (percent of total ~$302/week):**

- Groceries → 40% (~$120)
    
- Utilities → 28% (~$85)
    
- Transportation → 20% (~$60)
    
- Entertainment → 12% (~$37)
    

**Recommendations:**

- Cap entertainment at $40/week to smooth spikes.
    
- Build a 10% buffer fund for unexpected costs.
    
- Track groceries with variance indicators (KPI card style).
    
- Consider shifting savings from stable categories (utilities, transport) into discretionary buffer.