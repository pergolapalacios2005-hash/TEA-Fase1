import customtkinter as ctk

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_register_click, **kwargs):
        super().__init__(master, **kwargs)

        # Configuración de columnas (Lado izquierdo imagen, Lado derecho Formulario)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # LADO IZQUIERDO: Apartado para imagen
        self.img_container = ctk.CTkFrame(self, fg_color="#0d47a1", corner_radius=0)
        self.img_container.grid(row=0, column=0, sticky="nsew")
        
        # Contenido del lado izquierdo
        info_label = ctk.CTkLabel(
            self.img_container,
            text="🏥\n\nSistema Médico\nDiagnóstico Previo\n\nAcceso Seguro",
            text_color="white",
            font=("Helvetica", 24, "bold"),
            text_color_disabled="white"
        )
        info_label.pack(expand=True)

        self.form_container = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.form_container.grid(row=0, column=1, padx=40, pady=40, sticky="nsew")

        ctk.CTkLabel(
            self.form_container,
            text="Acceso al Sistema Médico",
            text_color="black",
            font=("Helvetica", 24, "bold")
        ).pack(pady=(40, 20))

        # Campos de entrada
        self.email_entry = ctk.CTkEntry(self.form_container, placeholder_text="Email", width=300)
        self.email_entry.pack(pady=10)
        self.pass_entry = ctk.CTkEntry(self.form_container, placeholder_text="Password", show="*", width=300)
        self.pass_entry.pack(pady=10)

        # Botón Login
        self.btn_login = ctk.CTkButton(self.form_container, text="Iniciar Sesión", width=300)
        self.btn_login.pack(pady=20)
        self.btn_login.configure(command=self.ejecutar_login)
        self.error_label = ctk.CTkLabel(
            self.form_container, 
            text="", 
            text_color="#e74c3c",
            font=("Helvetica", 12)
        )
        self.error_label.pack(pady=5)

        # Link a Registro
        self.btn_signup = ctk.CTkButton(
            self.form_container,
            text="¿No tienes cuenta? Regístrate aquí",
            fg_color="transparent",
            text_color="blue",
            hover=False,
            command=on_register_click
        )
        self.btn_signup.pack(pady=(10, 20))

        # Disclaimer médico
        disclaimer = ctk.CTkLabel(
            self.form_container,
            text="⚠️ Este sistema proporciona diagnóstico PRELIMINAR basado en IA.\nNO reemplaza consulta médica profesional.",
            font=("Helvetica", 10),
            text_color="orange",
            text_color_disabled="orange"
        )
        disclaimer.pack(pady=(10, 20))

    def ejecutar_login(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()

        if not email or not password:
            self.error_label.configure(text="Campos vacíos")
            return

        es_valido = self.master.master.db.verificar_usuario(email, password)

        if es_valido:
            self.error_label.configure(text="") # Limpiamos error
            # Guardar información del usuario actual
            self.master.master.current_user = self.master.master.db.obtener_usuario(email)
            self.master.master.transition(self.master.master.show_dashboard_view)
        else:
            self.error_label.configure(text="Correo o contraseña incorrectos")
