
# Surfs Up! Climate Analysis.

### Step 2 - Database Engineering

* Use SQLAlchemy to model your table schemas and create a sqlite database for your tables.

* Create a Jupyter Notebook called database_engineering.ipynb and use this to complete all of your Database Engineering work.

* You will need one table for measurements and one for stations.

* Use Pandas to read your cleaned measurements and stations CSV data.

* Use the engine and connection string to create a database called hawaii.sqlite.

* Use declarative_base and create ORM classes for each table.

* You will need a class for Measurement and for Station.

* Make sure to define your primary keys.

* Once you have your ORM classes defined, create the tables in the database using create_all.



```python
# Dependencies

import os
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
#from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ( Column, 
                         Integer, 
                         String, 
                         DateTime, 
                         Float
)
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

if os.path.isfile('./hawaii.sqlite'):    # True
    !rm hawaii.sqlite

data_folder = 'Resources'
base_file1 = 'clean_measurements.csv'
measurements_df = read_base_file(data_folder,base_file1)
base_file2 = 'clean_stations.csv'
stations_df = read_base_file(data_folder,base_file2)
```


```python
measurements_df.head()
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
      <td>0.03</td>
      <td>73</td>
    </tr>
  </tbody>
</table>
</div>




```python
stations_df.head()
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
      <td>21.2716</td>
      <td>-157.8168</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00513117</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.4234</td>
      <td>-157.8015</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>21.5213</td>
      <td>-157.8374</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00517948</td>
      <td>PEARL CITY, HI US</td>
      <td>21.3934</td>
      <td>-157.9751</td>
      <td>11.9</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3, HI US</td>
      <td>21.4992</td>
      <td>-158.0111</td>
      <td>306.6</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Use `declarative_base` from SQLAlchemy to model the measurement table
# an station table as an ORM classes

Base = declarative_base()

class Measurements(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(String)
    prcp = Column(Float)
    tobs = Column(Integer)
    
class Stations(Base):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    station = Column(String)
    name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
```


```python
# Create an engine to a SQLite database file called `hawaii.sqlite`
from sqlalchemy import create_engine, MetaData

engine = create_engine("sqlite:///hawaii.sqlite")

# Create a connection to the engine called `conn`
conn = engine.connect()

# Use `create_all` to create the measurement and station tables in the database
Base.metadata.create_all(engine)

from sqlalchemy.orm import Session

session = Session(bind=engine)
session.commit()
```


```python
measurements_df.to_sql(con=engine, name='measurement', if_exists= 'append', index=False)
stations_df.to_sql(con=engine, name='station', if_exists= 'append', index=False)
```
