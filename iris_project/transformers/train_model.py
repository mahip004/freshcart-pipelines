from __future__ import annotations
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(fn): return fn
    def test(fn): return fn

@transformer
def train_model(df: pd.DataFrame, max_depth: int = 3, random_state: int = 42):
    train = df[df.split == "train"]
    holdout = df[df.split == "test"]
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
    model.fit(train.drop(columns=["target", "split"]), train.target)
    accuracy = float(model.score(holdout.drop(columns=["target", "split"]), holdout.target))
    return {"model": model, "accuracy": accuracy, "max_depth": max_depth,
            "X_test": holdout.drop(columns=["target", "split"]), "y_test": holdout.target}

@test
def test_accuracy_is_acceptable(output, **kwargs):
    assert output["accuracy"] >= 0.9, f"accuracy too low: {output['accuracy']:.3f}"
