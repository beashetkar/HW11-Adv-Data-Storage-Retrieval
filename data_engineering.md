
# Surfs Up! Climate Analysis.

### Step 1 - Data Engineering (file data_engineering.ipynb).

We use two csv files: hawaii_measurements.csv and hawaii_stations.csv, and do all the Data Cleaning tasks and save the results
in clean_measurements.csv and clean_stations.csv.

The dependencies use in data_engineering.ipynb file are:

```python
# Dependencies
import os
import pandas as pd
```

#### Cleaning Data  - Table Measurements -

 I calculate the percentage of total missing rows in measurement (Total of missing prcp/ Total rows) and the result of missing data is : 7.40153452685422; so that, I use the interpolate method instead of removing rows with Naan values with df.dropna(axis=0, how='any').

```python

clean_measurements_df = measurements_df.interpolate(method='linear', axis=0).ffill().bfill()
print(f"Totals of missing data in clean_measurements :\n{clean_measurements_df.count()} ")

clean_measurements_df.head()
```
