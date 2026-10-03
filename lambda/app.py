import boto3
import urllib.parse

s3 = boto3.client("s3")


def lambda_handler(event, context):

    for record in event["Records"]:

        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        print(f"Processing file: s3://{bucket}/{key}")

        if not key.startswith("incoming/"):
            print("File is not inside incoming/. Skipping.")
            continue

        file_name = key.split("/")[-1]
        archive_key = f"archives/{file_name}"

        s3.copy_object(
            Bucket=bucket,
            CopySource={
                "Bucket": bucket,
                "Key": key
            },
            Key=archive_key
        )

        s3.delete_object(
            Bucket=bucket,
            Key=key
        )

        print(f"Archived file to: s3://{bucket}/{archive_key}")

    return {
        "statusCode": 200,
        "body": "File processing completed successfully"
    }