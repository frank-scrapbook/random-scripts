import argparse
import boto3

# Define the AWS region and DynamoDB client
region_name = 'your-aws-region'
dynamodb_client = boto3.client('dynamodb', region_name=region_name)

# Define command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('option', type=int, help='Choose an option (1 = List tables, 2 = List backups, 3 = Get table attributes, 4 = Restore backup)')
parser.add_argument('--table-name', help='Table name')
parser.add_argument('--backup-name', help='Backup name')
args = parser.parse_args()

# Option 1: List all DynamoDB tables dynamically using page iterators
if args.option == 1:
    paginator = dynamodb_client.get_paginator('list_tables')
    for page in paginator.paginate():
        for table_name in page['TableNames']:
            print(table_name)

# Option 2: List all DynamoDB backups dynamically using page iterators
elif args.option == 2:
    table_name = args.table_name
    paginator = dynamodb_client.get_paginator('list_backups')
    for page in paginator.paginate(TableName=table_name, BackupType='USER'):
        for backup in page['BackupSummaries']:
            print(backup['BackupName'])

# Option 3: Get all attributes for a specific DynamoDB table
elif args.option == 3:
    table_name = args.table_name
    response = dynamodb_client.describe_table(TableName=table_name)
    for attribute in response['Table']['AttributeDefinitions']:
        print(attribute['AttributeName'])

# Option 4: Restore a specific DynamoDB backup
elif args.option == 4:
    table_name = args.table_name
    backup_name = args.backup_name
    response = dynamodb_client.list_backups(TableName=table_name, BackupType='USER')
    for backup in response['BackupSummaries']:
        if backup['BackupStatus'] == 'AVAILABLE' and backup['BackupName'] == backup_name:
            backup_arn = backup['BackupArn']
            print(f"Restoring backup {backup_name} for table {table_name}...")
            restore_response = dynamodb_client.restore_table_from_backup(BackupArn=backup_arn)
            print(f"Restore initiated for table {table_name}.")
            break
    else:
        print(f"No backup found with name {backup_name} for table {table_name}.")
