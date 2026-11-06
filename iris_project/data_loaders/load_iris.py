import pandas as pd
from sklearn.datasets import load_iris
try:
    from mage_ai.data_preparation.decorators import data_loader
except ImportError:
    def data_loader(fn): return fn

@data_loader
def load_data(*args, **kwargs) -> pd.DataFrame:
    return load_iris(as_frame=True).frame

