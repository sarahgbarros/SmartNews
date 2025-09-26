import pandas as pd
import json
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def read_csv(filepath: str) -> List[Dict]:
    try:
        if not os.path.exists(filepath):
            return []
        
        df = pd.read_csv(filepath, sep=",")
        return df.to_dict('records')
        
    except Exception as e:
        return []

def read_json(filepath: str) -> List[Dict]:
    try:
        if not os.path.exists(filepath):
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    return value
            return [data]
        else:
            return [data]
            
    except Exception as e:
        logger.error(f"Erro ao ler JSON {filepath}: {e}")
        return []

