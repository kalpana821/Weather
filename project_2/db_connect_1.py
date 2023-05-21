def create_db(cursor,dataBaseName):
    db=f"create database {dataBaseName}"
    cursor.execute(db)

def create_table(cursor, tb_name):
    tb=f"CREATE TABLE IF NOT EXISTS {tb_name} (current_temperature float, Celsius float, current_pressure float, current_humidity float, date_time varchar(100), weather_description varchar(100));"
    cursor.execute(tb)

def insert_table(cursor,tb_name,lst):
    insert_query = f"INSERT INTO {tb_name}(current_temperature, Celsius, current_pressure, current_humidity, date_time, weather_description) VALUES (%(current_temperature)s, %(Celsius)s, %(current_pressure)s, %(current_humidity)s, %(date_time)s, %(weather_description)s);"
    cursor.executemany(insert_query,lst)