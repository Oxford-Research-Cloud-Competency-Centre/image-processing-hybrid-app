import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
REGION_NAME = os.getenv('REGION_NAME')
AWS_PROFILE = os.getenv('AWS_PROFILE')
IMAGE_METADATA_TABLE = os.getenv('IMAGE_METADATA_TABLE')

# Create a Boto3 session with profile
if AWS_PROFILE:
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=REGION_NAME)
else:
    session = boto3.Session(region_name=REGION_NAME)

# Create DynamoDB client with the specified region
dynamodb = session.resource('dynamodb')

table = dynamodb.Table(IMAGE_METADATA_TABLE)

def insert_metadata(image_id, original_filename, original_size, processed_filename, processed_size, upload_date, description):
    table.put_item(
        Item={
            'id': image_id,
            'original_filename': original_filename,
            'original_size': original_size,
            'processed_filename': processed_filename,
            'processed_size': processed_size,
            'upload_date': upload_date,
            'description': description
        }
    )

def get_metadata():
    try:
        response = table.scan()
        items = response['Items']
        # Convert the items to a list of lists for the template
        metadata = [
            [
                item.get('id', ''),
                item.get('original_filename', ''),
                item.get('original_size', ''),
                item.get('processed_filename', ''),
                item.get('processed_size', ''),
                item.get('upload_date', ''),
                item.get('description', '')
            ]
            for item in items
        ]
        return metadata
    except (BotoCoreError, ClientError) as e:
        return []
