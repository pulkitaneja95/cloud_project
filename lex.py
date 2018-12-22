import json
import boto3
import datetime

import random as r
import datetime


def generate_uuid():
    

    td = datetime.datetime.now()
    if td.month < 10:
        month = str(0) + str(td.month)
    else:
        month = str(td.month)
    if td.day < 10:
        day = str(0) + str(td.day)
    else:
        day = str(td.day)

    half_year = str(td.year % 100)
    random_string = 'C'
    date = str(month + day + half_year)
    random_string += str(date)
    random_str_seq = "0123456789"
    uuid_format = [7, 7]

    for n in uuid_format:
        if n != 10:
            random_string += '-'
        for i in range(0, n):
            random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])

    
    return random_string

def lambda_handler(event, context):
    # TODO implement
    if(event['currentIntent']['name'] == 'log_request'):
        dynamodb = boto3.resource('dynamodb')
        dynamoTable = dynamodb.Table('Tickets2')
        complaint_number = generate_uuid()
        
        dic = {
            "id": complaint_number,
            "value":event['currentIntent']['slots']
        }
        
        if 'image' in event['currentIntent']['slots']:
            sqs = boto3.resource('sqs')
            queue = sqs.get_queue_by_name(QueueName='ProjectQueue')
            response = queue.send_message(MessageBody=json.dumps({complaint_number:event['currentIntent']['slots']['image']}))
            
            
        # dynamoTable.put_item(Item = dic)
        
        dynamoTable.put_item(Item = dic)
    
        session_attributes = event['sessionAttributes'] if event['sessionAttributes'] is not None else {}
        
        reply = {
                "dialogAction": {
                                "type": "Close",
                                "fulfillmentState": "Fulfilled",
                                "message": {
                                  "contentType": "PlainText",
                                  "content": "Your complaint has been registered. Your complaint number is: " + complaint_number
                                            }
                                }
            }
    
        
       
        
    
        return reply
    return "test"