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
