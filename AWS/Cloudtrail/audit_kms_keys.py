import boto3
from datetime import datetime, timedelta

# To get the list of KMS keys that have been created or deleted in the CloudTrail logs in the last 6 months using the boto3 library for AWS

# Set the start and end time for the query
start_time = datetime.now() - timedelta(days=180)
end_time = datetime.now()

# Create a boto3 CloudTrail client
cloudtrail_client = boto3.client('cloudtrail')

# Create a dictionary to hold the KMS keys that have been created or deleted
kms_keys = {}

# Get the CloudTrail events for the specified time period
response = cloudtrail_client.lookup_events(
    LookupAttributes=[
        {'AttributeKey': 'EventName', 'AttributeValue': 'CreateKey'},
        {'AttributeKey': 'EventName', 'AttributeValue': 'ScheduleKeyDeletion'},
        {'AttributeKey': 'EventName', 'AttributeValue': 'CancelKeyDeletion'},
        {'AttributeKey': 'ResourceType', 'AttributeValue': 'AWS::KMS::Key'}
    ],
    StartTime=start_time,
    EndTime=end_time
)

# print(response)

# Parse the CloudTrail events to get the KMS keys that have been created or deleted
for event in response['Events']:
    event_time = event['EventTime']
    event_name = event['EventName']
    # key_arn = event['Resources'][0]['ResourceName']
    # key_id = key_arn.split('/')[-1]
    key_id = ''
    for resource in event['Resources']:
        if 'arn' in resource['ResourceName']:
            key_id = resource['ResourceName'].split('/')[-1]
    
    if key_id not in kms_keys:
        kms_keys[key_id] = {}
        kms_keys[key_id]['created'] = None
        kms_keys[key_id]['deleted'] = None
    
    if event_name == 'CreateKey':
        kms_keys[key_id]['created'] = event_time
    elif event_name == 'ScheduleKeyDeletion':
        kms_keys[key_id]['deleted'] = event_time
    elif event_name == 'CancelKeyDeletion':
        kms_keys[key_id]['deleted'] = None

# Print the list of KMS keys that have been created or deleted in the last 6 months
for key_id, key_data in kms_keys.items():
    if key_data['created']:
        print(f"KMS Key {key_id} was created on {key_data['created']}.")
    elif key_data['deleted']:
        print(f"KMS Key {key_id} was deleted on {key_data['deleted']}.")
