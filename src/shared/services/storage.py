import boto3, os, uuid

aws_s3_bucket_name = os.environ.get("aws_s3_bucket_name")
aws_s3_region = os.environ.get("aws_s3_region")
aws_access_key_id = os.environ.get("aws_access_key_id")
aws_secret_access_key = os.environ.get("aws_secret_access_key")


# Create an S3 resource object
s3 = boto3.resource(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_s3_region,
)
# Specify the S3 bucket name and access an S3 bucket
dispatchxchange_bucket = s3.Bucket(name=aws_s3_bucket_name)


def uid() -> str:
    return str(uuid.uuid4()).split("-")[0]


def upload_file(filename: str, data: str | bytes) -> str:
    filename = f"{uid()}-{filename}"
    dispatchxchange_bucket.put_object(Key=filename, Body=data, ACL="public-read")
    # dispatchxchange_bucket.put_object(Key=filename, Body=data, ACL="private")

    return f"https://{aws_s3_bucket_name}.s3.{aws_s3_region}.amazonaws.com/{filename}"

    return get_signed_url(filename)


def get_signed_url(filename: str, expiration: int = 3600) -> str:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_s3_region,
    )

    # Generate a signed URL
    signed_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": aws_s3_bucket_name, "Key": filename},
        ExpiresIn=expiration,
    )

    return signed_url


def get_2_url(url: str):
    urls = url.split("/")
    return get_signed_url(urls[-1])
