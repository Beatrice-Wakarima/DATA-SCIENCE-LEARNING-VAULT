

**Purpose:** Bridges between Power Automate and services.

- Connectors link flows to apps like Outlook, SharePoint, Salesforce.
    
- Over 1,000 available → email, storage, databases, enterprise systems, social platforms.
    
- Add a step → search connector → pick trigger/action card.
    
- First use requires sign‑in; connection reused automatically.
    

## 🗂 Standard vs Premium

**Purpose:** Licensing tiers.

- **Standard connectors** → included in Microsoft 365 (Outlook, SharePoint, Teams, OneDrive, Forms).
    
- **Premium connectors** → require Power Automate Premium license (Salesforce, SAP, Dataverse, custom connectors).
    
- Premium connectors marked with **PREMIUM badge** in gallery.
    

## 🗂 Common Standard Connectors

**Purpose:** Everyday automation tools.

- **Outlook V2** → send, read, reply emails.
    
- **SharePoint** → lists, files, document libraries.
    
- **Microsoft Forms** → form & survey responses.
    
- **Office 365 Users** → profile info about tenant users.
    
- **Microsoft Teams** → messages, channel posts, notifications.
    

## 🗂 Triggers vs Actions

**Purpose:** Flow mechanics.

- **Trigger** → how a flow starts (exactly one per flow).
    
- **Actions** → what flow does after running (can chain many).
    
- Connectors usually offer both.
    

## 🗂 Same Connector, Two Roles

**Purpose:** Dual functionality.

- Example: Outlook connector.
    
    - Trigger → new email arrives.
        
    - Action → send an email.
        
- Same connector, different roles in different flows.
    

## 🗂 Adding Connector Actions

**Purpose:** Expand flow steps.

- Click **+** below any card → action picker.
    
- Search bar at top.
    
- Filter by tier.
    
- Expand long lists with **See more**.
    

## 🗂 Polling vs Push Triggers

**Purpose:** Event detection methods.

- **Polling triggers** → check service on schedule (slight delay).
    
    - Premium plans poll faster.
        
    - Catch up on missed events when restarted.
        
- **Push/Webhook triggers** → service notifies instantly.
    
    - Flow fires immediately.
        
    - Missed events lost if flow was off.
        

## 🗂 Best Practices

**Purpose:** Build reliable flows.

- Rename every action → clear labels (e.g., “Send approval email”).
    
- Set time zone on Recurrence triggers → avoid UTC bugs.
    
- Test after every new action → easier debugging than fixing multi‑step flows later.