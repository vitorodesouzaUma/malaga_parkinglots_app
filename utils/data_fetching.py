from pymongo import MongoClient
from pymongo.server_api import ServerApi
import logging, requests, os


# MongoDB cnnection password as a environment variable.
MONGODB_URL = os.environ.get('MONGODB')

# Define a global variable to store parking lot data
parking_data = []

# Define a function to fetch parking lot data from the Malaga's open data portal
def fetch_parking_data():

    global parking_data

    # Fetch data from Malaga's open data portal.
    try:
        response = requests.get('https://datosabiertos.malaga.eu/recursos/aparcamientos/ocupappublicosmun/ocupappublicosmunfiware.json')
        response.raise_for_status()
        parking_data = response.json()
    except requests.exceptions.RequestException as e:
        parking_data = []
        print(e)
        logging.error(e)

    # MongoDB cnnection parameters.
    connection_url = f'mongodb+srv://vitor:{MONGODB_URL}@mastercluster.e1lyp47.mongodb.net/'

    # Define the aggregation pipeline to transform it and merge the parkinglots data into the 'parking_data' collection.
    pipeline = [
        {
            '$addFields': {
            'time': {
                '$toDate': "$$NOW",
            },
            },
        },
        {
            '$addFields': {
                'location.value.coordinates': {
                    '$map': {
                        "input": "$location.value.coordinates",
                        "as": "coord",
                        'in': {
                        '$toDouble': "$$coord",
                        }
                    }
                }
            }
        },
        {
            '$merge': {
                'into': "parking_data",
                'on': "_id",
                'whenMatched': "replace",
                'whenNotMatched': "insert",
            },
        },
    ]

    # Connect to MongoDB and execute the aggregation pipeline.
    with MongoClient(connection_url,server_api=ServerApi('1')) as client:
        try:
            # The collection 'parkinglots' is used to fetch data from malaga's open data portal
            # then transform it and add it into a final parking-data collection
            db = client.get_database('2023-master')
            col_original = db.get_collection('parkinglots')
            col_original.drop()
            col_original.insert_many(parking_data)
            col_original.aggregate(pipeline)

            # 'parking_data' has the historical data with timestamp and numerical coordinates
            col_merged = db.get_collection('parking_data')

            # Group the parkinglots data by the time of database insetion (previous step)
            # Then sort the documents by the timestamp in descending order
            # Then limit the results to one document to get the latest data
            parking_data_cursor = col_merged.aggregate([
                {
                    "$group": {
                        "_id": "$time",
                        "parkinglots": {
                            "$push": {
                                "status": "$status",
                                "category":"$category",
                                "name":"$name",
                                "requiredPermit": "$requiredPermit",
                                "allowedVehicleType": "$allowedVehicleType",
                                "availableSpotNumber": "$availableSpotNumber",
                                "source": "$source",
                                "totalSpotNumber": "$totalSpotNumber",
                                "location": "$location",
                                "chargeType": "$chargeType",
                                "owner": "$owner",
                                "occupancyDetectionType": "$occupancyDetectionType",
                                "dataProvider": "$dataProvider",
                                "type": "$type",
                                "id": "$id",
                                "description": "$description"
                            }
                        }
                    }
                },
                {
                    "$sort": {
                        "_id": -1
                    }
                }, 
                {
                    "$limit": 1
                }
            ])

            
            parking_data = []
            for doc in parking_data_cursor:
                parking_data.append(doc)

        except Exception as e:
            print(e)
            logging.error(e)

        
    return parking_data