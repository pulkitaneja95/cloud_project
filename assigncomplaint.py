import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    
    phone_no = event['phone']
    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('demoTable')
    
    dynamoTable.update_item(
        Key={
           "phone_no": phone_no
        },
        UpdateExpression="set assigned = :p",
        ExpressionAttributeValues={
            ':p': 'user1'
        },
        ReturnValues="UPDATED_NEW"
    )
    
    
    return "assigned"
