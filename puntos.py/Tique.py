class Tique:
    def __init__(self, id_tique, detalle_servicio, fecha_creacion, detalle_problema, area_id, tipo_id, criticidad_id, cliente_id, estado_id):
        self.id_tique = id_tique
        self.detalle_servicio = detalle_servicio
        self.fecha_creacion = fecha_creacion
        self.detalle_problema = detalle_problema
        self.area_id = area_id
        self.tipo_id = tipo_id
        self.criticidad_id = criticidad_id
        self.cliente_id = cliente_id
        self.estado_id = estado_id

    def get_id_tique(self):
        return self.id_tique

    def get_detalle_servicio(self):
        return self.detalle_servicio

    def get_fecha_creacion(self):
        return self.fecha_creacion

    def get_detalle_problema(self):
        return self.detalle_problema

    def get_area_id(self):
        return self.area_id

    def get_tipo_id(self):
        return self.tipo_id

    def get_criticidad_id(self):
        return self.criticidad_id

    def get_cliente_id(self):
        return self.cliente_id

    def get_estado_id(self):
        return self.estado_id

    def set_detalle_servicio(self, detalle_servicio):
        self.detalle_servicio = detalle_servicio

    def set_fecha_creacion(self, fecha_creacion):
        self.fecha_creacion = fecha_creacion

    def set_detalle_problema(self, detalle_problema):
        self.detalle_problema = detalle_problema

    def set_area_id(self, area_id):
        self.area_id = area_id

    def set_tipo_id(self, tipo_id):
        self.tipo_id = tipo_id

    def set_criticidad_id(self, criticidad_id):
        self.criticidad_id = criticidad_id

    def set_cliente_id(self, cliente_id):
        self.cliente_id = cliente_id

    def set_estado_id(self, estado_id):
        self.estado_id = estado_id

