

**Purpose:** Use Copilot to generate a **Canvas App** from either a conversation or an Excel file

### 🧩 Two Paths

- **Upload file** → Import Excel → Copilot converts into a Dataverse table → generates app.
    
- **Describe data** → Plain language description → Copilot builds Dataverse table + app.
    
- Both require a **Dataverse-enabled environment**.
    

### 📂 Conversation Path

- Maker Portal → _Start with data_ → _Create new data_.
    
- Example: _“Track product inventory with fields for product name, product type, color, and notes.”_
    
- Copilot generates table → refine with natural language (e.g., _“Add Choice column Product Line with Standard, Pro, Enterprise”_).
    
- Save → Open app in Studio.
    

### 📂 Upload File Path

- Download **ProductList.xlsx** → Upload via Maker Portal.
    
- Copilot creates **Product Inventory table**.
    
- Review column names/types:
    
    - Title, Code → Text
        
    - Product Line, Product Type, Color → Choice
        
    - Notes → Text
        
- Adjust via Copilot pane or Edit column.
    
- Save → Open app in Studio.
    

### 🧭 Evaluate Field Suggestions

- **Name** → meaningful, user-friendly.
    
- **Data type** → Choice for categories, Number/Currency for calculations, Date for time fields.
    
- **Required vs optional** → enforce validation in app, not Dataverse.
    

### 📱 Generated App

- Gallery (left) + Form (right).
    
- Search functionality → robust across text fields.
    
- Edit form → update records (e.g., _“Headphones 2000w → includes case”_).
    
- Responsive → preview across tablet/phone orientations.
    
- Save → Publish → Test in Preview mode.
    

### ✅ Summary

- Copilot accelerates app creation: **conversation** or **Excel upload**.
    
- Always review field names/types before saving.
    
- Result: fully functional app with gallery, form, search, and responsive design.