# DEPENDENCIAS EXTERNAS
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# DEPENDENCIAS INTERNAS
from compra import Compra
from components import *

class MainApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.user = {
            "user": None,
            "name": tk.StringVar()
        }

        #? INTERFAZ
        self.ventana.title("Sistema de Gestión Financiera - MeatFlow")
        self.ventana.geometry("1280x700")
        self.ventana.option_add("*Font", ("Inter", 10))
        self.ventana.iconbitmap("assets/favicon.ico")
        self.ventana.withdraw()

        #VENTANAS
        loginForm = LoginForm(self)
        changePasswForm = ChangePasswForm(self)
        stockForm = StockForm(self)
        buyForm = BuyForm(self)
        clientForm = Client(self)
        reportForm = ReporteForm(self)
        loginForm.hide()
        loginForm.show()
        # clientForm.show()
       

        #? MENÚ DE NAVEGACIÓN
        nav_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=nav_menu)

        #? MENU
        file_menu = tk.Menu(nav_menu, tearoff=0)
        file_menu.add_command(label="Cerrar Sesión", command=self.handle_main_quit)
        file_menu.add_command(label="Configuración")
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.handle_main_quit)

        user_menu = tk.Menu(nav_menu, tearoff=0)
        user_menu.add_command(label="Perfil")
        user_menu.add_command(label="Cambiar Contraseña", command=changePasswForm.show)

        nav_menu.add_cascade(label="Archivo", menu=file_menu)
        nav_menu.add_cascade(label="Usuario", menu=user_menu)

        #? CUERPO DE LA INTERFAZ
        # - LADO MENU
        self.menu = tk.Frame(self.ventana, width=300, bd=1, relief="ridge")
        # Logo
        self.logo = Image.open("assets/logo.png")
        self.logo_tk = ImageTk.PhotoImage(self.logo)
        labelImage = tk.Label(self.menu, image=self.logo_tk)
        labelImage.pack(pady=(50, 20))

        self.botones = tk.Frame(self.menu)

        gap=10
        ttk.Button(self.botones, command=buyForm.show, width=25, text="Registrar compra").pack(pady=gap)
        ttk.Button(self.botones, command=clientForm.show, width=25, text="Registrar venta").pack(pady=gap)
        ttk.Button(self.botones, command=stockForm.show, width=25, text="Ver inventario").pack(pady=gap)
        ttk.Button(self.botones, command=reportForm.show, width=25, text="Generar reporte").pack(pady=gap)

        self.botones.pack()

        ttk.Button(self.menu, width=25, text="Cerrar Sesión", command=self.handle_main_quit
        ).pack(side="bottom", pady=(0, 50))

        self.menu.pack_propagate(False)
        self.menu.pack(side="left", fill=tk.Y)


        # - LADO PANTALLA
        self.display = tk.Frame(self.ventana)
        self.display.pack_propagate(False)
        self.display.pack(side="left", fill=tk.BOTH, expand=True)

        tk.Label(self.display, text="Pruebaaa", font=("Inter Bold", 30)
        ).pack(pady=(40, 0))

        self.ventana.protocol("WM_DELETE_WINDOW", self.handle_main_quit)

        # Barra de Estado
        stsbar = tk.Frame(self.display, bd=1, relief=tk.SUNKEN)
        ttk.Label(stsbar, text="Bienvenido, ").grid(column=0, row=0)
        ttk.Label(stsbar, textvariable=self.user["name"]).grid(column=1, row=0)
        stsbar.pack(side=tk.BOTTOM, fill=tk.X)

    def handle_main_quit(self):
        answ = messagebox.askyesno(
            title="Estás a punto de salir...", 
            message="Deseas cerrar sesion y salir del sistema?"
        )
        if answ:
            self.ventana.destroy()

    def render(self):
        self.ventana.resizable(False, False)
        self.ventana.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.render()