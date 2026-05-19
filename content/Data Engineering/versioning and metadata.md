# 📓 Versioning & Metadata

## 🔹 Project Info

- **Project Name:** `{{PROJECT_NAME}}`
    
- **Author:** `{{AUTHOR}}`
    
- **Version:** `v{{VERSION_NUMBER}}`
    
- **Last Updated:** `{{DATE}}`
    

---

## 🔹 Config Metadata (`config.py`)

`# config.py  __version__ = "{{VERSION_NUMBER}}" __author__ = "{{AUTHOR}}" __last_updated__ = "{{DATE}}"  import os  RAW_DATA = os.getenv("RAW_DATA", "data/raw/{{RAW_FILE}}") CLEANED_DATA = os.getenv(     "CLEANED_DATA",     f"data/cleaned/{{OUTPUT_NAME}}_v{__version__}_{__last_updated__}.csv" ) LOG_FILE = f"data/logs/pipeline_{__version__}_{__last_updated__}.log"`

---

## 🔹 Output Naming Convention

- **Cleaned Data:**
    
    `{{OUTPUT_NAME}}_v{{VERSION_NUMBER}}_{{DATE}}.csv`
    
- **Reports:**
    
    `report_v{{VERSION_NUMBER}}_{{DATE}}.pdf`
    
- **Logs:**
    
    `pipeline_v{{VERSION_NUMBER}}_{{DATE}}.log`
    

---

## 🔹 Log Metadata Header

`[Pipeline Run ID: {{RUN_ID}}] Version: {{VERSION_NUMBER}} Author: {{AUTHOR}} Started: {{TIMESTAMP}} -----------------------------------`

---

## 🔹 Version History Log

|Version|Date|Author|Changes Made|
|---|---|---|---|
|v1.0|2025-09-10|Data Queen|Initial pipeline setup|
|v1.1|2025-09-14|Data Queen|Added cleaning for missing values|
|v1.2|2025-09-16|Data Queen|Introduced metadata + versioned output|
