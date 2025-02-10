import customtkinter as ctk
from tkinter import messagebox
from database import insertar_paciente, insertar_medico
from paciente import mostrar_interfaz_usuario
from medico import mostrar_interfaz_medico

def validar_registro(root_main, root_registro, user_type_var,
                     entry_cedula, entry_correo, entry_nombres, entry_apellidos,
                     entry_contrasena, entry_repetir_contrasena, entry_especialidad):
    cedula = entry_cedula.get().strip()
    correo = entry_correo.get().strip()
    nombres = entry_nombres.get().strip()
    apellidos = entry_apellidos.get().strip()
    contrasena = entry_contrasena.get().strip()
    repetir_contrasena = entry_repetir_contrasena.get().strip()
    user_type = user_type_var.get()  # "paciente" o "medico"
    especialidad = entry_especialidad.get().strip() if user_type == "medico" else ""
    
    if not cedula or not correo or not nombres or not apellidos or not contrasena or not repetir_contrasena:
        messagebox.showwarning("Advertencia", "Por favor complete todos los campos obligatorios.")
        return
    if contrasena != repetir_contrasena:
        messagebox.showwarning("Advertencia", "Las contraseñas no coinciden.")
        return
    if user_type == "medico" and not especialidad:
        messagebox.showwarning("Advertencia", "El campo de especialidad es obligatorio para médicos.")
        return
    
    try:
        if user_type == "paciente":
            paciente_id = insertar_paciente(cedula, correo, nombres, apellidos, contrasena)
            messagebox.showinfo("Éxito", "Registro exitoso como Paciente.")
            root_registro.destroy()
            mostrar_interfaz_usuario(root_main, {"id": paciente_id, "nombres": nombres, "apellidos": apellidos})
        elif user_type == "medico":
            medico_id = insertar_medico(cedula, correo, nombres, apellidos, contrasena, especialidad)
            messagebox.showinfo("Éxito", "Registro exitoso como Médico.")
            root_registro.destroy()
            mostrar_interfaz_medico(root_main, {"id": medico_id, "nombres": nombres, "apellidos": apellidos, "especialidad": especialidad})
    except Exception as e:
        messagebox.showerror("Error", f"Error en el registro: {str(e)}")

def cancelar_registro(root_main, root_registro):
    root_registro.destroy()
    root_main.deiconify()

def on_user_type_change(user_type_var, entry_especialidad):
    if user_type_var.get() == "medico":
        entry_especialidad.configure(state="normal")
    else:
        entry_especialidad.delete(0, ctk.END)
        entry_especialidad.configure(state="disabled")

