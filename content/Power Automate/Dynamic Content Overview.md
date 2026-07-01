

**Purpose:** Insert live values at runtime.

- Examples: today’s date, email sender, client name.
    
- Avoid hardcoding → flows stay flexible.
    

## 🗂 Tokens from Triggers & Actions

**Purpose:** Outputs available downstream.

- Each trigger/action produces tokens.
    
- Dynamic Content panel shows available tokens.
    
- One‑click insertion → no syntax needed.
    
- Example: “When a new email arrives” → tokens for sender, subject, body.
    

## 🗂 Opening the Panel

**Purpose:** Access dynamic content.

- **fx pill** beside field.
    
- **/** inline picker.
    
- **Lightning‑bolt icon**.
    
- **Gear icon → Use dynamic content**.
    
- All routes lead to same tabs: Dynamic content & Functions.
    

## 🗂 Expressions Overview

**Purpose:** Transform values.

- Expression Editor (fx button).
    
- Function names not case‑sensitive (e.g., `utcNow` vs `utcnow`).
    
- Always click **Add** to save expression.
    

## 🗂 Dynamic Content vs Expression

**Purpose:** Rule of thumb.

- **Dynamic Content** → raw values (e.g., sender email).
    
- **Expression** → format, combine, transform (e.g., lowercase string, format date).
    
- Often used together → token wrapped inside expression.
    

## 🗂 Function Categories

**Purpose:** Common expression functions.

- **String** → concat, toLower, trim.
    
- **Date & Time** → utcNow, formatDateTime.
    
- **Logical** → if, equals, greater.
    
- **Manipulation** → coalesce (fallback for empty values).
    

## 🗂 Example Flow: Client Welcome Email

**Purpose:** Dynamic + expression in practice.

- Manual trigger → inputs: Client Name, Client Company.
    
- Compose 1 → `toUpper(Client Name)` + concat “Dear”.
    
- Compose 2 → trim spaces, replace spaces with dash.
    
- Outputs dropped into welcome email as dynamic tokens.
    

## 🗂 Step‑by‑Step Expression Building

**Purpose:** Practical debugging habit.

- Build complex expressions piece by piece.
    
- Use Compose action for each function.
    
- Test outputs incrementally.
    
- Combine into final expression once each piece works.