import argparse
import boto3
from datetime import datetime, timedelta

def get_unused_kms_keys():
    """
    Finds KMS keys that haven't been used in the last 6 months
    """
    # Set the start and end time for the query
    start_time = datetime.now() - timedelta(days=180)
    end_time = datetime.now()

    # Create a boto3 CloudTrail client
    cloudtrail_client = boto3.client('cloudtrail')

    # Get the CloudTrail events for the specified time period
    response = cloudtrail_client.lookup_events(
        LookupAttributes=[
            {'AttributeKey': 'EventName', 'AttributeValue': 'Decrypt'},
            {'AttributeKey': 'ResourceType', 'AttributeValue': 'AWS::KMS::Key'}
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    print(response)

    # # Create a set of KMS key ids from the CloudTrail events
    # used_keys = set([event['Resources'][0]['ARN'].split('/')[-1] for event in response['Events']])

    # # Create a boto3 KMS client
    # kms_client = boto3.client('kms')

    # # Get a list of all KMS keys in the account
    # all_keys = kms_client.list_keys()['Keys']

    # # Find the KMS keys that haven't been used in the last 6 months
    # unused_keys = []
    # for key in all_keys:
    #     key_id = key['KeyId']
    #     if key_id not in used_keys:
    #         unused_keys.append(key_id)

    # # Print the list of unused KMS keys
    # print("The following KMS keys have not been used in the last 6 months:")
    # for key_id in unused_keys:
    #     print(key_id)


def delete_unused_kms_keys():
    """
    Deletes KMS keys that haven't been used in the last 6 months
    """
    # Set the start and end time for the query
    start_time = datetime.now() - timedelta(days=180)
    end_time = datetime.now()

    # Create a boto3 CloudTrail client
    cloudtrail_client = boto3.client('cloudtrail')

    # Get the CloudTrail events for the specified time period
    response = cloudtrail_client.lookup_events(
        LookupAttributes=[
            {'AttributeKey': 'EventName', 'AttributeValue': 'Decrypt'},
            {'AttributeKey': 'ResourceType', 'AttributeValue': 'AWS::KMS::Key'}
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    # Create a set of KMS key ids from the CloudTrail events
    used_keys = set([event['Resources'][0]['ARN'].split('/')[-1] for event in response['Events']])

    # Create a boto3 KMS client
    kms_client = boto3.client('kms')

    # Get a list of all KMS keys in the account
    all_keys = kms_client.list_keys()['Keys']

    # Find the KMS keys that haven't been used in the last 6 months
    unused_keys = []
    for key in all_keys:
        key_id = key['KeyId']
        if key_id not in used_keys:
            unused_keys.append(key_id)

    # Delete the unused KMS keys
    if unused_keys:
        print("The following KMS keys have not been used in the last 6 months and will be deleted:")
        for key_id in unused_keys:
            print(f"KMS key: {key_id}")
            kms_client.schedule_key_deletion(
                KeyId=key_id,
                PendingWindowInDays=7
            )

get_unused_kms_keys()