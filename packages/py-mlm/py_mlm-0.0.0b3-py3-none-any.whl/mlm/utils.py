#!/usr/bin/env python3
import json
import pathlib
import re
from os.path import join as os_join


def auto_title(dir_name, user_system):
    """
    Generate a title from dir_name
    e.g. /path/to/[Group] Show Season 01 (1080p) [Hash info]
    returns ' - path - to - Show Season 01 (1080p)'
    """

    title = re.sub(r"\s?\[[^]]*\]\s?", "", dir_name)
    if user_system == "Windows":
        title = re.sub("\\\\", " - ", title)
    else:
        title = re.sub(r"/", " - ", title)

    return title


def add_url(url, dir, user):
    """
    Associate the given url with given dir
    """
    lib = pathlib.Path(user.files["library_file"])
    dir_name = pathlib.Path(dir).name

    def backup_library():
        lib.replace(user.files["library_bak_file"])

    with open(user.files["library_file"], "r") as data:
        library = json.load(data)
    if dir_name in library.keys():
        library[dir_name]["url"] = url
        backup_library()
        with open(user.files["library_file"], "w+") as data:
            json.dump(library, data, indent=4)
            return 0
    return 1


def key_value_list(dic, search_key=None):
    """
    Take a dicionary and return two lists one for keys and one for values
    """
    # While it is easiest if dic is a true dict
    # it need not be. As long as the items in dic
    # _are_ true dicts then we can make do
    def psuedo_dic():
        for item in dic:
            if isinstance(item, dict):
                true_dic(item)

    def true_dic(d=dic):
        if search_key is None:
            keys.extend(d.keys())
            values.extend(d.values())
        else:
            for key, value in d.items():
                if key == search_key:
                    keys.append(key)
                    values.append(value)

    keys = []
    values = []
    if isinstance(dic, dict):
        true_dic()
    else:
        psuedo_dic()

    return keys, values


def join(a, b):
    return os_join(a, b)


def merge_libraries(old_dict, new_dict):
    """Takes two dictionaries and merges them"""
    merged_dict = {}
    pop_key = None
    for new_key, new_val in new_dict.items():
        match = False
        for old_key, old_val in old_dict.items():
            if old_key == new_key:
                match = True
                merged_dict[old_key] = old_val
                pop_key = old_key
                break
        if match:
            old_dict.pop(pop_key, None)
            continue
        merged_dict[new_key] = new_val
    return merged_dict
