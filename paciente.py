import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from database import obtener_medicos, insertar_cita, obtener_citas_por_paciente, eliminar_cita

def cerrar_sesion(window, root_main):
    window.destroy()
    root_main.deiconify()
    root_main.lift()

def mostrar_interfaz_usuario(root_main, paciente):
    root_main.withdraw()
    window = ctk.CTkToplevel(root_main)
    window.title("Panel del Paciente")
    window.geometry("1000x700")
    window.resizable(True, True)

    # Header
    header_frame = ctk.CTkFrame(master=window, corner_radius=10)
    header_frame.pack(fill="x", padx=20, pady=10)
    welcome_label = ctk.CTkLabel(
        master=header_frame,
        text=f"Bienvenido, {paciente['nombres']} {paciente['apellidos']}",
        font=("Segoe UI", 16, "bold")
    )
    welcome_label.pack(side="left", padx=10)
    btn_logout = ctk.CTkButton(
        master=header_frame,
        text="Cerrar Sesión",
        command=lambda: cerrar_sesion(window, root_main),
        corner_radius=10
    )
    btn_logout.pack(side="right", padx=10)

    # Separator
    separator = ctk.CTkFrame(master=window, height=2, fg_color="gray")
    separator.pack(fill="x", padx=20, pady=10)

    # Main container
    main_frame = ctk.CTkFrame(master=window, corner_radius=10)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Left column: Calendario
    left_frame = ctk.CTkFrame(master=main_frame, corner_radius=10)
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Usamos tkcalendar.Calendar (no hay versión nativa en CustomTkinter)
    cal = Calendar(left_frame, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(expand=True, fill="both", padx=10, pady=10)

    def refresh_calendar():
        cal.calevent_remove('all')
        citas = obtener_citas_por_paciente(paciente['id'])
        for cita in citas:
            # cita: (id, fecha, hora, estado, doc_nombres, doc_apellidos, doc_especialidad)
            cita_id, fecha_str, hora, estado, doc_nom, doc_ape, doc_esp = cita
            try:
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                cal.calevent_create(fecha_obj, f"{hora} - {estado}", "appt")
            except Exception as e:
                print(f"Error convirtiendo la fecha: {e}")
        cal.tag_config('appt', background='blue', foreground='white')
    refresh_calendar()

    selected_date_var = ctk.StringVar(value=cal.get_date())
    def on_date_change(event):
        selected_date_var.set(cal.get_date())
    cal.bind("<<CalendarSelected>>", on_date_change)

    # Right column: Formulario de agendamiento
    right_frame = ctk.CTkFrame(master=main_frame, corner_radius=10)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    sched_frame = ctk.CTkFrame(master=right_frame, corner_radius=10)
    sched_frame.pack(fill="x", padx=10, pady=10)

    lbl_fecha = ctk.CTkLabel(master=sched_frame, text="Fecha (del calendario):")
    lbl_fecha.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    lbl_selected_date = ctk.CTkLabel(master=sched_frame, textvariable=selected_date_var)
    lbl_selected_date.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    lbl_hora = ctk.CTkLabel(master=sched_frame, text="Seleccione la hora:")
    lbl_hora.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    horas = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    combobox_hora = ctk.CTkComboBox(master=sched_frame, values=horas, width=100)
    combobox_hora.set(horas[0])
    combobox_hora.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    lbl_medico = ctk.CTkLabel(master=sched_frame, text="Seleccione el médico:")
    lbl_medico.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    medicos = obtener_medicos()
    # Se añade la opción "Seleccionar" por defecto
    doctor_names = ["Seleccionar"]
    doctor_map = {}
    for m in medicos:
        doc_name = f"Dr. {m[3]} {m[4]} - {m[6]}"
        doctor_names.append(doc_name)
        doctor_map[doc_name] = m[0]
    combobox_medico = ctk.CTkComboBox(master=sched_frame, values=doctor_names, width=250)
    combobox_medico.set("Seleccionar")
    combobox_medico.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def schedule_appointment():
        date_val = selected_date_var.get()
        time_val = combobox_hora.get()
        doctor_val = combobox_medico.get()
        # Si se mantiene la opción "Seleccionar", se muestra advertencia
        if doctor_val == "Seleccionar":
            messagebox.showwarning("Advertencia", "Debe seleccionar un médico.")
            return
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
            insertar_cita(paciente['id'], doctor_map.get(doctor_val), date_val, time_val)
            messagebox.showinfo("Éxito", "Cita agendada exitosamente")
            refresh_calendar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agendar la cita: {str(e)}")
    
    btn_agendar = ctk.CTkButton(
        master=sched_frame,
        text="Agendar Cita",
        width=150,
        command=schedule_appointment,
        corner_radius=10
    )
    btn_agendar.grid(row=3, column=0, columnspan=2, pady=10)

    # Botón "Cancelar Cita" en el panel del paciente.
    # Se deshabilitará al abrir la ventana de cancelación para evitar múltiples ventanas.
    btn_cancel_appt = ctk.CTkButton(
        master=right_frame,
        text="Cancelar Cita",
        width=150,
        command=lambda: open_cancel_window(),
        corner_radius=10
    )
    btn_cancel_appt.pack(pady=10)

    def open_cancel_window():
        # Deshabilitar el botón para evitar aperturas múltiples
        btn_cancel_appt.configure(state="disabled")
        cancel_win = ctk.CTkToplevel(window)
        cancel_win.title("Cancelar Cita")
        cancel_win.geometry("600x400")
        tree_frame = ctk.CTkFrame(master=cancel_win)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)
        # Usamos ttk.Treeview para la tabla
        columns = ("ID", "Fecha", "Hora", "Estado", "Médico")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        citas = obtener_citas_por_paciente(paciente['id'])
        for cita in citas:
            cita_id, fecha, hora, estado, doc_nom, doc_ape, doc_esp = cita
            tree.insert("", "end", values=(cita_id, fecha, hora, estado, f"Dr. {doc_nom} {doc_ape} - {doc_esp}"))
        
        def cancel_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione una cita para cancelar.")
                return
            for item in selected:
                cita_id = tree.item(item)['values'][0]
                eliminar_cita(cita_id)
                tree.delete(item)
            messagebox.showinfo("Éxito", "Cita(s) cancelada(s).")
            refresh_calendar()
        
        btn_cancel = ctk.CTkButton(
            master=cancel_win,
            text="Cancelar Cita",
            width=150,
            command=cancel_selected,
            corner_radius=10
        )
        btn_cancel.pack(pady=10)
        
        # Función para reactivar el botón de cancelar cita cuando se cierra la ventana de cancelación
        def on_close_cancel_win():
            btn_cancel_appt.configure(state="normal")
            cancel_win.destroy()
        
        cancel_win.protocol("WM_DELETE_WINDOW", on_close_cancel_win)
    
    window.mainloop()

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    dummy_paciente = {"id": 1, "nombres": "Juan", "apellidos": "Perez"}
    mostrar_interfaz_usuario(root, dummy_paciente)
