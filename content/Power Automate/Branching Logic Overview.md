

**Purpose:** Move beyond straight‑line flows.

- Use **Condition** and **Switch** to make decisions.
    
- Branch flows based on values, rules, or cases.
    

## 🗂 Finding Condition & Switch

**Purpose:** Where they live.

- Action picker → **Control** category.
    
- Insert via plus icon → search by name or browse Built‑in → Control.
    

## 🗂 Condition Action

**Purpose:** Two‑path branching.

- Evaluates a rule → sends flow down True or False branch.
    
- Example: If value = “Approved” → send approval email; else → send rejection.
    
- Branches labeled True/False (older designs: Yes/No).
    

## 🗂 Setting Up a Condition

**Purpose:** Define rule.

- Card has three slots: Left value, Operator, Right value.
    
- Left value → token or variable.
    
- Operator → equal to, not equal to, contains, greater than, less than, empty, not empty.
    
- Right value → comparison target.
    

## 🗂 Combining Rules

**Purpose:** Multiple checks.

- Add row → another rule.
    
- Toggle **AND/OR** between rows.
    
- Use **Add row group** for mixed logic (e.g., status Pending AND amount > 1000 OR flagged true).
    
- Cleaner than nesting Conditions.
    

## 🗂 Run History Indicators

**Purpose:** Interpret results.

- Green check → branch ran.
    
- Grey dash → branch skipped.
    
- Skipped ≠ failed → means Condition didn’t send flow down that path.
    

## 🗂 Common Mistakes

**Purpose:** Avoid pitfalls.

- Case sensitivity → “Approved” ≠ “approved”.
    
- Trailing spaces → invisible whitespace breaks match.
    
- Type mismatch → string “5” vs number 5.
    
- Fix: use **toLower** for case, **trim** for whitespace.
    

## 🗂 Switch Action

**Purpose:** Multi‑path branching.

- Matches one value against multiple cases.
    
- Example: Status Pending → notify team; In Transit → update tracker; Delivered → close ticket.
    
- **Default case** → safety net for typos/unexpected values.
    

## 🗂 Condition vs Switch

**Purpose:** When to use each.

|**Condition**|**Switch**|
|---|---|
|Two outcomes (True/False)|Three+ distinct values|
|Range checks (e.g., > 100)|Exact matches only|
|Nesting possible but messy|Cleaner for multiple outcomes|
|Best for binary decisions|Best for categorical branching|