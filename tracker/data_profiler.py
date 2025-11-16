import pandas as pd
import hashlib
from typing import Union, Dict
from datasets import Dataset

def profile_dataset_auto(data: Union[str, pd.DataFrame, Dataset]) -> Dict:
    """
    Dataset autodetection: CSV file, pandas.DataFrame, HuggingFace Dataset
    """
    
    # CSV file
    if isinstance(data, str):
        df = pd.read_csv(data)
        path = data
        h = hashlib.sha256()
        with open(data, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        hash_value = h.hexdigest()
    
    # pandas DataFrame
    elif isinstance(data, pd.DataFrame):
        df = data
        path = "in_memory_df.csv"
        h = hashlib.sha256()
        h.update(pd.util.hash_pandas_object(df).values.tobytes())
        hash_value = h.hexdigest()
    
    # HuggingFace Dataset
    elif isinstance(data, Dataset):
        df = data.to_pandas()
        path = "hf_dataset"
        h = hashlib.sha256()
        h.update(pd.util.hash_pandas_object(df).values.tobytes())
        hash_value = h.hexdigest()
    
    else:
        raise ValueError("Unsupported dataset type")
    
    return {
        "name": path.split("/")[-1],
        "path": path,
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "schema": {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)},
        "hash": hash_value
    }
