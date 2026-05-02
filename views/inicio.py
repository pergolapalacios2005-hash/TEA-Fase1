import customtkinter as ctk

class InicioFrame(ctk.CTkFrame):
    """Pantalla de inicio - Sistema de Diagnóstico Médico."""
    
    def __init__(self, master, on_click_callback, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        
        # Botón que cubre el 100% de la pantalla
        self.btn_fondo = ctk.CTkButton(
            self,
            text="",
            fg_color="#0d1b2a",
            hover_color="#0d1b2a",
            corner_radius=0,
            command=on_click_callback
        )
        self.btn_fondo.pack(expand=True, fill="both")

        # Logotipo/Título principal
        self.lbl_logo = ctk.CTkLabel(
            self, 
            text="🏥\n\nSISTEMA MÉDICO\nDIAGNÓSTICO PREVIO\n\nBasado en IA", 
            font=("Helvetica", 44, "bold"),
            text_color="white",
            bg_color="#0d1b2a"
        )
        self.lbl_logo.place(relx=0.5, rely=0.4, anchor="center")

        # Subtítulo
        self.lbl_subtitulo = ctk.CTkLabel(
            self, 
            text="Análisis inteligente de síntomas para diagnóstico preliminar", 
            font=("Helvetica", 14),
            text_color="lightblue",
            bg_color="#0d1b2a"
        )
        self.lbl_subtitulo.place(relx=0.5, rely=0.6, anchor="center")

        # CTA (Call To Action)
        self.lbl_click = ctk.CTkLabel(
            self, 
            text="👆 TOCA AQUÍ PARA COMENZAR", 
            font=("Helvetica", 16, "bold"),
            text_color="white",
            bg_color="#0d1b2a"
        )
        self.lbl_click.place(relx=0.5, rely=0.8, anchor="center")

        # Disclaimer médico
        self.lbl_disclaimer = ctk.CTkLabel(
            self, 
            text="⚠️ Este sistema proporciona diagnóstico PRELIMINAR.\nNo reemplaza consulta médica profesional.", 
            font=("Helvetica", 10),
            text_color="orange",
            bg_color="#0d1b2a"
        )
        self.lbl_disclaimer.place(relx=0.5, rely=0.92, anchor="center")

        # Vincular eventos de clic
        self.lbl_logo.bind("<Button-1>", lambda e: on_click_callback())
        self.lbl_click.bind("<Button-1>", lambda e: on_click_callback())