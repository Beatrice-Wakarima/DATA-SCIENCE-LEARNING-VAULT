

**Purpose:** Build your first **Canvas App** using an Excel table as a data source. 

### 🧩 Exercise Overview

Three parts:

1. **Generate a three-screen app** from Excel data.
    
2. **Create a blank canvas app** for future enhancement.
    
3. **Explore templates** to understand app patterns.
    

### 📂 Data Setup

- Download and extract **Machine-Order-Data.xlsx**.
    
- Upload to **OneDrive → + Add new → Files upload**.
    
- Confirm upload via search.
    
- If error _Request failed with status code 400_, delete the extra Power Apps ID column.
    

### 📱 Three-Screen App

- Go to **make.powerapps.com → Start with data → Excel Online (Business)**.
    
- Connect to OneDrive → select _Machines_ table → Create app.
    
- Power Apps auto-generates a mobile app with **Browse**, **Detail**, and **Edit** screens.
    
- Use **Power Fx formulas**:
    
    - `ThisItem.'Machine Name'` → Title
        
    - `ThisItem.Price` → Subtitle
        
    - `ThisItem.Color` → Body
        
    - `ThisItem.Photo` → Image
        
- Preview with ▶️ (Play) or F5.
    
- Save and name your app.
    

### 🧠 Canvas App from Scratch

- Create → _Start from blank_ → Tablet layout.
    
- Insert **Vertical Gallery** → Connect to OneDrive → _Machine-Order-Data.xlsx → Machines table_.
    
- Add **Edit Form** → Connect to _Machines_.
    
- Add fields: Photo, Machine ID, Machine Name, Price, Color, Description, etc.
    
- Set **Item property** to `Gallery1.Selected`.
    
- Replace text box with **Image control** → `ThisItem.Photo`.
    
- Fix formula errors by referencing `Image2.Y + Image2.Height` and `Image2.Image`.
    
- Add **Save button** → `SubmitForm(Form1)`.
    
- Add **Header rectangle + label** → “Contoso Coffee Machines”.
    

### 🧱 Template Apps

- Create → Scroll to _App templates_.
    
- Explore templates (Expense reports, Asset tracking, Employee onboarding).
    
- Select → _Use this template_ → Modify data source and controls.
    
- Templates are ideal for learning structure and patterns.
    

### 🧭 Preview and Save

- Preview with ▶️ or Alt-click.
    
- Save → Name your app → Exit.
    
- You now have a **single-screen canvas app** that reads and updates data dynamically.
    

### 🎨 Visual Flow

Here’s how your process looks end-to-end: **Data (Excel → OneDrive) → Maker Portal → Gallery → Form → Save Button → Header → Preview → Publish.**