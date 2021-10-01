import re


def snake_case_keys(data):
    regex = re.compile(r"(?<=[a-zA-Z])(?=[A-Z0-9])")

    if isinstance(data, dict):
        data = {
            regex.sub("_", key).lower().replace("-", "_"): snake_case_keys(val)
            for key, val in data.items()
        }

    elif isinstance(data, list):
        data = [snake_case_keys(x) for x in data]

    return data