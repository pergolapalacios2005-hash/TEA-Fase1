"""
Vista de Panel Médico - Diagnóstico Previo
Reemplaza el dashboard anterior con funcionalidad médica
"""

import customtkinter as ctk
from views.sintomas import SintomasFrame

class DiagnosticoFrame(ctk.CTkFrame):
    """Frame principal del panel de diagnóstico médico."""
    
    def __init__(self, master, on_logout=None, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="#121212", **kwargs)
        
        self.on_logout = on_logout
        
        # Configuración de layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- MENÚ LATERAL ---
        self.create_sidebar()
        
        # --- CONTENIDO PRINCIPAL ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.show_welcome()
    
    def create_sidebar(self):
        """Crea el menú lateral del sistema médico."""
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1a1a1a")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(6, weight=1)
        
        # Logo del sistema
        logo_label = ctk.CTkLabel(
            sidebar,
            text="SISTEMA\nDE\nDIAGNÓSTICO",
            font=("Helvetica", 18, "bold"),
            text_color="#0d47a1"
        )
        logo_label.grid(row=0, column=0, padx=15, pady=(20, 30))
        
        # Botón: Nuevo Diagnóstico
        self.btn_nuevo_diag = ctk.CTkButton(
            sidebar,
            text="➕ Nuevo Diagnóstico",
            fg_color="#0d47a1",
            hover_color="#1565c0",
            text_color="white",
            font=("Helvetica", 12, "bold"),
            command=self.show_nuevo_diagnostico
        )
        self.btn_nuevo_diag.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        # Botón: Mi Historial
        self.btn_historial = ctk.CTkButton(
            sidebar,
            text="📋 Mi Historial",
            fg_color="transparent",
            hover_color="#262626",
            text_color="white",
            command=self.show_historial
        )
        self.btn_historial.grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        
        # Botón: Información Médica
        self.btn_info = ctk.CTkButton(
            sidebar,
            text="ℹ️ Información",
            fg_color="transparent",
            hover_color="#262626",
            text_color="white",
            command=self.show_informacion
        )
        self.btn_info.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        
        # Botón: Configuración
        self.btn_config = ctk.CTkButton(
            sidebar,
            text="⚙️ Configuración",
            fg_color="transparent",
            hover_color="#262626",
            text_color="white",
            command=self.show_configuracion
        )
        self.btn_config.grid(row=4, column=0, padx=15, pady=5, sticky="ew")
        
        # Botón: Ayuda
        self.btn_ayuda = ctk.CTkButton(
            sidebar,
            text="❓ Ayuda",
            fg_color="transparent",
            hover_color="#262626",
            text_color="white",
            command=self.show_ayuda
        )
        self.btn_ayuda.grid(row=5, column=0, padx=15, pady=5, sticky="ew")
        
        # Disclaimer médico
        disclaimer = ctk.CTkLabel(
            sidebar,
            text="⚠️ AVISO IMPORTANTE:\n\nEste sistema proporciona diagnóstico PRELIMINAR basado en IA.\n\nNO reemplaza consulta médica profesional.",
            font=("Helvetica", 9),
            text_color="orange",
            wraplength=180,
            justify="left"
        )
        disclaimer.grid(row=6, column=0, padx=12, pady=20, sticky="ews")
        
        # Botón: Cerrar Sesión
        self.btn_logout = ctk.CTkButton(
            sidebar,
            text="🚪 Cerrar Sesión",
            fg_color="#c0392b",
            hover_color="#a93226",
            text_color="white",
            command=self.on_logout if self.on_logout else self.do_logout
        )
        self.btn_logout.grid(row=7, column=0, padx=15, pady=(10, 20), sticky="ew")
    
    def show_welcome(self):
        """Muestra pantalla de bienvenida."""
        self.clear_main()
        
        # Título
        titulo = ctk.CTkLabel(
            self.main_content,
            text="Bienvenido al Sistema de Diagnóstico Médico",
            font=("Helvetica", 28, "bold"),
            text_color="white"
        )
        titulo.pack(pady=(20, 10))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            self.main_content,
            text="Análisis de Síntomas basado en Inteligencia Artificial",
            font=("Helvetica", 14),
            text_color="gray"
        )
        subtitulo.pack(pady=(0, 30))
        
        # Frame con información
        info_frame = ctk.CTkFrame(self.main_content, fg_color="#1a1a1a", corner_radius=15)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Texto de bienvenida
        bienvenida_text = """
        ¿Cómo funciona este sistema?
        
        1️⃣ Ingresa tus síntomas detalladamente
        2️⃣ El sistema IA analiza la información
        3️⃣ Recibes un diagnóstico preliminar
        4️⃣ Se guardan tus registros de salud
        
        ⚠️ IMPORTANTE:
        • Este sistema proporciona diagnóstico PRELIMINAR únicamente
        • Siempre consulta con un médico profesional
        • Ante emergencias, llama a emergencias local
        • No compartas información sensible innecesaria
        
        ✅ Comenzar: Haz clic en "Nuevo Diagnóstico"
        """
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=bienvenida_text,
            font=("Helvetica", 11),
            text_color="white",
            justify="left"
        )
        info_label.pack(padx=30, pady=30)
    
    def show_nuevo_diagnostico(self):
        """Muestra la vista de nuevo diagnóstico."""
        self.clear_main()
        
        self.sintomas_view = SintomasFrame(
            self.main_content,
            user_data=getattr(self.master.master, 'current_user', None),
            on_back_callback=self.show_welcome
        )
        self.sintomas_view.pack(expand=True, fill="both")
    
    def show_historial(self):
        """Muestra el historial de diagnósticos."""
        self.clear_main()
        
        titulo = ctk.CTkLabel(
            self.main_content,
            text="Mi Historial Médico",
            font=("Helvetica", 24, "bold"),
            text_color="white"
        )
        titulo.pack(pady=(0, 20))
        
        info = ctk.CTkLabel(
            self.main_content,
            text="Tu historial de diagnósticos previos aparecerá aquí.\n\nAún no hay diagnósticos registrados.",
            font=("Helvetica", 12),
            text_color="gray"
        )
        info.pack(pady=20)
    
    def show_informacion(self):
        """Muestra información médica."""
        self.clear_main()
        
        titulo = ctk.CTkLabel(
            self.main_content,
            text="Información Médica",
            font=("Helvetica", 24, "bold"),
            text_color="white"
        )
        titulo.pack(pady=(0, 20))
        
        info_frame = ctk.CTkFrame(self.main_content, fg_color="#1a1a1a", corner_radius=10)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        info_text = """
        ACERCA DEL SISTEMA:
        
        Este sistema utiliza inteligencia artificial (GPT) especializada en análisis 
        médico preliminar para ayudarte a entender tus síntomas.
        
        🔬 CARACTERÍSTICAS:
        • Análisis de síntomas con IA
        • Historial personalizado de diagnósticos
        • Recomendaciones basadas en patrones
        • Avisos de emergencia
        • Interfaz médica segura y privada
        
        📋 LÍMITES Y RESPONSABILIDADES:
        
        Este sistema NO:
        ✗ Reemplaza diagnóstico médico profesional
        ✗ Proporciona tratamientos
        ✗ Constituye consulta médica oficial
        ✗ Debe usarse en emergencias
        
        SIEMPRE CONSULTA CON:
        ✓ Médicos profesionales calificados
        ✓ Especialistas cuando sea necesario
        ✓ Servicios de emergencia (ante situaciones urgentes)
        
        🔐 PRIVACIDAD:
        Tus datos médicos se almacenan de forma segura y encriptada.
        """
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=("Helvetica", 10),
            text_color="white",
            justify="left"
        )
        info_label.pack(padx=20, pady=20)
    
    def show_configuracion(self):
        """Muestra configuración del sistema."""
        self.clear_main()
        
        titulo = ctk.CTkLabel(
            self.main_content,
            text="Configuración",
            font=("Helvetica", 24, "bold"),
            text_color="white"
        )
        titulo.pack(pady=(0, 20))
        
        mensaje = ctk.CTkLabel(
            self.main_content,
            text="Opciones de configuración disponibles próximamente.",
            font=("Helvetica", 12),
            text_color="gray"
        )
        mensaje.pack(pady=20)
    
    def show_ayuda(self):
        """Muestra pantalla de ayuda."""
        self.clear_main()
        
        titulo = ctk.CTkLabel(
            self.main_content,
            text="Ayuda",
            font=("Helvetica", 24, "bold"),
            text_color="white"
        )
        titulo.pack(pady=(0, 20))
        
        ayuda_frame = ctk.CTkFrame(self.main_content, fg_color="#1a1a1a", corner_radius=10)
        ayuda_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ayuda_text = """
        PREGUNTAS FRECUENTES:
        
        ¿Cómo usar el sistema?
        1. Ve a "Nuevo Diagnóstico"
        2. Describe tus síntomas en detalle
        3. Completa información adicional
        4. Espera el análisis de IA
        
        ¿Es seguro compartir mis síntomas?
        Sí, tus datos se almacenan encriptados y solo tú tienes acceso.
        
        ¿Qué hago si es emergencia?
        LLAMA AL NÚMERO DE EMERGENCIAS INMEDIATAMENTE.
        No uses este sistema en situaciones críticas.
        
        ¿Puedo ver mi historial?
        Sí, en "Mi Historial" verás todos tus diagnósticos previos.
        
        ¿Cuándo debo consultar a un médico?
        • Síntomas nuevos o inusuales
        • Síntomas que persisten
        • Antes de cualquier tratamiento
        • Para confirmar diagnósticos
        
        CONTACTO Y SOPORTE:
        Para soporte técnico: support@sistemamedicoia.com
        """
        
        ayuda_label = ctk.CTkLabel(
            ayuda_frame,
            text=ayuda_text,
            font=("Helvetica", 10),
            text_color="white",
            justify="left"
        )
        ayuda_label.pack(padx=20, pady=20)
    
    def clear_main(self):
        """Limpia el contenido principal."""
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def do_logout(self):
        """Ejecuta logout."""
        if self.on_logout:
            self.on_logout()
