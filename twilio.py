import json
import urllib
import boto3

def lambda_handler(event, context):
    print("Received event: " + str(event))
    
 
    
    client = boto3.client('lex-runtime')
    url = ''
    if 'MediaUrl0' in event:
        url = urllib.parse.unquote(event['MediaUrl0'])
        response = client.post_text(
       
            botName='cloudproject',
            botAlias='dev',
            userId= urllib.parse.unquote(event['From'])[1:],
            sessionAttributes={
                'string': 'string'
            },
            requestAttributes={
                'string': 'string'
            },
            inputText ='xxxxxxxx'+url
            )
        
    else:
        response = client.post_text(
       
            botName='cloudproject',
            botAlias='dev',
            userId= urllib.parse.unquote(event['From'])[1:],
            sessionAttributes={
                'string': 'string'
            },
            requestAttributes={
                'string': 'string'
            },
            inputText =event['Body']
            )
        
    print(response)

    #return format to Twilio via API Gateway
    return ('<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response><Message>' + response['message'] + '</Message></Response>')