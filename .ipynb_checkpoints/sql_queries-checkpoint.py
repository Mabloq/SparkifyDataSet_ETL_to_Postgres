# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songlplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays 
        (songplay_id serial, 
         start_time bigint NOT NULL,
         user_id varchar(20) NOT NULL,
         level text NOT NULL,
         song_id varchar(20) NOT NULL,
         artist_id varchar(20) NOT NULL,
         session_id text NOT NULL,
         location text NOT NULL,
         user_agent text NOT NULL,
         UNIQUE (start_time, user_id)
         );
       
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
        (user_id varchar(20) NOT NULL,
         first_name text NOT NULL,
         last_name text NOT NULL,
         gender text NOT NULL,
         level text NOT NULL,
         UNIQUE(user_id)
        );
        
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
        (song_id varchar(20),
         title text,
         artist_id varchar(20),
         year smallint,
         duration numeric(10,5),
         UNIQUE(song_id)
        );
        
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
        (artist_id varchar(20) NOT NULL,
         name text NOT NULL,
         location text NOT NULL,
         latitude numeric(10,5) NOT NULL,
         longitude numeric(10,5) NOT NULL,
         UNIQUE(artist_id)
        )
        
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
        (start_time bigint NOT NULL,
         hour smallint NOT NULL,
         day smallint NOT NULL,
         week smallint NOT NULL,
         month smallint NOT NULL,
         year smallint NOT NULL,
         weekday smallint NOT NULL,
         UNIQUE(start_time)
        )
        
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays
        (start_time,
         user_id,
         song_id,
         artist_id,
         level,
         session_id,
         location,
         user_agent
         ) 
         VALUES
         %s
         ON CONFLICT(start_time, user_id)
         DO NOTHING
""")

user_table_insert = ("""
    INSERT INTO users
        (user_id,
         first_name,
         last_name,
         gender,
         level
        )
        VALUES
        %s
        ON CONFLICT(user_id)
        DO NOTHING
""")

song_table_insert = ("""
    INSERT INTO songs
    (song_id,
     title,
     artist_id,
     year,
     duration
    )
    VALUES
    %s
    ON CONFLICT(song_id)
    DO NOTHING
""")

artist_table_insert = ("""
    INSERT INTO artists
        (artist_id,
         name,
         location,
         latitude,
         longitude
        )
        VALUES
        %s
        ON CONFLICT(artist_id)
        DO NOTHING
""")


time_table_insert = ("""
    INSERT INTO time
        (start_time,
         hour,
         day,
         week,
         month,
         year,
         weekday
        )
        VALUES
        %s
        ON CONFLICT(start_time)
        DO NOTHING
""")

# FIND SONGS
# get songid and artistid from song and artist tables
    
song_select = ("""
    SELECT s.song_id, a.artist_id
    FROM songs AS s
    JOIN artists AS a ON (s.artist_id = a.artist_id)
    WHERE a.name = (%s) AND s.title = (%s) AND s.duration = (%s)
""")
   

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]