

**Purpose:** Get flows into your team’s hands.

- Three sharing modes: Co‑owner, Run‑only, Send a copy.
    
- Connections behave differently across each mode.
    
- Moving flows between environments requires Export Package or Solutions.
    

## 🗂 Sharing Modes

**Purpose:** Choose based on recipient needs.

- **Co‑owner** → full edit access, view run history, reuse connections.
    
- **Run‑only** → trigger flow without editing (instant flows only).
    
- **Send a copy** → independent duplicate, no connections, recipient owns copy.
    

## 🗂 Connections Across Modes

**Purpose:** Clarify behavior.

- Co‑owners reuse your connections but cannot modify credentials.
    
- Run‑only → choose at share time: reuse your connections or require theirs.
    
- Send a copy → structure only, no connections.
    
- Catch: if you leave org, shared connections break → fix = service account.
    

## 🗂 Moving Flows Between Environments

**Purpose:** Deployment tools.

- **Export Package** → quick zip file, re‑authenticate connectors on import.
    
- **Solutions** → proper ALM vehicle, bundles flows + connection references + environment variables.
    
- Best practice for production deployment.
    

## 🗂 Copilot as Draft Tool

**Purpose:** Use responsibly.

- Strengths: scaffolding flows quickly, suggesting connectors/actions, explaining flows in plain English.
    
- Limitations: may use deprecated actions, hardcode values, omit error handling, pick wrong connector.
    
- Treat output as **first draft**, not final product.
    

## 🗂 Copilot Audit Checklist

**Purpose:** Five‑point review before sharing.

- Trigger type correct?
    
- All connections authenticated?
    
- Required fields filled?
    
- Actions in logical order?
    
- Error handling present? (usually missing → add manually).
    

## 🗂 Responsible Flow Lifecycle

**Purpose:** Reliable automation cycle.

- Build → Audit → Test with realistic data → Deploy real trigger → Monitor run history.
    
- Every change = new build, audit, test.
    
- Flows can break when connectors update → continuous monitoring separates quick automation from reliable automation.