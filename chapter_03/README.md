### Brief Description of Chapter 03
This chapter is not programmable. Of course not UI work. But it is fulfilled by bash and sql comments runned in CLI. We will
inject scraped data into instance of Cloud SQL, and generate a dashboard 

#### Previous Review
After going through Chapter_02, we have 12 csv files involving flights records from January 2015 to December 2015, stored 
in Cloud Storage. 

The work of this chapter consists of the following in order.

#### 1. Create Instance of Cloud SQL

    bash create_cloud_sql_instance.sh

In the UI of Cloud SQL, it finds a new created instance named "flights", its type is 'MySQL 5.7', 
status of 'High availability' is ADD (enabled). This is an empty instance now. We content it. 


#### 2. Create Table of The Instance of Cloud SQL
    
    bash create_table_in_sql_instance.sh
    
Now you can find an empty table with 27 features (27 columns). The UI of Cloud SQL cannot show the existence. 
We need to use the following commands in the terminal.

    mysql --host=public_ip_address_of_cloud_sql_instance --user=root --password=generated_by_openssl

Then the terminal will be switch to the CLI of MySQL, there should be a database named 'bts' where we can find the new created table 'flights'. Just go through the following steps

    mysql> use bts             # command 
    Database changed           # response from mysql
    mysql> describe flights;   # command
    +-----------------------+-------------+------+-----+---------+-------+
    | Field                 | Type        | Null | Key | Default | Extra |
    +-----------------------+-------------+------+-----+---------+-------+
    | FL_DATE               | date        | YES  |     | NULL    |       |
    | UNIQUE_CARRIER        | varchar(16) | YES  |     | NULL    |       |
    | AIRLINE_ID            | varchar(16) | YES  |     | NULL    |       |
    | CARRIER               | varchar(16) | YES  |     | NULL    |       |
    ......
    
It showed all the features and related properties. We check it has no content by looking into the first column 

    mysql> select DISTINCT(FL_DATE) from flights;

It will return that no content can be found in the table. 

#### 3. Populate Data In Table And Create Views of The Table (data from csv in Cloud Storage)

It is time to populate the empty table with flight records of Jan 2015 and Jul 2015. 
That means, extract the data from the csv files, 201501.csv and 201507.csv, and inject into the table.

    bash populate_table_with_csv_from_gcloud_storage.sh

Please note that the core tool, **_mysqlimport_**, cannot read directly from Cloud Storage. So we copy the target
file to the local directory, then use **_mysqlimport_** to read the data and inject to the table.

#### 4. Contingency Table / Confusion Matrix

The book calculated three contingency tables with three departure delay minutes, 10 minutes, 15 minutes and 20 minutes.

    bash bash contingengcy_table_10_minutes_departure_delay.sh 
    
    # the below are responds ....
    
    mysql: [Warning] Using a password on the command line interface can be insecure.
    --------------
    select count(dest) from flights where arr_delay < 15 and dep_delay < 10
    --------------
    
    count(dest)
    713545
    --------------
    select count(dest) from flights where arr_delay >= 15 and dep_delay < 10
    --------------
    
    count(dest)
    33823
    --------------
    select count(dest) from flights where arr_delay < 15 and dep_delay >= 10
    --------------
    
    count(dest)
    73563
    --------------
    select count(dest) from flights where arr_delay >= 15 and dep_delay >= 10
    --------------
    
    count(dest)
    169755

The above is calculation of contingency table of 10 minutes. The calculation of 15 minutes and 20 minutes has similar form. 
I agree with the book said 10 minutes is the best, because it has the smallest number of Type-1 error. 
In this case, the Type-I error is the counting number of _"**dep_delay >= some number**"_ (cancel the meeting) conditioned on _"**arr_delay >= 15**"_.
        

#### 5. Problem of Generating Dashboard as the book

Now we have data in Cloud SQL which can be data resource of Data Studio. Naturally, the book uses Data Studio to make a report. 
The report is a pdf (_flightsRecordsfromBTS.pdf_) file can be checked. We skip the steps (UI work) to generate the report. 
But I have to mention one point :

The book created three more views of table than build one more columns. Then the views were used as data source to charts. 
The inconvenience is that, the data source managing UI in DataStudio does not show tables' names, only the database name. So it would
be confused to check which data source standing behind which charts. 
