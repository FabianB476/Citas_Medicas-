import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from database import DATABASE_NAME, obtener_paciente_por_correo, obtener_medico_por_correo

def actualizar_contrasena_db(tabla, nuevo, correo):
    try:
        with sqlite3.connect(DATABASE_NAME, timeout=10) as connection:
            cursor = connection.cursor()
            query = f"UPDATE {tabla} SET contrasena = ? WHERE correo = ?"
            cursor.execute(query, (nuevo, correo))
            connection.commit()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar la contraseña: {e}")
        return False

def mostrar_interfaz_recuperar(root_main):
    # Ocultar la ventana principal (login)
    root_main.withdraw()
    
    # Crear la ventana de recuperación (con la misma geometría que el login: 600x500)
    window = ctk.CTkToplevel(root_main)
    window.title("Recuperar Contraseña")
    window.geometry("600x500")
    window.resizable(False, False)
    window.configure(fg_color="#FFFFFF")  # Fondo blanco
    
    # Configurar apariencia
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Usar un CTkScrollableFrame para que, si el contenido se extiende, se active el scrollbar
    frame = ctk.CTkScrollableFrame(master=window, corner_radius=20)
    frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Mostrar icono de recuperación (si existe)
    try:
        icon = ctk.CTkImage(light_image="recover_icon.png", size=(100, 100))
        lbl_icon = ctk.CTkLabel(master=frame, image=icon, text="")
        lbl_icon.image = icon  # Conservar referencia
        lbl_icon.grid(row=0, column=0, columnspan=2, pady=(10,5))
    except Exception as e:
        print("Icono de recuperación no encontrado:", e)
    
    # Título centrado
    lbl_titulo = ctk.CTkLabel(master=frame, text="Recuperar Contraseña", font=("Segoe UI", 20, "bold"))
    lbl_titulo.grid(row=1, column=0, columnspan=2, pady=(5,20))
    
    # Frame para los datos de verificación
    frame_verificar = ctk.CTkFrame(master=frame, corner_radius=10)
    frame_verificar.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")
    # Configurar 3 columnas para centrar los widgets
    frame_verificar.grid_columnconfigure(0, weight=1)
    frame_verificar.grid_columnconfigure(1, weight=1)
    frame_verificar.grid_columnconfigure(2, weight=1)
    
    lbl_tipo = ctk.CTkLabel(master=frame_verificar, text="Tipo de Usuario:")
    lbl_tipo.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    tipo_var = ctk.StringVar(value="paciente")
    rb_paciente = ctk.CTkRadioButton(master=frame_verificar, text="Paciente", variable=tipo_var, value="paciente")
    rb_paciente.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    rb_medico = ctk.CTkRadioButton(master=frame_verificar, text="Médico", variable=tipo_var, value="medico")
    rb_medico.grid(row=0, column=2, sticky="w", padx=5, pady=5)
    
    lbl_cedula = ctk.CTkLabel(master=frame_verificar, text="Cédula:")
    lbl_cedula.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_cedula = ctk.CTkEntry(master=frame_verificar, placeholder_text="Ingrese su cédula", width=200)
    entry_cedula.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=5)
    
    lbl_correo = ctk.CTkLabel(master=frame_verificar, text="Correo:")
    lbl_correo.grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_correo = ctk.CTkEntry(master=frame_verificar, placeholder_text="Ingrese su correo", width=200)
    entry_correo.grid(row=2, column=1, columnspan=2, sticky="w", padx=5, pady=5)
    
    lbl_nombres = ctk.CTkLabel(master=frame_verificar, text="Nombres:")
    lbl_nombres.grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_nombres = ctk.CTkEntry(master=frame_verificar, placeholder_text="Ingrese sus nombres", width=200)
    entry_nombres.grid(row=3, column=1, columnspan=2, sticky="w", padx=5, pady=5)
    
    lbl_apellidos = ctk.CTkLabel(master=frame_verificar, text="Apellidos:")
    lbl_apellidos.grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_apellidos = ctk.CTkEntry(master=frame_verificar, placeholder_text="Ingrese sus apellidos", width=200)
    entry_apellidos.grid(row=4, column=1, columnspan=2, sticky="w", padx=5, pady=5)
    
    lbl_especialidad = ctk.CTkLabel(master=frame_verificar, text="Especialidad:")
    lbl_especialidad.grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_especialidad = ctk.CTkEntry(master=frame_verificar, placeholder_text="Ingrese su especialidad", width=200)
    entry_especialidad.grid(row=5, column=1, columnspan=2, sticky="w", padx=5, pady=5)
    entry_especialidad.configure(state="disabled")
    
    def toggle_especialidad():
        if tipo_var.get() == "medico":
            entry_especialidad.configure(state="normal")
        else:
            entry_especialidad.delete(0, "end")
            entry_especialidad.configure(state="disabled")
    rb_paciente.configure(command=toggle_especialidad)
    rb_medico.configure(command=toggle_especialidad)
    toggle_especialidad()
    
    btn_verificar = ctk.CTkButton(master=frame_verificar, text="Verificar Datos", width=150)
    btn_verificar.grid(row=6, column=0, columnspan=3, pady=15)
    
    # Frame para actualización de contraseña (inicialmente oculto)
    frame_nueva = ctk.CTkFrame(master=frame, corner_radius=10)
    # Este frame se mostrará cuando la verificación sea exitosa
    
    # --- Incorporación del toggle (ojito) en los campos de contraseña ---
    # Se cargan los íconos para alternar la visibilidad
    try:
        eye_icon = ctk.CTkImage(light_image="eye_icon.png", size=(20, 20))
        eye_off_icon = ctk.CTkImage(light_image="eye_off_icon.png", size=(20, 20))
    except Exception as e:
        print("Iconos para el toggle no encontrados:", e)
        eye_icon = eye_off_icon = None

    # Variables de control para la visibilidad
    password_visible_new = False
    password_visible_confirm = False

    def toggle_password_visibility_new():
        nonlocal password_visible_new
        if password_visible_new:
            entry_nueva.configure(show="*")
            btn_toggle_nueva.configure(image=eye_icon)
            password_visible_new = False
        else:
            entry_nueva.configure(show="")
            btn_toggle_nueva.configure(image=eye_off_icon)
            password_visible_new = True

    def toggle_password_visibility_confirm():
        nonlocal password_visible_confirm
        if password_visible_confirm:
            entry_confirm.configure(show="*")
            btn_toggle_confirm.configure(image=eye_icon)
            password_visible_confirm = False
        else:
            entry_confirm.configure(show="")
            btn_toggle_confirm.configure(image=eye_off_icon)
            password_visible_confirm = True

    # Nueva contraseña con toggle
    lbl_nueva = ctk.CTkLabel(master=frame_nueva, text="Nueva Contraseña:")
    lbl_nueva.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    frame_entry_nueva = ctk.CTkFrame(master=frame_nueva, fg_color="transparent")
    frame_entry_nueva.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    entry_nueva = ctk.CTkEntry(master=frame_entry_nueva, placeholder_text="Ingrese nueva contraseña", width=180, show="*")
    entry_nueva.pack(side="left")
    btn_toggle_nueva = ctk.CTkButton(master=frame_entry_nueva, text="", width=40, command=toggle_password_visibility_new, corner_radius=10)
    btn_toggle_nueva.pack(side="left", padx=(5,0))
    if eye_icon is not None:
        btn_toggle_nueva.configure(image=eye_icon)
    
    # Confirmar contraseña con toggle
    lbl_confirm = ctk.CTkLabel(master=frame_nueva, text="Confirmar Contraseña:")
    lbl_confirm.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    frame_entry_confirm = ctk.CTkFrame(master=frame_nueva, fg_color="transparent")
    frame_entry_confirm.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    entry_confirm = ctk.CTkEntry(master=frame_entry_confirm, placeholder_text="Confirme la contraseña", width=180, show="*")
    entry_confirm.pack(side="left")
    btn_toggle_confirm = ctk.CTkButton(master=frame_entry_confirm, text="", width=40, command=toggle_password_visibility_confirm, corner_radius=10)
    btn_toggle_confirm.pack(side="left", padx=(5,0))
    if eye_icon is not None:
        btn_toggle_confirm.configure(image=eye_icon)
    
    btn_actualizar = ctk.CTkButton(master=frame_nueva, text="Actualizar Contraseña", width=150)
    btn_actualizar.grid(row=2, column=0, columnspan=2, pady=15)
    # --- Fin de la sección de toggle ---
    
    def verificar_datos():
        tipo = tipo_var.get()
        cedula = entry_cedula.get().strip()
        correo = entry_correo.get().strip()
        nombres = entry_nombres.get().strip()
        apellidos = entry_apellidos.get().strip()
        especialidad = entry_especialidad.get().strip() if tipo == "medico" else ""
        
        if not cedula or not correo or not nombres or not apellidos:
            messagebox.showwarning("Advertencia", "Complete todos los campos requeridos.")
            return
        
        if tipo == "paciente":
            registro = obtener_paciente_por_correo(correo)
            if not registro:
                messagebox.showerror("Error", "Usuario no encontrado.")
                return
            if registro[1].strip() != cedula or registro[3].strip().lower() != nombres.lower() or registro[4].strip().lower() != apellidos.lower():
                messagebox.showerror("Error", "Los datos no coinciden.")
                return
        else:
            registro = obtener_medico_por_correo(correo)
            if not registro:
                messagebox.showerror("Error", "Usuario no encontrado.")
                return
            if (registro[1].strip() != cedula or
                registro[3].strip().lower() != nombres.lower() or
                registro[4].strip().lower() != apellidos.lower() or
                registro[6].strip().lower() != especialidad.lower()):
                messagebox.showerror("Error", "Los datos no coinciden.")
                return
        
        # Si la verificación es correcta, deshabilitar los campos de verificación y mostrar el frame para actualizar
        for widget in frame_verificar.winfo_children():
            widget.configure(state="disabled")
        frame_nueva.grid(row=3, column=0, columnspan=2, pady=20)
    
    btn_verificar.configure(command=verificar_datos)
    
    def actualizar_contrasena():
        tipo = tipo_var.get()
        correo = entry_correo.get().strip()
        nueva = entry_nueva.get().strip()
        confirm = entry_confirm.get().strip()
        if not nueva or not confirm:
            messagebox.showwarning("Advertencia", "Complete los campos de la nueva contraseña.")
            return
        if nueva != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
        
        tabla = "pacientes" if tipo == "paciente" else "medicos"
        if actualizar_contrasena_db(tabla, nueva, correo):
            messagebox.showinfo("Éxito", "Contraseña actualizada exitosamente.")
            window.destroy()
            root_main.deiconify()
            root_main.lift()
    
    btn_actualizar.configure(command=actualizar_contrasena)
    
    def cancelar():
        window.destroy()
        root_main.deiconify()
        root_main.lift()
    
    btn_cancelar_main = ctk.CTkButton(master=frame, text="Cancelar", width=150, command=cancelar)
    btn_cancelar_main.grid(row=10, column=0, columnspan=2, pady=10)
    
    window.protocol("WM_DELETE_WINDOW", cancelar)
    
    window.mainloop()

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    mostrar_interfaz_recuperar(root)
