# AWS, Azure and GCP Service Comparison for Data Science & AI

This cheat sheet provides a comparison of the main services needed for data and AI-related work, from data engineering to data analysis and data science, to creating data applications.

Jun 19, 2023 · 17 min read

Contents

- [Storage](https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai#storage-%3Ctab)

- [Database](https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai#database-%3Ctab)

- [Compute](https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai#compute-%3Ctab)

- [Analytics](https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai#analytics-%3Ctab)

- [ML & AI](https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai#ml-&-ai-%3Ctab)

- [Networking & ​​Content Delivery](https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai#networking-&-%E2%80%8B%E2%80%8Bcontent-delivery-%3Ctab)

- [Containers](https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai#containers-%3Ctab)

- [Management & Security, Identity](https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai#management-&-security,-identity-%3Ctab)

## Training more people?

Get your team access to the full DataCamp for business platform.

For a bespoke solution [book a demo](https://www.datacamp.com/business/demo-2).

![](https://images.datacamp.com/image/upload/v1687256547/Infographic_AWS_Azure_and_GCP_Service_Comparison_for_Data_Science_and_AI_a899345e38.png)

Have this cheat sheet at your fingertips

Cloud computing eliminates the capital expenditure of building and maintaining data centers, enabling businesses to access and pay for only the resources they use. Its scalable nature allows for quick adjustment to changing business needs. Mirroring data simplifies data recovery and business continuity. By providing access to resources from anywhere, cloud computing also supports remote work and collaboration.

The big three [public clouds](https://www.datacamp.com/blog/public-private-cloud-difference) - Amazon Web Services, Microsoft Azure, and [Google Cloud Platform](https://www.datacamp.com/blog/what-is-gcp) - have hundreds of services, and it can be hard to determine what you need for any given project.

This cheat sheet provides a comparison of the main services needed for data and AI-related work, from data engineering to data analysis and data science, to creating data applications.

## Storage

|   |   |   |   |   |
|---|---|---|---|---|
|Service type|Description|AWS|Azure|GCP|
|Object storage|For storing any files you regularly use|[Simple Storage Service (S3)](https://aws.amazon.com/s3/)|[Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/)|[Cloud Storage Buckets](https://cloud.google.com/storage/docs/buckets)|
|Archive storage|Low cost (but slower) storage for rarely used files|[S3 Glacier Instant, Glacier Flexible, Glacier Deep Archive tiers](https://aws.amazon.com/s3/storage-classes/glacier/)|[Blob Cool/Cold/Archive tiers](https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview)|[Cloud Storage Nearline, Coldline, Archive tiers](https://cloud.google.com/storage/docs/storage-classes)|
|File storage|For storing files needing hierarchical organization|[Elastic File System (EFS)](https://aws.amazon.com/efs/), [FSx](https://aws.amazon.com/fsx/)|[Avers vFXT](https://azure.microsoft.com/en-us/products/storage/avere-vfxt/), [Files](https://azure.microsoft.com/en-us/products/storage/files/)|[Filestore](https://cloud.google.com/filestore/)|
|Block storage|For storing groups of related files|[Elastic Block Storage](https://aws.amazon.com/ebs/)|[Disk Storage](https://azure.microsoft.com/en-us/products/storage/disks/)|[Persistent Disk](https://cloud.google.com/persistent-disk/)|
|Hybrid storage|Move files between on-prem & cloud|[Storage Gateway](https://aws.amazon.com/storagegateway/)|[StorSimple](https://learn.microsoft.com/en-us/azure/storsimple/), [Migrate](https://azure.microsoft.com/en-us/products/azure-migrate/)|[Storage Transfer Service](https://cloud.google.com/storage-transfer-service)|
|Edge/offline storage|Move offline data to the cloud|[Snowball](https://aws.amazon.com/snowball/)|[Data Box](https://azure.microsoft.com/en-us/products/databox/)|[Transfer Appliance](https://cloud.google.com/transfer-appliance)|
|Backup|Prevent data loss|[Backup](https://aws.amazon.com/backup/)|[Backup](https://azure.microsoft.com/en-us/products/backup/)|[Backup and Disaster Recovery](https://cloud.google.com/backup-disaster-recovery)|

## Database

|   |   |   |   |   |
|---|---|---|---|---|
|Service type|Description|AWS|Azure|GCP|
|Relational DB management|Standard SQL DB (PostgreSQL, MySQL, SQL Server, etc.)|[Relational Database Service (RDS)](https://aws.amazon.com/rds/), [Aurora](https://aws.amazon.com/rds/aurora/)|[SQL](https://azure.microsoft.com/en-us/products/azure-sql/), [SQL Database](https://azure.microsoft.com/en-us/products/azure-sql/database/)|[Cloud SQL](https://cloud.google.com/sql/), [Cloud Spanner](https://cloud.google.com/spanner/)|
||||||
|NoSQL: Key-value|Redis-like DBs for semi-structured data|[DynamoDB](https://aws.amazon.com/dynamodb/)|[Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db), [Table storage](https://azure.microsoft.com/en-us/products/storage/tables/)|[Cloud BigTable](https://cloud.google.com/bigtable), [Firestore](https://cloud.google.com/firestore)|
|NoSQL: Document|MongoDB/CouchDB-like DBs for hierarchical JSON data|[DocumentDB](https://aws.amazon.com/documentdb/)|[Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db)|[Firestore](https://cloud.google.com/firestore), [Firebase Realtime Database](https://firebase.google.com/products/realtime-database/)|
|NoSQL: Column store|Cassandra/HBase-like DBs for structured hierarchical data|[Keyspaces](https://aws.amazon.com/keyspaces/)|[Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db)|[Cloud BigTable](https://cloud.google.com/bigtable)|
|NoSQL: Graph|Neo4j-like DBs for connected data|[Neptune](https://aws.amazon.com/neptune/)|N/A|N/A|
|Caching|Redis/Memcached-like memory for calculations|[ElastiCache](https://aws.amazon.com/elasticache/)|[Cache for Redis](https://azure.microsoft.com/en-us/products/cache/), [HPC Cache](https://azure.microsoft.com/en-us/products/hpc-cache/)|[Memorystore](https://cloud.google.com/memorystore)|
|Time Series DB|DB tuned for time series data|[Timestream](https://aws.amazon.com/timestream/)|[Time Series Insights](https://azure.microsoft.com/en-us/products/time-series-insights/)|[Cloud BigTable](https://cloud.google.com/bigtable)|
|Blockchain|Dogecoin, etc.|[Managed Blockchain](https://aws.amazon.com/managed-blockchain)|[Blockchain Service](https://azure.microsoft.com/en-us/services/blockchain-service/), [Blockchain Workbench](https://azure.microsoft.com/en-us/updates/azure-blockchain-workbench/), [Confidential Ledger](https://azure.microsoft.com/en-us/products/azure-confidential-ledger/)|N/A|

## Compute

|   |   |   |   |   |
|---|---|---|---|---|
|Service type|Description|AWS|Azure|GCP|
|Virtual machines|Software-emulated computers|[Elastic Compute Cloud (EC2)](https://aws.amazon.com/ec2/)|[Virtual Machines](https://azure.microsoft.com/en-us/products/virtual-machines/)|[Compute Engine](https://cloud.google.com/compute)|
|Spot virtual machines|Cost-effective VMs|[EC2 Spot Instances](https://aws.amazon.com/ec2/spot/)|[Spot Virtual Machines](https://azure.microsoft.com/en-us/products/virtual-machines/spot/)|[Spot VMs](https://cloud.google.com/spot-vms/)|
|Autoscaling|Adjust resources to match demand|[EC2 Auto Scaling](https://aws.amazon.com/ec2/autoscaling)|[Virtual Machine Scale Sets](https://azure.microsoft.com/en-us/products/virtual-machine-scale-sets/)|[Instance Groups](https://cloud.google.com/compute/docs/instance-groups)|
|Functions as a service (Serverless computing)|Execute code chunks without worrying about infrastructure|[Lambda](https://aws.amazon.com/lambda/)|[Functions](https://azure.microsoft.com/en-ca/products/functions/)|[Cloud Functions](https://cloud.google.com/functions)|
|Platform as a service|Manage applications without worrying about infrastructure|[Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk), [Red Hat OpenShift on AWS](https://aws.amazon.com/rosa/)|[App Service](https://azure.microsoft.com/en-us/products/app-service/), [Cloud Services](https://azure.microsoft.com/en-us/services/cloud-services/), [Spring Cloud](https://azure.microsoft.com/en-us/products/spring-apps/), [Red Hat OpenShift](https://azure.microsoft.com/en-us/products/openshift/)|[App Engine](https://cloud.google.com/appengine)|
|Batch scheduling|Run code at specified times|[Batch](https://aws.amazon.com/batch/)|[Batch](https://azure.microsoft.com/en-us/products/batch/)|[Batch](https://cloud.google.com/batch), [Cloud Scheduler](https://cloud.google.com/scheduler)|
|Isolated servers|VM on your own machine, for high security|[Dedicated Instances](https://aws.amazon.com/ec2/pricing/dedicated-instances/)|[Dedicated Host](https://azure.microsoft.com/en-us/products/virtual-machines/dedicated-host/)|[Sole-tenant Nodes](https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes), [Shielded VMs](https://cloud.google.com/shielded-vm)|
|On-premise/Edge devices|Cloud-services on your own hardware|[Outposts](https://aws.amazon.com/outposts), [Snow Family](https://aws.amazon.com/snow/)|[Modular Datacenter](https://azure.microsoft.com/en-us/products/azure-modular-datacenter/), [Stack Hub](https://azure.microsoft.com/en-gb/products/azure-stack/hub/), [Stack HCI](https://azure.microsoft.com/en-us/products/azure-stack/hci/), [Stack Edge](https://azure.microsoft.com/en-us/products/azure-stack/edge/)|N/A|
|Quantum computing|Determine if cat is alive or dead|[Braket](https://aws.amazon.com/braket)|[Quantum](https://azure.microsoft.com/en-us/products/quantum/)|N/A|

## Analytics

|   |   |   |   |   |
|---|---|---|---|---|
|Service type|Description|AWS|Azure|GCP|
|Data Warehouse|Centralized platform for all your data|[RedShift](https://aws.amazon.com/redshift/)|[Synapse Analytics](https://azure.microsoft.com/en-us/products/synapse-analytics/)|[BigQuery](https://cloud.google.com/bigquery)|
|Big data platform|Run Spark, Hadoop, Hive, Presto, etc.|[EMR](https://aws.amazon.com/emr/)|[Data Explorer](https://azure.microsoft.com/en-us/products/data-explorer/), [HDInsight](https://azure.microsoft.com/en-us/products/hdinsight/)|[Dataproc](https://cloud.google.com/dataproc/)|
|Business analytics|Dashboards and visualization|[Quicksight](https://aws.amazon.com/big-data/datalakes-and-analytics/#Solution_areas), [FinSpace](https://aws.amazon.com/finspace/)|[Power BI Embedded](https://azure.microsoft.com/en-us/products/power-bi-embedded/), [Graph Data Connect](https://azure.microsoft.com/en-gb/products/graph-data-connect/)|[Looker](https://www.looker.com/), [Looker Studio](https://cloud.google.com/looker-studio), [Vertex AI Workbench](https://cloud.google.com/vertex-ai-workbench)|
|Real-time analytics|Streaming data analytics|[Kinesis Data Analytics](https://aws.amazon.com/kinesis/data-analytics/), [Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/), [Managed Streaming for Kafka](https://aws.amazon.com/msk/)|[Stream Analytics](https://azure.microsoft.com/en-us/products/stream-analytics/), [Event Hubs](https://azure.microsoft.com/en-us/products/event-hubs/)|[Dataflow](https://cloud.google.com/dataflow/), [Pub/Sub](https://cloud.google.com/pubsub/), [Datastream](https://cloud.google.com/datastream)|
|Extract-Transform-Load (ETL)|Preprocessing and importing data|[Glue](https://aws.amazon.com/glue/), [Kinesis Data Firehose](https://aws.amazon.com/kinesis/data-firehose/), [SageMaker Data Wrangler](https://aws.amazon.com/sagemaker/data-wrangler/)|[Data Factory](https://azure.microsoft.com/en-us/products/data-factory/)|[Data Fusion](https://cloud.google.com/data-fusion/), [Dataflow](http://dataflow/), [Dataproc](https://cloud.google.com/dataproc/),<br><br>[Dataprep by Trifacta](https://cloud.google.com/dataprep)|
|Workflow orchestration|Build data and model pipelines|[Data Pipeline](https://aws.amazon.com/datapipeline/), [Managed Workflows for Airflow](https://aws.amazon.com/managed-workflows-for-apache-airflow/)|[Data Factory](https://azure.microsoft.com/en-us/products/data-factory/)|[Cloud Composer](https://cloud.google.com/composer)|
|Data lake creation|Import data into a lake|[Lake Formation](https://aws.amazon.com/lake-formation)|[Data Share](https://azure.microsoft.com/services/data-share/)|[Cloud Storage](https://cloud.google.com/storage/)|
|Managed search|Enterprise search|[CloudSearch](https://aws.amazon.com/cloudsearch/), [OpenSearch Service](https://aws.amazon.com/opensearch-service/), [Kendra](https://aws.amazon.com/kendra/)|[Cognitive Search](https://azure.microsoft.com/en-us/products/search/)|[Cloud Search](https://workspace.google.com/products/cloud-search/)|
|Data Catalog|Metadata management|[Glue Data Catalog](https://aws.amazon.com/glue/)|[Purview](https://azure.microsoft.com/en-us/products/purview/), [Data Explorer](https://azure.microsoft.com/en-us/products/data-explorer/)|[Data Catalog](https://cloud.google.com/data-catalog)|

## ML & AI

|   |   |   |   |   |
|---|---|---|---|---|
|Service type|Description|AWS|Azure|GCP|
|Machine Learning|Train, fit, validate, and deploy ML models|[SageMaker](https://aws.amazon.com/sagemaker)|[Machine Learning](https://azure.microsoft.com/en-us/products/machine-learning/)|[Vertex AI](https://cloud.google.com/vertex-ai/)|
|Jupyter notebooks|Write data analyses and reports|[SageMaker Notebooks](https://aws.amazon.com/sagemaker/notebooks/)|[Notebooks](https://visualstudio.microsoft.com/vs/features/notebooks-at-microsoft/)|[Colab](https://colab.research.google.com/notebook)|
|Data science/machine learning VM|Virtual machines tailored to data work|[Deep Learning AMIs](https://aws.amazon.com/machine-learning/amis/)|[Data Science Virtual Machines](https://azure.microsoft.com/en-us/products/virtual-machines/data-science-virtual-machines/)|[Deep Learning VM](https://cloud.google.com/deep-learning-vm)|
|AutoML|Automatically build ML models|[SageMaker](https://aws.amazon.com/sagemaker)|[Machine Learning Studio](https://ml.azure.com/),<br><br>[Automated ML](https://azure.microsoft.com/en-us/products/machine-learning/automatedml/)|[Vertex AI Workbench](https://cloud.google.com/vertex-ai-workbench)|
|Natural language Processing AI|Analyze text data|[Comprehend](https://aws.amazon.com/comprehend/)|[Text Analytics](https://azure.microsoft.com/en-us/products/cognitive-services/text-analytics/)|[Natural Language AI](https://cloud.google.com/natural-language)|
|Recommendation AI|Product recommendation engine|[Personalize](https://aws.amazon.com/personalize/)|[Personalizer](https://azure.microsoft.com/en-us/products/cognitive-services/personalizer/)|[Recommendations AI](https://cloud.google.com/recommendations)|
|Document capture|Extract text from printed text & handwriting|[Textract](https://aws.amazon.com/textract/)|[Form Recognizer](https://azure.microsoft.com/en-us/products/form-recognizer/)|[Document AI](https://cloud.google.com/document-ai)|
|Computer vision|Image classification, object detection & other AI with image data|[Rekognition](https://aws.amazon.com/rekognition/), [Panorama](https://aws.amazon.com/panorama/), [Lookout for Vision](https://aws.amazon.com/lookout-for-vision/)|[Cognitive Services for Vision](https://azure.microsoft.com/en-us/products/cognitive-services/vision-services/)|[Vision AI](https://cloud.google.com/vision)|
|Speech to text|Speech transcription|[Transcribe](https://aws.amazon.com/transcribe/)|[Cognitive Services for Speech to Text](https://azure.microsoft.com/en-us/products/cognitive-services/speech-to-text/), [Cognitive Services for Speaker Recognition](https://azure.microsoft.com/en-us/products/cognitive-services/speaker-recognition/)|[Speech-to-Text](https://cloud.google.com/speech-to-text)|
|Text to speech|Speech generation|[Polly](https://aws.amazon.com/polly/)|[Cognitive Services for Text to Speech](https://azure.microsoft.com/en-us/products/cognitive-services/text-to-speech/)|[Text-to-Speech](https://cloud.google.com/text-to-speech)|
|Translation AI|Convert text between human languages|[Translate](https://aws.amazon.com/translate/)|[Cognitive Services for Speech Translation](https://azure.microsoft.com/en-us/products/cognitive-services/speech-translation/), [Translator](https://azure.microsoft.com/en-us/products/cognitive-services/translator/)|[Translation AI](https://cloud.google.com/translate)|
|Video Intelligence|Video indexing and asset search|[Rekognition Video](https://aws.amazon.com/rekognition/video-features/)|[Video Indexer](https://azure.microsoft.com/en-us/products/video-indexer/)|[Video Intelligence API](https://cloud.google.com/video-intelligence/docs)|
|AI agents|Virtual assistants and chatbots|[Lex](https://aws.amazon.com/lex/), [Alexa Skills kit](https://developer.amazon.com/en-US/alexa/alexa-skills-kit)|[Bot Service](https://azure.microsoft.com/en-us/products/bot-services/), [Cognitive Services for Conversational Language Understanding](https://azure.microsoft.com/en-us/products/cognitive-services/conversational-language-understanding/)|[Dialogflow](https://cloud.google.com/dialogflow/)|
|Human-in-the-loop|Human-based quality control for AI|[Augmented AI (A2I)](https://aws.amazon.com/augmented-ai/)|[Cognitive Services Content Monitor](https://azure.microsoft.com/en-us/products/cognitive-services/content-moderator/)|N/A|

## Networking & ​​Content Delivery

|   |   |   |   |   |
|---|---|---|---|---|
|Service type|Description|AWS|Azure|GCP|
|Content delivery network|Serve content to users|[CloudFront](https://aws.amazon.com/cloudfront/)|[Content Delivery Network](https://azure.microsoft.com/en-us/products/cdn/)|[Cloud CDN and Media CDN](https://cloud.google.com/cdn/)|
|Application Programming Interface (API) management|Build and deploy APIs|[API Gateway](https://aws.amazon.com/api-gateway)|[API Apps](https://azure.microsoft.com/en-us/products/app-service/api/), [API Management](https://azure.microsoft.com/en-us/products/api-management/)|[Apigee API Management](https://cloud.google.com/apigee)|
|Domain Name System (DNS)|Route end users to applications|[Route 53](https://aws.amazon.com/route53)|[DNS](https://azure.microsoft.com/en-us/products/dns)|[Cloud DNS](https://cloud.google.com/dns)|
|Load balancing|Distribute work evenly across machines|[Elastic Load Balancing (ELB)](https://aws.amazon.com/elasticloadbalancing)|[Application Gateway](https://azure.microsoft.com/en-us/products/application-gateway/), [Load Balancer](https://azure.microsoft.com/en-us/products/load-balancer/), [Traffic Manager](https://azure.microsoft.com/en-us/products/traffic-manager/)|[Cloud Load Balancing](https://cloud.google.com/load-balancing)|

## Containers

|   |   |   |   |   |
|---|---|---|---|---|
|Service type|Description|AWS|Azure|GCP|
|Managed containers|Run and deploy containers|[Elastic Kubernetes Service](https://aws.amazon.com/eks), [Elastic Container Service](https://aws.amazon.com/ecs)|[Kubernetes Service](https://azure.microsoft.com/services/kubernetes-service), [Container Apps](https://azure.microsoft.com/products/container-apps/)|[Kubernetes Engine](https://cloud.google.com/kubernetes-engine)|
|Container registration|Manage container images|[Elastic Container Registry](https://aws.amazon.com/ecr)|[Container Registry](https://azure.microsoft.com/services/container-registry)|[Artifact Registry](https://cloud.google.com/artifact-registry)|

## Management & Security, Identity

|   |   |   |   |   |
|---|---|---|---|---|
|Service type|Description|AWS|Azure|GCP|
|Access management|User permissions and authentication|[Identity and Access Management (IAM)](https://aws.amazon.com/iam)|[Entra ID](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-id)|[Cloud Identity](https://cloud.google.com/identity/)|
|Activity tracking|Track user Activity|[CloudTrail](https://aws.amazon.com/cloudtrail/)|[Monitor](https://azure.microsoft.com/en-us/products/monitor/) Activity Log|[Access Transparency and Access Approval](https://cloud.google.com/access-transparency)|
|Security|Protect your data, network and applications|[Security Hub](https://aws.amazon.com/security-hub)|[Security](https://azure.microsoft.com/en-us/explore/security/)|[Security Command Center](https://cloud.google.com/security-command-center)|
|Monitoring|Monitor network traffic and detect anomalies|[CloudWatch](https://aws.amazon.com/cloudwatch/), [Transit Gateway Network Manager](https://aws.amazon.com/transit-gateway/network-manager/)|[Monitor](https://azure.microsoft.com/en-us/products/monitor/), [Anomaly Detector](https://azure.microsoft.com/en-us/products/cognitive-services/anomaly-detector/)|[Operations](https://cloud.google.com/products/operations), [Network Intelligence Center](https://cloud.google.com/network-intelligence-center)|
|Automation|Preform processes automatically|[OpsWorks](https://aws.amazon.com/opsworks)|[Automation](https://azure.microsoft.com/en-us/products/automation/)|[Compute Engine Management](https://cloud.google.com/compute)|
|Cost optimization|Reduce your cloud spend|[Cost Optimization](https://aws.amazon.com/architecture/cost-optimization)|[Cost Management](https://azure.microsoft.com/en-us/products/cost-management/)|[Recommender](https://cloud.google.com/recommender/)|