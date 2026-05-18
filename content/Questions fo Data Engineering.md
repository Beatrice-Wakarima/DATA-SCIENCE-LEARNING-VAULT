## 81 Platform and Pipeline Design Questions[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#81-platform-and-pipeline-design-questions "Direct link to heading")

Many people ask: "How do you select the platform, tools and design the pipelines?" The options seem infinite. Technology however should never dictate the decisions.

Here are 81 questions that you should answer when starting a project

### Data Source Questions[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#data-source-questions "Direct link to heading")

#### Data Origin and Structure[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#data-origin-and-structure "Direct link to heading")

- **What is the source?** Understand the "device."
- **What is the format of the incoming data?** (e.g., JSON, CSV, Avro, Parquet)
- **What’s the schema?**
- **Is the data structured, semi-structured, or unstructured?**
- **What is the data type?** Understand the content of the data.
- **Is the schema well-defined, or is it dynamic?**
- **How are changes in the data structure from the source (schema evolution) handled?**

#### Data Volume & Velocity[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#data-volume--velocity "Direct link to heading")

- **How much data is transmitted per transmission?**
- **How fast is the data coming in?** (e.g., messages per minute)
- **What is the maximum data volume expected per source per day?**
- **What scaling of sources/data is expected?**
- **Are there peaks for incoming data?**
- **How much data is posted per day across all sources?**
- **How does the data volume fluctuate?** (e.g., seasonal peaks, hourly/daily variations)
- **How will the system handle bursts of data?** (e.g., throttling or buffering)

#### Source Reliability & Redundancy[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#source-reliability--redundancy "Direct link to heading")

- **Is there data arriving late?**
- **Is there a risk of duplicate data from the source?** How will we handle de-duplication?
- **How reliable are the sources?** What’s the expected failure rate?
- **How do we handle data corruption or loss during transmission?**
- **What happens if a source goes offline?** Is there a fallback or failover source?
- **Do we need to retry failed transmissions or have fault-tolerance mechanisms in place?**

#### Data Extraction & New Sources[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#data-extraction--new-sources "Direct link to heading")

- **Do we need to extract the data from the sources?**
- **How many sources are there?**
- **Will new sources be implemented?**

#### Data Source Connectivity & Authentication[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#data-source-connectivity--authentication "Direct link to heading")

- **How is the data arriving?** (API, bucket, etc.)
- **How is the authentication done?**
- **What kind of connection is required for the data source?** (e.g., streaming, batch, API)
- **What protocols are used for data ingestion?** (e.g., REST, WebSocket, FTP)
- **Are there any rate limits or quotas imposed by the data source?**
- **How do we handle credentials?** Is there an API?
- **What is the retry strategy if data fails to be processed or transmitted?**

#### Data Security & Compliance[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#data-security--compliance "Direct link to heading")

- **Does the data need to be encrypted at the source before being transmitted?**
- **Are there any compliance frameworks (e.g., GDPR, HIPAA) that the source data must adhere to?**
- **Is there a requirement for data masking or obfuscation at the source?**

#### Metadata & Audit[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#metadata--audit "Direct link to heading")

- **Is there metadata for the client transmission stored somewhere?**
- **What metadata should be captured for each transmission?** (e.g., record counts, latency)
- **How do we track and log data ingestion events for audit purposes?**
- **Is there a need for tracking data lineage?** (i.e., source origin and changes over time)

---

### Goals and Destination Questions[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#goals-and-destination-questions "Direct link to heading")

#### Use Case & Data Consumption[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#use-case--data-consumption "Direct link to heading")

- **What kind of use case is this?** (Analytics, BI, ML, Transactional processing, Visualization, User Interfaces, APIs)
- **What are the typical use cases that require this data?** (e.g., predictive analytics, operational dashboards)
- **What are the downstream systems or platforms that will consume this data?**
- **How critical is real-time data versus historical data in this use case?**

#### Data Query & Delivery[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#data-query--delivery "Direct link to heading")

- **How is the data visualized?** (raw data, aggregated data)
- **How much raw data is processed at once?**
- **How much data is cold data, and how often is cold data queried?**
- **How fast do the results need to appear?**
- **How much data is going to be queried at once?**
- **How fresh does the data need to be?**
- **How often is the data queried?** (frequency)
- **What are the SLAs for delivering data to downstream systems or applications?**

#### Aggregation & Modeling[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#aggregation--modeling "Direct link to heading")

- **How is the data aggregated?** (by devices, topic, time)
- **When does the aggregation happen?** (on query, on schedule, while streaming)
- **What kind of data models are needed for this use case?** (e.g., star schema, snowflake schema)
- **Is there a need for pre-aggregations to speed up queries?**
- **Should partitioning or indexing strategies be implemented to optimize query performance?**

#### Performance & Availability[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#performance--availability "Direct link to heading")

- **What is the processing time requirement?**
- **What is the availability of analytics output?** (input vs output delay)
- **How fresh does the data need to be?**
- **What are the performance expectations for query speed?**
- **What is the acceptable query response time for end-users?**
- **How will the system handle an increase in concurrent queries from multiple users?**
- **What is the expected lag between data ingestion and availability for querying?**
- **Do we need horizontal scaling for query engines or databases?**

#### Data Lifecycle & Retention[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#data-lifecycle--retention "Direct link to heading")

- **What’s the data retention time?**
- **How often is data archived or moved to lower-cost storage?**
- **Will old data need to be transformed or reprocessed for new use cases?**
- **What are the data retention policies?** (e.g., hot vs cold storage)
- **How will the use case evolve as the data grows?** Will this affect how data is consumed or visualized?

#### Monitoring & Debugging[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#monitoring--debugging "Direct link to heading")

- **How will data delivery to the destination be monitored?** (e.g., time-to-load, query failures)
- **How will we monitor data pipeline health at the destination?** (e.g., throughput, latency)
- **What tools or methods will be used for debugging data delivery failures or performance bottlenecks?**
- **What metrics should be tracked to ensure data pipeline health?** (e.g., latency, throughput)
- **How do we handle issues such as data corruption or incomplete data at the destination?**

#### Data Access & Permissions[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#data-access--permissions "Direct link to heading")

- **Who is working with the platform, and who has access to query or visualize the data?**
- **Which tools are used to query the data?**
- **What kind of data export capabilities are required?** (e.g., CSV, API, direct database access)
- **Is role-based access control (RBAC) needed to segment data views for different users?**
- **How will access to sensitive data be managed?** (e.g., row-level security, encryption)

#### Scaling & Future Requirements[#](https://cookbook.learndataengineering.com/docs/03-AdvancedSkills#scaling--future-requirements "Direct link to heading")

- **What are the scalability requirements for the data platform as data volume grows?**
- **How will future business goals or scalability needs affect the design of data aggregation and retention strategies?**
- **How will the system handle an increasing load as more users query data or as data volume grows?**