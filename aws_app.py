"""
AWS Integration Module for LumiLens
This file contains AWS service integrations using boto3
Includes: DynamoDB, SNS, and IAM configurations
"""

import boto3
from botocore.exceptions import ClientError
import os

# ==================== AWS CONFIGURATION ====================

# AWS Region
AWS_REGION = 'us-east-1'

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
sns_client = boto3.client('sns', region_name=AWS_REGION)
iam_client = boto3.client('iam', region_name=AWS_REGION)

# ==================== DYNAMODB TABLES ====================

def create_users_table():
    """Create DynamoDB table for users"""
    try:
        table = dynamodb.create_table(
            TableName='LumiLens_Users',
            KeySchema=[
                {'AttributeName': 'email', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        print("Users table created successfully")
        return table
    except ClientError as e:
        print(f"Error creating users table: {e}")
        return None

def create_photographers_table():
    """Create DynamoDB table for photographers"""
    try:
        table = dynamodb.create_table(
            TableName='LumiLens_Photographers',
            KeySchema=[
                {'AttributeName': 'photographer_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'photographer_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        print("Photographers table created successfully")
        return table
    except ClientError as e:
        print(f"Error creating photographers table: {e}")
        return None

def create_bookings_table():
    """Create DynamoDB table for bookings"""
    try:
        table = dynamodb.create_table(
            TableName='LumiLens_Bookings',
            KeySchema=[
                {'AttributeName': 'booking_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'booking_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        print("Bookings table created successfully")
        return table
    except ClientError as e:
        print(f"Error creating bookings table: {e}")
        return None

# ==================== DYNAMODB OPERATIONS ====================

def add_user_to_dynamodb(email, user_data):
    """Add user to DynamoDB"""
    try:
        table = dynamodb.Table('LumiLens_Users')
        table.put_item(Item={'email': email, **user_data})
        print(f"User {email} added to DynamoDB")
        return True
    except ClientError as e:
        print(f"Error adding user: {e}")
        return False

def get_user_from_dynamodb(email):
    """Get user from DynamoDB"""
    try:
        table = dynamodb.Table('LumiLens_Users')
        response = table.get_item(Key={'email': email})
        return response.get('Item', None)
    except ClientError as e:
        print(f"Error getting user: {e}")
        return None

def add_booking_to_dynamodb(booking_id, booking_data):
    """Add booking to DynamoDB"""
    try:
        table = dynamodb.Table('LumiLens_Bookings')
        table.put_item(Item={'booking_id': booking_id, **booking_data})
        print(f"Booking {booking_id} added to DynamoDB")
        return True
    except ClientError as e:
        print(f"Error adding booking: {e}")
        return False

def update_booking_status_dynamodb(booking_id, new_status):
    """Update booking status in DynamoDB"""
    try:
        table = dynamodb.Table('LumiLens_Bookings')
        table.update_item(
            Key={'booking_id': booking_id},
            UpdateExpression='SET #status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': new_status}
        )
        print(f"Booking {booking_id} status updated to {new_status}")
        return True
    except ClientError as e:
        print(f"Error updating booking status: {e}")
        return False

# ==================== SNS NOTIFICATIONS ====================

def create_sns_topic():
    """Create SNS topic for booking notifications"""
    try:
        response = sns_client.create_topic(Name='LumiLens_Booking_Notifications')
        topic_arn = response['TopicArn']
        print(f"SNS topic created: {topic_arn}")
        return topic_arn
    except ClientError as e:
        print(f"Error creating SNS topic: {e}")
        return None

def send_booking_notification(topic_arn, booking_data):
    """Send booking notification via SNS"""
    try:
        message = f"""
        New Booking Notification - LumiLens
        
        Booking ID: {booking_data['id']}
        Client: {booking_data['client_name']}
        Photographer: {booking_data['photographer_name']}
        Event Type: {booking_data['event_type']}
        Event Date: {booking_data['event_date']}
        Status: {booking_data['status']}
        
        Please check your dashboard for more details.
        """
        
        response = sns_client.publish(
            TopicArn=topic_arn,
            Subject='New Booking - LumiLens',
            Message=message
        )
        print(f"Notification sent: {response['MessageId']}")
        return True
    except ClientError as e:
        print(f"Error sending notification: {e}")
        return False

def subscribe_email_to_topic(topic_arn, email):
    """Subscribe email to SNS topic"""
    try:
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email
        )
        print(f"Email {email} subscribed to topic")
        return response['SubscriptionArn']
    except ClientError as e:
        print(f"Error subscribing email: {e}")
        return None

# ==================== IAM ROLES ====================

def create_ec2_role():
    """Create IAM role for EC2 instance"""
    try:
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "ec2.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        response = iam_client.create_role(
            RoleName='LumiLens_EC2_Role',
            AssumeRolePolicyDocument=str(assume_role_policy),
            Description='IAM role for LumiLens EC2 instance'
        )
        print(f"IAM role created: {response['Role']['RoleName']}")
        return response['Role']
    except ClientError as e:
        print(f"Error creating IAM role: {e}")
        return None

def attach_dynamodb_policy_to_role(role_name):
    """Attach DynamoDB access policy to IAM role"""
    try:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess'
        )
        print(f"DynamoDB policy attached to {role_name}")
        return True
    except ClientError as e:
        print(f"Error attaching policy: {e}")
        return False

def attach_sns_policy_to_role(role_name):
    """Attach SNS access policy to IAM role"""
    try:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonSNSFullAccess'
        )
        print(f"SNS policy attached to {role_name}")
        return True
    except ClientError as e:
        print(f"Error attaching policy: {e}")
        return False

# ==================== SETUP FUNCTION ====================

def setup_aws_infrastructure():
    """Setup all AWS infrastructure"""
    print("Setting up AWS infrastructure for LumiLens...")
    
    # Create DynamoDB tables
    print("\n1. Creating DynamoDB tables...")
    create_users_table()
    create_photographers_table()
    create_bookings_table()
    
    # Create SNS topic
    print("\n2. Creating SNS topic...")
    topic_arn = create_sns_topic()
    
    # Create IAM role
    print("\n3. Creating IAM role...")
    role = create_ec2_role()
    if role:
        attach_dynamodb_policy_to_role('LumiLens_EC2_Role')
        attach_sns_policy_to_role('LumiLens_EC2_Role')
    
    print("\nAWS infrastructure setup complete!")
    print(f"SNS Topic ARN: {topic_arn}")
    
    return {
        'topic_arn': topic_arn,
        'role': role
    }

# ==================== MAIN ====================

if __name__ == '__main__':
    """
    Run this file to setup AWS infrastructure
    Make sure AWS credentials are configured via:
    - AWS CLI: aws configure
    - Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    - IAM role (when running on EC2)
    """
    print("LumiLens AWS Setup")
    print("=" * 50)
    setup_aws_infrastructure()
