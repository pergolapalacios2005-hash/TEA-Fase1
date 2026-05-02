import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
from views.diagnostico import DiagnosticoFrame
from views.inicio import InicioFrame
from views.login import LoginFrame
from views.register import RegisterFrame
from Fase1.database import DatabaseManager
from services.email_service import enviar_correo_bienvenida
import time
import threading

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = DatabaseManager()
        self.title("Sistema Médico - Diagnóstico Previo")
        self.current_user = None

        # Configuraciones de la ventana
        self.overrideredirect(True)
        self.geometry("1200x760+100+100")
        self.is_maximized = False
        self.previous_geometry = self.geometry()

        self.configure(fg_color="#121212")

        self.create_title_bar()

        # Contenedor dinámico
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both")

        self.show_inicio_view()
        self.bind("<Escape>", lambda e: self.destroy())

    def create_title_bar(self):
        self.title_bar = ctk.CTkFrame(self, fg_color="#1f1f1f", height=36, corner_radius=0)
        self.title_bar.pack(side="top", fill="x")

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)

        self.title_label = ctk.CTkLabel(
            self.title_bar,
            text="Sistema Médico - Diagnóstico Previo",
            text_color="white",
            anchor="w",
            font=("Helvetica", 12, "bold")
        )
        self.title_label.pack(side="left", padx=12)
        self.title_label.bind("<Button-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.on_move)

        botones_frame = ctk.CTkFrame(self.title_bar, fg_color="transparent")
        botones_frame.pack(side="right", padx=8)

        self.min_button = ctk.CTkButton(
            botones_frame, text="-", width=32, height=28,
            fg_color="#1f1f1f", hover_color="#2f2f2f",
            corner_radius=0, command=self.minimize_window
        )
        self.min_button.pack(side="left", padx=(0, 4))

        self.max_button = ctk.CTkButton(
            botones_frame, text="◻", width=32, height=28,
            fg_color="#1f1f1f", hover_color="#2f2f2f",
            corner_radius=0, command=self.toggle_maximize
        )
        self.max_button.pack(side="left", padx=(0, 4))

        self.close_button = ctk.CTkButton(
            botones_frame, text="✕", width=32, height=28,
            fg_color="#1f1f1f", hover_color="#c0392b",
            corner_radius=0, command=self.destroy
        )
        self.close_button.pack(side="left")

    def start_move(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def on_move(self, event):
        x = self.winfo_pointerx() - self._drag_x
        y = self.winfo_pointery() - self._drag_y
        self.geometry(f"+{x}+{y}")

    do_move = on_move

    def minimize_window(self):
        self.update_idletasks()
        self.overrideredirect(False)
        self.state("iconic")
        self.after(50, lambda: self.bind("<Map>", self.on_restore_from_minimize))

    def on_restore_from_minimize(self, event):
        self.overrideredirect(True)

    def show_dashboard_view(self):
        self.clear_container()
        from views.diagnostico import DiagnosticoFrame
        self.diagnostico_view = DiagnosticoFrame(self.container, on_logout=self.show_inicio_view)
        self.diagnostico_view.pack(side="top", fill="both", expand=True)

    def show_inicio_view(self):
        self.clear_container()
        self.current_user = None
        self.inicio_view = InicioFrame(self.container, on_click_callback=self.show_login_view)
        self.inicio_view.pack(side="top", fill="both", expand=True)

    def show_login_view(self):
        self.clear_container()
        self.login_view = LoginFrame(self.container, on_register_click=self.show_register_view)
        self.login_view.pack(side="top", fill="both", expand=True)

    def show_register_view(self):
        self.clear_container()
        self.register_view = RegisterFrame(self.container, on_back_to_login=self.show_login_view)
        self.register_view.pack(side="top", fill="both", expand=True)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def transition(self, view_func):
        view_func()
        self.unbind("<Map>")

    def toggle_maximize(self):
        if self.is_maximized:
            self.geometry(self.previous_geometry)
            self.is_maximized = False
            self.max_button.configure(text="◻")
        else:
            self.previous_geometry = self.geometry()
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            self.geometry(f"{screen_width}x{screen_height}+0+0")
            self.is_maximized = True
            self.max_button.configure(text="❐")

    def transition(self, target_function):
        """Efecto Fade Out/In Universal sin threads sobre widgets Tk."""
        def fade_out(step=10):
            if step >= 0:
                self.attributes("-alpha", step / 10)
                self.after(20, lambda: fade_out(step - 1))
            else:
                for w in self.container.winfo_children():
                    w.destroy()
                target_function()
                fade_in(0)

        def fade_in(step):
            if step <= 10:
                self.attributes("-alpha", step / 10)
                self.after(20, lambda: fade_in(step + 1))

        fade_out()

    def show_inicio_view(self):
        for w in self.container.winfo_children():
            w.destroy()

        v = InicioFrame(
            self.container,
            on_click_callback=lambda: self.transition(self.show_login_view)
        )
        v.pack(expand=True, fill="both")

    def show_login_view(self):
        for w in self.container.winfo_children():
            w.destroy()

        v = LoginFrame(self.container, on_register_click=lambda: self.transition(self.show_register_view))
        v.pack(expand=True, fill="both")

    def show_register_view(self):
        for w in self.container.winfo_children():
            w.destroy()

        v = RegisterFrame(self.container, on_back_to_login=lambda: self.transition(self.show_login_view))
        v.pack(expand=True, fill="both")
    
    def show_dashboard_view(self):
        for w in self.container.winfo_children():
            w.destroy()

        v = DiagnosticoFrame(
            self.container,
            on_logout=lambda: self.transition(self.show_login_view)
        )
        v.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()