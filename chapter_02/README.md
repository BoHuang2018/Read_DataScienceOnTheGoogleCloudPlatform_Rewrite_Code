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
1. 


