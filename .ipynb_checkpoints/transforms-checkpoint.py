import pandas as pd

def transform_time(time_df):
    #define column values
    values = ['artist','ts','userId','level','name','session_id','location','userAgent','artistId']
    #recreate time_df with approp. columns for insertion
    time_df = pd.DataFrame(time_df, columns=values) 
    time_df = pd.DataFrame(time_df, columns=values) 


    # convert timestamp column to datetime
    t = pd.to_datetime(time_df['ts'], unit='ms')
    
    # use dt attributes to extract date values and create new dataframe
    time_data = {
        "start_time": time_df['ts'],
        "hour" : t.dt.hour,
        "day" : t.dt.day,
        "week": t.dt.week,
        "month" : t.dt.month,
        "year" : t.dt.year,
        "weekday": t.dt.dayofweek
    }
    # insert time data records
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(time_data, columns=column_labels)
    #convert tolist() to convert numpy.int64/32 data types to python int
    time_df = time_df.values.tolist()
    #covert times to list of tuples to build bulk value arg strings
    time_df = [tuple(x) for x in time_df]
    
    return time_df