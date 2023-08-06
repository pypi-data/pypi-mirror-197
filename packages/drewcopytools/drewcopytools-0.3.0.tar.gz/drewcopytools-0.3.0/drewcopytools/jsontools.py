# Utility function to help with dealing with json files + content.

import json
from pathlib import Path
from typing import Union

from drewcopytools.filetools import _toStr
from drewcopytools.filetools import read_utf8_file
# --------------------------------------------------------------------------------------------------------------
def load_json(path: Union[Path,str]) -> json:
    """
    Load a json file from the given path, returning a json instance.
    This function will load json data with or without a BOM in the data.
    """    
    data = read_utf8_file(path)
    res = json.loads(data)
    return res

    # try:
    #   with open(path, 'r', encoding='utf-8') as rHandle:
    #       data = rHandle.read()

    # except Exception as ex:
    #   # try it with the signature.....
    #   with open(path, 'r', encoding='utf-8-sig') as rHandle:
    #       data = rHandle.read()
    #       res = json.loads(data)
    #       return res
           

