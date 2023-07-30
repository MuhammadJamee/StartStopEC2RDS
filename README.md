# StartStopEC2RDS

This Python script is an AWS Lambda function that checks the current time in the Sydney timezone and takes actions accordingly to start or stop an EC2 instance and an RDS instance. The script is designed to run asynchronously as an AWS Lambda function.

Here's a breakdown of the script:

1. Import necessary libraries:
   - `boto3`: The AWS SDK for Python, used to interact with AWS services.
   - `pytz`: A library to work with timezones, specifically used for the Sydney timezone.
   - `logging`: Used to log messages to the AWS CloudWatch logs.
   - `datetime`, `time`: Used to work with dates and times.

2. Define the EC2 and RDS instance IDs:
   Replace `ec2_instance_id` and `rds_instance_id` with the IDs of your specific EC2 and RDS instances that you want to manage.

3. Define the time range for running the instances:
   The `start_time` and `end_time` variables specify the time range during which you want the instances to be running. In this script, it's set to run from 9:00:00 AM to 11:59:59 PM in the Sydney timezone.

4. Define a function to check if the current time is within the specified time range:
   The `is_within_time_range` function takes the current time and the start and end times and returns `True` if the current time falls within the specified time range.

5. Get the Sydney timezone:
   The `sydney_tz` variable stores the Sydney timezone to be used later.

6. Define a function to check the current state of the RDS instance:
   The `get_rds_instance_state` function takes the RDS client and RDS instance ID as inputs and returns the current state of the RDS instance (e.g., 'running', 'stopped').

7. The Lambda handler function (`lambda_handler`):
   - Gets the current time in the Sydney timezone using `datetime.now(sydney_tz)`.
   - Checks if the current time is within the specified time range using the `is_within_time_range` function.
   - If the current time is within the range:
     - Checks if the EC2 instance is not running. If not, it starts the EC2 instance using the AWS EC2 client (`boto3.client("ec2")`) and logs the response.
     - Checks the state of the RDS instance. If it is in a stopped state or 'inaccessible-encryption-credentials-recoverable', it starts the RDS instance using the AWS RDS client (`boto3.client("rds")`) and logs the response. Otherwise, it logs that the RDS instance is already running or cannot be started in the current state.
   - If the current time is outside the specified time range:
     - Checks if the EC2 instance is running. If it is, it stops the EC2 instance using the AWS EC2 client and logs the response.
     - Checks the state of the RDS instance. If it is in an 'available' state, it stops the RDS instance using the AWS RDS client and logs the response. Otherwise, it logs that the RDS instance is already stopped or cannot be stopped in the current state.

8. Returns a response immediately (asynchronous behavior):
   The Lambda function returns a JSON response with the message "Lambda function is running asynchronously."

This Lambda function can be configured to run on a schedule using AWS CloudWatch Events to start and stop the instances according to the specified time range.





Run it on base directory for installing dependencies

pip install pytz -t .
