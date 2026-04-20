from __future__ import absolute_import, division, print_function

__metaclass__ = type


def underscore_to_hyphen(data):
    if isinstance(data, list):
        for i, elem in enumerate(data):
            data[i] = underscore_to_hyphen(elem)
    elif isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            new_data[k.replace("_", "-")] = underscore_to_hyphen(v)
        data = new_data
    return data


def hyphen_to_underscore(data):
    if isinstance(data, list):
        for i, elem in enumerate(data):
            data[i] = hyphen_to_underscore(elem)
    elif isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            new_data[k.replace("-", "_")] = hyphen_to_underscore(v)
        data = new_data
    return data
