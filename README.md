##SeeClickFix ETL pipeline project

SeeClickFix is an application some local municipalities uses to track resident's
complaints about anything from graffiti, abandoned cars, broken fire hydrants, 
etc. It includes a public API from which records, in JSON format, can be 
requested.   

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

I then migrated the dataset to Elasticsearch, which was for the most part a 
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

###Challenges:

The greatest challenge with this project was maintaining data integrity
while migrating the data between these various systems. In particular, I had an
issue writing directly from Pandas to Elasticsearch, as my latitude/longitude
coordinate pairs ended up in the wrong format/data type for Elasticsearch/Kibana
to recognize them as such. The issue turned out to be Pandas' datatype inference
that happens under the hood. I had to be more explicit in the way I was writing 
the records to Elasticsearch in order for the correct data types to be preserved. 
I now know that while Pandas is a powerful library for quickly exploring and 
modifying data it should probably be avoided as the final write engine. 

###Visualization samples:

![Bar graph of complaints over past 4 years](./assets/scf-bar.png 
"Bar graph of complaints over past 4 years")

![Pie/donut chart of complaint types](./assets/scf-pie.png 
"Pie/donut chart of complaint types")

![Screenshot of Airflow DAG run](./assets/scf-dag-in-action.png 
"Screenshot of Airflow DAG run")