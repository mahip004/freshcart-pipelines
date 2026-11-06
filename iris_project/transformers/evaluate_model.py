import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(fn): return fn
    def test(fn): return fn

@transformer
def evaluate_model(result, **kwargs):
    pred = result["model"].predict(result["X_test"])
    return {"confusion_matrix": confusion_matrix(result["y_test"], pred).tolist(),
            "metrics": classification_report(result["y_test"], pred, output_dict=True),
            "accuracy": result["accuracy"]}

@test
def test_metrics(output, **kwargs):
    assert len(output["confusion_matrix"]) == 3
    assert 0 <= output["accuracy"] <= 1

