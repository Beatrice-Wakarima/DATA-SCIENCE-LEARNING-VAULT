

**Purpose:** Understand common data sources and connector options for Power Apps.

### 📂 SharePoint

- Lists act like tables; document libraries store files.
    
- Use simple column types (Text, Number, Yes/No, Date).
    
- Avoid mandatory columns; enforce requirements in-app.
    
- No relational support → create key fields manually.
    
- Delegation limit → queries may truncate results.
    

### 📂 Excel

- Must format data as a **table**.
    
- Image columns labeled with `[image]`.
    
- File locks if open by another user → not ideal for multi-user apps.
    
- Best for learning and small datasets; SharePoint more robust.
    

### 📂 Dataverse

- Native integration, no API config.
    
- Supports large datasets, relationships, and scaling.
    
- Enables **Copilot** for natural language app generation.
    
- Full access via Maker Portal → _Start with data_.
    

### 📂 SQL

- Premium connector.
    
- Cloud-hosted SQL → straightforward connection.
    
- On-premises SQL → requires **Data Gateway**.
    
- Supports relational data and enterprise-scale apps.
    

### 🔗 Connectors

- **Standard connectors** → included (SharePoint, OneDrive, Excel, Teams, Outlook, Azure Blob).
    
- **Premium connectors** → require license (Dataverse, SQL, Salesforce, SAP, ServiceNow, HTTP with Entra ID).
    
- **Custom connectors** → build for any REST API with OpenAPI definition.
    

### 🧭 Evaluation Factors

- **Data location** → Microsoft vs third-party.
    
- **Licensing** → standard vs premium.
    
- **Volume/performance** → delegation support.
    
- **Read vs write** → not all connectors allow updates.
    
- **Security/compliance** → data residency and access rules.
    

### ✅ Summary

- **SharePoint & Excel** → no extra cost, good for learning and small/medium volumes.
    
- **Dataverse & SQL** → premium, scalable, relational, advanced scenarios.
    
- **Connectors ecosystem** → hundreds of services, extensible with custom connectors.