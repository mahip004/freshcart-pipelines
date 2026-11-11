from pathlib import Path

import pandas as pd

try:
    from mage_ai.data_preparation.decorators import data_exporter, test
except ImportError:
    def data_exporter(fn):
        return fn
    def test(fn):
        return fn


@data_exporter
def save_metrics(result, output_path="iris_metrics.csv", **kwargs):
    metrics = pd.DataFrame.from_dict(result["metrics"], orient="index")
    metrics.to_csv(output_path, index_label="label")
    return output_path


@test
def test_metrics_file(output, **kwargs):
    path = Path(output)
    assert path.is_file(), f"metrics file was not created: {path}"
    assert path.stat().st_size > 0, f"metrics file is empty: {path}"
