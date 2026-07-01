

**Purpose:** Automate human decision‑making.

- Standard connector → included in Microsoft 365.
    
- No trigger → must follow another trigger.
    
- First use provisions Dataverse database for approval records.
    

## 🗂 Approval Actions

**Purpose:** Four ways to request decisions.

- **Create an approval** → builds request, continues flow.
    
- **Wait for an approval** → pauses until response.
    
- **Start and wait for an approval** → most common, combines both.
    
- **Start and wait for an approval of text** → adds Suggested Text field for approver edits.
    

## 🗂 Approval Type Configuration

**Purpose:** Control response rules.

- **Approve/Reject** → two choices.
    
    - _First to respond_ → first reply decides.
        
    - _Everyone must approve_ → unanimous approval required.
        
- **Custom Responses** → add options (Proceed, Revise, Cancel).
    
- **Sequential Approval** → request moves in defined order, one approver at a time.
    

## 🗂 Approver Response Channels

**Purpose:** Multiple ways to respond.

- Outlook (desktop/browser).
    
- Microsoft Teams adaptive card.
    
- Power Automate approval center (web).
    
- Power Automate mobile app.
    
- Responses sync everywhere → no duplicates or race conditions.
    

## 🗂 Approval Metadata

**Purpose:** Rich dynamic content after response.

- **Outcome token** → literal string (“Approve”, “Reject”, or custom).
    
- Date/time stamps → request sent, response received, approval completed.
    
- Comments → captured per approver.
    
- Branching → wire Outcome into Condition (case‑sensitive: “Approve” ≠ “approve”).