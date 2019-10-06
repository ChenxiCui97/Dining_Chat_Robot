import json

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']
    
def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
    
    
    
def lambda_handler(event, context):
   

    response = {"dialogAction": {
        "type": "Close",
        "message": {
            "contentType": "PlainText",
            "content": "Message to convey to the user."
        }
    }
    }

    return dispatch(event)
def elict(slots,slot,mess):
    return {"dialogAction": {
           'type': 'ElicitSlot',
            'intentName': "DiningSuggestionsIntent",
            'slots': slots,
            'slotToElicit': slot,
            "message": {
                    "contentType": "PlainText",
                    "content": mess
                    }
                }
            }
            
def dispatch(event):
    slots = get_slots(event)
    
    '''location = slots['Location']
    foodtype = slot["Cuisine"]
    people = slot['NumberofPeople']
    date = slot['DiningDate']
    time = slot['DiningTime']
    phone = slot['PhoneNumber']
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'BestFootballer':'''
    
    
    if slots['Location'] is not None:
        location = slots['Location']
        if location.lower() not in['manhattan','new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix', 'san antonio', 'san diego', 'dallas', 'san jose','austin', 'jacksonville', 'san francisco', 'indianapolis', 'columbus', 'fort worth', 'charlotte', 'detroit', 'el paso', 'seattle', 'denver', 'washington dc','memphis', 'boston', 'nashville', 'baltimore', 'portland']:
            return elict(slots,"Location","The wrong answer!Please input your location again.")
    if slots["PhoneNumber"] is not None:
        if len(slots["PhoneNumber"])!=10:
            return elict(slots,"PhoneNumber","The wrong answer!Please input your phone again.")
            
    if slots["NumberofPeople"] is not None:
        if int(slots["NumberofPeople"])>=20:
            return elict(slots,"NumberofPeople","The wrong answer!Please input your Number of People again.")
        if slots["NumberofPeople"].isdigit()=="false":      
             return elict(slots,"NumberofPeople","The wrong answer!Please input your Number of People again.")
               
          
    output_session_attributes = event['sessionAttributes'] if event['sessionAttributes'] is not None else {} 
    return delegate(output_session_attributes,slots)