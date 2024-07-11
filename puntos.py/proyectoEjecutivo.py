import tkinter as tk
from tkinter import ttk
from DAO import DAO
from Tique import Tique
from Cliente import Cliente
from datetime import date
from tkinter import messagebox

class RegistrarTiqueAppEjecutivo:
    """
    Clase para la aplicación de registro de tiques ejecutivo usando Tkinter.

    Métodos:
    - __init__(self, root): Constructor que inicializa la interfaz de usuario.
    - actualizar_id_area(self, *args): Actualiza el ID del área seleccionada.
    - actualizar_id_criticidad(self, *args): Actualiza el ID de la criticidad seleccionada.
    - actualizar_id_tipo_tique(self, *args): Actualiza el ID del tipo de tique seleccionado.
    - registrar_tique(self): Registra un nuevo tique y cliente en la base de datos.
    - obtener_tiques(self): Obtiene todos los tiques de la base de datos y los muestra en un treeview.
    - buscar_tiques_por_rut(self): Busca tiques en la base de datos por el RUT del cliente.
    - mostrar_tique_seleccionado(self, event): Muestra la información del tique seleccionado en los campos.
    - eliminar_tique(self): Elimina el tique seleccionado de la base de datos y actualiza la lista de tiques.
    """
    def __init__(self, root):
        """
        Constructor de la clase RegistrarTiqueAppEjecutivo.

        Parámetros:
        - root (tk.Tk): Ventana principal de Tkinter donde se construye la aplicación.
        """
        self.root = root
        self.root.title("Registrar Tique")

        # Obtener el ancho y alto de la pantalla
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Establecer el tamaño de la ventana de la aplicación como un porcentaje de la resolución de pantalla
        app_width = int(screen_width * 0.8)
        app_height = int(screen_height * 0.8)
        self.root.geometry(f"{app_width}x{app_height}")

        self.dao = DAO()
        self.tiques_encontrados = []  # Variable para almacenar los tiques encontrados por RUT

        # Crear un Frame para contener los campos y botón de registro
        frame = ttk.Frame(root)
        frame.pack(expand=True, fill='both')  # Utilizamos pack para que el Frame se expanda

        # Configurar el peso de las filas y columnas para que se ajusten automáticamente
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(11, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # Crear variables para almacenar la información del tique y los IDs seleccionados
        self.rut_var = tk.StringVar()
        self.nombre_cliente_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.tipo_var = tk.StringVar()
        self.criticidad_var = tk.StringVar()
        self.detalle_servicio_var = tk.StringVar()
        self.detalle_problema_var = tk.StringVar()
        self.area_var = tk.StringVar()
        self.id_area_seleccionada = None
        self.id_criticidad_seleccionada = None
        self.id_tipo_tique_seleccionado = None
        self.rut_cliente_var = tk.StringVar()

        # Crear campos de entrada y menús desplegables
        tk.Label(frame, text="RUT del cliente:").grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.rut_var).grid(row=0, column=1)
        
        tk.Label(frame, text="Nombre del cliente:").grid(row=1, column=0)
        tk.Entry(frame, textvariable=self.nombre_cliente_var).grid(row=1, column=1)

        tk.Label(frame, text="Teléfono:").grid(row=2, column=0)
        tk.Entry(frame, textvariable=self.telefono_var).grid(row=2, column=1)

        tk.Label(frame, text="Correo electrónico:").grid(row=3, column=0)
        tk.Entry(frame, textvariable=self.correo_var).grid(row=3, column=1)

        tk.Label(frame, text="Tipo de tique:").grid(row=4, column=0)
        tipos = ["Selecciona El tipo de Tique",'Felicitación', 'Consulta', 'Reclamo', 'Problema']
        self.tipo_menu = ttk.OptionMenu(frame, self.tipo_var, *tipos)
        self.tipo_menu.grid(row=4, column=1)

        tk.Label(frame, text="Criticidad:").grid(row=5, column=0)
        criticidades = ["Seleciona Criticidad",'Baja', 'Media', 'Alta']
        self.criticidad_menu = ttk.OptionMenu(frame, self.criticidad_var, *criticidades)
        self.criticidad_menu.grid(row=5, column=1)

        tk.Label(frame, text="Detalle del servicio:").grid(row=6, column=0)
        tk.Entry(frame, textvariable=self.detalle_servicio_var).grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        tk.Label(frame, text="Detalle del problema:").grid(row=7, column=0)
        self.detalle_problema_text = tk.Text(frame, height=8, width=50, wrap=tk.WORD, padx=5, pady=5, 
                                            font=("Helvetica", 10))
        self.detalle_problema_text.grid(row=7, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        tk.Label(frame, text="Área para derivar:").grid(row=8, column=0)
        areas = ["Selecciona una Area","Area 1", "Area 2", "Area 3"]
        self.area_menu = ttk.OptionMenu(frame, self.area_var, *areas)
        self.area_menu.grid(row=8, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Agregar trace para actualizar los IDs seleccionados
        self.area_var.trace_add("write", self.actualizar_id_area)
        self.criticidad_var.trace_add("write", self.actualizar_id_criticidad)
        self.tipo_var.trace_add("write", self.actualizar_id_tipo_tique)

        # Botón para registrar el tique
        tk.Button(frame, text="Registrar Tique", command=self.registrar_tique).grid(row=9, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Crear un treeview para mostrar los tiques
        columns = ("ID Tique","Nombre del Cliente","Rut Cliente","Correo Electrónico" ,"Detalle Servicio", "Fecha Creación", "Área", "Tipo", "Criticidad", "Teléfono")
        self.treeview = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.treeview.heading(col, text=col)
        self.treeview.grid(row=11, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Agregar scrollbar horizontal
        scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=self.treeview.xview)
        scrollbar.grid(row=12, column=0, columnspan=4, sticky="ew")
        self.treeview.configure(xscrollcommand=scrollbar.set)

        # Configurar el evento para mostrar el tique seleccionado cuando se haga clic en un elemento del treeview
        self.treeview.bind("<ButtonRelease-1>", self.mostrar_tique_seleccionado)

        # Botón para eliminar tique seleccionado
        tk.Button(frame, text="Eliminar Tique", command=self.eliminar_tique).grid(row=13, column=0, padx=5, pady=5)

        self.obtener_tiques()

    def actualizar_id_area(self, *args):
        """
        Actualiza el ID del área seleccionada en base a la opción seleccionada en el menú desplegable.
        
        Parámetros:
        - *args: Argumentos adicionales para el trace de la variable.
        """
        selected_area = self.area_var.get()
        # Actualizar el ID del área seleccionada
        if selected_area == "Area 1":
            self.id_area_seleccionada = 1
        elif selected_area == "Area 2":
            self.id_area_seleccionada = 2
        elif selected_area == "Area 3":
            self.id_area_seleccionada = 3
        else:
            self.id_area_seleccionada = None  # Opcional: Manejar el caso de "Selecciona una Area"

        print("ID del área seleccionada:", self.id_area_seleccionada)

    def actualizar_id_criticidad(self, *args):
        """
        Actualiza el ID de la criticidad seleccionada en base a la opción seleccionada en el menú desplegable.
        
        Parámetros:
        - *args: Argumentos adicionales para el trace de la variable.
        """
        selected_criticidad = self.criticidad_var.get()
        # Actualizar el ID de la criticidad seleccionada
        if selected_criticidad == "Baja":
            self.id_criticidad_seleccionada = 1
        elif selected_criticidad == "Media":
            self.id_criticidad_seleccionada = 2
        elif selected_criticidad == "Alta":
            self.id_criticidad_seleccionada = 3
        else:
            self.id_criticidad_seleccionada = None  # Opcional: Manejar el caso de "Seleciona Criticidad"

        print("ID de la criticidad seleccionada:", self.id_criticidad_seleccionada)

    def actualizar_id_tipo_tique(self, *args):
        """
        Actualiza el ID del tipo de tique seleccionado en base a la opción seleccionada en el menú desplegable.
        
        Parámetros:
        - *args: Argumentos adicionales para el trace de la variable.
        """
        selected_tipo_tique = self.tipo_var.get()
        # Actualizar el ID del tipo de tique seleccionado
        if selected_tipo_tique == "Felicitación":
            self.id_tipo_tique_seleccionado = 1
        elif selected_tipo_tique == "Consulta":
            self.id_tipo_tique_seleccionado = 2
        elif selected_tipo_tique == "Reclamo":
            self.id_tipo_tique_seleccionado = 3
        elif selected_tipo_tique == "Problema":
            self.id_tipo_tique_seleccionado = 4
        else:
            self.id_tipo_tique_seleccionado = None  # Opcional: Manejar el caso de "Seleciona El tipo de Tique"

        print("ID del tipo de tique seleccionado:", self.id_tipo_tique_seleccionado)

    def registrar_tique(self):
        """
        Registra un nuevo tique y cliente en la base de datos utilizando los valores ingresados por el usuario.
        """
        # Obtener los valores ingresados por el usuario
        rut = self.rut_var.get()
        nombre_cliente = self.nombre_cliente_var.get()
        telefono = self.telefono_var.get()
        correo = self.correo_var.get()
        tipo = self.tipo_var.get()
        criticidad = self.criticidad_var.get()
        detalle_servicio = self.detalle_servicio_var.get()
        detalle_problema = self.detalle_problema_text.get("1.0", tk.END)  # Obtener el contenido del Text
        area = self.area_var.get()

        # Crear un objeto de tipo Tique con la información ingresada
        tique = Tique(
            id_tique=None,
            detalle_servicio=detalle_servicio,
            fecha_creacion=date.today(),  # Utilizamos la fecha actual directamente
            detalle_problema=detalle_problema,
            area_id=self.id_area_seleccionada,
            tipo_id=self.id_tipo_tique_seleccionado,
            criticidad_id=self.id_criticidad_seleccionada,
            cliente_id=None,
            estado_id=1,
        )

        # Crear un objeto de tipo Cliente con la información ingresada
        cliente = Cliente(
            id_cliente=None,
            nombre_cliente=nombre_cliente,
            rut=rut,
            correo_electronico=correo,
            telefono=telefono,
            usuario_id=None,
        )

        # Llamar a la función del DAO para registrar el tique en la base de datos
        self.dao.registrarTique(tique, cliente)

        # Limpiar los campos después de registrar el tique
        self.rut_var.set("")
        self.nombre_cliente_var.set("")
        self.telefono_var.set("")
        self.correo_var.set("")
        self.tipo_var.set("")
        self.criticidad_var.set("")
        self.detalle_servicio_var.set("")
        self.detalle_problema_text.delete("1.0", tk.END)  # Limpiar el contenido del Text
        self.area_var.set("")

        self.obtener_tiques() 

    def obtener_tiques(self):
        """
        Obtiene todos los tiques de la base de datos y los muestra en un treeview.
        """
        # Llamar a la función del DAO para obtener los tiques
        lista_tiques = self.dao.obtenerTiques()

        # Limpiar el treeview antes de mostrar los nuevos datos
        self.treeview.delete(*self.treeview.get_children())

        # Mostrar los datos en el treeview
        for tique in lista_tiques:
            nombre_area = self.dao.obtenerNombreArea(tique.area_id)
            nombre_tipo = self.dao.obtenerNombreTipo(tique.tipo_id)
            nombre_criticidad = self.dao.obtenerNombreCriticidad(tique.criticidad_id)

            # Aquí accedemos a los datos del cliente asociado al tique, si existe
            cliente = tique.cliente
            if cliente:
                nombre_cliente = cliente.nombre_cliente
                telefono_cliente = cliente.telefono
                correo_cliente = cliente.correo_electronico
                rut = cliente.rut
            else:
                # Si no hay cliente asociado, mostrar "N/A" o cualquier otro valor predeterminado
                nombre_cliente = "N/A"
                telefono_cliente = "N/A"
                correo_cliente = "N/A"
                rut = "N/A"
            # Insertar los datos en el treeview
            self.treeview.insert("", "end", values=(tique.id_tique, nombre_cliente, telefono_cliente, correo_cliente, tique.detalle_servicio, tique.fecha_creacion, nombre_area, nombre_tipo, nombre_criticidad, rut))

    def buscar_tiques_por_rut(self):
        """
        Busca tiques en la base de datos por el RUT del cliente ingresado por el usuario.
        """
        # Obtener el RUT ingresado por el usuario
        rut_cliente = self.rut_cliente_var.get()

        # Llamar a la función del DAO para obtener los tiques del cliente con el RUT ingresado
        self.tiques_encontrados = self.dao.obtenerTiquesPorRutCliente(rut_cliente)

    def mostrar_tique_seleccionado(self, event):
        """
        Muestra la información del tique seleccionado en los campos de entrada y menús desplegables.
        
        Parámetros:
        - event (tk.Event): Evento que desencadena la llamada a la función (clic en el treeview).
        """
        # Obtener el índice del tique seleccionado en el treeview
        selected_item = self.treeview.focus()
        if selected_item:
            index = int(selected_item.lstrip("I"))
            tique_seleccionado = self.tiques_encontrados[index]

            # Rellenar los campos con la información del tique seleccionado
            self.rut_var.set(tique_seleccionado.cliente.rut)
            self.nombre_cliente_var.set(tique_seleccionado.cliente.nombre_cliente)
            self.telefono_var.set(tique_seleccionado.cliente.telefono)
            self.correo_var.set(tique_seleccionado.cliente.correo_electronico)
            self.tipo_var.set(self.dao.obtenerNombreTipo(tique_seleccionado.tipo_id))
            self.criticidad_var.set(self.dao.obtenerNombreCriticidad(tique_seleccionado.criticidad_id))
            self.detalle_servicio_var.set(tique_seleccionado.detalle_servicio)
            self.detalle_problema_text.delete("1.0", tk.END)
            self.detalle_problema_text.insert(tk.END, tique_seleccionado.detalle_problema)
            self.area_var.set(self.dao.obtenerNombreArea(tique_seleccionado.area_id))


    def eliminar_tique(self):
        """
        Elimina el tique seleccionado de la base de datos y actualiza la lista de tiques en el treeview.
        """
        #Obtener el índice del tique seleccionado en el treeview
        selected_item = self.treeview.focus()
        info_item = self.treeview.item(selected_item)
        id_tiquet = info_item.get("values")[0]
        print(id_tiquet)
        if selected_item:
            mensaje = messagebox.askyesno(self.root, message="¿Estas seguro que quieres eliminar este tique?")
            if(mensaje == True):
                # Llamar a la función del DAO para eliminar el tique de la base de datos
                self.dao.eliminarTique(id_tiquet)

                # Actualizar la lista de tiques en el treeview
                self.obtener_tiques()

                # Limpiar los campos después de eliminar el tique
                self.rut_var.set("")
                self.nombre_cliente_var.set("")
                self.telefono_var.set("")
                self.correo_var.set("")
                self.tipo_var.set("")
                self.criticidad_var.set("")
                self.detalle_servicio_var.set("")
                self.detalle_problema_text.delete("1.0", tk.END)
                self.area_var.set("")
                messagebox.showinfo(self.root, message = "El tique ha sido eliminado")
            else:
                messagebox.showinfo(self.root, message="Se ha cancelado la acción de eliminar tique")

# Crear una instancia de Tkinter y la aplicación Registrar Tique
if __name__ == '__main__':
    root = tk.Tk()
    app = RegistrarTiqueAppEjecutivo(root)
    root.mainloop()