def mostrar_interfaz_registro(root_main):
    root_registro = ctk.CTkToplevel(root_main)
    root_registro.title("Registro de Usuario")
    root_registro.geometry("700x550")
    root_registro.resizable(False, False)
    
    # Crear un frame principal con bordes redondeados
    frame = ctk.CTkFrame(master=root_registro, corner_radius=20)
    frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    lbl_titulo = ctk.CTkLabel(master=frame, text="Registro de Usuario", font=("Segoe UI", 20, "bold"))
    lbl_titulo.pack(pady=20)
    
    # Panel contenedor para dos secciones
    container = ctk.CTkFrame(master=frame, corner_radius=20)
    container.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Sección izquierda: Información Personal
    frame_left = ctk.CTkFrame(master=container, corner_radius=20)
    frame_left.pack(side="left", expand=True, fill="both", padx=10, pady=10)
    
    lbl_cedula = ctk.CTkLabel(master=frame_left, text="Cédula *")
    lbl_cedula.pack(pady=5)
    entry_cedula = ctk.CTkEntry(master=frame_left, placeholder_text="Ingrese su cédula", width=200)
    entry_cedula.pack(pady=5)
    
    lbl_correo = ctk.CTkLabel(master=frame_left, text="Correo *")
    lbl_correo.pack(pady=5)
    entry_correo = ctk.CTkEntry(master=frame_left, placeholder_text="Ingrese su correo", width=200)
    entry_correo.pack(pady=5)
    
    lbl_nombres = ctk.CTkLabel(master=frame_left, text="Nombres *")
    lbl_nombres.pack(pady=5)
    entry_nombres = ctk.CTkEntry(master=frame_left, placeholder_text="Ingrese sus nombres", width=200)
    entry_nombres.pack(pady=5)
    
    lbl_apellidos = ctk.CTkLabel(master=frame_left, text="Apellidos *")
    lbl_apellidos.pack(pady=5)
    entry_apellidos = ctk.CTkEntry(master=frame_left, placeholder_text="Ingrese sus apellidos", width=200)
    entry_apellidos.pack(pady=5)
    
    # Sección derecha: Información de Seguridad
    frame_right = ctk.CTkFrame(master=container, corner_radius=20)
    frame_right.pack(side="right", expand=True, fill="both", padx=10, pady=10)
    
    lbl_contrasena = ctk.CTkLabel(master=frame_right, text="Contraseña *")
    lbl_contrasena.pack(pady=5)
    entry_contrasena = ctk.CTkEntry(master=frame_right, placeholder_text="Ingrese su contraseña", width=200, show="*")
    entry_contrasena.pack(pady=5)
    
    lbl_repetir_contrasena = ctk.CTkLabel(master=frame_right, text="Repetir Contraseña *")
    lbl_repetir_contrasena.pack(pady=5)
    entry_repetir_contrasena = ctk.CTkEntry(master=frame_right, placeholder_text="Repita su contraseña", width=200, show="*")
    entry_repetir_contrasena.pack(pady=5)
    
    lbl_especialidad = ctk.CTkLabel(master=frame_right, text="Especialidad (solo para médicos)")
    lbl_especialidad.pack(pady=5)
    entry_especialidad = ctk.CTkEntry(master=frame_right, placeholder_text="Ingrese su especialidad", width=200)
    entry_especialidad.pack(pady=5)
    entry_especialidad.configure(state="disabled")
    
    # Selección del tipo de usuario (Radiobuttons)
    user_type_var = ctk.StringVar(value="paciente")
    tipo_frame = ctk.CTkFrame(master=frame_right, corner_radius=10)
    tipo_frame.pack(pady=10)
    lbl_tipo = ctk.CTkLabel(master=tipo_frame, text="Tipo de usuario:")
    lbl_tipo.pack(side="left", padx=5)
    rb_paciente = ctk.CTkRadioButton(master=tipo_frame, text="Paciente", variable=user_type_var, value="paciente",
                                    command=lambda: on_user_type_change(user_type_var, entry_especialidad))
    rb_paciente.pack(side="left", padx=5)
    rb_medico = ctk.CTkRadioButton(master=tipo_frame, text="Médico", variable=user_type_var, value="medico",
                                  command=lambda: on_user_type_change(user_type_var, entry_especialidad))
    rb_medico.pack(side="left", padx=5)
    
    btn_frame = ctk.CTkFrame(master=frame, corner_radius=10)
    btn_frame.pack(pady=20)
    
    btn_registrar = ctk.CTkButton(master=btn_frame, text="Registrar", width=150,
                                  command=lambda: validar_registro(root_main, root_registro,
                                                                   user_type_var,
                                                                   entry_cedula, entry_correo, entry_nombres, entry_apellidos,
                                                                   entry_contrasena, entry_repetir_contrasena, entry_especialidad),
                                  corner_radius=10)
    btn_registrar.pack(side="left", padx=10)
    
    btn_cancelar = ctk.CTkButton(master=btn_frame, text="Cancelar", width=150,
                                 command=lambda: cancelar_registro(root_main, root_registro),
                                 corner_radius=10)
    btn_cancelar.pack(side="right", padx=10)
    
    root_registro.protocol("WM_DELETE_WINDOW", lambda: cancelar_registro(root_main, root_registro))
    
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    mostrar_interfaz_reg
