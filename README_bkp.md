# HW11-Adv-Data-Storage-Retrieval
Surfs Up! is a Climate Analysis Exercise 

### Step 1 - Data Engineering (file data_engineering.ipynb).

We use two csv files: hawaii_measurements.csv and hawaii_stations.csv, and do all the Data Cleaning tasks and save the results
in clean_measurements.csv and clean_stations.csv.

### Step 2 Database Engineering (file database_engineering.ipynb).

With the function  read_base_file,  I read the files clean_measurements.csv and clean_stations.csv in a given directory. The default directory is Resources/

def read_base_file(data_folder, base_file):
'''
    file_csv = os.path.join(data_folder,base_file)
    try:
        df = pd.read_csv(file_csv)
    except (IOException, e):
        print ("Error in reading", base_file)
        print (e)
        df = pd.DataFrame()
    return df
'''    

Then I Use `declarative_base` from SQLAlchemy to model the measurement table an station table as an ORM classes. Finally, 
I create an engine to a SQLite database file called `hawaii.sqlite` and use `create_all` to create the measurement and station tables in the database.

### Step 3 - Climate Analysis and Exploration (file climate_analysis.ipynb)

I define the lenght of the trip for 12 days. I look for the last date of the data and find the date one year ago using the function 

df get_start_date(end_date,t_move):

'''
qry = session.query(func.max(Measurements.date).label("last_date"))
res = qry.one()
last_date = res.last_date
year_ago_date = get_start_date(last_date, 'Y')
'''

def get_start_date(end_date,t_move):

    endDate = datetime.strptime(end_date, "%Y-%m-%d").date()
    ''' # vacation trip was 12 days long
    trip = 12

    ''' # reconstruct date fully
    if t_move == 'Y' :
        startDate = datetime(endDate.year - 1, endDate.month, endDate.day)
    else:
        startDate = datetime(endDate.year, endDate.month, endDate.day-trip)
    datetime.strftime(startDate, "%Y-%m-%d").replace(' 0', ' ')
    return (datetime.strftime(startDate, "%Y-%m-%d").replace(' 0', ' ')) 

#### Precipitation Analysis

I design a query to retrieve the last 12 months of precipitation data and select only the date and prcp values:

'''
prcp_year_df = pd.read_sql(session.query(Measurements.date,Measurements.prcp).\
               filter(Measurements.date.between(year_ago_date, last_date)).\
               order_by(Measurements.date.asc()).statement, session.bind)
'''              
#### Station Analysis

'''
total_num_stations = session.query(Stations.station).count()
print(f"Total number  of stations : {total_num_stations} ")
'''

The query for most Active stations.
'''
top_stations = session.query(Measurements.station, Stations.name, func.count(Measurements.tobs)).\
            filter(Measurements.station == Stations.station).\
            group_by(Measurements.station).\
            order_by(func.count(Measurements.tobs).desc()).all()
 '''
 
