class Tipo:
    def __init__(self, id_tipo, nombre_tipo):
        self.id_tipo = id_tipo
        self.nombre_tipo = nombre_tipo

    def get_id_tipo(self):
        return self.id_tipo

    def get_nombre_tipo(self):
        return self.nombre_tipo

    def set_nombre_tipo(self, nombre_tipo):
        self.nombre_tipo = nombre_tipo
