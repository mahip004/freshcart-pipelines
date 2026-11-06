import pandas as pd
try:
    from mage_ai.data_preparation.decorators import data_exporter, test
except ImportError:
    def data_exporter(fn): return fn
    def test(fn): return fn

@data_exporter
def save_results(result, output_path="iris_predictions.csv", **kwargs):
    pred = result["model"].predict(result["X_test"])
    pd.DataFrame({"actual": result["y_test"].to_numpy(), "predicted": pred}).to_csv(output_path, index=False)
    return output_path

@test
def test_file_path(output, **kwargs):
    assert output.endswith("iris_predictions.csv")

