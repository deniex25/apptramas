import pyodbc


# Parámetros de conexión (reemplaza con tus datos)
server = 'DATASERVER'
database = 'BDHIS_MINSA'
username = 'consultdb'
password = 'utes06$2025'
driver = '{SQL Server}'

# Cadena de conexión
conn_string = f"DRIVER={driver};SERVER={server};DATABASE={
    database};UID={username};PWD={password}"


def get_connection():
    try:
        conn = pyodbc.connect(conn_string)
        return conn

    except pyodbc.Error as ex:
        print.console("Error en la conexión:", ex)
        return None
