
# Surfs Up! Climate Analysis.

### Step 1 - Data Engineering

The climate data for Hawaii is provided through two CSV files. Start by using Python and Pandas to inspect the content of these files and clean the data.

Create a Jupyter Notebook file called data_engineering.ipynb and use this to complete all of your Data Engineering tasks.

* Use Pandas to read in the measurement and station CSV files as DataFrames.

* Inspect the data for NaNs and missing values. You must decide what to do with this data.

* Save your cleaned CSV files with the prefix clean_.


```python
# Dependencies
import os
import pandas as pd
```


```python
# Function for reading files in given directory.

def read_base_file(data_folder, base_file):
    file_csv = os.path.join(data_folder,base_file)
    try:
        df = pd.read_csv(file_csv)
    except (IOException, e):
        print ("Error in reading", base_file)
        print (e)
        df = pd.DataFrame()
    return df
```


```python
# CSV files to load

data_folder = 'Resources'
base_file1 = 'hawaii_measurements.csv'
measurements_df = read_base_file(data_folder,base_file1)
base_file2 = 'hawaii_stations.csv'
stations_df = read_base_file(data_folder,base_file2)
```

### Cleaning Data  - Table Measurements -


```python
# How many columns and rows has our initial dataset.
measurements_df.shape
```




    (19550, 4)




```python
measurements_df.columns
```




    Index(['station', 'date', 'prcp', 'tobs'], dtype='object')




```python
measurements_df.head(10)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519397</td>
      <td>2010-01-01</td>
      <td>0.08</td>
      <td>65</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00519397</td>
      <td>2010-01-02</td>
      <td>0.00</td>
      <td>63</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00519397</td>
      <td>2010-01-03</td>
      <td>0.00</td>
      <td>74</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00519397</td>
      <td>2010-01-04</td>
      <td>0.00</td>
      <td>76</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00519397</td>
      <td>2010-01-06</td>
      <td>NaN</td>
      <td>73</td>
    </tr>
    <tr>
      <th>5</th>
      <td>USC00519397</td>
      <td>2010-01-07</td>
      <td>0.06</td>
      <td>70</td>
    </tr>
    <tr>
      <th>6</th>
      <td>USC00519397</td>
      <td>2010-01-08</td>
      <td>0.00</td>
      <td>64</td>
    </tr>
    <tr>
      <th>7</th>
      <td>USC00519397</td>
      <td>2010-01-09</td>
      <td>0.00</td>
      <td>68</td>
    </tr>
    <tr>
      <th>8</th>
      <td>USC00519397</td>
      <td>2010-01-10</td>
      <td>0.00</td>
      <td>73</td>
    </tr>
    <tr>
      <th>9</th>
      <td>USC00519397</td>
      <td>2010-01-11</td>
      <td>0.01</td>
      <td>64</td>
    </tr>
  </tbody>
</table>
</div>




```python
def num_missing(x):
  return sum(x.isnull())
```


```python
# Check if measurements has duplicated values

duplicated = measurements_df.duplicated(subset=['station', 'date', 'prcp', 'tobs']).sum()
print(f"Total of duplicated values in measurement_df : {duplicated} ")

# Applying per column:
print (f"Missing values per column in measurements_df:\n{measurements_df.apply(num_missing, axis=0)}")

# Applying per row:
print (f"\nMissing values per row in measurements_df:\n{measurements_df.apply(num_missing, axis=1).head(20)}")
```

    Total of duplicated values in measurement_df : 0 
    Missing values per column in measurements_df:
    station       0
    date          0
    prcp       1447
    tobs          0
    dtype: int64
    
    Missing values per row in measurements_df:
    0     0
    1     0
    2     0
    3     0
    4     1
    5     0
    6     0
    7     0
    8     0
    9     0
    10    0
    11    0
    12    0
    13    0
    14    0
    15    0
    16    0
    17    0
    18    0
    19    0
    dtype: int64
    


```python
# Percentage of total missing rows in measurement (Total of missing prcp/ Total rows)

