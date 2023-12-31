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


def start_s3_client(
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    endpoint_url: str | None = None,
    environment: str = "dev",
):
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    if environment.lower() == "dev":
        return session.client(
            "s3",
            endpoint_url=endpoint_url,
        )
    return session.client("s3")
