import pandas as pd
import hashlib
from typing import Union, Dict
from datasets import Dataset

try: from datasets import Dataset as HFDataset
except Exception: HFDataset = None

def __hash_file_(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def __hash_dataframe_(df: pd.DataFrame) -> str:
    # deterministic: to bytes via to_numpy + dtypes
    h = hashlib.sha256()
    h.update(pd.util.hash_pandas_object(df, index=True).values.tobytes())
    return h.hexdigest()

def profile_dataset_auto(
        data: Union[str, pd.DataFrame, Dataset]
) -> Dict:
    """
    Dataset autodetection: CSV file, pandas.DataFrame, HuggingFace Dataset
    """
    
    if isinstance(data, str):
        df = pd.read_csv(data)
        path = data
        hash_val = __hash_file_(data)
    elif isinstance(data, pd.DataFrame):
        df = data
        path = 'in_memory_df'
        hash_val = __hash_dataframe_(df)
    elif HFDataset and isinstance(data, HFDataset):
        df = data.to_pandas()
        path = 'hd_dataset'
        hash_val = __hash_dataframe_(df)
    else:
        # TODO : something else? to search! 
        # TODO : make support of custom dataset
        raise ValueError('Unsupported dataset type')

    return {
        'name': path.split('/')[-1],
        'path': path,
        'num_rows': int(len(df)),
        'num_columns': int(len(df.columns)),
        'table_schema': {
            str(col): str(dtype)
            for col, dtype in zip(df.columns, df.dtypes)
        },
        'hash': hash_val
    }