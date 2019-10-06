import json
from botocore.vendored import requests
import random
import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    # TODO implement
    # sqs
    sqs = boto3.client('sqs')
    queue = sqs.get_queue_url(QueueName='info_u')
    queue_info = sqs.receive_message(QueueUrl=queue['QueueUrl'])
    print(json.dumps(queue_info, indent=2))
    content = queue_info["Messages"][0]['Body']
    handle = queue_info["Messages"][0]['ReceiptHandle']
    # print(handle)
    content = json.loads(content)
    phone = content['PhoneNumber']
    phonenum = '+1' + phone
    time = content['DiningTime']
    date = content['DiningDate']
    people = content['NumberofPeople']
    type = str.lower(content["Cuisine"])
    sqs.delete_message(
        QueueUrl=queue['QueueUrl'],
        ReceiptHandle=handle
    )

    # elasticsearch
    es_url = 'https://search-mynewdomain-xzn5s76muhhpsfdm3eaizf4pre.us-east-2.es.amazonaws.com/restaurants/_search?q=' + type + '&size=500'
    response = requests.get(es_url)
    data = response.json()
    i = random.randint(0, 496)
    rest_id = data["hits"]["hits"][i]["_source"]["RestaurantID"]
    rest_id2 = data["hits"]["hits"][i + 1]["_source"]["RestaurantID"]
    rest_id3 = data["hits"]["hits"][i + 2]["_source"]["RestaurantID"]
    rest_ids = [rest_id, rest_id2, rest_id3]
    # dynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('yelp-restaurants')
    Message = 'DCC: Hello! Here are my ' + type.capitalize() + ' restaurant suggestions for ' + people + ' people, for ' + date + ' at ' + time + ':'
    for i in range(0, 3):
        response = table.query(
            KeyConditionExpression=Key('BusinessID').eq(rest_ids[i])
        )
        name = response['Items'][0]['Name']
        address = response['Items'][0]['Address']
        reviews = response['Items'][0]['Number of Reviews']
        rating = response['Items'][0]['Rating']
        Message = Message + ' ' + str(
            i + 1) + '. ' + name + ', located at ' + address + ' with the rating of ' + rating + ' and ' + reviews + ' reviews.'
    Message = Message + " Enjoy your meal!"
    # SNS
    sns = boto3.client('sns')
    sns.publish(
        PhoneNumber=phonenum, Message=Message
    )
    return {
        'statusCode': 200,
        'elasticsearch': json.dumps(rest_id),
        'db_rest_name': json.dumps(name),
        'db_rest_address': json.dumps(address),
        'db_rest_rating': json.dumps(rating),
        'db_rest_reviews': json.dumps(reviews),
        'message': Message,
        'queue': queue_info,
        'randon': i,
        'phone': phonenum
    }
