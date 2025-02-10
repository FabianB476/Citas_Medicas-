import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from database import obtener_citas_por_medico, actualizar_estado_cita, insertar_cita, obtener_pacientes

# Configuración de apariencia de CustomTkinter
ctk.set_appearance_mode("System")  # También puede ser "Dark" o "Light"
ctk.set_default_color_theme("blue")

def cerrar_sesion(window, root_main):
    window.destroy()
    root_main.deiconify()
    root_main.geometry("400x350")
    root_main.lift()

def refrescar_citas(tree, medico_id):
    for row in tree.get_children():
        tree.delete(row)
    citas = obtener_citas_por_medico(medico_id)
    for cita in citas:
        # cita: (id, fecha, hora, nombres, apellidos, estado)
        cita_id, fecha, hora, nombres, apellidos, estado = cita
        tree.insert("", "end", values=(cita_id, fecha, hora, f"{nombres} {apellidos}", estado))

def marcar_cita(tree, medico_id, nuevo_estado):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Seleccione una cita.")
        return
    for item in selected:
        cita_id = tree.item(item)['values'][0]
        actualizar_estado_cita(cita_id, nuevo_estado)
    messagebox.showinfo("Éxito", f"Cita(s) marcadas como {nuevo_estado}.")
    refrescar_citas(tree, medico_id)

def mostrar_interfaz_medico(root_main, medico):
    # Oculta la ventana principal y crea una nueva ventana de CustomTkinter
    root_main.withdraw()
    window = ctk.CTkToplevel()
    window.title("Panel del Médico")
    window.geometry("1200x800")
    window.resizable(True, True)

    # Encabezado
    header_frame = ctk.CTkFrame(window)
    header_frame.pack(fill="x", padx=10, pady=10)
    welcome_label = ctk.CTkLabel(
        header_frame,
        text=f"Bienvenido, Dr. {medico['nombres']} {medico['apellidos']} - Especialidad: {medico['especialidad']}",
        font=("Segoe UI", 18, "bold")
    )
    welcome_label.pack(side="left", padx=5)
    btn_logout = ctk.CTkButton(header_frame, text="Cerrar Sesión", command=lambda: cerrar_sesion(window, root_main))
    btn_logout.pack(side="right", padx=5)

    # Notebook (Tabview) con dos pestañas
    notebook = ctk.CTkTabview(window)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    notebook.add("Citas Programadas")
    notebook.add("Agendar Cita")

    # Pestaña 1: Citas Programadas
    tab_citas = notebook.tab("Citas Programadas")
    tree_frame = ctk.CTkFrame(tab_citas)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "Fecha", "Hora", "Paciente", "Estado")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    btn_frame = ctk.CTkFrame(tab_citas)
    btn_frame.pack(pady=10)
    btn_atender = ctk.CTkButton(
        btn_frame, 
        text="Marcar como Atendida",
        command=lambda: marcar_cita(tree, medico['id'], "Atendida")
    )
    btn_atender.pack(side="left", padx=5)
    btn_cancelar = ctk.CTkButton(
        btn_frame, 
        text="Cancelar Cita",
        command=lambda: marcar_cita(tree, medico['id'], "Cancelada")
    )
    btn_cancelar.pack(side="left", padx=5)
    btn_refresh = ctk.CTkButton(
        btn_frame, 
        text="Refrescar",
        command=lambda: refrescar_citas(tree, medico['id'])
    )
    btn_refresh.pack(side="left", padx=5)

    refrescar_citas(tree, medico['id'])

    # Pestaña 2: Agendar Cita
    tab_agendar = notebook.tab("Agendar Cita")
    sched_frame = ctk.CTkFrame(tab_agendar)
    sched_frame.pack(fill="x", padx=10, pady=10)

    # Selección del paciente
    patient_label = ctk.CTkLabel(sched_frame, text="Seleccione el paciente:")
    patient_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    pacientes = obtener_pacientes()
    patient_names = []
    patient_map = {}
    for p in pacientes:
        # p: (id, cedula, correo, nombres, apellidos, contrasena)
        name = f"{p[3]} {p[4]} (Ced: {p[1]})"
        patient_names.append(name)
        patient_map[name] = p[0]
    combobox_patient = ctk.CTkComboBox(sched_frame, values=patient_names, state="readonly", width=300)
    if patient_names:
        combobox_patient.set(patient_names[0])
    combobox_patient.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Selección de la fecha (se utiliza tkcalendar)
    date_label = ctk.CTkLabel(sched_frame, text="Seleccione la fecha:")
    date_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    date_entry = DateEntry(sched_frame, width=12, background='darkblue',
                           foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Selección de la hora
    time_label = ctk.CTkLabel(sched_frame, text="Seleccione la hora:")
    time_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
    horas = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    combobox_hora = ctk.CTkComboBox(sched_frame, values=horas, state="readonly", width=100)
    combobox_hora.set(horas[0])
    combobox_hora.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def schedule_appointment_doctor():
        patient_name = combobox_patient.get()
        if not patient_name:
            messagebox.showerror("Error", "Debe seleccionar un paciente.")
            return
        paciente_id = patient_map.get(patient_name)
        date_val = date_entry.get()  # Cadena en formato 'yyyy-mm-dd'
        time_val = combobox_hora.get()
        # Validar que la fecha seleccionada no sea anterior a la actual
        try:
            appointment_date = datetime.strptime(date_val, '%Y-%m-%d').date()
        except Exception as e:
            messagebox.showerror("Error", f"Formato de fecha inválido: {e}")
            return
        current_date = datetime.now().date()
        if appointment_date < current_date:
            messagebox.showerror("Error", "No se pueden agendar citas en fechas anteriores a la fecha actual.")
            return
        try:
            insertar_cita(paciente_id, medico['id'], date_val, time_val)
            messagebox.showinfo("Éxito", "Cita agendada exitosamente.")
            refrescar_citas(tree, medico['id'])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agendar la cita: {str(e)}")

    btn_agendar_doc = ctk.CTkButton(sched_frame, text="Agendar Cita", command=schedule_appointment_doctor)
    btn_agendar_doc.grid(row=3, column=0, columnspan=2, pady=10)

    window.mainloop()

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()  # Se oculta la ventana raíz
    dummy_medico = {"id": 1, "nombres": "Carlos", "apellidos": "Lopez", "especialidad": "Cardiología"}
    mostrar_interfaz_medico(root, dummy_medico)
