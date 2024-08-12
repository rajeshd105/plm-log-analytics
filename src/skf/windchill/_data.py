import pymssql
import json

f = open('C:/Users/NZ8554/OneDrive - SKF/Documents/Rajesh_D/Development/Python/windchill-analytics/src/skf/windchill/config.json')
config = json.load(f)
f.close

def connect_sql():
    conn = pymssql.connect(config.get('db_host'), config.get('db_user'), config.get('db_password'), config.get('db_name'))
    return conn

def read_data(connection):
    try:
        with connection.cursor(as_dict=True) as cursor:
            sql = "SELECT * from UserMgmt"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    finally:
        connection.close()

def insert_data(connection):
    try:
        with connection.cursor(as_dict=True) as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('john@example.com', 'mypassword'))

        # Commit changes
        connection.commit()

        print("Record inserted successfully")
    finally:
        connection.close()

if __name__=='__main__':
    conn = connect_sql()
    rows = read_data(conn)
    print(rows)