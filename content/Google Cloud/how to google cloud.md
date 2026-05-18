In recent years, our society has produced so much data at such a fast pace. Consequently, efficient data management systems are more necessary than ever. 

Storage, management, and analysis systems are a core part of any modern organization and business. This is where data warehousing steps in—probably the most advanced technology of its type—to store large amounts of data in one single place while enhancing the analytics process.

Data warehousing technology has recently been consolidated to become more scalable and less expensive with the popularization of cloud services. That’s why in this article, we will discuss the [Google Cloud Platform (GCP)](https://www.datacamp.com/blog/what-is-gcp) and its robust data warehousing solution: BigQuery.

## What Is a Data Warehouse?

A data warehouse is a type of data management system designed to enable and support business intelligence activities, particularly analytics. 

While traditional databases are mainly used for processing transactions, a data warehouse is optimized for read-heavy operations and complex queries.

Data warehouses are ideal systems for centralizing an organization's business intelligence and enabling integrations with other data sources. [Data warehousing](https://www.datacamp.com/courses/data-warehousing-concepts), therefore, refers to the process of collecting data from multiple resources and storing it in a single location: the data warehouse.

### The advantages of using cloud data warehouses

A data warehouse can be hosted on-premises or in the cloud. Using cloud-based services brings five main benefits over traditional self-managed solutions:

- Scalability: You don’t have to worry about large hardware investments. Cloud services allow you to add or remove resources based on your current needs.
- Flexibility: You can modify infrastructure as your needs change.
- Advanced security: Cloud solutions offer top-notch security features such as automatic backups and disaster recovery capabilities.
- Cost-effective: Cloud solutions offer a pay-as-you-go pricing model, allowing you to pay just for what you use.
- Data sharing and collaboration: Using cloud-based services fosters data sharing and collaboration, allowing different teams and stakeholders to access and analyze data securely.

![Advantages of using cloud-based services.](https://media.datacamp.com/cms/google/ad_4nxfrkdsug5v6gw8mqt4mzbgba8wnq9cl7zs_x8rth6w_ztlaralw05ldytsrwyudsz62gnzbbtj5ukqhdm-rfzm7eehkvbfwzuwot7r7zh0po17vp2gsnpzbbqdquhoidzfq6mowucr4vgdseljknnoi6652.png)

Advantages of using cloud-based services. Image by Author.

Now that we understand the data warehouse concept and the main advantages of using the cloud, the next natural question is why we should choose GCP and their data warehousing solution, BigQuery. Let’s discuss that in the following sections.

## Introduction to Google Cloud Platform (GCP)

[GCP](https://www.datacamp.com/blog/what-is-gcp) is a cloud-based computing platform that allows organizations to build and deploy their applications using Google’s infrastructure. It offers a wide variety of services, covering everything from computing and storage to networking and machine learning.

If you want to learn more about GCP, I recommend getting a full overview by enrolling in our [Introduction to GCP](https://www.datacamp.com/courses/introduction-to-gcp) course.

![Google Cloud services.](https://media.datacamp.com/cms/google/ad_4nxdvhffsl1xsss9qlfsp2hgdkso7dt0mskyl9quch_k3nryhijhgjpuzutpjonyyjzxj-toangjpdn29l6_qrltcabaud6paxpscl9toefibmfhfz61r2rq1zvqmoecznyyzrzxoukptuq1xyq0fxcl7q2a.png)

Google Cloud services overview. Image by [Google Cloud.](https://cloud.google.com/icons/?hl=en) 

Some of the GCP key services include:

- Compute: Virtual machines running in Google’s data centers.
- Storage: Scalable and secure object storage service.
- Cloud SQL: Fully managed relational database service.
- Cloud Pub/Sub: Messaging service for building event-driven systems.
- Cloud Dataflow: Stream and batch data processing service.

[This cheat sheet](https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai) summarizes all services offered by GCP, Azure, and AWS, the most prominent cloud providers, for an in-depth comparison.

### The advantages of using GCP for data warehousing

Using any cloud-based infrastructure for data warehousing provides us with some advantages, like the ones mentioned before. However, using GCP may offer some additional benefits worth mentioning:

- Performance: GCP’s global infrastructure ensures high performance and low latency.
- Integration: GCP services are designed to work seamlessly together, enabling you to build integrated data solutions.
- Managed services: Services like BigQuery (GCP’s data warehouse service) are fully managed, allowing you to focus on analyzing your data rather than managing the infrastructure.
- Advanced analytics and AI: GCP provides advanced analytics and AI capabilities, including integration with Google AI and machine learning services.
- Ease of use: GCP offers flexible tools and a user-friendly interface, making it easy to set up, manage, and scale.

## What Is BigQuery?

BigQuery is a fully managed, serverless data warehouse provided by GCP. It is designed to handle large-scale data analytics and enables super-fast SQL queries. It eliminates the need for managing infrastructure, allowing users to focus on its main purpose: analyzing their data.

### BigQuery features and main advantages

BigQuery offers several features that make it a powerful data warehousing solution:

- Serverless architecture: Users don’t need to worry about managing infrastructure, as it is a serverless service. 
- SQL support: BigQuery supports standard SQL, making it easy for users to retrieve and analyze data. 
- Scalability: BigQuery can scale automatically to handle large datasets and complex queries.
- Real-time analytics: BigQuery supports real-time data ingestion and analysis, enabling users to gain insights from streaming data.
- Integration with GCP services: For data ingestion and usage, BigQuery seamlessly integrates with other GCP services, such as Dataflow, Pub/Sub, and Cloud Storage.
- Machine learning: BigQuery ML allows users to build and deploy machine learning models directly within BigQuery using SQL.

Additionally, BigQuery’s cost-effective pricing model, based on data processed by queries, is ideal for large-scale data analysis and to reduce the associated cost of querying data.

In summary, BigQuery combines speed, ease of use, cost-effectiveness, and flexibility, making it a top choice for modern data warehousing.

## Setting Up BigQuery on GCP

Getting started with BigQuery is straightforward and involves the following steps:

### 1. Creating a GCP account

To use BigQuery, the first step is to create a GCP account. You should go to the [Google Cloud Platform website](https://cloud.google.com/?hl=en), create your account, and set up a billing account. 

It is important to note that Google offers a free tier with a $300 credit for new users. This allows you to explore GCP services without incurring costs during your first three months of usage.

### 2. Setting up a project in GCP

Once you have an account, go to the [GPC console](https://console.cloud.google.com/). You will see your $300 credits or the proportion you have already used if you have an active free trial.

![GCP interface main view.](https://media.datacamp.com/cms/google/ad_4nxdad4blidw3vzrh5n3jzxam8zuyhhu9zlzrnwkuxlye-vn_r_0theewmvffmzwbigiz44tfgdvhk0fl0ocs8n_xk8pdjjdinzgtja2hv-ufywpirc4rlklasmgfhpwttdevwek1bqqhixfuphlmdlbti1ep.png)

GCP interface: Console view. 

After you create a new account, a project called “My First Project” will be automatically created for you. A project is a container for all your GCP resources, including BigQuery datasets and tables.

To create a new project, click on the selector next to the Google Cloud logo in the upper navigation bar. A new section with a listing of all your projects should appear. You can create a new project by clicking the “New Project” button.

![GCP interface list of projects.](https://media.datacamp.com/cms/google/ad_4nxe17s_xqnhdqzgfb1iuepc2ralbwangejgcwgxhf4pnggszhhcpozumrwpnocf3iaamw6w6gw8xykczcl_5dl95tyouvq5jvkkay-a0zqyuk1ru2ksuvcip9rf3jytbqsrmmojcccyandpp0byaiocoaebv.png)

GCP interface: List of projects. 

You may be required to provide billing information to activate a new project, but remember that you can take advantage of the free credits to avoid any cost. Now, you need to provide a name for your project and click on the “Create” button.

 ![GCP interface: Creating a new project.](https://media.datacamp.com/cms/google/ad_4nxdyq3c627dgh3dij_lub5qlfprv-na2ncuefofir1yc4znnlmuk12dpjd5cmnkxbrfs78lazbuqs9wgjxwxswc5nii2s0qp1r13eevzsiylaprzvrciakwgoom2hitdk1836w-qxvwwlyzfg2qxyjfdfxl5.png)

GCP interface: Creating a new project. 

For this tutorial, I created a new project called “DataCamp-BQ-Tutorial.” Feel free to do the same. 

### ![GCP interface: Selecting a project.](https://media.datacamp.com/cms/google/ad_4nxfgx1wuwgz_n_fr7sbiwh2kqtl8bcmzepa0rrul5xilgiwbzer4lfpplzwkqa8grcxnte_zgtby74bsqaevvi1gxetrh-9l3sxojv5hejdt76elo_gjwod_gqmaldi1mawznnp1k3optc6d0pph1kvzwfef.png)

GCP interface: Selecting a project. 

### 3. Enabling the BigQuery API

To use BigQuery, you need to enable the BigQuery API for your project. You can do this either by going directly to the BigQuery service and activating it from there or by going to the “API & Services” dashboard in the GCP console. 

If you are not familiar with the GCP interface, I recommend you take the [Introduction to GCP](https://www.datacamp.com/courses/introduction-to-gcp) course to learn some of the first notions. 

To find the BigQuery service, we can use the search bar in the GCP console, as you can observe in the following screenshot. 

![GCP interface looking for the BigQuery service.](https://media.datacamp.com/cms/google/ad_4nxfsi7fxhcapvjd7rlamkfwif5ru4ihahgtdp2vt69lpcv-uksxuqysk-y5518bnnkk981qickbouqcxeowmnvl-9jw_blze4vguxtjr8xd2vwdsasmlwudomy2nxaw9uuhe9cubynabtlcnnto3yigmalxg.png)

GCP interface: Looking for the BigQuery service. 

A view like the following one should appear, asking us to enable the BigQuery API.

![GCP interface enabling the BigQuery API](https://media.datacamp.com/cms/google/ad_4nxfyxpcuugihsmd42itgm21dggctkzyhlqewutcsriojzvgalb1iphx97yeu9j6hlirmlsfma7xdhpcmlj2c9sytf10avsxr1sgxqphd9_0whe21oydikwyvxtepmcml1zyuaembu2kihlfs8sbvjh7ywfs.png)

GCP interface: Enabling the BigQuery API. 

After you click the “Enable” button, the API will be enabled. It will take a few seconds.

### 4. Accessing the BigQuery console

Once the API is enabled, you should be taken to the BigQuery console, a web-based interface allowing you to interact with the BigQuery service. The console provides tools for managing datasets, writing and executing queries, and monitoring job statuses.

You can always access the BigQuery console from the GCP main console, either by using the search bar as shown in the previous step or by going to the main menu at the top left corner of the screen.

![GCP interface BigQuery console main interface.](https://media.datacamp.com/cms/google/ad_4nxcpx7t2a28ryywnaqvzxi6azxixhcgrksucefjiolwusemzwisi0xvfbgh6fqal89b76pgnkwn0secuoyb60uiqumic650roczyelskcqq4d-phx_glmaudopgknr8-z7wx2p5n2frc1yh1epdhusugzvln.png)

GCP interface: BigQuery console main interface. 

## Querying Data in BigQuery

BigQuery supports two [SQL dialects](https://www.datacamp.com/blog/all-about-sql-the-essential-language-for-database-management): standard SQL and legacy SQL. Standard SQL is the preferred choice for querying data in BigQuery because it complies with the ANSI SQL 2011 standard. 

To further understand how BigQuery works, it is important to consider that data is organized into datasets and tables:

- Datasets are top-level containers that hold tables. A dataset groups related tables together, similar to a database in traditional relational database systems. Each dataset belongs to a specific project and is identified by a combination of the `project ID` and `dataset ID`.
- Tables are structured collections of data within a dataset. Each table consists of rows and columns, each with a specific data type. Tables can store structured data, such as JSON or CSV, and can be queried using SQL.

To further exemplify these two concepts, tables are the smallest unit of data we can have, and the datasets work as “folders” that contain those tables. Within a single dataset, tables are identified by their names and can be organized logically according to the needs of the data and project.

Now, we are ready to start querying data in BigQuery, but you will notice a big problem: There is no data at all.

To get started, we will play with the public datasets BigQuery provides for free. To access them, click on the “Add” button next to the “Explorer.”

 ![GCP interface: BigQuery console main interface add a dataset.](https://media.datacamp.com/cms/google/ad_4nxffqfabfe1pbfmbmblub9makvzihkedfvotvl6x6nedh7lyu1l33du-pqnxuyvm5p8cn99crb_rcxeofvduhh3qxyagvxrcj5nakwp6gdg9fkno5ogex9ldrx7ru0xpaajirolpj-xpytzjwtvbuadjmpg.png)

GCP interface: BigQuery console main interface, add a dataset.

Then, a new interface with several options for adding data to BigQuery will appear. 

There are simple integrations, such as Google Drive, or more advanced integrations, such as [Amazon S3](https://www.datacamp.com/tutorial/aws-s3-efs-tutorial) or Azure Blob Storage. 

In our case, we will select “Public Datasets.”

![GCP interface: BigQuery console adding data options.](https://media.datacamp.com/cms/google/ad_4nxcqfm8u8gztdbqrqumt1zhhtmavgz93wnd1qn4ryciasi_ytnojqjzbirz-xhw_q4kcugpe1me08ov_dohhzfk0pgnp5ypt8tob4y1lkhn6_p1ewed-jvxamnoomgcb1akifzdrdgywn4d1mdgn4ek6pueo.png)

GCP interface: BigQuery console adding data options.

We will then be taken to the “Marketplace,” which will show us all the public datasets available for use.

![GCP interface: Data marketplace for public datasets.](https://media.datacamp.com/cms/google/ad_4nxfha3cxfvjtrsnd0ehkuyxco5mm9nl92msppaxw9fqfihkiuiwqtbj1wwntk4bb2lbkv5bkcpjhpc0h39ab_gvafm4jbdin74voxf_xw0njt2hkyqxsw8ol6izvlg1zocx_cgxvwabgjbxf82pvdrlfwmy.png)

GCP interface: Data marketplace for public datasets. 

You can select any dataset of interest to you. The data will appear automatically in BigQuery under the `big-query-public-data` dataset. Some datasets contain a single table, while others store multiple ones. 

![GCP interface: BigQuery main interface, selecting a new table.](https://media.datacamp.com/cms/google/ad_4nxf1kbb_8zdkma2m6vz0yvlisun4zvct9fu-dfeimwxcpgvmqv3p39n6bnanvp4ovtxm4skij4zgycfjdxofszcrjmbe2hx-f2xp_k_igbktkhbqey4rf0jhmyhbifz7ruzsfjqmz_limpdmkzmi-ghfuzfp.png)

GCP interface: BigQuery main interface, selecting a new table. 

When you select any table, the schema will be displayed. Clicking on the interface's different options will give you more details about the tables or even a data preview.

My personal suggestion is just to start exploring these datasets on your own.

![GCP interface: BigQuery main interface, selecting a table.](https://media.datacamp.com/cms/google/ad_4nxdxai1ox0orbfbduhst65dkgcejkoipvfeahrp7ueydftf8nzsabb9zkdwjehmsl5aijox8ygegc8z8gaaps3yxnlx0xewh9r-ljj1cphh5cp6l1ilgs59sphd7fkhiygfr_kmjs3mmxuceu85pgs8ko78.png)

GCP interface: BigQuery main interface, selecting a table.

### Basic SQL queries

Getting started with querying data in BigQuery involves understanding basic SQL commands. You can perform simple SELECT statements to retrieve specific columns from a dataset.

For instance, we can generate a simple query to get the `station_id` and the corresponding `name` from the `bikeshare_stations` table contained within the `austin_bikeshare` dataset.

`` SELECT station_id, name FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations` ``

[Powered By](https://www.datacamp.com/datalab) 

If we execute the query by clicking on the “Run” button, we will immediately obtain the result.

![GCP interface: BigQuery main interface, running a query.](https://media.datacamp.com/cms/google/ad_4nxdxj-_sppcyekeyuphdheehfy9fzpv6l2tmzaz-sc9w7mh1_npollbx0teh8qmva8_ezjcnvwdcruzmgejnn6ksqwk8cv3ia4nfocrqmb00tpydj3hhqj-2gg3w65fwquhktkqx46xy1zlfdxy99f5nt7ev.png)

GCP interface: BigQuery main interface, running a query.

If you are unfamiliar with SQL, you can start with [this amazing code-along](https://www.datacamp.com/code-along/getting-started-in-sql) to understand the language's most basic commands. 

### Advanced querying techniques

Once you have mastered the basic commands of SQL, you can further enhance your skills with advanced queries. 

BigQuery offers advanced SQL features such as window functions, common table expressions (CTEs), and subqueries. These tools allow more complex data manipulation and analysis. 

For example, we can generate a new query using a window function to calculate a running total duration of trips for each individual bike, using the `bikeshare_trips` table from the `austin_bikeshare` dataset:

``SELECT  trip_id,  bike_id,  start_time,  duration_minutes,  SUM(duration_minutes) OVER (PARTITION BY bike_id ORDER BY start_time) AS cumulative_duration FROM  `bigquery-public-data.austin_bikeshare.bikeshare_trips` ORDER BY  bike_id,  start_time;``

[Powered By](https://www.datacamp.com/datalab) 

To learn more about advanced SQL commands, I recommend you to read our [How to Become a SQL Expert](https://www.datacamp.com/blog/how-to-become-a-sql-expert) article.

![GCP interface: BigQuery main interface, query results.](https://media.datacamp.com/cms/google/ad_4nxfaqae0cyqbhwvpexjwggzbcs8cckjd1y4qklilj4aocrgf1sifca6dzjo75cq6cb7jwf9mhtyt1iliwvk4v89bhjtns5m9qtc8adh4ecp1v8z0hctl2alzxvwwxbukgyhjngin8g7n-_cad7ckmyicf0un.png)

GCP interface: BigQuery main interface, query results.

### Query optimization tips

Optimizing queries in BigQuery can significantly enhance performance and reduce costs. One of the easiest ways to reduce costs is always to check how much data you will execute before running the query.

When generating a new query, GCP will approximate the amount of data you will be executing.

![GCP interface: BigQuery main interface, amount of data to be processed.](https://media.datacamp.com/cms/google/ad_4nxd2yvktn31hihh0cob3r-lx_asma6ldddlf-8ti01ge8ztcc3zrifcpabj1kcloba4rrawq1bh0dgnmggylb41-o2xqlqfyy_itbkk9poqtcuzrl-doqtzgudwlnoohhmd37khll6knwkdomy6xyifek_0.png)

GCP interface: BigQuery main interface, amount of data to be processed.

Some other tips to keep in mind are: 

- Avoid using `SELECT *` by specifying only the columns you need, and leverage query caching whenever possible.
- Break complex queries into smaller, manageable parts using CTEs to improve readability and maintainability. 
- Take advantage of BigQuery's partitioning and clustering features to minimize the amount of data scanned. We will discuss this in more detail in the coming section.
- Consider materialized views for frequently accessed data to speed up query execution. 

Following these tips can ensure more efficient and cost-effective queries in BigQuery.

### Using BigQuery ML for machine learning

BigQuery ML simplifies machine learning by enabling data scientists and analysts to build and deploy models using SQL queries directly within BigQuery. This integration allows users to leverage BigQuery's powerful data processing capabilities, eliminating the need to move data between platforms.

With BigQuery ML, you can create, train, and evaluate various machine learning models, such as linear regression, without the need to use any other tool. 

For example, to create a linear regression model predicting sales, you would use:

``CREATE OR REPLACE MODEL `datacamp_test.bike_usage_model` OPTIONS(model_type='linear_reg', input_label_cols=['duration_minutes']) AS SELECT  start_time,  EXTRACT(HOUR FROM start_time) AS hour_of_day,  start_station_id,  end_station_id,  subscriber_type,  bike_type,  duration_minutes FROM  `bigquery-public-data.austin_bikeshare.bikeshare_trips`;``

[Powered By](https://www.datacamp.com/datalab) 

If we execute the code, a new model will be generated based on the data we have selected. 

![GCP interface: BigQuery main interface, running an ML model.](https://media.datacamp.com/cms/google/ad_4nxedje52yahfysxl5pn6xf-yw36ctsfseih9r_ywxyvlxk3bx64xal1yz6bvxfy9c46mbihzu7l0ornl4dbtvrh5xnwyyozizjaes_5ywgv9sg1wb4cudjssoev9d93jw88kymoiy1eofwznngwp5qgiqiqu.png)

GCP interface: BigQuery main interface, running an ML model.

This integration simplifies the process of applying machine learning to your data, streamlining the workflow and making machine learning more accessible and efficient.

## Designing a Data Warehouse in BigQuery

Designing an efficient data warehouse schema is crucial for optimizing query performance in BigQuery. 

Remember that any process that runs in the cloud comes with an associated cost. Therefore, I recommend to: 

- Reduce the amount of data to be processed. 
- Optimize the performance of the queries that you will execute. 

Before deciding on a final schema, we need to think about how we will be accessing the data. BigQuery generally provides high performance across many data model methodologies.

Let’s review some common schema design strategies.

### Denormalization

Unlike [normalization](https://www.datacamp.com/tutorial/normalization-in-machine-learning), which minimizes redundancy and organizes data into smaller, related tables, denormalization intentionally introduces redundancy for efficiency. It involves merging tables and including duplicate data to reduce the complexity of queries, which can lead to faster read times.

![Denormalized table examples.](https://media.datacamp.com/cms/google/ad_4nxdax1k4bgdot_0dvgbnxsivmo2lziehwwbmzui3b6jcme_oztgsnapmibdt3gmnb6mqg1yldbq2qvi_ffifsqvt2s2a0slexix7ffvgvqhuvgwmyk2xeavemukqopdxme3svte-ld2atxfcthjkrzep1ae.png)

Denormalized table examples. Image by [Google Cloud](https://cloud.google.com/bigquery/docs/partitioned-tables#:~:text=A%20partitioned%20table%20is%20divided,bytes%20read%20by%20a%20query.). 

In a denormalized database, data retrieval operations often become simpler and quicker because fewer joins are required, reducing the overall query execution time. This approach is particularly useful in data warehousing and analytical databases, like BigQuery, where read operations are more frequent than write operations.

However, normalization increases data storage requirements. That’s why the recommended way to denormalize data in BigQuery is to use nested fields.

![Comparison of different data normalization strategies.](https://media.datacamp.com/cms/google/ad_4nxeix-49ioug7bd15hck-ekojp5uolwgungmswvyqlx-jj7a84ru0yonhkwq8_nfwfari5dqc_ml7g45vxfxdssq-rj1ygzftjzgm8-ff9_ufh_wr2qnjzp66wj2pplgmr91fme_6qv6oa6mflnmy0qo3xt8.png)

Comparison of different data normalization strategies: Original tables on the left, denormalized data with nested order records in the middle, and denormalized data with repeated records on the right. Image by [Google Cloud](https://cloud.google.com/bigquery/docs/partitioned-tables#:~:text=A%20partitioned%20table%20is%20divided,bytes%20read%20by%20a%20query.). 

### Partitioning and clustering

Partitioning and clustering are powerful features in BigQuery that help optimize storage and query performance. 

A partitioned table is divided into segments, called partitions, that make it easier to manage and query the data. By splitting a large table into smaller partitions, you can improve query performance and control costs by reducing the number of bytes read by a query. 

Tables can be partitioned by specifying a partition column which is used to segment the table.

A clustered table implies organizing the data contained within the table according to single or multiple columns to optimize the queries when applying specific constraints.

You can observe both concepts in the following diagram. 

![Table cluster and partition examples.](https://media.datacamp.com/cms/google/ad_4nxdtpyngvysgvi8tktb8v-weucyhnvrxdpbkfdxcodxz6cmkfk9ic1fq9tzkw4qfo6crab3gsmqxq354oot41gll-qjeymosydb6yqidcrjq_xvmifmcaag9deyjfknv4o1xfgbrzz_t56zzymowobnbki14.png)

Table cluster and partition examples: The default table is on the left, the clustered table is in the middle, and the clustered and partitioned table is on the right. Image by [Google Cloud](https://cloud.google.com/bigquery/docs/partitioned-tables#:~:text=A%20partitioned%20table%20is%20divided,bytes%20read%20by%20a%20query.). 

### Data types and structure

When storing and querying data, it is helpful to keep the following data type properties in mind:

- Nullable records: Variables that can present a null value. 
- Orderable data types: Expressions of orderable data types can be used in an `ORDER BY` clause. This applies to all data types except for `ARRAY`, `STRUCT`, `GEOGRAPHY`, and `JSON`.
- Groupable data types: Groupable data types can generally appear in an expression following `GROUP BY`, `DISTINCT`, and `PARTITION BY`. All data types except `ARRAY`, `STRUCT`, `GEOGRAPHY`, and `JSON` are supported. 
- Data type sizes: The following table shows the size in logical bytes for each supported data type.

![BigQuery data types.](https://media.datacamp.com/cms/google/ad_4nxdknbqe_vbrqja3o7bngabjjolgaorwjp42ipxghblz_sfymviwwuqv6ajg_8ibp-g1653qmnfhfv5yvc9oh_yiomjru1jswxaba47htpp_kdu8l34pbrav8biu2f_1vyz8ce7ppovfh3nuzlsb4tgilve.png)

BigQuery data types. Image from [Google Cloud Documentation.](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-typesLoading%20Data%20into%20BigQuery) 

Remember to use the appropriate data types for each variable, and always try to use the smallest unit datatype right for a given value.

Now that we know the best data modeling strategies, how can we load data into BigQuery?

## Loading Data Into BigQuery

To start using BigQuery for business intelligence or other data operations, we usually need to “ingest” data from different sources into it. Let’s review some methods to do that.

### Data ingestion methods

BigQuery supports various data ingestion methods, including batch loading, streaming, and multiple integrations with Cloud Storage. Choosing the right method depends on your use case and data volume.

#### Batch loading

Batch loading involves loading large volumes of data into BigQuery in bulk. This method is suitable for historical data loads and periodic data updates that are not too frequent. 

Traditional [extract, transform, and load](https://www.datacamp.com/courses/etl-and-elt-in-python) (ETL) jobs fall into this category. 

Options for batch loading in BigQuery include:

- Load jobs: A [load job](https://cloud.google.com/bigquery/docs/batch-loading-data) loads data from Cloud Storage or a local file. The records can be in Avro, CSV, JSON, ORC, or Parquet format. The data must be staged for intermediate storage, typically in Cloud Storage, before making it to BigQuery.
- SQL: The [LOAD DATA](https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#load_data_statement) SQL statement loads data from one or more files into a new or existing BigQuery table.
- BigQuery Data Transfer Service: The [BigQuery Data Transfer Service](https://cloud.google.com/bigquery/docs/dts-introduction) automates the loading of data from Google Software as a Service (SaaS) apps or from third-party applications and services.
- BigQuery Storage Write API: The [Storage Write API](https://cloud.google.com/bigquery/docs/write-api) lets you batch-process a large number of records and commit them in a single atomic operation. If the commit operation fails, you can safely retry the operation. 
- Other managed services: Other managed services can export data from an external data store and import it into BigQuery. For example, you can load data from [Firestore exports](https://cloud.google.com/bigquery/docs/loading-data-cloud-firestore).

Batch loading can be done as a one-time operation or on a recurring schedule. To generate a recurrent schedule, you can simply run BigQuery Data Transfer Service transfers on a schedule, use an orchestration service such as Cloud Composer to schedule load jobs or use a cron job to load data on a schedule like Pub/Sub.

#### Streaming data

Streaming data allows you to ingest data into BigQuery in real time. This method is ideal for applications that require up-to-date data for analysis and reporting.  

Options for streaming in BigQuery include the following:

- Storage Write API: The [Storage Write API](https://cloud.google.com/bigquery/docs/write-api) supports high-throughput streaming ingestion with exactly-once delivery semantics.
- Dataflow: You can use [Dataflow](https://cloud.google.com/dataflow/docs) with the Apache Beam SDK to set up a streaming pipeline that writes to BigQuery.
- Datastream: The [Datastream](https://cloud.google.com/datastream-for-bigquery) service uses change data capture (CDC) functionality and the [Storage Write API](https://cloud.google.com/bigquery/docs/write-api) to replicate data and schema updates from operational databases directly into BigQuery. 
- BigQuery Connector for SAP: The BigQuery Connector for SAP enables near real-time replication of SAP data directly into BigQuery. 
- Pub/Sub: You can use the [Pub/Sub](https://cloud.google.com/pubsub/docs/overview) messaging service to coordinate streaming analytics and data integration pipelines. You can use [BigQuery subscriptions](https://cloud.google.com/pubsub/docs/bigquery) to write messages directly to an existing BigQuery table.

### Generated data

Another alternative is to use SQL to generate new data from existing tables and store the results in BigQuery. Options for generating data include:

- Using [data manipulation language](https://cloud.google.com/bigquery/docs/data-manipulation-language) (DML) statements to perform bulk inserts into an existing table or store query results in a new table.
- Using a [CREATE TABLE ... AS](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_table_statement) statement to create a new table from a SQL query result.
- Running a query and save the results to a table. You can append the results to an existing table or write them down to a new table.

## Managing and Monitoring BigQuery

Monitoring is crucial for running reliable applications in the cloud. BigQuery workloads are no exception, especially if your workload has high volumes or is mission-critical. 

Any job within BigQuery relies on security permissions, requires some resources, and implies an associated cost, so it is important to monitor its activity. 

### Resource management 

Effective resource management is important for optimizing BigQuery's performance. It involves strategically allocating resources such as slots and reservations to ensure that queries are executed efficiently. 

Proper resource management helps to avoid bottlenecks and ensures that workloads are distributed evenly, thereby maximizing the system’s throughput and minimizing wait times.

### Monitoring performance and usage

Monitoring performance and usage is essential to maintaining BigQuery's efficiency. This includes tracking query performance, identifying slow-running queries, and analyzing usage patterns. To monitor BigQuery’s performance, it is important to leverage logs. 

Logs are text records that are generated in response to particular events or actions. BigQuery creates log entries for actions such as creating or deleting a table, purchasing slots, or running a load job.

### Security and access control

Ensuring the security of your BigQuery data involves implementing robust access controls. Use IAM (Identity and Access Management) roles to grant appropriate permissions to users and groups. 

Encrypting data both at rest and in transit provides an additional layer of security. Regularly auditing access logs and permissions helps maintain compliance and prevent unauthorized access. 

The [Comprehensive Guide to Mastering Cloud Services](https://www.datacamp.com/blog/what-is-gcp) provides vast information about security in GCP.

### Cost management strategies

Cost management strategies are vital for controlling expenses while using BigQuery. These strategies include setting budgets, taking advantage of cost controls, and optimizing queries to reduce the amount of data processed. 

Leveraging BigQuery’s pricing models, such as flat-rate pricing for predictable workloads and on-demand pricing for variable workloads, can help manage costs effectively. 

Additionally, leveraging techniques already discussed, such as partitioned tables, can further optimize query costs by reducing the amount of data scanned.

## BigQuery Use Cases and Real-World Scenarios

BigQuery has been successfully implemented in various real-world scenarios to efficiently manage and analyze large datasets. Some notable examples are:

- [Etsy utilizes BigQuery's advanced capabilities](https://cloud.google.com/customers/etsy) for data logging, semantic labeling, and mapping, ensuring that the data is well-structured and easily accessible for comprehensive analysis and reporting. 
- [Podimo leverages BigQuery to streamline data processing](https://cloud.google.com/customers/podimo), enabling real-time optimization of content recommendations and, consequently, improving their user experience.