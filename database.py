import sqlite3

DATABASE_NAME = "usuarios.db"

def create_tables():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    # Tabla para pacientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            contrasena TEXT NOT NULL
        )
    """)
    # Tabla para médicos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            contrasena TEXT NOT NULL,
            especialidad TEXT NOT NULL
        )
    """)
    # Tabla para citas (se incluye la columna 'estado')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            medico_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente',
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
            FOREIGN KEY (medico_id) REFERENCES medicos(id)
        )
    """)
    connection.commit()
    # Si la tabla ya existía, intentamos agregar la columna 'estado' (se ignora el error si ya existe)
    try:
        cursor.execute("ALTER TABLE citas ADD COLUMN estado TEXT NOT NULL DEFAULT 'Pendiente'")
    except sqlite3.OperationalError:
        pass
    connection.commit()
    connection.close()

def insertar_paciente(cedula, correo, nombres, apellidos, contrasena):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO pacientes (cedula, correo, nombres, apellidos, contrasena)
        VALUES (?, ?, ?, ?, ?)
    """, (cedula, correo, nombres, apellidos, contrasena))
    connection.commit()
    paciente_id = cursor.lastrowid
    connection.close()
    return paciente_id

def insertar_medico(cedula, correo, nombres, apellidos, contrasena, especialidad):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO medicos (cedula, correo, nombres, apellidos, contrasena, especialidad)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cedula, correo, nombres, apellidos, contrasena, especialidad))
    connection.commit()
    medico_id = cursor.lastrowid
    connection.close()
    return medico_id

def insertar_cita(paciente_id, medico_id, fecha, hora):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO citas (paciente_id, medico_id, fecha, hora, estado)
        VALUES (?, ?, ?, ?, 'Pendiente')
    """, (paciente_id, medico_id, fecha, hora))
    connection.commit()
    connection.close()

def eliminar_cita(cita_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM citas WHERE id = ?", (cita_id,))
    connection.commit()
    connection.close()

def actualizar_estado_cita(cita_id, estado):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("UPDATE citas SET estado = ? WHERE id = ?", (estado, cita_id))
    connection.commit()
    connection.close()

def obtener_citas_por_medico(medico_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    query = """
        SELECT citas.id, citas.fecha, citas.hora, pacientes.nombres, pacientes.apellidos, citas.estado
        FROM citas
        JOIN pacientes ON citas.paciente_id = pacientes.id
        WHERE citas.medico_id = ?
        ORDER BY citas.fecha, citas.hora
    """
    cursor.execute(query, (medico_id,))
    citas = cursor.fetchall()
    connection.close()
    return citas

def obtener_citas_por_paciente(paciente_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    query = """
        SELECT citas.id, citas.fecha, citas.hora, citas.estado, medicos.nombres, medicos.apellidos, medicos.especialidad
        FROM citas
        JOIN medicos ON citas.medico_id = medicos.id
        WHERE citas.paciente_id = ?
        ORDER BY citas.fecha, citas.hora
    """
    cursor.execute(query, (paciente_id,))
    citas = cursor.fetchall()
    connection.close()
    return citas

def obtener_medicos():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT id, cedula, correo, nombres, apellidos, contrasena, especialidad FROM medicos")
    medicos = cursor.fetchall()
    connection.close()
    return medicos

def obtener_medico_por_correo(correo):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT id, cedula, correo, nombres, apellidos, contrasena, especialidad FROM medicos WHERE correo = ?", (correo,))
    medico = cursor.fetchone()
    connection.close()
    return medico

def obtener_paciente_por_correo(correo):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT id, cedula, correo, nombres, apellidos, contrasena FROM pacientes WHERE correo = ?", (correo,))
    paciente = cursor.fetchone()
    connection.close()
    return paciente

def obtener_pacientes():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT id, cedula, correo, nombres, apellidos, contrasena FROM pacientes")
    pacientes = cursor.fetchall()
    connection.close()
    return pacientes
