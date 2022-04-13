'''

import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

'''
import json
import boto3
import requests
import time

def lambda_handler(event, context):
    #getting the photo details 
    s3_info = event['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']

    s3 = boto3.client('s3')
    tresponse = s3.head_object(Bucket=bucket_name, Key=key_name)
    clabel = tresponse["ResponseMetadata"]["HTTPHeaders"]["x-amz-meta-customlabels"]
    dans = []
    if(clabel == "*" or clabel == ""):
        dans = []
    else:
        nlabel = clabel.split(",")
        nlabel = [x.strip(' ') for x in nlabel]
        dans = nlabel
        
    #connect to rekognition client 
    client = boto3.client('rekognition')
    pass_object = {'S3Object':{'Bucket':bucket_name,'Name':key_name}}
    resp = client.detect_labels(Image=pass_object)
    timestamp=time.time()
    

    #label creation 
    labels = []
    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])
    labels = labels + dans
    
    
    print('<------------Now label list----------------->')
    print(labels)
    #print('<------------Now required json-------------->')
    format = {'objectKey':key_name,'bucket':bucket_name,'createdTimestamp':timestamp,'labels':labels}
    
    
    url = "https://search-photos-7yuqxqmmovsewjxdwkver6e2mq.us-east-1.es.amazonaws.com/photo/_doc/"
    headers = {"Content-Type": "application/json"}
    r = requests.post(url,auth=('himanshu', 'London@1985'),data=json.dumps(format).encode("utf-8"), headers=headers)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }