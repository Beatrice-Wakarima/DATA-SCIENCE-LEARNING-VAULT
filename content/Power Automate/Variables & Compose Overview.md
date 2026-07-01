

**Purpose:** Store values between steps.

- Flows alone can’t remember values.
    
- **Variables** and **Compose** provide memory and flexibility.
    
- Building blocks for advanced automation.
    

## 🗂 Why Store Values

**Purpose:** Three main reasons.

- **Reuse** → fetch once, reference everywhere (e.g., Project Name).
    
- **Update** → counters or accumulating strings.
    
- **Compare** → branch logic in Conditions or Switches.
    

## 🗂 Initialize Variable

**Purpose:** Declare variables before use.

- Two‑step pattern: Initialize → Update.
    
- Declare **name, type, starting value**.
    
- Types: String, Integer, Float, Boolean, Array, Object.
    
- Each variable needs its own Initialize action.
    
- Rule: Always initialize before use → otherwise flow fails.
    

## 🗂 Updating Variables

**Purpose:** Modify values.

- **Set Variable** → replaces entire value.
    
- **Append** → adds to string/array.
    
- **Increment/Decrement** → adjust numbers.
    
- Warning: Set inside a loop only keeps last item.
    

## 🗂 Example: Append vs Set

**Purpose:** Common mistake & fix.

- Dan at Vantara builds weekly report for Crestline Logistics.
    
- Loop with **Set** → overwrites each iteration → only last item survives.
    
- Fix: Use **Append** → builds onto existing value.
    
- Rule: Inside loops, always use Append.
    

## 🗂 Compose Action

**Purpose:** Store single values.

- Write once, set, never change.
    
- No type declaration → infers automatically.
    
- Can be placed anywhere (loops, branches).
    
- Best use: **expression debugger** → test outputs, then remove.
    

## 🗂 Variables vs Compose

**Purpose:** Comparison table.

|**Variables**|**Compose**|
|---|---|
|Updated as needed|Write‑once snapshot|
|Requires type declaration|Infers type automatically|
|Must initialize at top level|Can be used anywhere|
|Can cause locking in parallel|Lightweight in loops|
|Best for counters/accumulators|Best for debugging/snapshots|