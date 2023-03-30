import boto3

# Define the AWS region and your credentials
aws_region = 'us-west-2'
aws_access_key_id = 'your_access_key_id'
aws_secret_access_key = 'your_secret_access_key'

# Create a new DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=aws_region,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)

# Retrieve a list of all DynamoDB backups in the account
backup_arns = []
response = dynamodb.list_backups()
while True:
    for backup in response['BackupSummaries']:
        backup_arns.append(backup['BackupArn'])
    if 'LastEvaluatedBackupArn' in response:
        response = dynamodb.list_backups(ExclusiveStartBackupArn=response['LastEvaluatedBackupArn'])
    else:
        break

# Restore each table from its backup
for arn in backup_arns:
    try:
        response = dynamodb.describe_backup(BackupArn=arn)
        table_name = response['BackupDescription']['SourceTableDetails']['TableName']
        existing_tables = dynamodb.list_tables()['TableNames']
        
        if table_name in existing_tables:
            print(f"Table {table_name} already exists and cannot be restored.")
        else:
            response = dynamodb.restore_table_from_backup(
                TargetTableName=table_name,
                BackupArn=arn
            )
            print(f"Table {table_name} is being restored from backup {arn}.")
    except Exception as e:
        print(f"Failed to restore table from backup {arn}: {e}")
