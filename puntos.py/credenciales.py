def get_credenciales():
    """
    Retorna un diccionario con las credenciales de conexión a la base de datos.

    Returns:
        dict: Diccionario con las siguientes credenciales:
            - 'host' (str): Dirección del host de la base de datos (sql10.freesqldatabase.com en este caso).
            - 'user' (str): Usuario de la base de datos (sql10718780 en este caso).
            - 'password' (str): Contraseña de acceso a la base de datos (yrxnDNiUiR en este caso).
            - 'database' (str): Nombre de la base de datos a la que se desea conectar (sql10718780 en este caso).
    """
    credenciales = {
        'host': 'sql10.freesqldatabase.com',
        'user': 'sql10718780',
        'password': 'yrxnDNiUiR',
        'database': 'sql10718780',
    }
    return credenciales
