class Estado:
    def __init__(self, id_estado, nombre_estado):
        self.id_estado = id_estado
        self.nombre_estado = nombre_estado

    def get_id_estado(self):
        return self.id_estado

    def get_nombre_estado(self):
        return self.nombre_estado

    def set_nombre_estado(self, nombre_estado):
        self.nombre_estado = nombre_estado
