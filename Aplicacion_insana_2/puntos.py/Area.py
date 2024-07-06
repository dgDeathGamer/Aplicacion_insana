class Area:
    def __init__(self, id_area, nombre_area):
        self.id_area = id_area
        self.nombre_area = nombre_area

    def get_id_area(self):
        return self.id_area

    def get_nombre_area(self):
        return self.nombre_area

    def set_nombre_area(self, nombre_area):
        self.nombre_area = nombre_area
