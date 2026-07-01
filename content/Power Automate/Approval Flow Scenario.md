

**Purpose:** Real‑world workflow with human decision.

- Example: Expense approvals, leave requests, contract sign‑offs.
    
- Trigger: Expense request lands in SharePoint list.
    
- Flow wakes up → begins approval process.
    

## 🗂 Get Manager Action

**Purpose:** Identify approver.

- Finds manager from company directory.
    
- User UPN field accepts email from trigger.
    

## 🗂 Create vs Start Approval

**Purpose:** Important distinction.

- **Create an approval** → sets up request, continues flow immediately.
    
- Allows intermediate steps (e.g., Teams notification).
    
- **Start and wait for an approval** → pauses flow until response.
    

## 🗂 Teams Adaptive Card

**Purpose:** Notify approver interactively.

- Posts card in Teams channel.
    
- Approver can approve/reject without leaving Teams.
    
- Details field pulls dynamic data (employee name, amount, description).
    
- Item Link → direct access to SharePoint record.
    

## 🗂 Wait for an Approval

**Purpose:** Pause flow until response.

- Run history shows **Running** until approver responds.
    
- Response can take seconds, hours, or days.
    

## 🗂 Outcome Condition

**Purpose:** Branch flow based on decision.

- Condition checks **Outcome token**.
    
- Case‑sensitive → must equal “Approve” with capital A.
    
- Yes branch → Update item → Approval Status = Approved.
    
- No branch → Update item → Approval Status = Rejected.
    

## 🗂 Run History Example

**Purpose:** Verify execution.

- Adaptive card lands in Teams channel.
    
- Approver responds → flow resumes.
    
- Condition evaluates → SharePoint item updated.
    
- Expense request status shows Approved.