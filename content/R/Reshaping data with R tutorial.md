# Data Reshaping in R Tutorial

Learn about data reshaping in R, different functions like rbind(), cbind(), along with Melt(), Dcast(), and finally about the transpose function.

May 5, 2020 · 7 min read

Contents

- [Creating your Data](https://www.datacamp.com/tutorial/data-reshaping-in-r#creating-your-data-let's)

- [Congratulations](https://www.datacamp.com/tutorial/data-reshaping-in-r#congratulations-congr)

## Training more people?

Get your team access to the full DataCamp for business platform.

For a bespoke solution [book a demo](https://www.datacamp.com/business/demo-2).

Data Reshaping in R is something like arranged rows and columns in your own way to use it as per your requirements, mostly data is taken as a [data frame format in R](https://www.datacamp.com/tutorial/intro-data-frame-r) to do data processing using functions like 'rbind()', 'cbind()', etc.

In this process, you reshape or re-organize the data into rows and columns. Reshaping is re-organized data in a particular way which you need the data to process further.

## Creating your Data

Let's create a random number generator and make columns to concatenate them in the data frame. Also, insert the id for later use. 'set.seed(123)' is used for producing the random numbers where the same sample is reproduced across all the machine anyone who uses it. Three variables, colm1, colm2, colm3, are made. With the help of 'sample()', the value from 1 to 15 is generated, and the same value can get repeated. Also, a data frame is used to store data in the table, and id is also joined, which is a unique number.

`set.seed(123) N <- 15 colm1  <- sample(1:15, N, replace=TRUE) colm2  <- sample(1:15, N, replace=TRUE) colm3  <- sample(1:15, N, replace=TRUE) df_Temp <- data.frame(colm1, colm2,colm3) df_Temp$id<-seq(nrow(df_Temp)) df_Temp`

[Powered By](https://www.datacamp.com/datalab) 

The above code gives the following output where there are three columns named as 'colm1', 'colm2', 'colm3' and consists of id from 1 to 15. The values in the respective column are filled up from 1 to 15, where some numbers are repeated, whereas some numbers may not occur.

 `colm1   colm2   colm3  id   15      11     14     1   15      5      3      2   3       3      4      3   14      11     14     4   3       9      1      5   10      12     11     6   2       9      7      7   6       9      5      8   11      13     12     9   5       3      15     10   4       8      10     11   14      10     13     12   6       7      7      13   9       10     9      14  10       9      9      15` 

[Powered By](https://www.datacamp.com/datalab) 

### cbind function

**Usage**: used to combine vectors, matrix, and data frames by columns.  
**Parameters**:cbind(v1,v2): v1,v2 can be vectors, matrix or data frames

Let's see the example of binding in action.

id can be selected by 'df_Temp[,4]' whereas 'df_Temp[,2]' selects 'colm2' of df_Temp as below which acts as a parameter to 'cbind()' and gets stored in 'cbindexample' variable. Further, the column names can be changed through the help of 'colnames()' which accepts the variable with the vectors input c to a new value, i.e. 'newid', 'new_colm2'.

`cbindexample<-cbind(df_Temp[,4],df_Temp[,2]) colnames(cbindexample)<- c('newid','new_colm2') cbindexample`

[Powered By](https://www.datacamp.com/datalab) 

The above code gives the following output that you can bind two columns of id and column2 using 'cbind' function to make a new data frame. Also, the column name has been changed to 'new_colm2' whereas 'id' changed to 'newid'.

`newid   new_colm2 1         11 2         5 3         3 4         11 5         9 6         12 7         9 8         9 9         13 10         3 11         8 12         10 13         7 14         10 15         9`

[Powered By](https://www.datacamp.com/datalab) 

### rbind function:

**usage:** rbind used to combines the vectors, matrix, or data frames by columns.  
**Parameters:** rbind(v1,v2):v1,v2 can be vectors, matrix or data frames.

Let's create a new vector called 'new_vector' and combine it with a new 'cbindexample' of 2 columns by using 'rbind' where both are concatenated and stored to 'rbindexample'.

`new_vector<- c(16,15) rbindexample<- rbind(cbindexample,new_vector) rbindexample`

[Powered By](https://www.datacamp.com/datalab) 

The above code gives the output below where the new row is added with the values of 16 and 15, respectively, in 'newid' and 'new_colm2'.

`newid    new_colm2 1        11 2        5 3        3 4        11 5        9 6        12 7        9 8        9 9        13 10       3 11       8 12       10 13       7 14       10 15       9 16       15`

[Powered By](https://www.datacamp.com/datalab) 

### Melt Function:

**Usage:** Melt function used to convert an object to convert into a molten state, means that it takes multiple columns of data and convert it into a single column of data.  
**Parameters:** melt(data,…,na.rm=FALSE/TRUE, value.name=”value” ),  
**Data:** Input which you are going to melt.  
**...:** Input that is passed to or from.  
**Na.rm:** It is used to convert explicit missing values into implicit missing.  
**Value.name:**for storing values into variables  
Let's look at code that you 'molt' the data using the id variable into one column with column name and value:

Let's import the library named 'reshape2' using 'library()' and use melt to combine the 'dfTemp' columns called colm1,colm2,colm3 in a single place called 'variable' according to the 'id' variable.

`library(reshape2) molted=melt(df_Temp,id.vars=c("id")) molted`

[Powered By](https://www.datacamp.com/datalab) 

`id    variable value 1    colm1    15 2    colm1     15 3    colm1     3 4    colm1     14 5    colm1     3 6    colm1     10 7    colm1     2 8    colm1     6 9    colm1     11 10    colm1     5 11    colm1     4 12    colm1     14 13    colm1     6 14    colm1     9 15    colm1     10 1    colm2     11 2    colm2     5 3    colm2     3 4    colm2     11 5    colm2     9 6    colm2     12 7    colm2     9 8    colm2     9 9    colm2     13 10    colm2     3 11    colm2     8 12    colm2     10 13    colm2     7 14    colm2     10 15    colm2     9 1    colm3     14 2    colm3     3 3    colm3     4 4    colm3     14 5    colm3     1 6    colm3     11 7    colm3     7 8    colm3     5 9    colm3     12 10    colm3     15 11    colm3     10 12    colm3     13 13    colm3     7 14    colm3     9 15    colm3     9`

[Powered By](https://www.datacamp.com/datalab) 

The above output shows that when you molt the data of colm1, colm2, colm3 according to the id variable, it combined into one column named as 'variable' and the values of the column are contained in 'value'.

### Dcast function:

**Usage:** when you have a molten dataset then you can convert the molten dataset into an original format using this function.  
**Parameters:** dcast(data,id_variable~value),  
**data:** molten data which needs to convert into original form.  
**Id_variable:** single or multiple columns that used to molten the data of other columns into one column.  
**~:** after this sign, we use the values or new molted column of the molten dataset.

You can see below code where the 'reshape2' is imported using 'library()' where 'dcast()' takes the first parameter as the data which was performed 'molt()' function and the '~' sign with id where the new molted column gets formed.

`library(reshape2) dcast(molted,id~variable)`

[Powered By](https://www.datacamp.com/datalab) 

`id    colm1    colm2    colm3 1        15        11        14 2        15        5         3 3        3        3         4 4        14        11       14 5        3        9         1 6        10        12        11 7        2         9         7 8        6        9         5 9       11        13        12 10       5        3        15 11       4        8        10 12       14        10        13 13       6        7        7 14       9        10        9 15      10        9        9`

[Powered By](https://www.datacamp.com/datalab) 

You can see that the data changes after 'molt()' function gets changed to the original dataset. There are three columns with their respective values in the columns and id in the separate column.

### Transpose function:

**Usage:** It is used to change the rows into columns and columns into rows.  
**Parameters:** t(data), data is the data frame which you need to pass and get transpose.

Let's change the row to column and vice-versa by using the transpose function. It can be simply done by using 't(df_Temp)' as done below.

`trans <- t(df_Temp) trans`

[Powered By](https://www.datacamp.com/datalab) 

The above code gives following output:

`colm1    15    15    3    14    3    10    2    6    11    5    4    14    6    9    10 colm2    11    5    3    11    9    12    9    9    13    3    8    10    7    10    9 colm3    14    3    4    14    1    11    7    5    12    15    10    13    7    9    9 id    1    2    3    4    5    6    7    8    9    10    11    12    13    14    15`

[Powered By](https://www.datacamp.com/datalab) 

You can see that the data frame having the shape of 15 rows and four columns is changed into 15 columns and 3 rows by getting transpose of data.