

**Purpose:** Different ways flows start.

- **Instant** → button click, on demand.
    
- **Scheduled** → runs on a clock.
    
- **Automated** → fires when an event happens.
    

## 🗂 Scheduled Flows

**Purpose:** Run on a clock.

- Uses **Recurrence trigger** automatically.
    
- Set **Frequency** (hour, day, week, month).
    
- Set **Interval** (e.g., every 1 day, every 3 hours).
    
- Critical step: set **time zone** (default UTC).
    
- Example: Weekly report every Monday at 9 AM New York time → set explicitly.
    

## 🗂 Recurrence Trigger Outputs

**Purpose:** Understand limitations.

- Recurrence produces **no outputs**.
    
- Dynamic Content panel after Recurrence = empty.
    
- Use **expressions** for date/time.
    
    - `utcNow()` → current timestamp.
        
    - `addDays(utcNow(), -1)` → yesterday’s date.
        
- Common pattern in scheduled flows.
    

## 🗂 Automated Triggers

**Purpose:** Event‑driven automation.

- Fire when something happens (new email, SharePoint item, form response).
    
- Produce **rich outputs** → subject, sender, attachments, list fields.
    
- Key difference: Recurrence = schedule/no data, Automated = event/full data.
    

## 🗂 Trigger Cheat Sheet

**Purpose:** Quick recap.

|**Trigger Type**|**Starts When**|**Outputs**|**Best Use**|
|---|---|---|---|
|**Instant**|Button click|User input|On‑demand tasks|
|**Scheduled**|Clock/time|None|Recurring reports, syncs|
|**Automated**|Event occurs|Rich data|Notifications, approvals|
