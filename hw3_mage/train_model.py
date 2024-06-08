import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


def create_data_dicts(df: pd.DataFrame) -> dict:
    df["PULocationID"] = df["PULocationID"].astype(str)
    df["DOLocationID"] = df["DOLocationID"].astype(str)
    return df[["PULocationID", "DOLocationID"]].to_dict(orient='records')


@data_exporter
def export_data(df, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """

    data_dicts = create_data_dicts(df)
    vectorizer = DictVectorizer(sparse=True)
    feature_matrix = vectorizer.fit_transform(data_dicts)
    print("Feature matrix shape:", feature_matrix.shape)
        
    model = LinearRegression()
    model.fit(feature_matrix, df['duration'])

    predictions = model.predict(feature_matrix)

    rmse = mean_squared_error(df['duration'], predictions) ** 0.5
    print("Root Mean Squared Error (RMSE) on training data:", rmse)
    print(model.intercept_)

    return model, vectorizer
