import polars as pl
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def prepare_data(url: str, remove_outliers: bool = True) -> pl.DataFrame:
    df = pl.read_parquet(url)
    print("Number of columns in dataframe:", df.shape[1])

    #df.glimpse()

    df = df.with_columns(
        (pl.col("tpep_dropoff_datetime") - pl.col("tpep_pickup_datetime")).dt.total_minutes().alias("duration")
    )
    print("Standard Deviation of duration:", df['duration'].std())

    if remove_outliers:
        num_rows = df.height
        df = df.filter((pl.col("duration") >= 1) & (pl.col("duration") <= 60))
        print(f"Percentage of rows remaining: {(df.height/num_rows) * 100}%")
        
    return df


# Convert the 'PULocationID' and 'DOLocationID' columns to string to prepare for one-hot encoding
def create_data_dicts(df: pl.DataFrame) -> dict:
    df = df.with_columns(
        pl.col("PULocationID").cast(pl.Utf8).alias("PULocationID"),
        pl.col("DOLocationID").cast(pl.Utf8).alias("DOLocationID")
    )
    return df.select(["PULocationID", "DOLocationID"]).to_dicts()

def fit_model_and_vectorizer(url: str) -> [LinearRegression, DictVectorizer]:
    df = prepare_data(url)

    data_dicts = create_data_dicts(df)
    vectorizer = DictVectorizer(sparse=True)
    feature_matrix = vectorizer.fit_transform(data_dicts)
    print("Feature matrix shape:", feature_matrix.shape)
        
    model = LinearRegression()
    model.fit(feature_matrix, df['duration'])

    predictions = model.predict(feature_matrix)

    rmse = mean_squared_error(df['duration'], predictions) ** 0.5
    print("Root Mean Squared Error (RMSE) on training data:", rmse)

    return model, vectorizer


def calc_validation_rmse(model: LinearRegression, vectorizer: DictVectorizer, url: str):
    df = prepare_data(url, remove_outliers = True)
    data_dicts = create_data_dicts(df)

    feature_matrix = vectorizer.transform(data_dicts)
    predictions = model.predict(feature_matrix)

    rmse = mean_squared_error(df['duration'], predictions) ** 0.5
    print("Root Mean Squared Error (RMSE) on validation data:", rmse)


def main():
    model, vectorizer = fit_model_and_vectorizer(URL_JAN)
    calc_validation_rmse(model, vectorizer, URL_FEB)

URL_JAN = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
URL_FEB = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-02.parquet"


if __name__ == '__main__':
    main()

