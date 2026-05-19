#!/bin/bash

cd ~/quartz/content

# 1. Data Engineering MOC
cat > "Data Engineering MOC.md" << 'EOF'
---
title: Data Engineering MOC
---

# ⚙️ Data Engineering MOC

> Notes on building and managing data pipelines and infrastructure.

## Core Concepts
- [[Data Engineering/Extracting data|Extracting Data]]
- [[Data Engineering/Downloading data with curl and wget|Downloading Data]]
- [[Data Engineering/Secure Database Connections|Secure Database Connections]]
- [[Data Engineering/Dbt|DBT]]

## Related MOCs
- [[SQL MOC]]
- [[DBT MOC]]
- [[Kafka MOC]]
- [[Snowflake MOC]]
- [[Databricks MOC]]
- [[Kubernetes MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 2. Python MOC
cat > "Python MOC.md" << 'EOF'
---
title: Python MOC
---

# 🐍 Python MOC

> Notes on Python programming for data science and automation.

## Core Concepts
- [[Python/Basics|Python Basics]]
- [[Python/Functions|Functions]]
- [[Python/Automation|Automation]]

## Related MOCs
- [[Machine Learning MOC]]
- [[Data Engineering MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 3. Excel MOC
cat > "Excel MOC.md" << 'EOF'
---
title: Excel MOC
---

# 📊 Excel MOC

> Notes on Excel for data analysis and reporting.

## Core Concepts
- Formulas & Functions
- Pivot Tables
- Data Cleaning
- Charts & Visualizations

## Related MOCs
- [[Spreadsheets MOC]]
- [[Power BI MOC]]
- [[Business Intelligence MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 4. Power BI MOC
cat > "Power BI MOC.md" << 'EOF'
---
title: Power BI MOC
---

# 📈 Power BI MOC

> Everything on building dashboards and reports in Power BI.

## Getting Started
- [[Power Bi/Power BI Tutorial for Beginners|Beginners Tutorial]]
- [[Power Bi/Power BI Tutorial|Power BI Tutorial]]
- [[Power Bi/Cheat sheet|Cheat Sheet]]

## DAX
- [[Power Bi/Power BI DAX Tutorial for Beginners|DAX for Beginners]]
- [[Power Bi/Power BI Calculate Tutorial|CALCULATE]]
- [[Power Bi/DAX SUMMARIZE(),A Guide to Grouping and Summarizing Data|SUMMARIZE]]
- [[Power Bi/Mastering COUNTIF() in Power BI, A DAX-Based Approach|COUNTIF in DAX]]
- [[Power Bi/Mastering SWITCH in DAX for Power BI, A Comprehensive Guide|SWITCH]]
- [[Power Bi/A Comprehensive Guide to DAX LOOKUPVALUE|LOOKUPVALUE]]
- [[Power Bi/How to Use the SUMX Power BI Functions|SUMX]]
- [[Power Bi/Power BI RELATED DAX Function, Introduction and Use Cases|RELATED]]

## Visuals
- [[Power Bi/Introduction to Power BI Visuals,A Beginner's Guide|Intro to Visuals]]
- [[Power Bi/Crafting Effective Visuals|Crafting Effective Visuals]]
- [[Power Bi/Visualizations cheat sheet|Visualizations Cheat Sheet]]
- [[Power Bi/How to Create a Power BI Heatmap|Heatmap]]
- [[Power Bi/How to Create a Power BI Waterfall Chart, 5 Easy Steps|Waterfall Chart]]
- [[Power Bi/Power BI Gantt Chart,A Complete How-To|Gantt Chart]]
- [[Power Bi/Top 9 Power BI Dashboard Examples|Dashboard Examples]]

## Reports & Dashboards
- [[Power Bi/Power BI Dashboard Tutorial|Dashboard Tutorial]]
- [[Power Bi/Power BI Dashboards vs Reports,A Comprehensive Guide|Dashboards vs Reports]]
- [[Power Bi/Designing Engaging Power BI Reports Tutorial|Designing Reports]]
- [[Power Bi/Dashboard Checklist|Dashboard Checklist]]
- [[Power Bi/Power BI Report Builder, A Guide For Beginners|Report Builder]]
- [[Power Bi/Creating Paginated Reports in Power BI, A Step-by-Step Guide|Paginated Reports]]

## Data Modeling
- [[Power Bi/Data Modeling in Power BI Tutorial|Data Modeling]]
- [[Power Bi/How to Create Date Tables in Power BI Tutorial|Date Tables]]
- [[Power Bi/Power BI Hierarchies, A Comprehensive Guide|Hierarchies]]
- [[Power Bi/Power BI Matrix, A Comprehensive Guide|Matrix]]
- [[Power Bi/Power BI Merge Tables,A Complete Guide with Examples|Merge Tables]]
- [[Power Bi/Creating and Customizing Pivot Tables in Power BI|Pivot Tables]]

## Advanced
- [[Power Bi/Advanced Analytical Features in Power BI Tutorial|Advanced Analytics]]
- [[Power Bi/Mastering Predictive Analytics with Power BI, A Comprehensive Guide for Data Practitioners|Predictive Analytics]]
- [[Power Bi/Running Python Scripts in Power BI Tutorial|Python in Power BI]]
- [[Power Bi/SQL with Power BI|SQL with Power BI]]
- [[Power Bi/Power BI API, A Comprehensive Guide for Developers and Data Professionals|Power BI API]]
- [[Power Bi/Power BI Row-Level Security (RLS),A Comprehensive Tutorial|Row-Level Security]]
- [[Power Bi/How to Use Power BI Copilot in Microsoft Fabric|Copilot in Fabric]]

## Related MOCs
- [[Business Intelligence MOC]]
- [[SQL MOC]]
- [[Excel MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 5. Docker MOC
cat > "Docker MOC.md" << 'EOF'
---
title: Docker MOC
---

# 🐳 Docker MOC

> Notes on containerization with Docker.

## Core Concepts
- [[Docker/docker|Docker Overview]]
- [[Docker/Docker Cheat sheet|Cheat Sheet]]
- [[Docker/Why Docker|Why Docker]]
- [[Docker/Learning Docker]]
- [[Docker/blog|Blog Notes]]

## Docker for Postgres
- [[Docker for postgres/backup strategy|Backup Strategy]]
- [[Docker for postgres/best practices|Best Practices]]
- [[Docker for postgres/Security hardening|Security Hardening]]
- [[Docker for postgres/Why Docker|Why Docker for Postgres]]

## Interview Prep
- [[Docker/Docker Interview checklist|Interview Checklist]]
- [[Docker/Docker Q and A|Q & A]]

## Related MOCs
- [[Kubernetes MOC]]
- [[Postgres MOC]]
- [[Data Engineering MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 6. Git MOC
cat > "Git MOC.md" << 'EOF'
---
title: Git MOC
---

# 🌿 Git MOC

> Notes on version control with Git and GitHub.

## Core Concepts
- Git Basics
- Branching & Merging
- Remote Repositories
- GitHub Workflows

## Commands Reference
- Clone, Add, Commit, Push, Pull
- Branching: branch, checkout, merge
- History: log, diff, status

## Related MOCs
- [[Data Engineering MOC]]
- [[Projects MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 7. Business Intelligence MOC
cat > "Business Intelligence MOC.md" << 'EOF'
---
title: Business Intelligence MOC
---

# 📉 Business Intelligence MOC

> Notes on BI tools, strategy, and reporting.

## Core Concepts
- Data Warehousing
- Dashboards & Reporting
- KPIs & Metrics
- Data Storytelling

## Tools
- [[Power BI MOC]]
- [[Excel MOC]]
- [[Spreadsheets MOC]]
- [[SQL MOC]]
- [[Snowflake MOC]]

## Related MOCs
- [[Data Engineering MOC]]
- [[Databricks MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 8. Artificial Intelligence MOC
cat > "Artificial Intelligence MOC.md" << 'EOF'
---
title: Artificial Intelligence MOC
---

# 🤖 Artificial Intelligence MOC

> Notes on AI concepts, tools, and applications.

## Core Concepts
- Machine Learning
- Deep Learning
- Natural Language Processing
- Computer Vision

## Related MOCs
- [[Machine Learning MOC]]
- [[Python MOC]]
- [[Databricks MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 9. R MOC
cat > "R MOC.md" << 'EOF'
---
title: R MOC
---

# 📐 R MOC

> Notes on R programming for statistics and data analysis.

## Core Concepts
- R Basics
- Data Wrangling with tidyverse
- ggplot2 Visualization
- Statistical Analysis

## Related MOCs
- [[Python MOC]]
- [[Machine Learning MOC]]
- [[Business Intelligence MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 10. Spreadsheets MOC
cat > "Spreadsheets MOC.md" << 'EOF'
---
title: Spreadsheets MOC
---

# 🗂️ Spreadsheets MOC

> Notes on spreadsheet tools for data analysis.

## Core Concepts
- Formulas & Functions
- Data Validation
- Pivot Tables
- Charts

## Tools
- [[Excel MOC]]
- Google Sheets

## Related MOCs
- [[Business Intelligence MOC]]
- [[Power BI MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 11. Snowflake MOC
cat > "Snowflake MOC.md" << 'EOF'
---
title: Snowflake MOC
---

# ❄️ Snowflake MOC

> Notes on the Snowflake cloud data warehouse.

## Core Concepts
- Architecture
- Virtual Warehouses
- Data Sharing
- Time Travel

## SQL in Snowflake
- [[SQL MOC]]

## Related MOCs
- [[Data Engineering MOC]]
- [[DBT MOC]]
- [[Business Intelligence MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 12. Postgres MOC
cat > "Postgres MOC.md" << 'EOF'
---
title: Postgres MOC
---

# 🐘 Postgres MOC

> Notes on PostgreSQL database management.

## Core Concepts
- [[Docker for postgres/Security hardening|Security Hardening]]
- [[Docker for postgres/backup strategy|Backup Strategy]]
- [[Docker for postgres/best practices|Best Practices]]
- [[Data Engineering/Secure Database Connections|Secure Connections]]

## Related MOCs
- [[SQL MOC]]
- [[Docker MOC]]
- [[Data Engineering MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 13. DBT MOC
cat > "DBT MOC.md" << 'EOF'
---
title: DBT MOC
---

# 🔧 DBT MOC

> Notes on dbt (data build tool) for data transformation.

## Core Concepts
- [[Data Engineering/Dbt|DBT Notes]]
- Models & Sources
- Tests & Documentation
- dbt Cloud vs CLI

## Related MOCs
- [[Data Engineering MOC]]
- [[SQL MOC]]
- [[Snowflake MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 14. Kafka MOC
cat > "Kafka MOC.md" << 'EOF'
---
title: Kafka MOC
---

# 📨 Kafka MOC

> Notes on Apache Kafka for real-time data streaming.

## Core Concepts
- Topics & Partitions
- Producers & Consumers
- Kafka Connect
- Stream Processing

## Related MOCs
- [[Data Engineering MOC]]
- [[Kubernetes MOC]]
- [[Databricks MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 15. Kubernetes MOC
cat > "Kubernetes MOC.md" << 'EOF'
---
title: Kubernetes MOC
---

# ☸️ Kubernetes MOC

> Notes on container orchestration with Kubernetes.

## Core Concepts
- Pods & Nodes
- Deployments & Services
- ConfigMaps & Secrets
- Helm Charts

## Related MOCs
- [[Docker MOC]]
- [[Data Engineering MOC]]
- [[Kafka MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 16. Databricks MOC
cat > "Databricks MOC.md" << 'EOF'
---
title: Databricks MOC
---

# 🧱 Databricks MOC

> Notes on Databricks for big data and ML workloads.

## Core Concepts
- Delta Lake
- Spark & PySpark
- Notebooks
- MLflow

## Related MOCs
- [[Data Engineering MOC]]
- [[Machine Learning MOC]]
- [[Snowflake MOC]]
- [[Python MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 17. Projects MOC
cat > "Projects MOC.md" << 'EOF'
---
title: Projects MOC
---

# 🚀 Projects MOC

> My data science projects and case studies.

## Projects
- [[Projects/Bank marketing pipeline|Bank Marketing Pipeline]]
- [[Projects/Google Trends Analysis|Google Trends Analysis]]
- [[Projects/Loan Prediction|Loan Prediction]]
- [[Projects/Pig Farm IoT|Pig Farm IoT]]

## Related MOCs
- [[Machine Learning MOC]]
- [[Data Engineering MOC]]
- [[Python MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 18. SQL MOC
cat > "SQL MOC.md" << 'EOF'
---
title: SQL MOC
---

# 🗄️ SQL MOC

> Notes on SQL for querying and managing databases.

## Core Concepts
- SELECT, WHERE, GROUP BY, JOIN
- Window Functions
- CTEs & Subqueries
- Indexes & Performance

## Databases
- [[Postgres MOC]]
- [[Snowflake MOC]]

## Related MOCs
- [[Data Engineering MOC]]
- [[DBT MOC]]
- [[Power BI MOC]]

## Back
- [[index|🏠 Home]]
EOF

# 19. Machine Learning MOC
cat > "Machine Learning MOC.md" << 'EOF'
---
title: Machine Learning MOC
---

# 🧠 Machine Learning MOC

> Notes on machine learning concepts and tools.

## Concepts
- [[Machine Learning/Supervised|Supervised Learning]]
- [[Machine Learning/Unsupervised|Unsupervised Learning]]
- [[Machine Learning/Model Evaluation|Model Evaluation]]

## Tools
- [[Machine Learning/Supervised learning with scikit learn|Scikit Learn]]
- [[Machine Learning/machine learning cheat sheet|ML Cheat Sheet]]

## Related MOCs
- [[Python MOC]]
- [[Artificial Intelligence MOC]]
- [[Databricks MOC]]

## Back
- [[index|🏠 Home]]
EOF

echo "✅ All 19 MOCs created successfully!"
