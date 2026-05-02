import threading 
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from services.email_service import enviar_correo_bienvenida
import re

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, on_back_to_login, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="#f2f2f2", **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # LADO IZQUIERDO: Información médica
        self.img_container = ctk.CTkFrame(self, fg_color="#0d47a1", corner_radius=0)
        self.img_container.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_img_placeholder = ctk.CTkLabel(
            self.img_container, 
            text="🏥\n\nRegistro en\nSistema Médico\n\nDiagnóstico Previo",
            text_color="white",
            font=("Helvetica", 20, "bold")
        )
        self.lbl_img_placeholder.pack(expand=True)

        # Eventos para mover ventana
        self.img_container.bind("<ButtonPress-1>", master.master.start_move)
        self.img_container.bind("<B1-Motion>", master.master.do_move)

        # --- SECCIÓN DERECHA: FORMULARIO ---
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.grid(row=0, column=1, sticky="nsew")

        # Frame con scroll para el formulario (usando Canvas estándar de tkinter)
        self.canvas = tk.Canvas(self.right_container, bg="white", highlightthickness=0, relief="flat")
        self.scrollbar = ctk.CTkScrollbar(self.right_container, command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self.scrollbar.pack(side="right", fill="y")

        # Contenedor del formulario
        self.form = ctk.CTkFrame(self.scrollable_frame, fg_color="white", corner_radius=0)
        self.form.pack(fill="both", expand=True)

        # Título
        ctk.CTkLabel(
            self.form, text="Crear Cuenta Médica", 
            text_color="black", font=("Helvetica", 20, "bold")
        ).pack(pady=(20, 15))

        # --- INFORMACIÓN PERSONAL ---
        ctk.CTkLabel(self.form, text="📋 INFORMACIÓN PERSONAL", text_color="black", 
                    font=("Helvetica", 11, "bold")).pack(anchor="w", padx=30, pady=(15, 5))

        # Email
        ctk.CTkLabel(self.form, text="Email *", text_color="black", font=("Helvetica", 11)).pack(anchor="w", padx=30)
        self.email_entry = ctk.CTkEntry(self.form, placeholder_text="correo@ejemplo.com", width=300, height=32)
        self.email_entry.pack(pady=(0, 10), padx=30)

        # Edad
        ctk.CTkLabel(self.form, text="Edad", text_color="black", font=("Helvetica", 11)).pack(anchor="w", padx=30)
        self.edad_entry = ctk.CTkEntry(self.form, placeholder_text="Ej: 30", width=300, height=32)
        self.edad_entry.pack(pady=(0, 10), padx=30)

        # Género
        ctk.CTkLabel(self.form, text="Género", text_color="black", font=("Helvetica", 11)).pack(anchor="w", padx=30)
        self.genero_var = ctk.StringVar(value="No especificado")
        genero_combo = ctk.CTkComboBox(
            self.form, 
            values=["Masculino", "Femenino", "Otro", "Prefiero no decir"],
            variable=self.genero_var,
            width=300,
            height=32,
            fg_color="white",
            text_color="black",
            border_color="gray",
            button_color="#0d47a1"
        )
        genero_combo.pack(pady=(0, 15), padx=30)

        # --- INFORMACIÓN MÉDICA ---
        ctk.CTkLabel(self.form, text="🏥 INFORMACIÓN MÉDICA", text_color="black", 
                    font=("Helvetica", 11, "bold")).pack(anchor="w", padx=30, pady=(15, 5))

        # Antecedentes médicos
        ctk.CTkLabel(self.form, text="Antecedentes Médicos Relevantes", 
                    text_color="black", font=("Helvetica", 11)).pack(anchor="w", padx=30)
        self.antecedentes_text = ctk.CTkTextbox(self.form, height=70, width=300, fg_color="white",
                                               text_color="black", border_color="gray", border_width=1)
        self.antecedentes_text.pack(pady=(0, 15), padx=30)
        self.antecedentes_text.insert("0.0", "Ej: Diabetes, Hipertensión, Alergias... (opcional)")

        # --- SEGURIDAD ---
        ctk.CTkLabel(self.form, text="🔒 SEGURIDAD", text_color="black", 
                    font=("Helvetica", 11, "bold")).pack(anchor="w", padx=30, pady=(15, 5))

        # Password
        ctk.CTkLabel(self.form, text="Contraseña *", text_color="black", font=("Helvetica", 11)).pack(anchor="w", padx=30)
        self.pass_entry = ctk.CTkEntry(self.form, placeholder_text="Contraseña segura", 
                                      show="*", width=300, height=32)
        self.pass_entry.pack(pady=(0, 10), padx=30)

        # Confirmar Password
        ctk.CTkLabel(self.form, text="Confirmar Contraseña *", text_color="black", font=("Helvetica", 11)).pack(anchor="w", padx=30)
        self.pass_confirm_entry = ctk.CTkEntry(self.form, placeholder_text="Repite tu contraseña", 
                                              show="*", width=300, height=32)
        self.pass_confirm_entry.pack(pady=(0, 15), padx=30)

        # --- TÉRMINOS ---
        self.terminos_var = ctk.BooleanVar(value=False)
        terminos_check = ctk.CTkCheckBox(
            self.form,
            text="Acepto los términos y condiciones de privacidad médica",
            variable=self.terminos_var,
            text_color="black",
            fg_color="#0d47a1"
        )
        terminos_check.pack(anchor="w", padx=30, pady=(0, 15))

        # Botones
        botones_frame = ctk.CTkFrame(self.form, fg_color="white")
        botones_frame.pack(fill="x", padx=30, pady=(10, 20))

        self.btn_create = ctk.CTkButton(
            botones_frame, text="✓ Crear Cuenta", fg_color="#0d47a1", hover_color="#1565c0",
            width=300, height=40, font=("Helvetica", 12, "bold"),
            command=self.ejecutar_registro
        )
        self.btn_create.pack(pady=(0, 10))

        self.error_label = ctk.CTkLabel(
            botones_frame, 
            text="", 
            text_color="#e74c3c", 
            font=("Helvetica", 11),
            bg_color="white",
            wraplength=300
        )
        self.error_label.pack(pady=5)

        self.btn_back = ctk.CTkButton(
            botones_frame, text="← Volver a Iniciar Sesión", 
            fg_color="transparent", text_color="#0d47a1", hover=False,
            font=("Helvetica", 11), command=on_back_to_login
        )
        self.btn_back.pack()

        # Disclaimer
        disclaimer = ctk.CTkLabel(
            botones_frame,
            text="⚠️ Tu información médica será almacenada de forma segura y encriptada.",
            font=("Helvetica", 9),
            text_color="orange",
            wraplength=300
        )
        disclaimer.pack(pady=(10, 0))

    def validar_email(self, email):
        """Valida el formato básico del email usando regex."""
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(patron, email) is not None

    def ejecutar_registro(self):
        """Lógica para registrar usuario con información médica."""
        email = self.email_entry.get()
        password = self.pass_entry.get()
        password_confirm = self.pass_confirm_entry.get()
        edad = self.edad_entry.get()
        genero = self.genero_var.get()
        antecedentes = self.antecedentes_text.get("0.0", "end").strip()
        
        if not email or not password:
            self.mostrar_error("Email y contraseña son obligatorios.")
            return
        
        if not self.validar_email(email):
            self.mostrar_error("Formato de email inválido.")
            return
        
        if len(password) < 6:
            self.mostrar_error("La contraseña debe tener al menos 6 caracteres.")
            return
        
        if password != password_confirm:
            self.mostrar_error("Las contraseñas no coinciden.")
            return
        
        if not self.terminos_var.get():
            self.mostrar_error("Debes aceptar los términos y condiciones.")
            return
        
        # Registrar en BD con información médica
        exito, mensaje = self.master.master.db.crear_usuario(
            email, password, edad, genero, antecedentes
        )

        if exito:
            # Enviar correo de bienvenida
            threading.Thread(target=self._enviar_correo, args=(email,), daemon=True).start()
            
            # Transición al Login
            self.master.master.transition(self.master.master.show_login_view)
        else:
            self.mostrar_error(mensaje)

    def _enviar_correo(self, email):
        """Envía correo de bienvenida en thread separado."""
        if enviar_correo_bienvenida(email):
            print(f"Correo de bienvenida enviado a {email}")

    def mostrar_error(self, mensaje):
        self.error_label.configure(text=mensaje)