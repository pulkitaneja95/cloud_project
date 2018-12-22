import json
import boto3

dynamodb = boto3.resource('dynamodb')
dynamoTable = dynamodb.Table('demoTable')

def lambda_handler(event, context):
    # TODO implement

    data=dynamoTable.scan()
    print(data['Items'])

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(data['Items'])
    # }
    
    return data['Items']
