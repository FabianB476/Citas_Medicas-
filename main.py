import customtkinter as ctk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from registro import mostrar_interfaz_registro
from database import create_tables, obtener_paciente_por_correo, obtener_medico_por_correo
from paciente import mostrar_interfaz_usuario
from medico import mostrar_interfaz_medico

# Crear las tablas (se ejecuta solo una vez)
create_tables()

# Variable global para controlar la visibilidad de la contraseña
password_visible = False

def toggle_password_visibility():
    """Función para alternar la visibilidad de la contraseña."""
    global password_visible
    if password_visible:
        entry_contrasena.configure(show="*")
        btn_toggle_password.configure(image=eye_icon)
        password_visible = False
    else:
        entry_contrasena.configure(show="")
        btn_toggle_password.configure(image=eye_off_icon)
        password_visible = True

def iniciar_sesion():
    correo = entry_correo.get().strip()
    contrasena = entry_contrasena.get().strip()
    if not correo or not contrasena:
        messagebox.showwarning("Advertencia", "Debe ingresar correo y contraseña")
        return
    paciente = obtener_paciente_por_correo(correo)
    medico = obtener_medico_por_correo(correo)
    if paciente and paciente[5] == contrasena:
        root.withdraw()
        mostrar_interfaz_usuario(root, {"id": paciente[0], "nombres": paciente[3], "apellidos": paciente[4]})
    elif medico and medico[5] == contrasena:
        root.withdraw()
        mostrar_interfaz_medico(root, {"id": medico[0], "nombres": medico[3], "apellidos": medico[4], "especialidad": medico[6]})
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

def abrir_interfaz_registro():
    root.withdraw()
    mostrar_interfaz_registro(root)

def abrir_interfaz_recuperar():
    root.withdraw()
    from recuperar import mostrar_interfaz_recuperar
    mostrar_interfaz_recuperar(root)

# Configuración global de CustomTkinter
ctk.set_appearance_mode("light")         # Modo claro (también puedes usar "dark")
ctk.set_default_color_theme("blue")        # Puedes elegir "blue", "dark-blue" o "green"

# Crear la ventana principal
root = ctk.CTk()
root.title("Sistema de Gestión de Citas MEDICAS  CYBERMAS")
root.geometry("600x500")
root.resizable(False, False)
try:
    root.iconbitmap("bank_icon.ico")
except Exception as e:
    print("Icono no encontrado:", e)

# Crear un frame principal con bordes redondeados y fondo suave
frame = ctk.CTkFrame(master=root, corner_radius=20, fg_color="#F7F7F7")
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Mostrar logotipo (si existe)
try:
    logo_image = ctk.CTkImage(light_image="logo.png", size=(100, 100))
    lbl_logo = ctk.CTkLabel(master=frame, image=logo_image, text="")
    lbl_logo.pack(pady=10)
except Exception as e:
    print("Logo no encontrado:", e)

# Título de bienvenida
lbl_titulo = ctk.CTkLabel(master=frame, text="Bienvenido al Sistema de Citas Iess- CAYAMBE ", font=("Segoe UI", 20, "bold"))
lbl_titulo.pack(pady=10)

# Campo para ingresar el correo
entry_correo = ctk.CTkEntry(master=frame, placeholder_text="Correo Electrónico", width=300, height=40,
                             border_width=2, corner_radius=10)
entry_correo.pack(pady=5)

# --- Creación del campo de contraseña con botón de toggle ---
# Contenedor para el campo de contraseña y el botón "ojo"
password_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
password_frame.pack(pady=5)

# Campo de contraseña (inicialmente oculta con show="*")
entry_contrasena = ctk.CTkEntry(master=password_frame, placeholder_text="Contraseña", width=250, height=40,
                               border_width=2, corner_radius=10, show="#")
entry_contrasena.pack(side="left")

# Cargar iconos para el botón de visibilidad
try:
    eye_icon = ctk.CTkImage(light_image="eye_icon.png", size=(20, 20))
    eye_off_icon = ctk.CTkImage(light_image="eye_off_icon.png", size=(20, 20))
except Exception as e:
    print("Iconos para el toggle no encontrados:", e)
    eye_icon = eye_off_icon = None

# Botón para alternar la visibilidad de la contraseña
btn_toggle_password = ctk.CTkButton(master=password_frame, text="", width=40, height=40,
                                    command=toggle_password_visibility, corner_radius=10)
btn_toggle_password.pack(side="left", padx=(5,0))
if eye_icon is not None:
    btn_toggle_password.configure(image=eye_icon)
# --- Fin del campo de contraseña con toggle ---

# Cargar iconos para los botones principales
try:
    login_icon = ctk.CTkImage(light_image="login_icon.png", size=(20, 20))
    register_icon = ctk.CTkImage(light_image="register_icon.png", size=(20, 20))
    recover_icon = ctk.CTkImage(light_image="recover_icon.png", size=(20, 20))
except Exception as e:
    print("Error al cargar iconos:", e)
    login_icon = register_icon = recover_icon = None

# Botón para iniciar sesión
btn_login = ctk.CTkButton(master=frame, text=" Iniciar Sesión", width=200, height=40,
                          image=login_icon, compound="left", command=iniciar_sesion, corner_radius=10)
btn_login.pack(pady=10)

# Botón para registrar
btn_registrar = ctk.CTkButton(master=frame, text=" Registrar", width=200, height=40,
                              image=register_icon, compound="left", command=abrir_interfaz_registro, corner_radius=10)
btn_registrar.pack(pady=10)

# Botón para recuperar contraseña
btn_recuperar = ctk.CTkButton(master=frame, text=" Recuperar Contraseña", width=200, height=40,
                              image=recover_icon, compound="left", command=abrir_interfaz_recuperar, corner_radius=10)
btn_recuperar.pack(pady=10)

root.mainloop()
