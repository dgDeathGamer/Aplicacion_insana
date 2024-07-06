class Rol:
    def __init__(self, id_rol, nombre_rol):
        self.id_rol = id_rol
        self.nombre_rol = nombre_rol

    def get_id_rol(self):
        return self.id_rol

    def get_nombre_rol(self):
        return self.nombre_rol

    def set_nombre_rol(self, nombre_rol):
        self.nombre_rol = nombre_rol
