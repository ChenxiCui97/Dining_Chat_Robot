import csv
import json
import requests
import decimal
import boto3
from datetime import datetime

def main():
    
    new_header = {'Authorization': 'Bearer %s' % API_KEY, }

    # Get the service resource.
    # dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    # table = dynamodb.Table('yelp-restaurants')

    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    # print(table.creation_date_time)


    ##writing csv file
    file = open("originalinfo.csv", "a")
    writer = csv.writer(file)
    writer.writerow(['restaurant_id','restaurant_type','restaurant_name','restaurant_address','coordinates_lat','coordinates_long','restaurant_rating','restaurant_reviews','restaurant_zip'])
    cuisine_list = ['Chinese','American','Japanese','Thai','Mexico','Italian']
    count = 0
    for i in range(0,6):
        cuisine_type = cuisine_list[i]
        for j in range(0,999,50):
            count +=1
            print("offset",j)
            para_dict ={'offset':j,'location':'Manhattan','limit':50,'term':cuisine_type}
            conn = requests.get("https://api.yelp.com/v3/businesses/search",params = para_dict,headers=new_header)
            #print(conn.status_code)
            conn.encoding = "utf-8"
            data = json.loads(conn.text)
            print(data)
            restaurant_info = data['businesses']
            r = data['businesses']
            for r in restaurant_info:
                    #print('in rest of',restaurant_info.index(r))
                    restaurant_id = r['id']
                    restaurant_name = r['name']
                    restaurant_address = "\'{}\'".format(str(r['location']['display_address'][0]))
                    restaurant_type = cuisine_list[i]
                    #print(restaurant_type)
                    coordinates_lat = str(r['coordinates']['latitude'])
                    coordinates_long = decimal.Decimal(str(r['coordinates']['longitude']))
                    restaurant_rating = decimal.Decimal(str(r['rating']))
                    restaurant_reviews = r['review_count']
                    restaurant_zip = r['location']['zip_code']
                    timestamp = str(datetime.now())
                    print(restaurant_id,restaurant_name,restaurant_address,coordinates_lat,coordinates_long,restaurant_rating,restaurant_reviews,restaurant_zip,timestamp)
                    #print(count)
                    writer.writerow([restaurant_id,restaurant_type,restaurant_name,restaurant_address,coordinates_lat,coordinates_long,restaurant_rating,restaurant_reviews,restaurant_zip])








    conn.close()
        #file.close()
        # print(count)


if __name__ == "__main__":
    main()
