

**Purpose:** Capture techniques for making reports behave more like applications.

### 📌 Button States & Styles

- **Button States** → Default, Hover, Press, Disabled.
    
- Each state can control **appearance** (text, icons).
    
- Cannot alter **visual header** or **action**.
    

### 📌 Custom Tooltips

- **Custom Tooltips** → Power BI pages shown on hover.
    
- Types:
    
    - Context‑sensitive (filters based on hovered element).
        
    - Header help tooltip (report‑level info).
        
- Not interactive → keep simple, minimal complexity.
    

### 📌 Unicode Symbols & Emoji

- **Unicode & Emoji** supported.
    
- Compact way to convey meaning.
    
- Risk: may be unclear to new users.
    

### 📌 Conditional Formatting on Tables

- **Conditional Formatting** → Background/font colors, data bars, icons, URLs.
    
- Example:
    
    - Data bar → activity by date.
        
    - Filled box icon → percentiles for actual amount.
        

### 📌 Edit Interactions

- **Edit Interactions** → Control cross‑filtering between visuals.
    
- Example: treemap selection filters table rows.
    
- Disable → treemap selection doesn’t filter table.
    
- One‑way interactions: table → treemap still applies.
    

### 📌 Drill‑down Interactions

- Certain visuals (e.g., treemaps) → option to apply drill‑down filters to **page** or **visual only**.
    
- Use case: prevent totals cards from updating when users filter/slice.
    

### 📌 Filter vs Highlight

- **Filter vs Highlight** → Choice when interacting with area charts (treemaps, bar charts).
    
- Highlight → dims non‑selected areas.
    
- Filter → removes non‑selected areas.
    
- Depends on use case, neither is “right” or “wrong.”
    

### 🔗 Connections

- Links to **Bookmarks, Buttons & Navigation** for navigation context.
    
- Connects with **Increasing Report Interaction** for drillthrough + scatter chart interactivity.
    
- Bridges into **Dashboards vs Reports** for storytelling design.
    

### 🚀 Next Steps

- Practice creating **custom tooltips** in exercises.
    
- Experiment with **conditional formatting** for clarity.
    
- Use **edit interactions** to fine‑tune report behavior.
    
- Apply **Unicode/emoji** sparingly for compact storytelling.