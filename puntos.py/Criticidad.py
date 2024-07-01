class Criticidad:
    def __init__(self, id_criticidad, nombre_criticidad):
        self.id_criticidad = id_criticidad
        self.nombre_criticidad = nombre_criticidad

    def get_id_criticidad(self):
        return self.id_criticidad

    def get_nombre_criticidad(self):
        return self.nombre_criticidad

    def set_nombre_criticidad(self, nombre_criticidad):
        self.nombre_criticidad = nombre_criticidad
