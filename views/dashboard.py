import customtkinter as ctk

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, on_logout, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="#121212", **kwargs)
        
        # Configuración de layout: Menú lateral (0) y Contenido (1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- MENU LATERAL ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1) # Espaciador para empujar el logout abajo

        self.logo_label = ctk.CTkLabel(self.sidebar, text="SISTEMA\nMULTIMODAL", font=("Helvetica", 20, "bold"), text_color="#1a73e8")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_ia = ctk.CTkButton(self.sidebar, text="Cámara IA", fg_color="transparent", hover_color="#2b2b2b")
        self.btn_ia.grid(row=1, column=0, padx=20, pady=10)

        self.btn_chat = ctk.CTkButton(self.sidebar, text="Asistente Chat", fg_color="transparent", hover_color="#2b2b2b")
        self.btn_chat.grid(row=2, column=0, padx=20, pady=10)

        self.btn_logout = ctk.CTkButton(self.sidebar, text="Cerrar Sesión", fg_color="#c0392b", hover_color="#a93226", command=on_logout)
        self.btn_logout.grid(row=5, column=0, padx=20, pady=20)

        # --- CONTENIDO PRINCIPAL ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.welcome_label = ctk.CTkLabel(self.main_content, text="Bienvenido al Panel Principal", font=("Helvetica", 24, "bold"))
        self.welcome_label.pack(pady=20)
        
        self.info_label = ctk.CTkLabel(self.main_content, text="Selecciona una opción del menú para comenzar.", text_color="gray")
        self.info_label.pack()