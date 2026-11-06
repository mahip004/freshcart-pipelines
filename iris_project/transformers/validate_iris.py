from sklearn.datasets import load_iris
try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(fn): return fn
    def test(fn): return fn

@transformer
def validate_iris(df, **kwargs):
    assert not df.isna().any().any()
    assert df["target"].nunique() == 3
    return df

@test
def test_three_classes(output, **kwargs):
    assert output["target"].nunique() == 3

