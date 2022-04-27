##SeeClickFix ETL pipline project

---

###Objective:

This project represents my first ETL pipeline, giving me experience finding
and connecting to interesting public data sources and APIs, exploring and 
analysing the dataset, cleaning it, migrating it to other systems, and 
ultimately creating a dashboard to create useful visualizations of the data.

###Implementation:

Python scripts, orchestrated with Apache Airflow, connect to the SeeClickFix
API and load the data into a Pandas dataframe. From there, Pandas methods are 
used to clean the data. There were a total 41 columns in the dataframe and 
many were storing broken or redundant web links back to the API data itself. 
These columns were dropped resulting in a dataset half the size. There were 
also dates stored as strings which I then converted to proper datetimes.

I then migrated the dataset to Elasticsearch, which was actually a pretty 
straight-forward process. I also found a Python library that I may try out in 
the future called 'es-pandas', which might make the process even easier or 
be better in terms of data integrity -more research will be done into this 
package.

###Requirements:

This application requires...

###