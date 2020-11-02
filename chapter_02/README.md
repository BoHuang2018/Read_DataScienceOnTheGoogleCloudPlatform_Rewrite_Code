### Brief description of Contents
Data collection is a precondition of all data science and/or data engineering work. The project of the whole book is to do some 
data science work on USA's flights record. 

Briefly speaking, what this chapter doing is to scrape USA's domestic flights records from 
https://transtats.bts.gov/DL_SelectFields.asp?Table_ID=236 
by scripts in python, store the data for further usage. And append the storage regularly.

Of course, there finds a sequence of steps we need to walk through to do the job.

#### Working List in Order
1. Send a request with proper parameters (fields of tabular data) to the URL, then get response including required data in zip.
2. Unzip the scraped data to csv.
3. Clean and verify the csv is qualified.
4. Store the qualified data in a bucket of Cloud Storage (GCP) 
`(The above four works are wrapped in one python function.)`
5. Schedule the function running the above four tasks, to extend stored data regularly. 

#### Architecture on GCP
To implement the data collection work on GCP, we need to use the following GCP products
1. Cloud Function 
   * to run the the python function wrapping up the above works from 1 to 4
2. Cloud Storage
   * to store the scraped data (csv)
3. Cloud Schedular
   * to invoke the instance of cloud function regularly

#### Tutorial with code snips
Now let's go though the work list and see expected results step by step.

##### Precondition
We need a project (billed) on GCP. If you run the code on the Cloud Shell on GCP (like the book's author did), 
no more configuration will be needed. If you run the code on your PC (like me, on my Macbook), you will need to install the _gloud command line tool_,
(https://cloud.google.com/sdk/gcloud). And python3.8 need to be installed. 

##### Create Bucket on Cloud Storage
It is quite initial to use the UI (GCP console) to create a bucket, so we skip the details here. 
The only thing we need to mention here is bucket naming pattern. The recommended name is _project-name-add-something_.
For example, the project name is "pretty-project", we add "ugly-bucket", 
so the bucket name will be "pretty-project-ugly-bukcet".

In the new created bucket, we need to use the button "CREATE FOLDER" to create a folder named 'flights', 
then, create a child folder named 'raw' in the flights. The completed path in the bucket is 

    `pretty-project-ugly-bukcet/flights/raw`

This is where we store scraped data.

##### Deploy Cloud Functions Instance
In the book, the author tested the code locally (on the Cloud Shell, so it should be locally on a virtual machine). 
Here, we run it directly on the instance of Cloud Functions. In my eyes, Cloud Functions has better generality than single machine. 
1. ***Prepare configuration parameters and token***
To the issue of security, we generate a token which will be embedded into code and name of the instance of Cloud Functions.
    
    `cd chapter_02/monthly_flights_data_collecter`
    
    `bash generate_token.sh`
    
    It returns a token consists of a sequence of random characters. Copy the token and paste into a file, gcp_configuration.sh, in the same 
    directory. Besides the token, we need to put value of PROJECT, BUCKET, REGION, CLOUD_FUNCTION into the file.
    So the content of the file would looks like
    
    `PROJECT=name of GCP project`
    
    `BUCKET=name of bucket in Cloud Storage`
    
    `REGION=some region of GCP`
     
    `CLOUD_FUNCTION=flights_data_collect_the_new_generated_token_stay_here`
    
    `TOKEN_RUN_CLOUD_FUNCTION=the_new_generated_token_stay_here`
    
    Then, use .gitignore to avoid this gcp_configuration file.

2. ***Deploy Cloud Functions***
    
    All code (bash) is ready to use in a bash file. Just use it 
    
    `bash cloud_function_deploy_run_with_security_layer/call_cloud_function_trigger_url_to_collect_data_of_2015.sh`
    
    After some seconds, we can see a instance of Cloud Functions on the GCP console. The name would be "_flights_data_collect78jdf..._", 
    the wield characters after '_flights_data_collect_' is the token we generated. This instance has an unguessable name. 
    
    Please note the value of 'Memory allocated' is "1GiB", the value in the book is default as "256MiB". In my tests, "256MiB" was not enough and led to errors. 

    Now we can use the deployed function to collect flight records.

3. ***Collect Flight-Records In Batch***
   
   In the following chapters, object of data work is the flights record of 2015. So we need to scrape the flight-records 
   from January 2015 to December 2015, and store the data in the bucket of Cloud Storage. This can be done as 
   (the current path is `/Read_DataScienceOnTheGoogleCloudPlatform_Rewrite_Code/chapter_02/monthly_flights_data_collecter
`)
   
   `bash cloud_function_deploy_run_with_security_layer/call_cloud_function_trigger_url_to_collect_data_of_2015.sh
`    

   After one or two minutes, in the bucket, you will see twelve new csv files, 201501.csv, 201502.csv, ..., 201512.csv.
   All of the data has been verified and cleared. 

4. ***Regular Data Updating with Cloud Scheduler***
    
    Usually, we need to keep scraping new upcoming data to update the analysis. Now we have all data of 2015 stayed in 
    the bucket of Cloud Storage. We use Cloud Scheduler to make the Cloud Function run once a month to scrape next month's 
    flight record. The work flow is 
    
    (1). Detect the latest month of data in the bucket of Cloud Storage
    
    (2). Generate the parameters of month and year to scrape data of "next month"
    
    (3). Append new scraped data to the bucket of Storage if the scraping succeed.
    
    The above steps will be implemented at given time point. In addition, Cloud Scheduler has a button of 'RUN NOW', to run 
    the instance of Cloud Functions whenever you want. 
    
    The code to configure Cloud Scheduler is ready in the bash file `setup_cloud_scheduler.sh`. Just use it
    
    `bash setup_cloud_scheduler.sh`
    
    In the UI of Cloud Scheduler of GCP Console, it will find a new instance named "flights_data_collect_workflow", the value 
    of the column named "Target" is URL of the instance of Cloud Functions. In the column named "Run", we see a button named 
    "RUN NOW". Clicking the button, the function will scrape the data of January 2016 from the website of BTS.
