import boto3
import csv
import sys
import re

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the functions

def paginate(operation, **kwargs):
    """
    A generator that yields paginated responses from AWS API operations.
    """
    while True:
        response = operation(**kwargs)
        yield response
        try:
            kwargs['ExclusiveStartTableName'] = response['LastEvaluatedTableName']
        except KeyError:
            break

def list_tables():
    try:
        table_list = []
        for response in paginate(dynamodb.list_tables):
            table_list += response['TableNames']
        print("List of DynamoDB Tables:")
        for table_name in table_list:
            print(table_name)
    except Exception as e:
        print(f"Error listing tables: {e}")
        sys.exit()

def write_pitr_status_to_csv(filename):
    try:
        table_list = []
        for response in paginate(dynamodb.list_tables):
            table_list += response['TableNames']
        # Filter DynamoDB Table List for only master and exclude ones with slices (identified by two consecutive numbers, e.g. tl-09 or dso-1234)
        filtered_table_list = [table_name for table_name in table_list if 'master' in table_name or not bool(re.search(r'\d{2,}', table_name))]
    except Exception as e:
        print(f"Error listing tables: {e}")
        sys.exit()

    try:
        with open(filename, mode='w') as csv_file:
            fieldnames = ['table_name', 'pitr_status']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            # For each table, get the point in time recovery status and write it to the CSV file
            for table_name in filtered_table_list:
                try:
                    table_description = dynamodb.describe_table(TableName=table_name)
                    if 'PointInTimeRecoveryDescription' in table_description:
                        pitr_status = table_description['PointInTimeRecoveryDescription']['PointInTimeRecoveryStatus']
                        writer.writerow({'table_name': table_name, 'pitr_status': pitr_status})
                    else:
                        writer.writerow({'table_name': table_name, 'pitr_status': 'not enabled'})
                except Exception as e:
                    print(f"Error getting PITR status for table {table_name}: {e}")
                    writer.writerow({'table_name': table_name, 'pitr_status': 'error'})
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        sys.exit()

def main():
    print("Please select an option:")
    print("1. List DynamoDB Tables")
    print("2. Write PITR Status to CSV File")
    option = input("Option: ")

    if option == '1':
        list_tables()
    elif option == '2':
        filename = input("Enter the filename for the CSV file: ")
        write_pitr_status_to_csv(filename)
    else:
        print("Invalid option")

if __name__ == '__main__':
    main()
