import boto3
import csv
from datetime import datetime

# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('yelp-restaurants')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)


with open("originalinfo_new.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    data = []  # 创建列表准备接收csv各行数据
    # data = [row for row in reader]
    for one_line in reader:
        data.append(one_line)
    #print(data)

for r in range(len(data)-1):
    restaurant_id = data[r][0]
    restaurant_type = data[r][1]
    restaurant_name = data[r][2]
    restaurant_address = data[r][3]
    coordinates_lat = data[r][4]
    coordinates_long = data[r][5]
    restaurant_rating = data[r][6]
    restaurant_reviews = data[r][7]
    restaurant_zip = data[r][8]
    timestamp = str(datetime.now())
    #print(restaurant_id)
    # print(restaurant_type)
    ##writing tinto database
    dynamo_info = {"BusinessID": restaurant_id, "Name": restaurant_name,
                   "Cuisine Type": restaurant_type, "Address": restaurant_address,
                   "Latitude": coordinates_lat, "Longitude": coordinates_long,
                   "Rating": restaurant_rating, "Number of Reviews": restaurant_reviews,
                   "Zip Code": restaurant_zip, "timestamp": timestamp}
    print(dynamo_info)
    # dynamo_data = {key: value for key, value in dynamo_info.items() if value}
    print(dynamo_info)

    # response = table.put_item(Item=dynamo_data)

