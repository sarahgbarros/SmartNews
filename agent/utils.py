import pandas as pd
import json
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def read_csv(filepath: str) -> List[Dict]:
    try:
        df = pd.read_csv(filepath, sep=",")
        
        return df.to_dict('records')
        
    except Exception as e:
        return e


def read_json(filepath: str) -> List[Dict]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return data
        
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list) and len(value) > 0:
                    return value
            
            return [data]
        
        return [data]
            
    except Exception as e:
        
        return e


