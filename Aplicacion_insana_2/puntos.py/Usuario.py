class Usuario:
    def __init__(self, id_usuario, nombre_usuario, contrasenia, rol_id):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.contrasenia = contrasenia
        self.rol_id = rol_id

    def get_id_usuario(self):
        return self.id_usuario

    def get_nombre_usuario(self):
        return self.nombre_usuario

    def get_contrasenia(self):
        return self.contrasenia

    def get_rol_id(self):
        return self.rol_id
