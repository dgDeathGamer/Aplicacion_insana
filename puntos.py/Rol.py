class Rol:
    """
    Clase para representar un rol en el sistema.

    Attributes:
        id_rol (int): ID único del rol.
        nombre_rol (str): Nombre del rol.

    Methods:
        __init__(id_rol, nombre_rol):
            Inicializa un objeto de tipo Rol.

        get_id_rol():
            Obtiene el ID del rol.

        get_nombre_rol():
            Obtiene el nombre del rol.

        set_nombre_rol(nombre_rol):
            Actualiza el nombre del rol.
    """

    def __init__(self, id_rol, nombre_rol):
        """
        Inicializa un objeto de tipo Rol.

        Args:
            id_rol (int): ID único del rol.
            nombre_rol (str): Nombre del rol.
        """
        self.id_rol = id_rol
        self.nombre_rol = nombre_rol

    def get_id_rol(self):
        """
        Obtiene el ID del rol.

        Returns:
            int: ID del rol.
        """
        return self.id_rol

    def get_nombre_rol(self):
        """
        Obtiene el nombre del rol.

        Returns:
            str: Nombre del rol.
        """
        return self.nombre_rol

    def set_nombre_rol(self, nombre_rol):
        """
        Actualiza el nombre del rol.

        Args:
            nombre_rol (str): Nuevo nombre del rol.
        """
        self.nombre_rol = nombre_rol
