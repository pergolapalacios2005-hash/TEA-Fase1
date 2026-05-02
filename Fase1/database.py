import sqlite3
import os
import hashlib

class DatabaseManager:
    def __init__(self, db_name="app_data.db"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        # Creamos la carpeta 'data' en la raíz (subiendo un nivel desde 'Fase 1')
        self.data_dir = os.path.join(self.base_dir, "..", "data")
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self.db_path = os.path.join(self.data_dir, db_name)
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Verificar si necesitamos migrar la tabla users
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                # Verificar estructura de la tabla
                cursor.execute("PRAGMA table_info(users)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                
                # Columnas requeridas para la nueva estructura (sin nombre)
                required_columns = ['id', 'email', 'password', 'edad', 'genero', 'antecedentes_medicos', 'created_at']
                
                # Forzar recreación si la estructura no es correcta
                needs_recreate = ('nombre' in column_names or 
                                not all(col in column_names for col in required_columns) or
                                len(column_names) != len(required_columns))
                
                if needs_recreate:
                    # La tabla tiene estructura incorrecta, migrar
                    cursor.execute("ALTER TABLE users RENAME TO users_old")
                    
                    # Crear nueva tabla con estructura correcta
                    cursor.execute('''
                        CREATE TABLE users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            edad INTEGER,
                            genero TEXT,
                            antecedentes_medicos TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    ''')
                    
                    # Copiar datos relevantes (solo email, password, edad, genero, antecedentes si existen)
                    columns_to_copy = []
                    select_columns = []
                    
                    if 'email' in column_names:
                        columns_to_copy.append('email')
                        select_columns.append('email')
                    if 'password' in column_names:
                        columns_to_copy.append('password') 
                        select_columns.append('password')
                    if 'edad' in column_names:
                        columns_to_copy.append('edad')
                        select_columns.append('edad')
                    if 'genero' in column_names:
                        columns_to_copy.append('genero')
                        select_columns.append('genero')
                    if 'antecedentes_medicos' in column_names:
                        columns_to_copy.append('antecedentes_medicos')
                        select_columns.append('antecedentes_medicos')
                    if 'created_at' in column_names:
                        columns_to_copy.append('created_at')
                        select_columns.append('created_at')
                    
                    if columns_to_copy:
                        cursor.execute(f'''
                            INSERT INTO users ({', '.join(columns_to_copy)})
                            SELECT {', '.join(select_columns)}
                            FROM users_old
                        ''')
                    
                    # Eliminar tabla antigua
                    cursor.execute("DROP TABLE users_old")
            else:
                # Crear tabla por primera vez
                cursor.execute('''
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        edad INTEGER,
                        genero TEXT,
                        antecedentes_medicos TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            
            # Tabla de diagnósticos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS diagnosticos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    sintomas TEXT NOT NULL,
                    diagnostico_sugerido TEXT NOT NULL,
                    confianza REAL,
                    notas TEXT,
                    descartadas TEXT,
                    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Tabla de síntomas registrados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sintomas_registro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    sintoma TEXT NOT NULL,
                    duracion TEXT,
                    severidad INTEGER,
                    ubicacion TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()

    def _hash_password(self, password):
        """Transforma la contraseña en un hash SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def crear_usuario(self, email, password, edad="", genero="", antecedentes=""):
        """Registra un nuevo usuario con información médica básica (anónimo)."""
        try:
            hashed_pw = self._hash_password(password)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (email, password, edad, genero, antecedentes_medicos) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (email, hashed_pw, edad, genero, antecedentes))
                conn.commit()
                return True, "Usuario creado con éxito."
        except sqlite3.IntegrityError:
            return False, "El correo ya está registrado."

    def verificar_usuario(self, email, password):
        """Compara la contraseña ingresada con el hash guardado."""
        hashed_pw = self._hash_password(password)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hashed_pw))
            user = cursor.fetchone()
            return user is not None

    def obtener_user_id(self, email):
        """Obtiene el ID del usuario por email."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            result = cursor.fetchone()
            return result[0] if result else None

    def obtener_usuario(self, email):
        """Obtiene toda la información del usuario."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, email, edad, genero, antecedentes_medicos FROM users WHERE email = ?', (email,))
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'email': result[1],
                    'edad': result[2],
                    'genero': result[3],
                    'antecedentes': result[4]
                }
            return None

    def guardar_diagnostico(self, user_id, sintomas, diagnostico, confianza=0.0, notas="", descartadas=""):
        """Guarda un diagnóstico previo en la base de datos."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO diagnosticos (user_id, sintomas, diagnostico_sugerido, confianza, notas, descartadas)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, sintomas, diagnostico, confianza, notas, descartadas))
                conn.commit()
                return True, "Diagnóstico guardado exitosamente."
        except Exception as e:
            return False, f"Error al guardar diagnóstico: {str(e)}"

    def obtener_historial_diagnosticos(self, user_id):
        """Obtiene el historial de diagnósticos de un usuario."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, sintomas, diagnostico_sugerido, confianza, fecha_consulta, notas
                FROM diagnosticos
                WHERE user_id = ?
                ORDER BY fecha_consulta DESC
            ''', (user_id,))
            diagnosticos = cursor.fetchall()
            return diagnosticos if diagnosticos else []