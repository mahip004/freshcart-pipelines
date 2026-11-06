from __future__ import annotations
import pandas as pd
from sklearn.model_selection import train_test_split

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(fn): return fn
    def test(fn): return fn

@transformer
def transform(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> pd.DataFrame:
    """Return Iris rows tagged train/test using a reproducible stratified split."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")
    if "target" not in df.columns:
        raise ValueError("input must contain a target column")
    train_idx, test_idx = train_test_split(
        df.index, test_size=test_size, random_state=random_state,
        stratify=df["target"],
    )
    out = df.copy()
    out["split"] = "train"
    out.loc[test_idx, "split"] = "test"
    return out

@test
def test_split_sizes(output: pd.DataFrame, **kwargs):
    assert (output["split"] == "train").sum() == 120
    assert (output["split"] == "test").sum() == 30

