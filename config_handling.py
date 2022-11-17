"""
        author: Adrian Scheubrein
        date: 18.01.2022
        version: 1.0.0
        license: MIT
"""
"""
[This Module handles the Config File. It reads, writes and can restore the config to the default]
"""
import json
import config_dict_default_template as my_cddt
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def restore_config(cwd_path:str):
    # Serializing json
    json_object = json.dumps(my_cddt.my_dict_list, indent = 2)
    # Writing to sample.json
    with open(f"{cwd_path}/config.json", "w") as outfile:
        outfile.write(json_object)
    logging.debug("config_handling restore_config -- Restored Config to Default")

def read_config(cwd_path:str):
    # Opening JSON file
    with open(f'{cwd_path}/config.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    return json_object