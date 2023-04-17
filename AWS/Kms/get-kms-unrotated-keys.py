import boto3
from datetime import datetime, timedelta

# Create a boto3 KMS client
kms_client = boto3.client('kms')


def get_unrotated_keys():
    # Get a list of all the KMS keys
    response = kms_client.list_keys()
    # print(response)
    # Check each key to see if it has been rotated in the last 6 months
    for key in response['Keys']:
        key_id = key['KeyId']
        key_rotation_status = kms_client.get_key_rotation_status(KeyId=key_id)
        print(key_rotation_status)
        # last_rotated = kms_client.get_key_rotation_status(KeyId=key_id)['LastKeyRotationTimestamp']
        # last_rotated_time = datetime.strptime(last_rotated, '%Y-%m-%dT%H:%M:%S.%fZ')
        # if last_rotated_time < (datetime.now() - timedelta(days=180)):
        #     print(f"{key_id} hasn't been rotated in the last 6 months.")

#  Schedules the key for deletion 7 to 30 days from the time it's called (depending on your AWS account configuration), so the key won't be immediately deleted.
def schedule_deletion_for_unrotated_keys():
    # Get a list of all the KMS keys
    response = kms_client.list_keys()

    # Check each key to see if it has been rotated in the last 6 months
    for key in response['Keys']:
        key_id = key['KeyId']
        last_rotated = kms_client.get_key_rotation_status(KeyId=key_id)['LastKeyRotationTimestamp']
        last_rotated_time = datetime.strptime(last_rotated, '%Y-%m-%dT%H:%M:%S.%fZ')
        if last_rotated_time < (datetime.now() - timedelta(days=180)):
            # Delete the KMS key
            kms_client.schedule_key_deletion(KeyId=key_id)
            print(f"{key_id} has been scheduled for deletion.")

def main():
    get_unrotated_keys()

if __name__ == "__main__":
    main()