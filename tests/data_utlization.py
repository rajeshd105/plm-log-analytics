from skf.util._data import connect_sql,read_data

conn = connect_sql()

result= read_data(conn)

print(result)


