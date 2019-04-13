# ETL Pipeline Json Files -> Pandas -> PostgresDB


Given a **song** data set and a user **events** data set, this code project extracts the json data from song json files and dumps it into a pandas dataframe to be filterd and transformed before being bulk inserted into a postgres database.

[Link to Excel Documentation for the ETL Process](https://drive.google.com/file/d/1amL35lKId6jjRxZAdXvKhsrlplXUR_uy/view?usp=sharing)

# song_data.json -> songs table
| Source Column            	| Source Data Type 	| Source Nullable 	| Transformation             	| Destination Column 	| Dest. Data Type 	| Dest. Nullable 	| Reason for transformation                                                   	|
|--------------------------	|------------------	|-----------------	|----------------------------	|--------------------	|-----------------	|----------------	|-----------------------------------------------------------------------------	|
| song_id                  	| string           	| no              	|                            	| song_id            	| varchar(20)     	| no             	|                                                                             	|
| title                    	| string           	| no              	|                            	| title              	| varchar(100)    	| no             	|                                                                             	|
| artist_id                	| sting            	| no              	|                            	| artist_id          	| varchar(20)     	| no             	|                                                                             	|
| year                     	| number           	| no              	|                            	| year               	| int             	| no             	|                                                                             	|
| duration                 	| number           	| no              	|                            	| duration           	| numeric(5)      	| no             	|                                                                             	|

# song_data.json -> artists table
| Source Column            	| Source Data Type 	| Source Nullable 	| Transformation             	| Destination Column 	| Dest. Data Type 	| Dest. Nullable 	| Reason for transformation                                                   	|
|--------------------------	|------------------	|-----------------	|----------------------------	|--------------------	|-----------------	|----------------	|-----------------------------------------------------------------------------	|
| artist_id                	| string           	| no              	|                            	| artist_id          	| varchar(20)     	| NO             	|                                                                             	|
| artist_name              	| string           	| no              	|                            	| name               	| text            	| NO             	|                                                                             	|
| artist_location          	| string           	| yes             	| convert to "NA"            	| location           	| text            	| NO             	| Want to be able to filter by location includeing when location is not avail 	|
| artist_latitude          	| number           	| yes             	| convert to 0 if null       	| lattitude          	| numeic(5)       	| NO             	| want to be able to filter by lattitude, including when not avail            	|
| artist_longitude         	| number           	| yes             	| convert to 0 if null       	| longitude          	| numeric(5)      	| NO             	| want to be able to filter by lattitude, including when not avail            	|

# log_data.json -> time table

| Source Column            	| Source Data Type 	| Source Nullable 	| Transformation             	| Destination Column 	| Dest. Data Type 	| Dest. Nullable 	| Reason for transformation                                                   	|
|--------------------------	|------------------	|-----------------	|----------------------------	|--------------------	|-----------------	|----------------	|-----------------------------------------------------------------------------	|
| ts                       	| datetime          |                 	| convert to pd.to_datetime  	| start_time         	|                 	|                	|                                                                             	|
| ts                       	| datetime          |                 	| extract get hour from ts   	| hour               	| smallint        	|                	|                                                                             	|
| ts                       	| datetime          |                 	| extract get day from ts    	| day                	| smallint        	|                	|                                                                             	|
| ts                       	| datetime          |                 	| extract week from ts       	| week               	| smallint        	|                	|                                                                             	|
| ts                       	| datetime          |                 	| extract month from ts      	| month              	| smallint        	|                	|                                                                             	|
| ts                       	| datetime          |                 	| extract year from ts       	| year               	| smallint        	|                	|                                                                             	|
| ts                       	| datetime          |                 	| extract dayofweek  from ts 	| weekday(0-6)       	| smallint        	|                	|                                                                             	|

# log_data.json -> users table
| Source Column            	| Source Data Type 	| Source Nullable 	| Transformation             	| Destination Column 	| Dest. Data Type 	| Dest. Nullable 	| Reason for transformation                                                   	|
|--------------------------	|------------------	|-----------------	|----------------------------	|--------------------	|-----------------	|----------------	|-----------------------------------------------------------------------------	|
| userId                   	| int              	|                 	|                            	| user_id            	| int             	|                	|                                                                             	|
| firstName                	|                  	|                 	|                            	| first_name         	| varchar(50)     	|                	|                                                                             	|
| lastName                 	|                  	|                 	|                            	| last_name          	| varchar(50)     	|                	|                                                                             	|
| gender                   	|                  	|                 	|                            	| gender             	| text            	|                	|                                                                             	|
| level                    	|                  	|                 	|                            	| level              	| varchar(10)     	|                	|                                                                             	|

# log_data.json -> song plays table
| Source Column            	| Source Data Type 	| Source Nullable 	| Transformation             	| Destination Column 	| Dest. Data Type 	| Dest. Nullable 	| Reason for transformation                                                   	|
|--------------------------	|------------------	|-----------------	|----------------------------	|--------------------	|-----------------	|----------------	|-----------------------------------------------------------------------------	|
| none                     	|                  	|                 	|                            	| songplay_id        	| serial          	|                	|                                                                             	|
| ts                       	|                  	|                 	|                            	| start_time         	| bigint          	|                	|                                                                             	|
| UserId                   	|                  	|                 	|                            	| user_id            	| varchar(20)     	|                	|                                                                             	|
| level                    	|                  	|                 	|                            	| level              	| text            	|                	|                                                                             	|
| songId                   	|                  	|                 	|                            	| song_id            	| varchar(20)     	|                	|                                                                             	|
| sessionId                	|                  	|                 	|                            	| session_id         	| text            	|                	|                                                                             	|
| location                 	|                  	|                 	|                            	| location           	| text            	|                	|                                                                             	|
| userAgent                	|                  	|                 	|                            	| user_agent         	| text            	|                	|                                                                             	|
| artist                   	|                  	|                 	|                            	| artist_id          	| varchar(20)     	|                	|                                                                             	|


# Prequisites
  - Must have python 3.x installed on your machine
  - Must have a local postgresdb installed on your machine
  - Must create  "studentdb" database with a user "student" with CREATE & Read Priveleges and password "student"
  - **Connection String should work:** psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")


# Usage
  - In terminal, clone this github project and cd into the project folder
  Run these commands:
    ```sh
    python create_tables.py
    python etl.py
    ```
  - The tabels will be autmatically created abd populated with data read from the /data folder
# Using Your own db name and and user account
You may want to use your own existing database names and users, you can edit the connection in ~/create_tables.py to your use case.
```python
    def create_database():
    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    return cur, conn
```





