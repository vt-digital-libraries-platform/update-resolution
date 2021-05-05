import boto3
from boto3.dynamodb.conditions import Attr
import json
import os
from datetime import datetime
import requests

# Environment variables
collection_category = os.getenv('Collection_Category')
region_name = os.getenv('Region')
collection_table_name = os.getenv('Collection_Table')
archive_table_name = os.getenv('Archive_Table')
mint_table_name = os.getenv('Mint_Table')
long_url_path = os.getenv('Long_URL_Path')
short_url_path = os.getenv('Short_URL_Path')
noid_scheme = os.getenv('NOID_Scheme')
noid_naa = os.getenv('NOID_NAA')
api_key = os.getenv('API_Key')
api_endpoint = os.getenv('API_Endpoint')

try:
    dyndb = boto3.resource('dynamodb', region_name=region_name)
    archive_table = dyndb.Table(archive_table_name)
    collection_table = dyndb.Table(collection_table_name)
    mint_table = dyndb.Table(mint_table_name)
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
    raise e

def fetch_short_ids():
    try:
        response = mint_table.scan(
            FilterExpression=Attr('created_at').not_exists()
        )
        mint_table_items = response['Items']
        print(f"The number of missing items found: {len(mint_table_items)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    return mint_table_items

def get_long_url(short_id, table_name, category_type, item_type):
    custom_key = noid_scheme + noid_naa + "/" + short_id
    long_url = None
    try:
        scan_kwargs = {
            'FilterExpression': Attr(category_type).eq(collection_category) & Attr('custom_key').eq(custom_key),
            'ProjectionExpression': "#id",
            'ExpressionAttributeNames': {"#id": "id"}
        }
        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = table_name.scan(**scan_kwargs)
            if len(response['Items']) > 0:
                done = True
                long_url = long_url_path + item_type + "/" + short_id
            else:
                start_key = response.get('LastEvaluatedKey', None)
                done = start_key is None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    return long_url

def update_NOID(long_url, short_url, noid, create_date):
    headers = { 'x-api-key': api_key }
    body = "long_url=" + long_url + "&short_url=" + short_url + "&noid=" + noid + "&create_date=" + create_date
    url = api_endpoint + 'update'
    response = requests.post(url, data=body, headers=headers)
    print(f"update_NOID: {response.text}")

def lambda_handler(event, context):
    try:
        for item in fetch_short_ids():
            if "short_id" in item:
                short_id = item["short_id"]
                long_url = None
                long_url = get_long_url(short_id, collection_table, 'collection_category', 'collection')
                if long_url is None:
                    long_url = get_long_url(short_id, archive_table, 'item_category', 'archive')
                if long_url is not None:    
                    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    short_url = short_url_path + noid_scheme + noid_naa + "/" + short_id
                    update_NOID(long_url, short_url, short_id, now)
                else:
                   print(f"Could not find short_id: {short_id}") 
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Process completed.",
            }),
        }
    
    except Exception as e:
        # Send some context about this error to Lambda Logs
        print(e)
        raise e
