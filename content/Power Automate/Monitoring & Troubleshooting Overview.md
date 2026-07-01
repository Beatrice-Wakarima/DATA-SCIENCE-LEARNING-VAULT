

**Purpose:** Three pillars of reliability.

- **Test before things break.**
    
- **Monitor while flows run.**
    
- **Troubleshoot when run history turns red.**
    

## 🗂 Flow Checker

**Purpose:** First line of defense.

- Runs automatically on each save.
    
- **Errors** → block save (missing fields, malformed expressions, unreferenced variables).
    
- **Warnings** → allow save but flag issues (e.g., action referencing unavailable data).
    
- Manual run → stethoscope icon in designer toolbar.
    

## 🗂 Test Modes

**Purpose:** Validate flows.

- Save first → Test won’t run unsaved changes.
    
- **Manual mode** → fire trigger yourself with inputs.
    
- **Automatic mode** → replay recent run (ideal after bug fix).
    
- Best habit: test after every step, not just at the end.
    

## 🗂 Run History Deep Dive

**Purpose:** Debugging tool.

- Status icons: Green = succeeded, Amber = running/waiting, Red = failed, Grey = skipped.
    
- Skipped ≠ failed → indicates branch not taken.
    
- Always start at **first red action** → root cause.
    
- Analytics tab → 30‑day rolling view of run counts and errors.
    

## 🗂 Inputs vs Outputs

**Purpose:** Pinpoint root cause.

- **Inputs** → what action received (data/config).
    
- **Outputs** → what action produced.
    
- Bad inputs → problem upstream.
    
- Bad outputs → problem in current action.
    

## 🗂 Configure Run After

**Purpose:** Error handling pattern.

- Default → action runs only if previous succeeded.
    
- Add parallel branch → Settings → Run after.
    
- Switch to “has failed” (or timed out/skipped).
    
- Red dotted arrow = visual cue.
    
- Handles both success and failure outcomes.
    

## 🗂 Resubmit & Compose

**Purpose:** Two troubleshooting levers.

- **Resubmit** → replay failed run with original payload. Quick debugging loop.
    
- **Compose** → drop between steps to inspect values.
    
    - Save, test, check output in run history.
        
    - Remove after confirming.
        
- Treat Compose as magnifying glass for debugging.