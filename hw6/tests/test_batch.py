#from hw6.batch import read_data
#from .. import batch
from ..batch import prepare_data
from datetime import datetime
import pandas as pd
from deepdiff import DeepDiff

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_read_data():
    #read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet', ['PULocationID', 'DOLocationID'])
    

    data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    actual_output = prepare_data(df, ['PULocationID', 'DOLocationID'])
    
    expected_output = pd.Series([9.0, 8.0], name='duration')
    assert DeepDiff(expected_output, actual_output['duration'], ignore_order=True) == {}

    expected_output = {
        'PULocationID': ['-1', '1'],
        'DOLocationID': ['-1', '1'],
        'tpep_pickup_datetime': [pd.Timestamp('2023-01-01 01:01:00'), pd.Timestamp('2023-01-01 01:02:00')],
        'tpep_dropoff_datetime': [pd.Timestamp('2023-01-01 01:10:00'), pd.Timestamp('2023-01-01 01:10:00')],
        'duration': [9.0, 8.0]
    }
    assert DeepDiff(expected_output, actual_output.to_dict(orient='list'), ignore_order=True) == {}

