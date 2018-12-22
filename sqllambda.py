import json
import base64
import boto3
from botocore.vendored import requests


def lambda_handler(event, context):

    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/956378083355/ProjectQueue'
    
    #Read messages from queue
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            MessageAttributeNames=['All']
        )
    except:
        return
    messages = response['Messages']
    
    # session = boto3.Session(profile_name='default')
    # rekognition = session.client('rekognition')
    rekognition = boto3.client('rekognition')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Tickets2')

    
    for message in messages:
        
        message_body = message['Body']
        message_body = json.loads(message_body)
        id = list(message_body.keys())[0]
        
        receipt_handle = message['ReceiptHandle']
        
        image_url = message_body[id]
        image_url = image_url[image_url.index("h"):]
        
        if(image_url == 'no'):
            continue
        response = requests.get(image_url)
        response_content = response.content
        
        label_response = rekognition.detect_labels(Image={'Bytes': response_content})
        
        labels=[]
        for label in label_response['Labels']:
            labels.append(label['Name'])
            
        
        response = table.update_item(
            Key={
               "id": id
            },
            UpdateExpression="set rekogtags = :a",
            ExpressionAttributeValues={
                ':a': labels
            },
            ReturnValues="UPDATED_NEW"
        )
        
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )