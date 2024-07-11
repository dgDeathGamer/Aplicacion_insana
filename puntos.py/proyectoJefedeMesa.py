"""
Esta clase implementa una aplicación para el registro y gestión de tiques.
Utiliza Tkinter para la interfaz gráfica y se comunica con una base de datos a través de un objeto DAO.
"""
import tkinter as tk
from tkinter import ttk
from DAO import DAO
from Tique import Tique
from Cliente import Cliente
from datetime import date
from Area import Area
from Criticidad import Criticidad
from Estado import Estado
from Tipo import Tipo
from tkinter import messagebox


class RegistrarTiqueAppJefeDeMesa:
    def __init__(self, root):
        """
        Inicializa la aplicación de registro de tique.

        Args:
            root (tk.Tk): La raíz de la aplicación Tkinter.
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
        areas = self.dao.obtenerAreas()  
        self.tiques_encontrados = []  # Variable para almacenar los tiques encontrados por RUT
        self.id_area_seleccionada = None  # Agregar esta línea para inicializar el atributo

        # Crear un Frame para contener los campos y botón de registro
        frame = ttk.Frame(root)
        frame.pack(expand=True, fill='both')  # Utilizamos pack para que el Frame se expanda

        # Configurar el peso de las filas y columnas para que se ajusten automáticamente
        for i in range(12):
            frame.rowconfigure(i, weight=1)
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
        # Atributo para almacenar el nombre del área a crear
        self.nuevo_nombre_area = tk.StringVar()
        # Atributo para almacenar el nombre del tipo tique a crear
        self.nuevo_nombre_tipo_tique = tk.StringVar()
        # Atributo para almacenar el nombre de la criticidad a crear
        self.nuevo_nombre_criticidad = tk.StringVar()

        # Crear campos de entrada y menús desplegables
        tk.Label(frame, text="RUT del cliente:").grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.rut_var).grid(row=0, column=1)

        tk.Label(frame, text="Nombre del cliente:").grid(row=1, column=0)
        tk.Entry(frame, textvariable=self.nombre_cliente_var).grid(row=1, column=1)

        tk.Label(frame, text="Teléfono:").grid(row=2, column=0)
        tk.Entry(frame, textvariable=self.telefono_var).grid(row=2, column=1)

        tk.Label(frame, text="Correo electrónico:").grid(row=3, column=0)
        tk.Entry(frame, textvariable=self.correo_var).grid(row=3, column=1)

        #Crear el menu desplegable de Tipos de tique con la opcion por defecto
        tk.Label(frame, text="Tipo de tique:").grid(row=4, column=0)
        # Obtener la lista de tipos de tique utilizando el metodo ObtenerTipos() del DAO
        dao = DAO()
        tipos = dao.obtenerTipos()
        
        # Crear una lista que contenga los nombres de los tipos para utilizar en el menú desplegable
        nombres_tipos = ["Selecciona un Tipo de tique"] + [tipo.nombre_tipo for tipo in tipos]
        
        # Usar la lista de nombres de Tipos de tique para el menu desplegable
        self.tipo_menu = ttk.OptionMenu(frame, self.tipo_var, *nombres_tipos)
        self.tipo_menu.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        
        #Crear el menú desplegable de criticidades con la opcion por defecto
        tk.Label(frame, text="Criticidades:").grid(row=5, column=0)
        #Obtener la lista de criticidades utilizando el método obtenerCriticidades() del DAO
        dao = DAO()
        criticidades = dao.obtenerCriticidades()
        
        # Crear una lista que contenga los nombres de las criticidades para utilizar en el menú desplegable
        nombres_criticidades = ["Selecciona una Criticidad"] + [criticidad.nombre_criticidad for criticidad in criticidades]
        
        #Usar la lista de nombres de criticidades para el menú desplegable
        self.criticidad_menu = ttk.OptionMenu(frame, self.criticidad_var, *nombres_criticidades)
        self.criticidad_menu.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame, text="Detalle del servicio:").grid(row=6, column=0)
        tk.Entry(frame, textvariable=self.detalle_servicio_var).grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        tk.Label(frame, text="Detalle del problema:").grid(row=7, column=0)
        self.detalle_problema_text = tk.Text(frame, height=8, width=50, wrap=tk.WORD, padx=5, pady=5, 
                                            font=("Helvetica", 10))
        self.detalle_problema_text.grid(row=7, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Crear el menú desplegable de áreas con la opción por defecto
        tk.Label(frame, text="Área para derivar:").grid(row=8, column=0)
        # Obtener la lista de áreas utilizando el método obtenerAreas() del DAO
        dao = DAO()
        areas = dao.obtenerAreas()

        # Crear una lista que contenga los nombres de las áreas para utilizar en el menú desplegable
        nombres_areas = ["Selecciona un Área"] + [area.nombre_area for area in areas]
        
        # Usar la lista de nombres de áreas para el menú desplegable
        self.area_menu = ttk.OptionMenu(frame, self.area_var, *nombres_areas)
        self.area_menu.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

        # Agregar trace para actualizar los IDs seleccionados
        self.area_var.trace_add("write", self.actualizar_id_area)
        self.criticidad_var.trace_add("write", self.actualizar_id_criticidad)
        self.tipo_var.trace_add("write", self.actualizar_id_tipo)

        # Botón para registrar el tique
        tk.Button(frame, text="Registrar Tique", command=self.registrar_tique).grid(row=9, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Crear un treeview para mostrar los tiques-----------------------------------------------------------------------------------------------------------------------------
        columns = ("ID Tique","Nombre del Cliente","Rut Cliente","Correo Electrónico" ,"Detalle Servicio", "Fecha Creación", "Área", "Tipo", "Criticidad", "Teléfono")
        self.treeview = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.treeview.heading(col, text=col)
        self.treeview.grid(row=11, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Agregar scrollbar horizontal
        scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=self.treeview.xview)
        scrollbar.grid(row=12, column=0, columnspan=4, sticky="ew")
        self.treeview.configure(xscrollcommand=scrollbar.set)

        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Agregar un botón para crear un área
        tk.Button(frame, text="Crear Área", command=self.mostrar_dialogo_crear_area).grid(row=10, column=2, padx=5, pady=5, sticky="ew")
        
        # Agregar un botón para crear un tipo de tique
        tk.Button(frame, text="Crear Tipo de Tique", command=self.mostrar_dialogo_crear_tipo_tique).grid(row=8, column=2, padx=5, pady=5, sticky="ew")

    
        # Agregar un botón para crear una criticidad
        tk.Button(frame, text="Crear Criticidad", command=self.mostrar_dialogo_crear_criticidad).grid(row=9, column=2, padx=5, pady=5, sticky="ew")

        # Configurar el evento para mostrar el tique seleccionado cuando se haga clic en un elemento del treeview
        self.treeview.bind("<ButtonRelease-1>", self.mostrar_tique_seleccionado)



        # Configurar el evento para mostrar el tique seleccionado cuando se haga clic en un elemento del treeview
        self.treeview.bind("<ButtonRelease-1>", self.mostrar_tique_seleccionado)


        # Botón para eliminar tique seleccionado
        tk.Button(frame, text="Eliminar Tique", command=self.eliminar_tique).grid(row=13, column=0, padx=5, pady=5)

        self.obtener_tiques()

    def actualizar_id_area(self, *args):
        """
        Actualiza el ID del área seleccionada según la opción elegida en el menú desplegable.

        Args:
            *args: Argumentos adicionales.
        """
        selected_area = self.area_var.get()

        # Si el área seleccionada no es la opción predeterminada, buscamos el objeto Area correspondiente en la lista de áreas
        if selected_area != "Selecciona un Área":
            dao = DAO()
            areas = dao.obtenerAreas()

            # Buscamos el objeto Area que corresponde al nombre seleccionado
            for area in areas:
                if selected_area == area.nombre_area:
                    # Cuando encontramos el objeto Area con el nombre seleccionado, establecemos su ID en self.area_id
                    self.id_area_seleccionada = area.id_area
                    break
        else:
            # Si se selecciona la opción predeterminada, establecemos el ID del área como None
            self.id_area_seleccionada = None

        print("ID de Área seleccionada:", self.id_area_seleccionada)

    def actualizar_id_criticidad(self, *args):
        """
        Actualiza el ID de la criticidad seleccionada según la opción elegida en el menú desplegable.

        Args:
            *args: Argumentos adicionales.
        """
        selected_criticidad = self.criticidad_var.get()
    
        # Si la criticidad seleccionada no es la opcion predeterminada, buscamos el objeto criticidad correspondiente en la lista de criticidades
        if selected_criticidad != "Selecciona una criticidad":
            dao = DAO()
            criticidades = dao.obtenerCriticidades()
            
            #Buscamos el objeto Criticidad que corresponde al nombre seleccionado
            for criticidad in criticidades:
                if selected_criticidad ==criticidad.nombre_criticidad:
                    #Cuando encontramos el objeto Criticidad con el nombre seleccionado, establecemos su ID en self.criticidad_id
                    self.id_criticidad_seleccionada = criticidad.id_criticidad
                    break
        else:
            #Si se selecciona la opción predeterminada, establecemos el id de la criticidad como None
            self.id_criticidad_seleccionada = None
            
        print("ID de Criticidad seleccionada:", self.id_criticidad_seleccionada)

    def actualizar_id_tipo(self, *args):
        """
        Actualiza el ID del tipo de tique seleccionado según la opción elegida en el menú desplegable.

        Args:
            *args: Argumentos adicionales.
        """
        selected_tipo = self.tipo_var.get()
        
        # Si el tipo seleccionada no es la opción predeterminada, buscamos el objeto Tipo correspondiente en la lista de tipos
        if selected_tipo != "Selecciona un Tipo de Tique":
            dao = DAO()
            tipos = dao.obtenerTipos()
            
            #Buscamos el objeto Tipo que corresponde al nombre seleccionado
            for tipo in tipos:
                if selected_tipo == tipo.nombre_tipo:
                    # Cuando encontramos el objeto Tipo con el nombre seleccionado, establecemos su ID en self.tipo_id
                    self.id_tipo_tique_seleccionado = tipo.id_tipo
                    break
        else:
            #Si se selecciona la opción predeterminada, establecemos el ID del tipo como None
            self.id_tipo_tique_seleccionado = None
            
        print("ID de Tipo de Tique Seleccionada:", self.id_tipo_tique_seleccionado)

    def registrar_tique(self):
        """
        Registra un nuevo tique utilizando la información ingresada por el usuario.

        Se utiliza la instancia del DAO para registrar el tique en la base de datos.

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
        fecha_creacion=date.today(),
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
        Obtiene todos los tiques de la base de datos y los muestra en el treeview.

        Utiliza la instancia del DAO para obtener los tiques y luego los muestra en el treeview de la interfaz gráfica.
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
        Busca tiques en la base de datos por el RUT del cliente ingresado.

        Utiliza la instancia del DAO para buscar tiques asociados a un cliente específico según su RUT.
        """
        # Obtener el RUT ingresado por el usuario
        rut_cliente = self.rut_cliente_var.get()

        # Llamar a la función del DAO para obtener los tiques del cliente con el RUT ingresado
        self.tiques_encontrados = self.dao.obtenerTiquesPorRutCliente(rut_cliente)

        # Obtener todas las áreas desde la base de datos
        dao = DAO()
        areas = dao.obtenerAreas()
        # Actualizar las opciones del menú desplegable de áreas con las áreas obtenidas
        menu = self.area_menu['menu']
        menu.delete(1, tk.END)  # Borrar todas las opciones existentes, excepto "Selecciona una Area"
        for area in areas:
            menu.add_command(label=area[1], command=lambda a=area[1]: self.area_var.set(a))

    def mostrar_tique_seleccionado(self, event):
        """
        Muestra la información del tique seleccionado en el treeview en los campos de entrada correspondientes.

        Args:
            event (tk.Event): El evento que activa la función (clic en el treeview).
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
    
    
    
    
    def actualizar_menu_tipos_tique(self):
        """
        Actualiza el menú desplegable de tipos de tique con los tipos de tique disponibles en la base de datos.

        Utiliza la instancia del DAO para obtener los tipos de tique y actualizar el menú desplegable.
        """
        # Obtener todos los tipos de tique desde el DAO
        dao = DAO()
        tipos_tique = dao.obtenerTipos()

        # Limpiar el menú desplegable de tipos de tique
        self.tipo_menu['menu'].delete(0, tk.END)

        # Agregar la opción "Selecciona el tipo de Tique" al menú desplegable
        self.tipo_menu['menu'].add_command(label="Selecciona El tipo de Tique", command=lambda tipo="Selecciona El tipo de Tique": self.tipo_var.set(tipo))

        # Agregar los tipos de tique obtenidos desde la base de datos al menú desplegable
        for tipo in tipos_tique:
            self.tipo_menu['menu'].add_command(label=tipo.nombre_tipo, command=lambda tipo=tipo.nombre_tipo: self.tipo_var.set(tipo))


    def actualizar_menu_criticidades(self):
        """
        Actualiza el menú desplegable de criticidades con las criticidades disponibles en la base de datos.

        Utiliza la instancia del DAO para obtener las criticidades y actualizar el menú desplegable.
        """
        # Obtener todas las criticidades desde el DAO
        dao = DAO()
        criticidades = dao.obtenerCriticidades()

        # Limpiar el menú desplegable de criticidades
        self.criticidad_menu['menu'].delete(0, tk.END)

        # Agregar la opción "Selecciona Criticidad" al menú desplegable
        self.criticidad_menu['menu'].add_command(label="Selecciona Criticidad", command=lambda criticidad="Selecciona Criticidad": self.criticidad_var.set(criticidad))

        # Agregar las criticidades obtenidas desde la base de datos al menú desplegable
        for criticidad in criticidades:
            self.criticidad_menu['menu'].add_command(label=criticidad.nombre_criticidad, command=lambda criticidad=criticidad.nombre_criticidad: self.criticidad_var.set(criticidad))

            
            
    def actualizar_menu_areas(self):
        """
        Actualiza el menú desplegable de áreas con las áreas disponibles en la base de datos.

        Utiliza la instancia del DAO para obtener las áreas y actualizar el menú desplegable.
        """
        # Obtener todas las áreas desde la base de datos
        dao = DAO()
        areas = dao.obtenerAreas()

        # Limpiar el menú desplegable de áreas
        self.area_menu['menu'].delete(0, tk.END)

        # Agregar la opción "Selecciona un Área" al menú desplegable
        self.area_menu['menu'].add_command(label="Selecciona un Área", command=lambda area="Selecciona un Área": self.area_var.set(area))

        # Agregar las áreas obtenidas desde la base de datos al menú desplegable
        for area in areas:
            self.area_menu['menu'].add_command(label=area.nombre_area, command=lambda area=area.nombre_area: self.area_var.set(area))
        
    #-------------------------------------------------------------------------------------------------------  
        
    def crear_area(self):
        """
        Crea un nuevo área en la base de datos utilizando el nombre ingresado por el usuario.

        Utiliza la instancia del DAO para crear el área en la base de datos.
        """
        # Obtener el nombre del área ingresado por el usuario
        nombre_area = self.nuevo_nombre_area.get()

        # Verificar si se ingresó un nombre de área válido
        if not nombre_area:
            print("Ingrese un nombre de área válido.")
            return

        # Llamar a la función del DAO para crear el área en la base de datos
        dao = DAO()
        nueva_area = dao.crearArea(nombre_area)

        if nueva_area:
            print(f"Área '{nombre_area}' creada con ID: {nueva_area.id_area}")
            # Limpiar el campo de nombre del área para futuras creaciones
            self.nuevo_nombre_area.set("")
            # Actualizar las opciones del menú desplegable de áreas con las áreas recién creadas
            self.actualizar_menu_areas()



    def mostrar_dialogo_crear_area(self):
        """
        Muestra un diálogo para que el usuario ingrese el nombre del área a crear.

        Llama al método `crear_area` para procesar la creación del área con el nombre ingresado por el usuario.
        """
        # Crear un diálogo para ingresar el nombre del área
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Crear Área")

        tk.Label(dialogo, text="Nombre del Área:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(dialogo, textvariable=self.nuevo_nombre_area).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(dialogo, text="Aceptar", command=self.crear_area).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        
        
    def crear_tipo_tique(self):
        """
        Crea un nuevo tipo de tique en la base de datos utilizando el nombre ingresado por el usuario.

        Utiliza la instancia del DAO para crear el tipo de tique en la base de datos.
        """
        # Obtener el nombre del tipo de tique ingresado por el usuario
        nombre_tipo_tique = self.nuevo_nombre_tipo_tique.get()

        # Verificar si se ingresó un nombre de tipo de tique válido
        if not nombre_tipo_tique:
            print("Ingrese un nombre de tipo de tique válido.")
            return

        # Llamar a la función del DAO para crear el tipo de tique en la base de datos
        dao = DAO()
        nuevo_tipo_tique = dao.crearTipoTique(nombre_tipo_tique)

        if nuevo_tipo_tique:
            print(f"Tipo de tique '{nombre_tipo_tique}' creado con ID: {nuevo_tipo_tique.id_tipo}")
            # Limpiar el campo de nombre del tipo de tique para futuras creaciones
            self.nuevo_nombre_tipo_tique.set("")
            # Actualizar las opciones del menú desplegable de tipos de tique con los tipos recién creados
            self.actualizar_menu_tipos_tique()
         
            
    def mostrar_dialogo_crear_tipo_tique(self):
        """
        Muestra un diálogo para que el usuario ingrese el nombre del tipo de tique a crear.

        Llama al método `crear_tipo_tique` para procesar la creación del tipo de tique con el nombre ingresado por el usuario.
        """
        # Crear un diálogo para ingresar el nombre del tipo de tique
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Crear Tipo de Tique")

        tk.Label(dialogo, text="Nuevo Tipo de Tique:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(dialogo, textvariable=self.nuevo_nombre_tipo_tique).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(dialogo, text="Aceptar", command=self.crear_tipo_tique).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    
        
        
        
    def crear_criticidad(self):
        """
        Crea una nueva criticidad en la base de datos utilizando el nombre ingresado por el usuario.

        Utiliza la instancia del DAO para crear la criticidad en la base de datos.
        """
        # Obtener el nombre de la criticidad ingresado por el usuario
        nombre_criticidad = self.nuevo_nombre_criticidad.get()

        # Verificar si se ingresó un nombre de criticidad válido
        if not nombre_criticidad:
            print("Ingrese un nombre de criticidad válido.")
            return

        # Llamar a la función del DAO para crear la criticidad en la base de datos
        dao = DAO()
        nueva_criticidad = dao.crearCriticidad(nombre_criticidad)

        if nueva_criticidad:
            print(f"Criticidad '{nombre_criticidad}' creada con ID: {nueva_criticidad.id_criticidad}")
            # Limpiar el campo de nombre de la criticidad para futuras creaciones
            self.nuevo_nombre_criticidad.set("")
            # Actualizar las opciones del menú desplegable de criticidades con las criticidades recién creadas
            self.actualizar_menu_criticidades()
            
            
            
    def mostrar_dialogo_crear_criticidad(self):
        """
        Muestra un diálogo para que el usuario ingrese el nombre de la criticidad a crear.

        Llama al método `crear_criticidad` para procesar la creación de la criticidad con el nombre ingresado por el usuario.
        """
        # Crear un diálogo para ingresar el nombre de la criticidad
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Crear Criticidad")

        tk.Label(dialogo, text="Nueva Criticidad:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(dialogo, textvariable=self.nuevo_nombre_criticidad).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(dialogo, text="Aceptar", command=self.crear_criticidad).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    

    def eliminar_tique(self):
        """
        Elimina el tique seleccionado de la base de datos.

        Utiliza la instancia del DAO para eliminar el tique seleccionado de la base de datos.
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
    app = RegistrarTiqueAppJefeDeMesa(root)
    root.mainloop()