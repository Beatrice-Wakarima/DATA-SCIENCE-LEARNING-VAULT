

**Purpose:** Capture demo steps for building interactive Power BI reports.

### 📌 Dataset Structure

- **Food Inspections** → Fact table with inspection date + score (0–100).
    
- **Restaurant Dimension** → HSIS ID key, restaurant details.
    
- **Violations** → Description, comments, points lost (severity-based).
    
- **Date Dimensions** → Links inspection, violation, and restaurant open dates.
    

### 📌 DAX Measures

- **Number of Inspections** → Count of inspection keys.
    
- **Number of Violations** → Count of violations.
    
- **Points Lost** → Sum of violation points.
    

### 📌 Overview Page

- Rename page → “Overview.”
    
- **Clustered Bar Chart** → Inspections by inspector.
    
- **Table Visual** → Inspection date, HSIS ID, restaurant name, violations.
    
- Formatting tweaks: remove Y-axis title, rename “Number of Violations” → “Violations.”
    

### 📌 Inspection Report Page

- Drill-through field: **inspection key** → auto back button.
    
- **Map Visual** → Restaurant location (lat/long).
    
- **Bar Chart** → Violation types (axis = code, values = count, tooltip = description).
    
- Drill-through setup: add filter column to table → right-click row → Drill through → Inspection Report.
    

### 📌 Scatter Chart (Overview Page)

- X-axis: Number of inspections.
    
- Y-axis: Average inspection score (format 90–101).
    
- Legend: Facility type.
    
- Size: Count of HSIS IDs.
    
- Play Axis: Year + quarter → dynamic time view.
    
- Insight: Public school lunchrooms score highest.
    

### 🔗 Connections

- Links to **Dashboards vs Reports** note.
    
- Connects to **Paginated Reports** for broader reporting context.
    
- Bridges into **Wake County Watchdog Data** for exercises.
    

### 🚀 Next Steps

- Expand visuals with slicers + filters.
    
- Add navigation buttons for multi-page flow.
    
- Refine interactivity for storytelling with Q&A visual.