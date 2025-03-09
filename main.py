# DEPENDENCIAS EXTERNAS
import tkinter as tk
from tkinter import messagebox

# DEPENDENCIAS INTERNAS
from components import *

def handleMainQuit():
    answ = messagebox.askyesno(
        title="Estas a punto de salir", 
        message="Deseas salir y cerrar sesión?"
    )
    if answ:
        loginForm.userLogout()
        ventana.destroy()

#? VENTANA MAIN
ventana = tk.Tk()
ventana.title("Sistema Gestion - MeatFlow")
ventana.geometry("1280x720")
ventana.option_add("*Font", ("Inter", 10))

# Ocultamos inicialmente la ventana main
ventana.withdraw()

#? VENTANA LOGIN
loginForm = LoginForm(ventana)
loginForm.show()

#? COMPONENTES PRINCIPALES (VENTANA MAIN)
#- Formulario Productos
productForm = ProductForm(ventana)
productForm.show()

#- Formulario Inventario
stockForm = StockForm(ventana)
stockForm.show()

#- Formulario Proveedores
supplierForm = SupplierForm(ventana)
supplierForm.show()





reporteform=ReporteForm(ventana)
reporteform.show()
#? LOOP & CONFIG DE VENTANA
ventana.protocol("WM_DELETE_WINDOW", handleMainQuit)
ventana.resizable(False, False)
ventana.mainloop()