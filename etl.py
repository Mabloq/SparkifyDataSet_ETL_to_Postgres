import os
import glob
import psycopg2
import pandas as pd
import json
from sql_queries import *
from transforms import transform_time


def gen_data_arr(filepath):
    data = []
    for f in filepath:
        with open(f) as json_data:
            data.append(json.load(json_data))
    return data


def multi_json_obj(filepath):
    data = []
    for f in filepath:
        for line in open(f, mode="r"):
            data.append(json.loads(line))
    return data


def process_song_file(cur, filepath):
    # ===============1.) Load json filedata int song arr =====================

    songs = gen_data_arr(filepath)

    # ===============2.) CREATE PANDAS DATAFRAMES ============================

    # creating songs dataframe
    songs_df = pd.DataFrame(songs, columns=['song_id', 'title', 'artist_id', 'year', 'duration'])

    # creating artist dataframe
    artist_df = pd.DataFrame(songs, columns=['artist_id', 'artist_name', 'artist_location', \
                                             'artist_latitude', 'artist_longitude'])
    # ===============2.) BULK INSERT TO SONGS AND ARTISTS TABLES ============================

    # covert songs to list of tuples to build bulk value arg strings
    song_data = [tuple(x) for x in songs_df.values]
    # build bulk value arg string to avoid overhead of multiple execute statements
    song_args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s)", x).decode("utf-8") for x in song_data)
    # bulk insert songs
    cur.execute(song_table_insert % song_args_str)

    # covert artists to list of tuples to build bulk value arg string
    artist_data = [tuple(x) for x in artist_df.values]
    # build bulk value arg string to avoid overhead of multiple execute statements
    artist_args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s)", x).decode("utf-8") for x in artist_data)
    # bulk insert artists
    cur.execute(artist_table_insert % artist_args_str)


def process_log_file(cur, filepath):
    # ===============1.) Load json filedata int logs arr =====================
    #
    # ========================================================================

    # store json data in logs arr
    logs = multi_json_obj(filepath)

    # ===============2.) CREATE time_df DATAFRAME AND INSERT to time TABLE =====================
    #
    # =========================================================================================
    time_df = pd.DataFrame(logs)
    # filter by NextSong action
    time_df.loc[time_df['page'] == 'NextSong']
    # use imported transform_time(time_df) function
    time_df = transform_time(time_df)
    # build bulk value time_arg string to avoid overhead of multiple execute statements
    time_args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x).decode("utf-8") for x in time_df)

    cur.execute(time_table_insert % time_args_str)

    # ===============2.) CREATE user_df DATAFRAME AND INSERT to users TABLE =====================
    #
    # =========================================================================================
    # load user table
    user_df = pd.DataFrame(logs)
    # filter out people who are logged out and drop duplicates on UserId (even though taken care of with ON CONFLICT in SQL)
    user_df = user_df.loc[user_df['auth'] != 'Logged Out'].drop_duplicates('userId')
    # recreate filtered dataframe with approp. columns for insertion
    user_df = pd.DataFrame(user_df, columns=['userId', 'firstName', 'lastName', 'gender', 'level'])
    # covert users to list of tuples to build bulk value arg strings
    user_df = [tuple(x) for x in user_df.values]
    # build bulk value user_args string to avoid overhead of multiple execute statements
    user_args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s)", x).decode("utf-8") for x in user_df)
    # bulk insert users
    cur.execute(user_table_insert % user_args_str)

    # ========================3.) CREAT songplays_df and INSERT to songplays TABLE ===========================================
    #
    # =================================================================================================

    # create songplays dataframe
    songplays_df = pd.DataFrame(logs)
    # filter out by NextSong Action
    songplays_df = songplays_df.loc[songplays_df['page'] == 'NextSong']
    # creates storage for
    songplay_data = []
    for index, row in songplays_df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = 'NA', 'NA'

        # append combined data to songplay_data
        songplay_data.append([row.ts, row.userId, artistid, songid, row.level, row.sessionId, \
                              row.location, row.userAgent])
    # columns for insertion
    values = ['ts', 'userId', 'artistId', 'songId', 'level', 'sessionId', 'location', 'userAgent']
    # create songplay_data df for insertion
    songplay_data = pd.DataFrame(songplay_data, columns=values)
    # convert song_data to list of tuples to build bulk value arg strings
    data = [tuple(x) for x in songplay_data.values]
    # build bulk value songdata_args string to avoid overhead of multiple execute statements
    songdata_args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s)", x).decode("utf-8") for x in data)
    cur.execute(songplay_table_insert % songdata_args_str)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process

    func(cur, all_files)  # json loader
    conn.commit()
    print('{} files processed.'.format(num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    # get num rows in each table
    cur.execute("SELECT COUNT(*) from songplays")
    plays = cur.fetchone()
    cur.execute("SELECT COUNT(*) from users")
    users = cur.fetchone()
    cur.execute("SELECT COUNT(*) from songs")
    songs = cur.fetchone()
    cur.execute("SELECT COUNT(*) from artists")
    artists = cur.fetchone()
    cur.execute("SELECT COUNT(*) from time")
    time = cur.fetchone()

    print("# rows in songplays: ", plays)
    print("# rows in users: ", users)
    print("# rows in songs: ", songs)
    print("# rows in artists:", artists)
    print("# rows in time: ", time)
    conn.close()


if __name__ == "__main__":
    main()