import boto3
from datetime import datetime, timedelta

def get_kms_cost():
    # Get the current account ID
    sts_client = boto3.client('sts')
    account_id = sts_client.get_caller_identity()['Account']

    # Set the time range for the cost explorer report
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30*6)

    # Create a boto3 Cost Explorer client
    ce_client = boto3.client('ce')

    # Get the KMS cost for each month in the last 6 months
    print("KMS usage cost in the last 6 months:")
    for i in range(6):
        start = start_time.strftime('%Y-%m-%d')
        end = (start_time + timedelta(days=30)).strftime('%Y-%m-%d')

        result = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            Filter={
                "And": [
                    {
                        "Dimensions": {
                            "Key": "USAGE_TYPE_GROUP",
                            "Values": [
                                "AWS Key Management Service"
                            ]
                        }
                    },
                    {
                        "Dimensions": {
                            "Key": "LINKED_ACCOUNT",
                            "Values": [
                                account_id
                            ]
                        }
                    }
                ]
            }
        )

        # Print the KMS cost for each month in the last 6 months
        cost = float(result['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
        print(f"{start[:7]}: ${cost:.2f}")

        start_time += timedelta(days=30)

get_kms_cost()