
import sqlite3
from sqlite3 import Error
import json

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

#https://www.vultr.com/docs/how-to-install-the-latest-version-of-sqlite3/
#Installed at
    #/usr/local/lib

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def create_table(conn):
    """
    Create a new task
    :param conn:
    :
    """

    sql = ''' CREATE TABLE IF NOT EXISTS DATABASE
            ([data] JSON)
            '''
    cur = conn.cursor()      
    cur.execute(sql) 
    conn.commit()
    return   

def create_data(conn):
    """
    Create a new task
    :param conn:
    :
    """
    ip15 = '''{
                "IP15": [
                {
                "Gas_reading": 0,
                "iso": "2022-08-19T14:40:55.069Z",
                "location": "Garage",
                "timestamp": 1660920055
                }
                ]
                }'''

    sql2 = '''
          INSERT INTO DATABASE (DATA)

                VALUES
                ({
                "IP22": [
                {
                "Electricity_reading": 2.787,
                "iso": "2022-08-19T14:41:31.765Z",
                "location": "Garage",
                "timestamp": 1660920092
                }
                ]
                })
          '''     
    #json.loads take a string as input and returns a dictionary as output.
    #json.dumps take a dictionary as input and returns a string as output.

    x = json.dumps(ip15)
    y = json.loads(ip15)
    print(x)
    print(y)

    #cur = conn.cursor()      
    #cur.execute("INSERT INTO DATABASE (DATA) VALUES (?)", x) 
    #cur.execute(sql2) 
    #conn.commit()
    return 
          

def main():
    print(sqlite3.__file__)
    print(sqlite3.sqlite_version)

    #database = r"D:\DATA\DATABASE.db"
    database = r"/mnt/d/apps/influxdb/DATABASE.db"
    # create a database connection
    #conn = create_connection(database)
    #with conn:
        # create a new project
        #project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        #project_id = create_project(conn, project)

        # tasks
        #task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        #task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

        # create tasks
        #create_task(conn, task_1)
        #create_task(conn, task_2)
        #create_table(conn)
        #create_data(conn)
    return


if __name__ == '__main__':
    main()