missing_prcp = sum(pd.isnull(measurements_df['prcp']))
pctg_Naan_prcp = (missing_prcp/len(measurements_df['prcp']))*100
print(f"The percentage of missing data is : {pctg_Naan_prcp}" )
```

    The percentage of missing data is : 7.40153452685422
    


```python
# Using interpolate method instead of removing rows with Naan values with df.dropna(axis=0, how='any')
# ‘linear’: ignore the index and treat the values as equally spaced.
# axis = 0: fill column-by-column
# ffill() Synonym for DataFrame.fillna(method='ffill')
# bffill() Synonym fo DataFrame.fillna(method='bfill')

clean_measurements_df = measurements_df.interpolate(method='linear', axis=0).ffill().bfill()
print(f"Totals of missing data in clean_measurements :\n{clean_measurements_df.count()} ")

clean_measurements_df.head()
```

    Totals of missing data in clean_measurements :
    station    19550
    date       19550
    prcp       19550
    tobs       19550
    dtype: int64 
    




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519397</td>
      <td>2010-01-01</td>
      <td>0.08</td>
      <td>65</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00519397</td>
      <td>2010-01-02</td>
      <td>0.00</td>
      <td>63</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00519397</td>
      <td>2010-01-03</td>
      <td>0.00</td>
      <td>74</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00519397</td>
      <td>2010-01-04</td>
      <td>0.00</td>
      <td>76</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00519397</td>
      <td>2010-01-06</td>
      <td>0.03</td>
      <td>73</td>
    </tr>
  </tbody>
</table>
</div>




```python
clean_measurements_df.dtypes
```




    station     object
    date        object
    prcp       float64
    tobs         int64
    dtype: object



### Cleaning Data - Table Stations -


```python
# How many columns and rows has our initial dataset.
stations_df.shape
```




    (9, 5)




```python
stations_df.columns
```




    Index(['station', 'name', 'latitude', 'longitude', 'elevation'], dtype='object')




```python
# No Missing data in Stations DataFrame
stations_df.head(10)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>elevation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519397</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00513117</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.42340</td>
      <td>-157.80150</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>21.52130</td>
      <td>-157.83740</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00517948</td>
      <td>PEARL CITY, HI US</td>
      <td>21.39340</td>
      <td>-157.97510</td>
      <td>11.9</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3, HI US</td>
      <td>21.49920</td>
      <td>-158.01110</td>
      <td>306.6</td>
    </tr>
    <tr>
      <th>5</th>
      <td>USC00519523</td>
      <td>WAIMANALO EXPERIMENTAL FARM, HI US</td>
      <td>21.33556</td>
      <td>-157.71139</td>
      <td>19.5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>USC00519281</td>
      <td>WAIHEE 837.5, HI US</td>
      <td>21.45167</td>
      <td>-157.84889</td>
      <td>32.9</td>
    </tr>
    <tr>
      <th>7</th>
      <td>USC00511918</td>
      <td>HONOLULU OBSERVATORY 702.2, HI US</td>
      <td>21.31520</td>
      <td>-157.99920</td>
      <td>0.9</td>
    </tr>
    <tr>
      <th>8</th>
      <td>USC00516128</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Check if stations has duplicated values
duplicated = stations_df.duplicated(subset=['station', 'name', 'latitude', 
                                            'longitude', 'elevation']).sum()
print(f"Total of duplicated values in stations_df : {duplicated} ")

# Check if stations does not have missing data

# Applying per column:
print (f"Missing values per column in stations_df:\n{stations_df.apply(num_missing, axis=0)}")

# Applying per row:
print (f"\nMissing values per row in stations_df:\n{stations_df.apply(num_missing, axis=1).head(10)}")
```

    Total of duplicated values in stations_df : 0 
    Missing values per column in stations_df:
    station      0
    name         0
    latitude     0
    longitude    0
    elevation    0
    dtype: int64
    
    Missing values per row in stations_df:
    0    0
    1    0
    2    0
    3    0
    4    0
    5    0
    6    0
    7    0
    8    0
    dtype: int64
    

### Save cleaned data to CSV files.


```python
# Save to a csv file.
clean_measurements_df.to_csv('Resources/clean_measurements.csv', index=False)
stations_df.to_csv('Resources/clean_stations.csv', index=False)
```
