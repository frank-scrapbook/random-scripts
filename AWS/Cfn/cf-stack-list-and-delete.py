import boto3
import argparse

# Create CloudFormation client
cf_client = boto3.client('cloudformation')

# Parse command line arguments
parser = argparse.ArgumentParser(description='Script to list or delete CloudFormation stacks.')
parser.add_argument('option', type=int, choices=[1, 2], help='Choose an option: 1. List all stacks, 2. Delete a stack')
parser.add_argument('--states', nargs='+', type=str, choices=['CREATE_IN_PROGRESS', 'CREATE_FAILED', 'CREATE_COMPLETE', 'ROLLBACK_IN_PROGRESS', 'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE', 'DELETE_IN_PROGRESS', 'DELETE_FAILED', 'DELETE_COMPLETE', 'UPDATE_IN_PROGRESS', 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_IN_PROGRESS', 'UPDATE_ROLLBACK_FAILED', 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS', 'UPDATE_ROLLBACK_COMPLETE'], help='Filter the list of stacks by state')
args = parser.parse_args()

# List all stacks
if args.option == 1:
    # Get a list of all stacks
    if args.states:
        response = cf_client.list_stacks(StackStatusFilter=args.states)
    else:
        response = cf_client.list_stacks()

    # Print the name and state of each stack
    for stack in response['StackSummaries']:
        print(f"Stack Name: {stack['StackName']}\nStatus: {stack['StackStatus']}")

# Delete a stack
elif args.option == 2:
    # Ask user for the name of the stack to delete
    stack_name = input("Enter the name of the stack to delete (leave blank to exit): ")

    # Delete the specified stack
    if stack_name:
        try:
            cf_client.delete_stack(StackName=stack_name)
            print(f"Stack {stack_name} deletion initiated.")
        except cf_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ValidationError':
                print(f"Stack {stack_name} does not exist or is in an invalid state.")
    else:
        print("No stack was deleted.")
