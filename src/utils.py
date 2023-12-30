import boto3


def strtobool(val: str | bool) -> bool:
    """
    Converts a string or boolean to a boolean value.

    Args:
        val (str | bool): The value to convert.

    Returns:
        bool: The boolean representation of 'val'.

    Raises:
        ValueError: If 'val' is a string not representing a boolean.
    """
    if isinstance(val, bool):
        return val

    val_lower = val.lower()
    if val_lower in {"y", "yes", "t", "true", "on", "1"}:
        return True
    elif val_lower in {"n", "no", "f", "false", "off", "0"}:
        return False
    else:
        raise ValueError(f"Invalid boolean string: '{val}'.")


def start_s3_client():
    session = boto3.Session(
        aws_access_key_id="minio",
        aws_secret_access_key="p@ssw0rd",
    )
    return session.client(
        "s3",
        endpoint_url="http://localhost:9000",
    )


def write_to_s3(s3_client, file_content: bytes, bucket: str, object_key: str):
    response = s3_client.put_object(
        Body=file_content,
        Bucket=bucket,
        Key=object_key,
    )
    return response
