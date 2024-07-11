"""
Sistema de Gestión de Tiques

Este script implementa un sistema de gestión de tiques utilizando Tkinter para la interfaz gráfica.
Permite registrar usuarios, iniciar sesión y según el rol del usuario, inicia diferentes aplicaciones.

Módulos necesarios:
- tkinter (tk, ttk, messagebox): Para la creación de la interfaz gráfica.
- DAO: Contiene la lógica de acceso a la base de datos.
- Usuario: Define la estructura del usuario.
- os: Utilizado para operaciones de sistema (no usado explícitamente en este script).
- proyecto, proyectoEjecutivo, proyectoJefedeMesa: Importa las aplicaciones específicas según el rol del usuario.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from DAO import DAO
from Usuario import Usuario
import os
from proyecto import RegistrarTiqueApp
from proyectoEjecutivo import RegistrarTiqueAppEjecutivo
from proyectoJefedeMesa import RegistrarTiqueAppJefeDeMesa

dao = DAO()
ventana = tk.Tk()
ventana.title("Sistema de Tiques")
ventana.geometry("800x600")

# Definir variables globales para entry_nombre y entry_password
entry_nombre = None
entry_password = None

def mostrar_opciones():
    """
    Muestra las opciones disponibles al iniciar la aplicación:
    - Registrar un nuevo usuario.
    - Iniciar sesión.
    """
    # Definir y colocar los widgets necesarios
    label_opciones = tk.Label(ventana, text="¿Qué quieres hacer?")
    label_opciones.pack(pady=10)

    # Botón para registrar un nuevo usuario
    btn_registrar = tk.Button(ventana, text="Registrar", command=mostrar_formulario_registrar)
    btn_registrar.pack(pady=5)

    # Botón para iniciar sesión
    btn_iniciar_sesion = tk.Button(ventana, text="Iniciar Sesión", command=mostrar_formulario_iniciar_sesion)
    btn_iniciar_sesion.pack(pady=5)

def mostrar_formulario_registrar():
    """
    Muestra el formulario para registrar un nuevo usuario.
    """
    global entry_nombre, entry_password
    limpiar_ventana()

    # Definir y colocar los widgets necesarios para registrar un nuevo usuario
    label_nombre = tk.Label(ventana, text="Nombre:")
    label_nombre.pack(pady=5)

    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack(pady=5)

    label_password = tk.Label(ventana, text="Contraseña:")
    label_password.pack(pady=5)

    entry_password = tk.Entry(ventana, show="*")  # Campo de contraseña oculta
    entry_password.pack(pady=5)

    # Etiqueta y menú desplegable para seleccionar el rol
    label_rol = tk.Label(ventana, text="Rol:")
    label_rol.pack(pady=5)

    opciones_roles = ["Usuario Común", "Jefe de Mesa", "Ejecutivo"]
    rol_seleccionado = tk.StringVar()
    rol_seleccionado.set(opciones_roles[0])  # Establecer el valor predeterminado
    combo_rol = ttk.Combobox(ventana, values=opciones_roles, textvariable=rol_seleccionado)
    combo_rol.pack(pady=5)

    # Botón para registrar un nuevo usuario
    btn_registrar = tk.Button(ventana, text="Registrar", command=lambda: registrar_usuario(entry_nombre.get(), entry_password.get(), combo_rol.get()))
    btn_registrar.pack(pady=10)

    # Botón para volver a las opciones principales
    btn_volver = tk.Button(ventana, text="Volver", command=volver_a_opciones)
    btn_volver.pack(pady=5)
    

def mostrar_formulario_iniciar_sesion():
    """
    Muestra el formulario para iniciar sesión.
    """
    global entry_nombre, entry_password
    limpiar_ventana()

    # Definir y colocar los widgets necesarios para iniciar sesión
    label_nombre = tk.Label(ventana, text="Nombre:")
    label_nombre.pack(pady=5)

    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack(pady=5)

    label_password = tk.Label(ventana, text="Contraseña:")
    label_password.pack(pady=5)

    entry_password = tk.Entry(ventana, show="*")  # Campo de contraseña oculta
    entry_password.pack(pady=5)

    # Botón para iniciar sesión
    btn_iniciar_sesion = tk.Button(ventana, text="Iniciar Sesión", command=lambda: iniciar_sesion(entry_nombre.get(), entry_password.get()))
    btn_iniciar_sesion.pack(pady=10)

    # Botón para volver a las opciones
    btn_volver = tk.Button(ventana, text="Volver", command=volver_a_opciones)
    btn_volver.pack(pady=5)

def limpiar_ventana():
    """
    Limpia todos los widgets en la ventana.
    """
    for widget in ventana.winfo_children():
        widget.pack_forget()

def volver_a_opciones():
    """
    Vuelve a mostrar las opciones iniciales de registrar o iniciar sesión.
    """
    limpiar_ventana()
    mostrar_opciones()

def registrar_usuario(nombre, contrasenia, rol_elegido):
    """
    Registra un nuevo usuario en la base de datos.

    Parámetros:
        nombre (str): Nombre del usuario.
        contrasenia (str): Contraseña del usuario.
        rol_elegido (str): Rol seleccionado por el usuario (Usuario Común, Jefe de Mesa, Ejecutivo).
    """
    # Obtener el ID del rol seleccionado
    if rol_elegido == "Usuario Común":
        rol_id = 1
    elif rol_elegido == "Jefe de Mesa":
        rol_id = 2
    elif rol_elegido == "Ejecutivo":
        rol_id = 3
    else:
        # Si ocurre algún error inesperado, mostrar un mensaje y detener el registro.
        messagebox.showerror("Error", "Rol inválido")
        return

    # Validar que los campos no estén vacíos
    if nombre == "" or contrasenia == "":
        messagebox.showerror("Error", "Nombre y contraseña son requeridos")
        return

    # Crear un nuevo objeto Usuario
    usuario = Usuario(id_usuario=None, nombre_usuario=nombre, contrasenia=contrasenia, rol_id=rol_id)

    # Registrar el usuario en la base de datos
    dao.registrar_usuario(usuario)

    # Mostrar mensaje de éxito
    messagebox.showinfo("Registro exitoso", "El usuario ha sido registrado correctamente")

    # Volver a mostrar las opciones para que el usuario pueda decidir si quiere registrar o iniciar sesión nuevamente
    limpiar_ventana()
    mostrar_opciones()

def iniciar_sesion(nombre, contrasenia):
    """
    Inicia sesión del usuario en el sistema.

    Parámetros:
        nombre (str): Nombre del usuario.
        contrasenia (str): Contraseña del usuario.
    """
    # Validar que los campos no estén vacíos
    if nombre == "" or contrasenia == "":
        messagebox.showerror("Error", "Nombre y contraseña son requeridos")
        return

    # Verificar las credenciales del usuario en la base de datos
    usuario = dao.verificar_credenciales(nombre, contrasenia)
    if usuario:
        # Mostrar mensaje de éxito
        messagebox.showinfo("Inicio de sesión exitoso", "Bienvenido al sistema")

        ventana.destroy()

        # Dependiendo del rol, iniciará la aplicación correspondiente
        if usuario.rol_id == 1:
            root = tk.Tk()
            app = RegistrarTiqueApp(root)  # Esto cargará el proyecto.py
        elif usuario.rol_id == 2:
            root = tk.Tk()
            app = RegistrarTiqueAppJefeDeMesa(root)  # Esto cargará el proyectoEjecutivo.py
        elif usuario.rol_id == 3:
            root = tk.Tk()
            app = RegistrarTiqueAppEjecutivo(root)  # Esto cargará el proyectoJefeDeMes.py
        root.mainloop()
    else:
        messagebox.showerror("Inicio de sesión fallido", "Credenciales incorrectas")

    # Limpiar los campos de entrada
    entry_nombre.delete(0, "end")
    entry_password.delete(0, "end")

# Mostrar las opciones al iniciar la aplicación
mostrar_opciones()

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()
