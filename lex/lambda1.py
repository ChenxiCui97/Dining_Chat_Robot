import json
from botocore.vendored import requests
from urllib.parse import quote
import boto3
import logging



def lambda_handler(event, context):
   

    response = {"dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Message to convey to the user."
                }
    }
    }


    return dispatch(event)
def dispatch(event):
    

    intent = event['currentIntent']['name']
    logging.info(event)
    print('fef', event)
    
    if intent == "GreetingIntent":
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Hi there, how can I help?"
                }
            }
        }

    elif intent == "ThankYouIntent":
        return {"dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "You are more than welcome"
                }
                }
                }
    elif intent == "DiningSuggestionsIntent":
        slot = event['currentIntent']['slots']
        location = slot['Location']
        foodtype = slot["Cuisine"]
        people = slot['NumberofPeople']
        date = slot['DiningDate']
        time = slot['DiningTime']
        
        phone = slot['PhoneNumber']
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName='info_u')
        message = json.dumps(slot)
        logging.info(message)
        print('fef', message)
        response = queue.send_message(MessageBody=message)
        Messageshow= "Your location is "+location+". You want "+people+" people to have "+foodtype+" at "+ date+" "+time+". Your phone is"+ phone+ ". We will inform you via text message a few minute later."
        print(Messageshow)
        return {"dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": Messageshow
                }
                }
                }
    else:
        return {"dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "I cannot give you restaurant suggestion."
                }
                }
                }
                
