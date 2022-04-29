import requests
import pandas as pd
import time
import datatime as dt
from datetime import timedelta
import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


dataframes = []

def request_scf():
    url = 'https://seeclickfix.com/api/v2/issues?'
    params = {'place_url': 'bernalillo-county', 'per_page': '200'}
    r = requests.get(url, params=params)
    r = r.json()
    print(r['metadata']['pagination']['pages'])
    df = pd.json_normalize(r, record_path="issues")
    dataframes.append(df)
    # while r['metadata']['pagination']['page'] <= r['metadata']['pagination']['pages']:
    for i in range(10):
        if r['metadata']['pagination']['page'] <= i:
            time.sleep(1)
            print(r['metadata']['pagination']['page'])
            url = r['metadata']['pagination']['next_page_url']
            if url == None:
                break
            else:
                r = requests.get(f'{url}', params=params)
                r = r.json()
                df = pd.json_normalize(r, record_path="issues")
                dataframes.append(df)

def concat_dfs(dataframes):
    full_df = pd.concat(dataframes)
    full_df.to_csv('/Users/mike/Desktop/Main/Programming/Projects/Tutorials/311/scf_issues.csv', index=False)


def drop_columns():
    df = pd.read_csv('/Users/mike/Desktop/Main/Programming/Projects/Tutorials/311/scf_issues.csv')
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
    df.to_csv('/Users/mike/Desktop/Main/Programming/Projects/Tutorials/311/scf_issues.csv', index=False)


def convert_to_datetime():
    df = pd.read_csv('/Users/mike/Desktop/Main/Programming/Projects/Tutorials/311/scf_issues.csv')
    cols = ['created_at', 'acknowledged_at', 'closed_at', 'reopened_at', 'updated_at']
    for col in cols:
        df[col] = pd.to_datetime(df[col])
    df.to_csv('/Users/mike/Desktop/Main/Programming/Projects/Tutorials/311/scf_issues.csv', index=False)


def drop_null_descriptions():
    '''Drop all rows where summary and description columns are null'''

    df = pd.read_csv('/Users/mike/Desktop/Main/Programming/Projects/Tutorials/311/scf_issues.csv')
    orig_df_len = len(df.index)
    new_df = df.dropna(axis='index', how='all', subset=['summary', 'description'])
    new_df_len = len(new_df.index)
    new_df.to_csv('/Users/mike/Desktop/Main/Programming/Projects/Tutorials/311/scf_issues.csv', index=False)
    return f'Total rows dropped: {orig_df_len - new_df_len}'


def insert_elasticsearch():
    from elasticsearch import Elasticsearch
    host = os.environ.get('ELASTIC_HOST')
    password = os.environ.get('ELASTIC_PASSWORD')
    cert = os.environ.get('ELASTIC_CERT')
    es = Elasticsearch(host, ca_certs=cert, basic_auth=("elastic", password))

    df = pd.read_csv('/Users/mike/Desktop/Main/Programming/Projects/Tutorials/311/scf_issues_test.csv')
    for i, r in df.iterrows():
        doc = r.to_json()
        res = es.index(index="seeclickfix2", document=doc)
        print(res)


def query_elasticsearch():
    from elasticsearch import Elasticsearch
    host = os.environ.get('ELASTIC_HOST')
    password = os.environ.get('ELASTIC_PASSWORD')
    cert = os.environ.get('ELASTIC_CERT')
    es = Elasticsearch(host, ca_certs=cert, basic_auth=("elastic", password))

    query = {"matchall":{}}
    res = es.search(index='seeclickfix', size=10, query=query)
    for doc in res['hits']['hits']:
        print(doc['_source'])


default_args = {
    'owner': 'mike',
    'start_date': dt.datetime(2022, 4, 29),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)
}

with DAG('seeclickfix',
         default_args=default_args,
    schedule_interval=timedelta(minutes=30)) as dag:

    query_scf = PythonOperator(task_id='Query_SCF',
                               pythoncallable=query_scf)

    concat_df = PythonOperator(task_id='Concat_DFs',
                               pythoncallable=concat_dfs)

    drop_columns = PythonOperator(task_id='Drop_Columns',
                                  pythoncallable=drop_columns)


    insert_data = PythonOperator(task_id='InsertDataElasticsearch',
                                 python_callable=insert_elasticsearch)