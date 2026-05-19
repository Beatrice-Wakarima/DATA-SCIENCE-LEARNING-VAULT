## 

Extracting Data

Extracting data is almost always the first step when building a data pipelines. There are tons of shapes and sizes that data can be extracted from. Here are just a few:

- API's
- SFTP sites
- Relational databases
- NoSQL databases (columnar, document, key-value)
- Flat-files

In this code-along, we'll focus on extracting data from flat-files. A flat file might be something like a `.csv` or a `.json` file. The two files that we'll be extracting data from are the `apps_data.csv` and the `review_data.csv` file. To do this, we'll used `pandas`. Let's take a closer look!

1. After importing `pandas`, read the `apps_data.csv` DataFrame into memory. Print the head of the DataFrame.
2. Similar to before, read in the DataFrame stored in the `review_data.csv` file. Take a look at the first few rows of this DataFrame.
3. Print the column names, shape, and data types of the `apps` DataFrame.
up:: [[Data Engineering MOC]]
