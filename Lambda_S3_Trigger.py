import json
import boto3
import logging
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Log the received event
    logger.info("Received event: " + json.dumps(event, indent=2))

    # Extract bucket name and file key (object path) from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Log the bucket and file key (object path)
    logger.info(f"Bucket: {bucket_name}, Key: {file_key}")

    try:
        # Get the file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        
        logger.info("File content received successfully")
        
        # Process the CSV content
        csv_reader = csv.reader(file_content.splitlines())
        for row in csv_reader:
            logger.info(f"Row: {row}")

        return {
            'statusCode': 200,
            'body': json.dumps('CSV file processed successfully.')
        }
    except Exception as e:
        logger.error(f"Error processing file {file_key} from bucket {bucket_name}. Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing the CSV file.')
        }