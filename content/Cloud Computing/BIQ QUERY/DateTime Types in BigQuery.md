

### **Why Dates Matter**

- Filter long datasets efficiently.
    
- Extract parts of dates (day of week, month, etc.) for analysis.
    
- Partition data for faster queries (common strategy, not covered here).
    

### **DATE**

- Represents a single day (day, month, year).
    
- Example: `DATE '2010-05-19'` → BigQuery launch date.
    

### **TIMESTAMP**

- Absolute point in time.
    
- Contains both date and time.
    
- Defaults to UTC unless timezone specified.
    

### **DATETIME & TIME**

- **TIME** → time only, no date.
    
- **DATETIME** → date + time, but no timezone.
    
- Less frequently used compared to DATE and TIMESTAMP.
    

### **Date & Timestamp Parts**

- **DATE parts:** day, week, month, year.
    
- **TIMESTAMP parts:** hour, minute, second. 🔗 Reference: [Timestamp functions](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_trunc)
    

### **ADD, SUBTRACT, DIFF**

- Functions: `DATE_ADD`, `DATE_SUB`, `TIMESTAMP_ADD`, `TIMESTAMP_SUB`.
    
- Use `INTERVAL <integer> <date_part>` syntax.
    
- `DATE_DIFF` / `TIMESTAMP_DIFF` → difference between two dates/times.
    

### **EXTRACT**

- Extracts specific parts of a date/timestamp.
    
- Example: `EXTRACT(DAYOFWEEK FROM DATE '2010-05-19')` → returns 4 (Wednesday).
    

### **FORMAT**

- Converts dates/timestamps into human‑readable formats.
    
- Examples:
    
    - `FORMAT_DATE('%m/%d/%Y', DATE '2010-05-19')` → `05/19/2010`
        
    - `FORMAT_DATE('%A, %B %d, %Y', DATE '2010-05-19')` → `Wednesday, May 19, 2010` 🔗 Reference: [Format elements](https://cloud.google.com/bigquery/docs/reference/standard-sql/format-elements#format_elements_date_time)
        

### **Current Date/Timestamp**

- Functions: `CURRENT_DATE()`, `CURRENT_TIMESTAMP()`.
    
- Useful for calculating differences from “now.”
    

### **Cheat Sheet**

- **DATE** → day, month, year
    
- **TIMESTAMP** → absolute point in time (UTC default)
    
- **DATETIME** → date + time, no timezone
    
- **TIME** → time only
    
- Functions: ADD, SUB, DIFF, EXTRACT, FORMAT, CURRENT