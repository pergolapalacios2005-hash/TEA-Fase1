"""
Vista para ingreso de síntomas - Sistema de Diagnóstico Médico
"""

import customtkinter as ctk
from utils.gpt_medical import GPTMedicalClient
import threading

class SintomasFrame(ctk.CTkFrame):
    """Frame para que el usuario ingrese sus síntomas."""
    
    def __init__(self, master, user_data=None, on_back_callback=None, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="#121212", **kwargs)
        
        self.user_data = user_data
        self.on_back_callback = on_back_callback
        self.gpt_client = GPTMedicalClient()
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- MENÚ LATERAL ---
        self.create_sidebar()
        
        # --- CONTENIDO PRINCIPAL ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            self.main_frame,
            text="Ingresa tus Síntomas",
            font=("Helvetica", 28, "bold"),
            text_color="white"
        )
        titulo.pack(pady=(0, 10))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            self.main_frame,
            text="Describe detalladamente los síntomas que estás experimentando",
            font=("Helvetica", 12),
            text_color="gray"
        )
        subtitulo.pack(pady=(0, 20))
        
        # Frame para información del usuario
        info_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        if user_data:
            info_text = f"Paciente Anónimo | "
            info_text += f"Edad: {user_data.get('edad', 'No especificada')} | "
            info_text += f"Género: {user_data.get('genero', 'No especificado')}"
            
            ctk.CTkLabel(
                info_frame,
                text=info_text,
                font=("Helvetica", 11),
                text_color="lightblue"
            ).pack(padx=15, pady=10)
        
        # Campo de entrada de síntomas
        ctk.CTkLabel(
            self.main_frame,
            text="Describe tus síntomas:",
            font=("Helvetica", 12, "bold"),
            text_color="white"
        ).pack(anchor="w", pady=(10, 5))
        
        self.sintomas_text = ctk.CTkTextbox(
            self.main_frame,
            height=200,
            fg_color="#1a1a1a",
            text_color="white",
            border_color="#0d47a1",
            border_width=2
        )
        self.sintomas_text.pack(fill="both", expand=True, pady=(0, 15))
        self.sintomas_text.insert("0.0", "Ejemplo: Tengo dolor de cabeza desde hace 3 días, fiebre de 38.5°C y nauseas...")
        
        # Frame para opciones adicionales (Edad, género, antecedentes)
        opciones_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        opciones_frame.pack(fill="x", pady=15)
        
        # Durabilidad del síntoma
        duracion_frame = ctk.CTkFrame(opciones_frame, fg_color="transparent")
        duracion_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            duracion_frame,
            text="¿Cuánto tiempo llevas con estos síntomas?",
            font=("Helvetica", 11),
            text_color="white"
        ).pack(side="left", padx=(0, 10))
        
        self.duracion_var = ctk.StringVar(value="menos de 24 horas")
        duracion_combo = ctk.CTkComboBox(
            duracion_frame,
            values=["menos de 24 horas", "1-3 días", "4-7 días", "1-2 semanas", "más de 2 semanas"],
            variable=self.duracion_var,
            fg_color="#1a1a1a",
            text_color="white",
            border_color="#0d47a1",
            border_width=1
        )
        duracion_combo.pack(side="left")
        
        # Severidad
        severidad_frame = ctk.CTkFrame(opciones_frame, fg_color="transparent")
        severidad_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            severidad_frame,
            text="Severidad del síntoma (1-10):",
            font=("Helvetica", 11),
            text_color="white"
        ).pack(side="left", padx=(0, 10))
        
        self.severidad_slider = ctk.CTkSlider(
            severidad_frame,
            from_=1,
            to=10,
            number_of_steps=9,
            fg_color="#0d47a1",
            button_color="#0d47a1"
        )
        self.severidad_slider.pack(side="left", fill="x", expand=True)
        
        self.severidad_label = ctk.CTkLabel(
            severidad_frame,
            text="5",
            font=("Helvetica", 11),
            text_color="lightblue",
            width=30
        )
        self.severidad_label.pack(side="left", padx=(10, 0))
        
        self.severidad_slider.configure(command=self.update_severidad)
        
        # Botones de acción
        botones_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        botones_frame.pack(fill="x", pady=(20, 0))
        
        self.btn_analizar = ctk.CTkButton(
            botones_frame,
            text="Analizar Síntomas con IA",
            font=("Helvetica", 12, "bold"),
            fg_color="#0d47a1",
            hover_color="#1565c0",
            height=40,
            command=self.analizar_sintomas
        )
        self.btn_analizar.pack(side="left", padx=(0, 10), fill="both", expand=True)
        
        self.btn_limpiar = ctk.CTkButton(
            botones_frame,
            text="Limpiar",
            font=("Helvetica", 12),
            fg_color="#424242",
            hover_color="#616161",
            height=40,
            command=self.limpiar_campos
        )
        self.btn_limpiar.pack(side="left", padx=(0, 10))
        
        btn_volver = ctk.CTkButton(
            botones_frame,
            text="Volver",
            font=("Helvetica", 12),
            fg_color="#c0392b",
            hover_color="#a93226",
            height=40,
            command=on_back_callback
        )
        btn_volver.pack(side="left")
        
        # Label de estado
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Helvetica", 11),
            text_color="yellow",
            wraplength=500
        )
        self.status_label.pack(pady=(10, 0))
    
    def create_sidebar(self):
        """Crea el menú lateral."""
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1a1a1a")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(4, weight=1)
        
        # Logo
        logo = ctk.CTkLabel(
            sidebar,
            text="SISTEMA\nMÉDICO",
            font=("Helvetica", 16, "bold"),
            text_color="#0d47a1"
        )
        logo.grid(row=0, column=0, padx=15, pady=(20, 30))
        
        # Menú
        menu_items = [
            ("Nuevo Diagnóstico", self.on_nuevo_diagnostico),
            ("Mi Historial", self.on_historial),
            ("Información Médica", self.on_info_medica),
        ]
        
        for i, (texto, comando) in enumerate(menu_items, start=1):
            btn = ctk.CTkButton(
                sidebar,
                text=texto,
                fg_color="transparent",
                hover_color="#262626",
                text_color="white",
                command=comando
            )
            btn.grid(row=i, column=0, padx=15, pady=8, sticky="ew")
        
        # Disclaimer
        disclaimer = ctk.CTkLabel(
            sidebar,
            text="⚠ AVISO:\nEste sistema proporciona diagnóstico preliminar únicamente.\nNO reemplaza consulta médica profesional.",
            font=("Helvetica", 9),
            text_color="orange",
            wraplength=160
        )
        disclaimer.grid(row=5, column=0, padx=10, pady=20, sticky="ew")
    
    def update_severidad(self, value):
        """Actualiza el label de severidad."""
        self.severidad_label.configure(text=f"{int(float(value))}")
    
    def limpiar_campos(self):
        """Limpia los campos de entrada."""
        self.sintomas_text.delete("0.0", "end")
        self.sintomas_text.insert("0.0", "Describe tus síntomas aquí...")
        self.duracion_var.set("menos de 24 horas")
        self.severidad_slider.set(5)
        self.status_label.configure(text="")
    
    def analizar_sintomas(self):
        """Realiza el análisis de síntomas con IA."""
        sintomas = self.sintomas_text.get("0.0", "end").strip()
        
        if not sintomas or sintomas == "Describe tus síntomas aquí...":
            self.status_label.configure(text="⚠ Por favor, describe tus síntomas", text_color="red")
            return
        
        # Validar entrada
        es_valido, mensaje = self.gpt_client.validar_entrada_medica(sintomas)
        if not es_valido:
            self.status_label.configure(text=f"✗ {mensaje}", text_color="red")
            return
        
        # Deshabilitar botón mientras se procesa
        self.btn_analizar.configure(state="disabled", text="Analizando...")
        self.status_label.configure(text="⏳ Procesando con IA Médica...", text_color="yellow")
        
        # Ejecutar análisis en thread para no bloquear UI
        threading.Thread(
            target=self._ejecutar_analisis,
            args=(sintomas,),
            daemon=True
        ).start()
    
    def _ejecutar_analisis(self, sintomas):
        """Ejecuta el análisis de síntomas en background."""
        try:
            edad = self.user_data.get('edad', '') if self.user_data else ''
            genero = self.user_data.get('genero', '') if self.user_data else ''
            antecedentes = self.user_data.get('antecedentes', '') if self.user_data else ''
            
            resultado = self.gpt_client.analizar_sintomas(
                sintomas, edad, genero, antecedentes
            )
            
            if resultado.get('exito'):
                self.status_label.configure(
                    text="✓ Análisis completado. Resultados disponibles.",
                    text_color="green"
                )
                # Aquí se podría guardar en BD y mostrar resultados en nueva vista
            else:
                self.status_label.configure(
                    text=f"✗ {resultado.get('error', 'Error en análisis')}",
                    text_color="red"
                )
        
        except Exception as e:
            self.status_label.configure(
                text=f"✗ Error: {str(e)[:100]}",
                text_color="red"
            )
        
        finally:
            self.btn_analizar.configure(state="normal", text="Analizar Síntomas con IA")
    
    def on_nuevo_diagnostico(self):
        """Callback para nuevo diagnóstico."""
        self.limpiar_campos()
        self.status_label.configure(text="Nuevo diagnóstico listo", text_color="green")
    
    def on_historial(self):
        """Callback para ver historial."""
        self.status_label.configure(text="Historial (próximamente)", text_color="yellow")
    
    def on_info_medica(self):
        """Callback para información médica."""
        self.status_label.configure(text="Info Médica (próximamente)", text_color="yellow")
