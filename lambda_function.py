import boto3
import pytz
import logging
from datetime import datetime, time

# Replace these with your EC2 and RDS instance IDs
ec2_instance_id = "YOUR_EC2_INSTANCE_ID"
rds_instance_id = "YOUR_RDS_INSTANCE_ID"

# Define the time range for running the instances (Sydney timezone)
start_time = time(hour=9, minute=0, second=0)
end_time = time(hour=23, minute=59, second=59)

# Function to check if current time is within the specified time range
def is_within_time_range(current_time, start_time, end_time):
    return start_time <= current_time.time() <= end_time

# Get Sydney timezone
sydney_tz = pytz.timezone("Australia/Sydney")

# Function to check the current state of the RDS instance
def get_rds_instance_state(rds_client, rds_instance_id):
    response = rds_client.describe_db_instances(DBInstanceIdentifier=rds_instance_id)
    if len(response['DBInstances']) > 0:
        return response['DBInstances'][0]['DBInstanceStatus']
    return None

# Lambda handler function
def lambda_handler(event, context):
    # Get the current time in Sydney timezone
    current_time = datetime.now(sydney_tz)

    # Check if the current time is within the specified time range
    if is_within_time_range(current_time, start_time, end_time):
        # Start EC2 instance if it is not running
        ec2_client = boto3.client("ec2")
        ec2_instance = ec2_client.describe_instances(InstanceIds=[ec2_instance_id])
        if ec2_instance['Reservations'][0]['Instances'][0]['State']['Name'] != 'running':
            response = ec2_client.start_instances(InstanceIds=[ec2_instance_id])
            logging.info("EC2 instance started: %s", response)

        # Start RDS instance if it is in 'stopped' or 'inaccessible-encryption-credentials-recoverable' state
        rds_client = boto3.client("rds")
        rds_state = get_rds_instance_state(rds_client, rds_instance_id)
        if rds_state in ['stopped', 'inaccessible-encryption-credentials-recoverable']:
            response = rds_client.start_db_instance(DBInstanceIdentifier=rds_instance_id)
            logging.info("RDS instance started: %s", response)
        else:
            logging.info("RDS instance is already running or cannot be started in the current state: %s", rds_state)
    else:
        # Stop EC2 instance if it is running
        ec2_client = boto3.client("ec2")
        ec2_instance = ec2_client.describe_instances(InstanceIds=[ec2_instance_id])
        if ec2_instance['Reservations'][0]['Instances'][0]['State']['Name'] == 'running':
            response = ec2_client.stop_instances(InstanceIds=[ec2_instance_id])
            logging.info("EC2 instance stopped: %s", response)

        # Stop RDS instance if it is in 'available' state
        rds_client = boto3.client("rds")
        rds_state = get_rds_instance_state(rds_client, rds_instance_id)
        if rds_state == 'available':
            response = rds_client.stop_db_instance(DBInstanceIdentifier=rds_instance_id)
            logging.info("RDS instance stopped: %s", response)
        else:
            logging.info("RDS instance is already stopped or cannot be stopped in the current state: %s", rds_state)

    # Return a response immediately (asynchronous behavior)
    return {"message": "Lambda function is running asynchronously."}
