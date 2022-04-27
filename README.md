##SeeClickFix ETL pipline project

SeeClickFix is an application some local municipalities uses to track resident's
complaints about anything from graffiti, abandoned cars, broken fire hydrants, 
etc.

---

###Objective:

This project represents my first ETL pipeline, giving me experience finding
and connecting to interesting public data sources and APIs, exploring and 
analysing the dataset, cleaning it, migrating it to other systems, and 
ultimately creating a dashboard to create useful visualizations of the data.

###Implementation:

A Python script/DAG, orchestrated with Apache Airflow, connects to the SeeClickFix
API and loads the data into a Pandas dataframe. From there, Pandas methods are 
used to clean the data. There were a total 41 columns in the dataframe and 
many were storing broken or redundant web links back to the API data itself. 
These columns were dropped resulting in a dataset half the size. There were 
also dates stored as strings which I then converted to proper datetimes.

I then migrated the dataset to Elasticsearch, which was actually a pretty 
straight-forward process. I also found a Python library that I may try out in 
the future called 'es-pandas', which might make the process even easier or 
be better in terms of data integrity -more research will be done into this 
package.

The primary reason for incorporating Elasticsearch was to take advantage 
of the Kibana dashboard tools, which I now see are quite powerful and provide 
for very fast development. I created a few visualizations (samples below)
that display the total number of records, a bar graph showing submitted 
complaints over time, a pie/donut chart showing the proportion of the top
complaint types. 

It is my goal to find a dashboard tool to develop directly from Python but 
there are many available and I'm still researching which I'd like to learn. 

###Visualizations:



###