# Datasets to discretize
from pandas import DataFrame, read_csv, cut, qcut
from ds_charts import get_variable_types

data_air: DataFrame = read_csv('data/air_quality_scaled_zscore_fs.csv')
#data_air["ALARM"] = data_air["ALARM"].map({0: "Safe", 1: "Danger"})
data_air.pop('ALARM')
filename_air = "air_quality"

data_nyc: DataFrame = read_csv('data/NYC_collisions_scaled_minmax_fs.csv')
#data_nyc["PERSON_INJURY"] = data_nyc["PERSON_INJURY"].map({0: "Injured", 1: "Killed"})
data_nyc.pop('PERSON_INJURY')
filename_nyc = "NYC_collisions"


def discard_numeric(data: DataFrame, filename):
    variables = get_variable_types(data)['Numeric']
    data.drop(labels=variables, axis=1, inplace=True)
    data.to_csv(f'data/{filename}_discretized_no_numeric.csv', index=False)
    
#discard_numeric(data_air, filename_air)
#discard_numeric(data_nyc, filename_nyc)

def equal_width(data: DataFrame, filename):
    variables = get_variable_types(data)['Numeric']
    for var in variables:
        print("var:",var,"bins:",cut(data[var], 50))
        
        #data.drop(labels=variables, axis=1, inplace=True)
    #data.to_csv(f'data/{filename}_discretized_equal_width.csv', index=False)
    
equal_width(data_air, filename_air)
equal_width(data_nyc, filename_nyc)

def equal_frequency(data: DataFrame, filename):
    variables = get_variable_types(data)['Numeric']
    for var in variables:
        print("var:",var,"bins:",qcut(data[var], 10, duplicates="drop"))
        
        #data.drop(labels=variables, axis=1, inplace=True)
    #data.to_csv(f'data/{filename}_discretized_equal_frequency.csv', index=False)
    
equal_frequency(data_air, filename_air)
equal_frequency(data_nyc, filename_nyc)