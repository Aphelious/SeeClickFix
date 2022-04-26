import requests
import pandas as pd
import time


# import json
# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from airflow.operators.python import PythonOperator


dataframes = []

def request_scf():
    url = 'https://seeclickfix.com/api/v2/issues?'
    params = {'place_url': 'bernalillo-county', 'per_page': '200', "status": "Archived"}
    r = requests.get(url, params=params)
    r = r.json()
    print(r['metadata']['pagination']['pages'])
    df = pd.json_normalize(r, record_path="issues")
    dataframes.append(df)
    # while r['metadata']['pagination']['page'] <= r['metadata']['pagination']['pages']:
    #     time.sleep(2)
    #     print(r['metadata']['pagination']['page'])
    #     url = r['metadata']['pagination']['next_page_url']
    #     if url == None:
    #         break
    #     else:
    #         r = requests.get(f'{url}', params=params)
    #         r = r.json()
    #         df = pd.json_normalize(r, record_path="issues")
    #         dataframes.append(df)

def concat_dfs(dataframes):
    full_df = pd.concat(dataframes)
    return full_df


def drop_columns(df):
    cols = ['flag_url',
           'comment_url',
           'request_type.url',
           'request_type.related_issues_url',
           'reporter.avatar.full',
           'reporter.avatar.square_100x100',
           'media.image_square_100x100',
           'reporter.civic_points',
           'transitions.open_url',
           'transitions.close_url',
           'media.representative_image_url',
           'media.image_full',
           'reporter.witty_title',
           'media.representative_image_url',
           'shortened_url',
           'reporter.role',
           'private_visibility',
           'url']
    df.drop(columns=cols, inplace=True)
    return df


def insert_elasticsearch():
    from elasticsearch import Elasticsearch
    host = 'https://localhost:9200'
    ELASTIC_PASSWORD = "Q0AYUcVWmef*wPgMOGHj"
    cert = "/Users/mike/elasticsearch-8.1.2/config/certs/http_ca.crt"
    es = Elasticsearch(host, ca_certs=cert, basic_auth=("elastic", ELASTIC_PASSWORD))

    df = pd.read_csv('/Tutorials/311/AF_Version/scf_issues_all_active.csv')
    for i, r in df.iterrows():
        doc = r.to_json()
        res = es.index(index="seeclickfix", document=doc)
        print(res)


def query_elasticsearch():
    from elasticsearch import Elasticsearch
    host = 'https://localhost:9200'
    ELASTIC_PASSWORD = "Q0AYUcVWmef*wPgMOGHj"
    cert = "/Users/mike/elasticsearch-8.1.2/config/certs/http_ca.crt"
    es = Elasticsearch(host, ca_certs=cert, basic_auth=("elastic", ELASTIC_PASSWORD))

    query = {"match":{"name": "Ashley Morgan"}}
    res = es.search(index='seeclickfix', size=10, query=query)
    for doc in res['hits']['hits']:
        print(doc['_source'])




