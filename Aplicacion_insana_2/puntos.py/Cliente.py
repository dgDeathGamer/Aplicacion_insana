class Cliente:
    def __init__(self, id_cliente, nombre_cliente, rut, correo_electronico, telefono, usuario_id):
        self.id_cliente = id_cliente
        self.nombre_cliente = nombre_cliente
        self.rut = rut
        self.correo_electronico = correo_electronico
        self.telefono = telefono
        self.usuario_id = usuario_id

    def get_id_cliente(self):
        return self.id_cliente

    def get_nombre_cliente(self):
        return self.nombre_cliente

    def get_rut(self):
        return self.rut

    def get_correo_electronico(self):
        return self.correo_electronico

    def get_telefono(self):
        return self.telefono

    def get_usuario_id(self):
        return self.usuario_id

    def set_nombre_cliente(self, nombre_cliente):
        self.nombre_cliente = nombre_cliente

    def set_rut(self, rut):
        self.rut = rut

    def set_correo_electronico(self, correo_electronico):
        self.correo_electronico = correo_electronico

    def set_telefono(self, telefono):
        self.telefono = telefono

    def set_usuario_id(self, usuario_id):
        self.usuario_id = usuario_id
