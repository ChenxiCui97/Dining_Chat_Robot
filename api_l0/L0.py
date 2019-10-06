import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    id_recieved = '19953647'
    content_recieved = 'hi'
    if len(event) > 0:
        id_recieved = event['id']
        content_recieved = event['content']
    client = boto3.client('lex-runtime')
    botresponse = client.post_text(
        botName='OrderDishes',
        botAlias='sara',
        userId=id_recieved,
        sessionAttributes={},
        requestAttributes={},
        inputText=content_recieved
    )
    
    
    response = {}
    response["id"] = id
    response["content"] = botresponse["message"]
    # response['other'] = [id_recieved,content_recieved]
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
