import pymssql
import logging

logger = logging.getLogger(__name__)

def connect_sql(host,user,password,database):
    try:
        conn = pymssql.connect(host, user, password, database)
        logger.debug("The connection to database is successfully established...")
        return conn
    except Exception as e:
        logger.error("The connection to database is failed to establish, please check the connection details!!!")
    return None

def read_data(connection, query):
    try:
        with connection.cursor(as_dict=True) as cursor:
            # query = "SELECT * from UserMgmt"
            cursor.execute(query)
            logger.debug("SELECT Query executed successfully...")
            rows = cursor.fetchall()
            return rows
    except Exception:
        logger.error("Failed to retrieve information from Database.")

def update_data(connection, query):
    try:
        with connection.cursor(as_dict=True) as cursor:
            # Create a new record
            # query = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            # cursor.execute(query, ('john@example.com', 'mypassword'))
            cursor.execute(query)
            logger.debug("Insert/Update/Delete Query executed successfully...")

        # Commit changes
        connection.commit()

    except Exception as err:
        logger.error("Error occurred while inserting data to Database." + err)

def update_data_multirow(connection, query1, query2):
    try:
        with connection.cursor(as_dict=True) as cursor:
            # Create a new record
            # query = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            # cursor.execute(query, ('john@example.com', 'mypassword'))
            cursor.executemany(query1, query2)
            logger.debug("Multi Row Insert Query executed successfully...")

        # Commit changes
        connection.commit()
        logger.debug(str(cursor.rowcount) + " rows inserted successfully..")
    except Exception as err:
        logger.error("Error occurred while inserting Multirow data to Database." + err)

def disconnect_sql(connection):
    try:
        connection.close()
    except Exception:
        logger.error("Failed to close the connection")

# if __name__=='__main__':
#     conn = connect_sql()
#     rows = read_data(conn)
#     print(rows)