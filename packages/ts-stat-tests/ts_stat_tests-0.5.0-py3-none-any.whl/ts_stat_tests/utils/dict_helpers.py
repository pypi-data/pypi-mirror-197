from typing import Iterable, List, Union


def dict_slice_by_keys(dictionary: dict, keys: Union[str, List[str]]):
    if isinstance(keys, str):
        keys = [keys]
    return {key: value for key, value in dictionary.items() if key in keys}


def dict_reverse_key_values(dictionary: dict):
    new_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, str):
            new_dict[value] = key
        elif isinstance(value, Iterable):
            for item in value:
                new_dict[item] = key
        else:
            new_dict[value] = key
    return new_dict
