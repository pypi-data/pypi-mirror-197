import mysql.connector
import requests
import hashlib
from . import api
import json

def get_credentials(api_key, api_schema, db_schema):
    response = requests.get(f"{api_schema}/api/db_credentials", headers={'key': api_key, 'db':db_schema}).json()
    if response['msg'] == 'success':
        return response['data']
    else:
        print(response)
        return None


def get(api_key, api_schema=None, db_schema=None,  buffered=True, dictionary=False):
    if not api_schema:
        api_schema = api.prod

    credentials = get_credentials(api_key=api_key, api_schema=api_schema, db_schema=db_schema)
    if not credentials:
        return None, None
    cnx = mysql.connector.connect(
        user=credentials['user'],
        password=credentials['password'],
        host=credentials['host'],
        database=credentials['database']
    )
    
    cur = cnx.cursor(buffered=buffered, dictionary=dictionary)
    return cnx, cur


def hash(url):
    return hashlib.sha256(url.encode()).hexdigest()


def convert_json(records):
    """
    checks if column title has '_json' in string and converts to dict
    make sure that all json columns have _json in title (and only json columns)
    """
    if records and isinstance(records[0], dict):
        for record in records:
            for column, value in record.items():
                if '_json' in column:
                    record[column] = json.loads(value)
    return records



def null2None(records, dictionary=True):
    result = []
    for record in records:
        if isinstance(record, dict):
            for col_name, val in record.items():
                if val == 'null':
                    record[col_name] = None
        else:
            record = list(record)
            for i, val in enumerate(record):
                if val == 'null':
                    record[i] = None
            record = tuple(record)

        result.append(record)
    return result

if __name__ == '__main__':
    records = [{'id': 1,
  'url': 'https://newsroom.porsche.com/de/unternehmen.html',
  'name': 'porsche_com',
  'request_params': 'null',
  'file_path': None,
  'headers': None,
  'next_content_update': None,
  'content_type': None,
  'update_cycle': 'null',
  'link_index': 'null',
  '_status': ''},
 {'id': 2,
  'url': 'https://ffg-ea.com/de/unternehmen/news/',
  'name': 'ffg_ea_com',
  'request_params': 'null',
  'file_path': None,
  'headers': None,
  'next_content_update': None,
  'content_type': None,
  'update_cycle': 'null',
  'link_index': 'null',
  '_status': None}]
    
    print(null2None(records))