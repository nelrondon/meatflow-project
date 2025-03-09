import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from cliente import Cliente
from datetime import datetime

from auth import AuthUser, Auth
from handledb import DB

COLOR1 = "#225270"
COLOR1_SOFT = "#C4DDED"


class Widget:
    @staticmethod
    def MainLabel(parent, text):
        ttk.Label(parent, text=text,foreground=COLOR1, font=("Inter ExtraBold", 24)
        ).pack(padx=90, pady=(30, 0))

    @staticmethod
    def SecLabel(parent, text):
        ttk.Label(parent, text=text, font=("Inter", 10)
        ).pack()

    @staticmethod
    def Caption(parent, text, side="top"):
        ttk.Label(parent, text=text, foreground=COLOR1, font=("Inter SemiBold", 10)
        ).pack(side=side)
    
    @staticmethod
    def CaptionGrid(parent, text, arr, cspan=1, rspan=1):
        ttk.Label(parent, text=text, foreground=COLOR1, font=("Inter SemiBold", 10)
        ).grid(column=arr[0], row=arr[1], columnspan=cspan, rowspan=rspan, sticky="w")

    @staticmethod
    def Input(parent, text, var, fs=10, js="left", width=None):
        Widget.Caption(parent, text)
        ttk.Entry(parent, justify=js, textvariable=var, width=width, font=("Inter", fs)
        ).pack()

    @staticmethod
    def InputGrid(parent, text, var, arr, cspan=1, rspan=1, width=None, fs=10, js="left", state="normal"):
        fr = ttk.Frame(parent)
        Widget.CaptionGrid(fr, text, arr, cspan, rspan)
        et = None
        if width:
            et = ttk.Entry(fr, state=state, justify=js, textvariable=var, font=("Inter", fs), width=width)
        else:
            et = ttk.Entry(fr, state=state, justify=js, textvariable=var, font=("Inter", fs))

        et.grid(column=arr[0], row=(arr[1]+1), columnspan=cspan, rowspan=rspan)
        fr.grid(column=arr[0], row=arr[1], padx=8)

class MsgBox:
    def PopUp(self, mode, title, msg):
        if mode=="info":
            messagebox.showinfo( 
                parent=self.toplevel,
                title=title, 
                message=msg
            )
        elif mode=="error":
            messagebox.showerror(
                parent=self.toplevel,
                title=title, 
                message=msg
            )
        elif mode=="warning":
            messagebox.showwarning(
                parent=self.toplevel,
                title=title, 
                message=msg
            )

class Form (MsgBox):
    def __init__(self, app, title):
        self.app = app
        self.main_window = self.app.ventana
        self.toplevel = tk.Toplevel(self.main_window)
        self.toplevel.iconbitmap("assets/favicon.ico")
        self.toplevel.attributes("-topmost", True)
        self.toplevel.title(f"{title} - MeatFlow")
        Widget.MainLabel(self.toplevel, title)
        self.toplevel.withdraw()  # Inicialmente oculto

        self.buttonStyle = ttk.Style()
        self.buttonStyle.configure("TButton", relief="groove", font=("Inter SemiBold", 10), foreground=COLOR1)

        self.toplevel.resizable(False, False)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.hide)
        # self.toplevel.protocol("WM_DELETE_WINDOW", self.handleQuit)

    def show(self):
        self.toplevel.deiconify()  # Mostrar el formulario

    def hide(self):
        self.toplevel.withdraw()  # Mostrar el formulario

    def handleQuit(self):
        self.toplevel.destroy()
        self.main_window.destroy()

class SecForm (MsgBox):
    def __init__(self, form, title):
        self.form = form
        self.toplevel = tk.Toplevel(self.form.main_window)
        self.toplevel.title(f"{title} - MeatFlow")
        self.toplevel.attributes("-topmost", True)
        Widget.MainLabel(self.toplevel, title)
        self.toplevel.withdraw()  # Inicialmente oculto

        self.buttonStyle = ttk.Style()
        self.buttonStyle.configure("TButton", relief="groove", font=("Inter SemiBold", 10), foreground=COLOR1)

        self.toplevel.resizable(False, False)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.hide)

    def show(self):
        self.toplevel.deiconify()  # Mostrar el formulario

    def hide(self):
        self.toplevel.withdraw()  # Mostrar el formulario

class ChangePasswForm(Form):
    def __init__(self, app):
        super().__init__(app, "Cambiar contraseña")
        self.newPassw = tk.StringVar()

        Widget.SecLabel(self.toplevel, "Ingresa tu nueva contraseña")

        fr = tk.Frame(self.toplevel); fr.pack(pady=(10, 20))

        Widget.Input(fr, "Nueva contraseña:", self.newPassw, js="center")
        
        ttk.Button(fr, text="Cambiar contraseña", width=20, command=self.changePassw).pack(pady=20)

    def changePassw(self):
            if Auth.changePassw(self.app.user["user"], self.newPassw.get()):
                self.hide()

class LoginForm (Form):
    def __init__(self, main_window):
        super().__init__(main_window, "Inicio de Sesión")
        self.user = None

        # Variables de los inputs
        self.userVar = tk.StringVar()
        self.passVar = tk.StringVar()

        # Titulo
        Widget.SecLabel(self.toplevel, "Ingresa con las credenciales provistas")

        # Frame (Usuario)
        fUser = tk.Frame(self.toplevel)
        fUser.pack(pady=10)

        # Frame (Contraseña)
        fPassw = tk.Frame(self.toplevel)
        fPassw.pack(pady=10)

        # Frame (Botones)
        fBtns = tk.Frame(self.toplevel)
        fBtns.pack(pady=(30, 30))

        Widget.Caption(fUser, "Usuario:")
        ttk.Entry(fUser, textvariable=self.userVar, justify="center", font=("Inter", 11)
        ).pack()
        
        Widget.Caption(fPassw, "Contraseña:")
        ttk.Entry(fPassw, textvariable=self.passVar, justify="center", show="*", font=("Inter", 11)
        ).pack()

        # Button (Limpiar)
        ttk.Button(fBtns, text="Limpiar", width=10, command=self.handleClean).grid(column=1, row=0, padx=5)
        # Button (Ingresar)
        ttk.Button(fBtns, text="Ingresar...", width=15, command=self.handleLoginSubmit).grid(column=0, row=0, padx=5)
        self.toplevel.bind("<Return>", self.handleLoginSubmit)

        self.toplevel.protocol("WM_DELETE_WINDOW", self.handleQuit)
        self.show()
        

    def userLogout(self):
        self.user.logout()

    def handleLoginSubmit(self, event=None):
        if self.userVar.get() and self.passVar.get():
            self.user = AuthUser(self.userVar.get())
            try:
                result = self.user.login(self.passVar.get())
                if result:
                    self.app.user["user"] = result["user"]
                    self.app.user["name"].set(result["name"])
                    self.hide()
                    self.main_window.deiconify()
            except Exception as e:
                messagebox.showwarning(
                    parent=self.toplevel,
                    title="Error al iniciar sesión", 
                    message=str(e)
                )

    def handleClean(self):
        self.userVar.set("")
        self.passVar.set("")

class ProductForm (SecForm):
    def __init__(self, main_window):
        super().__init__(main_window, "Productos")
        Widget.SecLabel(self.toplevel, "Añade un nuevo producto")

        self.nameVar = tk.StringVar()
        self.catVar = tk.StringVar()
        self.pr_buyVar = tk.DoubleVar()
        self.pr_sellVar = tk.DoubleVar()
        self.expVar = tk.StringVar()
        self.stockVar = tk.IntVar()
        self.typeVar = tk.StringVar()

        fr1 = tk.Frame(self.toplevel); fr1.pack(pady=5, padx=60)
        fr2 = tk.Frame(self.toplevel); fr2.pack(pady=5)
        fr3 = tk.Frame(self.toplevel); fr3.pack(pady=5)
        fr4 = tk.Frame(self.toplevel); fr4.pack(pady=5)
        fr5 = tk.Frame(self.toplevel); fr5.pack(pady=30)

        Widget.InputGrid(fr1, "Nombre producto:", self.nameVar, [0, 0], width=40)

        # Option Menu (Categoria)
        estilo = ttk.Style()
        estilo.configure("Basic.TMenubutton",
                width=15,
                background="white",
                font=("Inter", 10))

        o_cat = ["Seleccionar", "Carniceria", "Comida", "Producto"]
        fr = tk.Frame(fr2)
        Widget.CaptionGrid(fr, "Categoria:", [0, 0])
        self.catVar.set(o_cat[0])
        ttk.OptionMenu(fr, self.catVar, *o_cat, style="Basic.TMenubutton").grid(column=0, row=1)
        fr.grid(column=0, row=0)

        Widget.InputGrid(fr2, "Tipo:", self.typeVar, [1, 0], width=15)

        Widget.InputGrid(fr3, "Precio Compra:", self.pr_buyVar, [0, 0], width=16)
        Widget.InputGrid(fr3, "Precio Venta:", self.pr_sellVar, [1, 0], width=16)
        Widget.InputGrid(fr4, "Stock:", self.stockVar, [0, 0], width=8)
        Widget.InputGrid(fr4, "Fecha de Vencimiento:", self.expVar, [1, 0], width=20)

        ttk.Button(fr5,text="Añadir",width=20, command=self.addProduct
        ).grid(column=0, row=0)

    def addProduct(self):
        if self.nameVar.get()!="" and self.catVar.get()!="" and self.expVar.get()!="" and self.typeVar.get()!="" and self.pr_buyVar.get()!=0 and self.pr_sellVar.get()!=0 and self.stockVar.get()!=0:
            data = {
                "name": self.nameVar.get(),
                "category": self.catVar.get(),
                "price_buy": self.pr_buyVar.get(),
                "price_sell": self.pr_sellVar.get(),
                "exp_date": self.expVar.get(),
                "stock": self.stockVar.get(),
                "type": self.typeVar.get(),
            }
            try:
                self.form.addProduct(data)
                self.PopUp("info", 
                    parent=self.toplevel,
                    title="Producto agregado!", 
                    message="Se agrego correctamente!"
                    )
                self.setDefault()
            except Exception as e:
                messagebox.showwarning(
                    parent=self.toplevel,
                    title="Error en producto!", 
                    message="No se completo el registro!"
                )
        else:
            messagebox.showwarning(
                parent=self.toplevel,
                title="Campos requeridos", 
                message="Todos los campos son requeridos"
            )

    def setDefault(self):
        self.nameVar.set("")
        self.catVar.set("")
        self.pr_buyVar.set(0)
        self.pr_sellVar.set(0)
        self.expVar.set("")
        self.stockVar.set(0)
        self.typeVar.set("")

class StockForm (Form):
    def __init__(self, main_window):
        super().__init__(main_window, "Inventario")
        Widget.SecLabel(self.toplevel, "Visualiza el inventario actual")

        self.products = self.loadFromDB()

        def handleFilter():
            resutl = DB.searchBy("productos", "name", self.namefl.get())
            self.setData(resutl)

        #? FILTRO DE BUSQUEDA
        self.namefl = tk.StringVar()

        tk.Label(self.toplevel, text="Filtros").pack()
        ftfr = tk.Frame(self.toplevel)
        tk.Label(ftfr, text="Nombre: ").pack(side="left")
        ttk.Entry(ftfr, textvariable=self.namefl).pack(side="left", padx=10)
        ttk.Button(ftfr, text="Filtrar", command=handleFilter).pack(side="left")
        ftfr.pack(pady=(0, 20))

        #? COMPONENTE DE LISTA INVENTARIO
        w=800
        container = tk.Frame(self.toplevel)
        container.pack(pady=(0, 50))

        canvas = tk.Canvas(container, width=w, height=400)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrolly = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.config(yscrollcommand=scrolly.set)

        self.hd = tk.Frame(canvas)
        canvas.create_window((w/2,0), window=self.hd, anchor="n")

        def update_scroll(event):
            canvas.config(scrollregion=canvas.bbox("all"))

        self.hd.bind("<Configure>", update_scroll)

        self.setData(self.products)

    def loadFromDB(self):
        return DB.get("productos")
    
    def setData(self, data=None):
        self.clearCanvas()
        if data == []:
            messagebox.showerror("No existen coincidencias", "No hay productos en la base de datos, que cumplan con la petición")
            data = self.loadFromDB()
            
        gap = 5
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Nombre:").grid(column=0, row=0, padx=gap, sticky="w")
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Categoria:").grid(column=1, row=0, padx=gap)
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Precio Compra:").grid(column=2, row=0, padx=gap)
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Precio Venta:").grid(column=3, row=0, padx=gap)
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Vencimiento:").grid(column=4, row=0, padx=gap)
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Stock:").grid(column=5, row=0, padx=gap)
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Tipo:").grid(column=6, row=0, padx=gap)

        for i, prod in enumerate(data):
            bg = COLOR1_SOFT if i%2==0 else None
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["name"]).grid(column=0, row=(i+1), padx=gap, sticky="w")
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["category"]).grid(column=1, row=(i+1), padx=gap)
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["price_buy"]).grid(column=2, row=(i+1), padx=gap)
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["price_sell"]).grid(column=3, row=(i+1), padx=gap)
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["exp_date"]).grid(column=4, row=(i+1), padx=gap)
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["stock"]).grid(column=5, row=(i+1), padx=gap)
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["type"]).grid(column=6, row=(i+1), padx=gap)
    
    def clearCanvas(self):
        for wg in self.hd.winfo_children():
            wg.destroy()

class BuyForm (Form):
    def __init__(self, form):
        super().__init__(form, "Compra")
        Widget.SecLabel(self.toplevel, "Registra una nueva compra")

        self.productForm = ProductForm(self)
        self.products = []

        fr0 = tk.Frame(self.toplevel); fr0.pack(pady=5)
        fr1 = tk.Frame(self.toplevel); fr1.pack(pady=5, padx=80)
        fr2 = tk.Frame(fr1); fr2.grid(column=0, row=0, padx=10)
        fr3 = tk.Frame(fr1); fr3.grid(column=1, row=0, padx=10)
        footer = tk.Frame(self.toplevel); footer.pack(pady=(20, 40))

        self.nameVar = tk.StringVar()
        self.timeDVar = tk.IntVar()
        self.prodSearch = tk.StringVar()
        self.costoVar = tk.IntVar()

        Widget.InputGrid(fr0, "Nombre proveedor:", self.nameVar, [0,0])
        
        Widget.InputGrid(fr0, "Tiempo de entrega: (min)", self.timeDVar, [1,0], width=8)

        Widget.CaptionGrid(fr2, "Productos Comprados:", [0, 2])
        self.prodNameList = tk.Listbox(fr2, height=7)

        ttk.Button(fr3, text="Agregar producto", command=self.showProductForm).pack()
        ttk.Button(fr3, text="Eliminar selección", command=self.deleteProduct).pack(pady=(0, 20))

        Widget.Caption(fr3, "Costo Total")
        ttk.Entry(fr3, state="readonly", textvariable=self.costoVar, font=("Inter", 10), width=10).pack()

        ttk.Button(footer, text="Registrar compra", command=self.addBuy, width=20).pack()

        self.prodNameList.grid(column=0, row=3)

    def addProduct(self, data):
        self.products.append(data)
        self.prodNameList.insert(tk.END, data["name"])
        self.updateCostoTotal()
    
    def deleteProduct(self):
        indice = self.prodNameList.curselection()[0]
        del self.products[indice]
        self.prodNameList.delete(indice)
        self.updateCostoTotal()

    def updateCostoTotal(self):
        costo = 0
        for _ in self.products:
            costo += (_["price_buy"] * _["stock"])
        self.costoVar.set(costo)

    def addBuy(self):
        # Datos proveedor
        nameSupp = self.nameVar.get()
        timeDel = self.timeDVar.get()
        
        if nameSupp != "" and timeDel != 0 and len(self.products):
            self.PopUp(
                "info",
                "Compra realizada",
                "Se añadio una nueva compra (NOTA NO SE HA AGREGADO A LA BASE DE DATOS)"
            )
        else:
            self.PopUp(
                "warning",
                "Campos requeridos",
                "Añade suficientes datos para procesar la compra"
            )

            

    def showProductForm(self):
        self.productForm.show()

class Client(Form):
    def __init__(self, main_window):
        super().__init__(main_window, "Registro Cliente")
        self.name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.id = tk.StringVar()
        self.feedback = tk.StringVar()

        self.sale = Sale(self)

        self.sale.show()
        
        def validar_cliente(bol):
            result = DB.getOneBy("clientes", "id", self.id.get())
            if result != None and self.id.get() == result["id"]:
                name, last_name = result["name"].split(" ",1)
                self.name.set(name)
                self.last_name.set(last_name)
                self.feedback.set("")
                return False
            else:
                if bol:
                    self.PopUp("info", "Cliente", "Cliente no registrado")
                return True
        
        def registrar():
            if validar_cliente(False):
                if self.id.get() != "" and self.last_name.get() != "" and self.name.get() != "":
                        data = {
                            "id": self.id.get(),
                            "name": f"{self.name.get()} {self.last_name.get()}",
                            "frec_visit": 1,
                            "feedback": self.feedback.get()
                        }
                        cliente = Cliente(data)
                        cliente.register()
                else: 
                    self.PopUp("info", "Cliente", "Debe llenar todos los campos")
            else:
                self.PopUp("info", "Cliente", "Cliente ya registrado")
                
        def showSaleForm():
            if self.id.get() != "" and self.last_name.get() != "" and self.name.get() != "":
                if not validar_cliente(True):
                    self.sale.show()
            else:
                if self.id.get() != "":
                    self.PopUp("info", "Cliente", "Consulte el cliente")
                else:
                    self.PopUp("info", "Cliente", "Ingrese la V- del cliente")
                
        fr1 = tk.Frame(self.toplevel); fr1.pack(pady=10, padx=30)
        fr2 = tk.Frame(self.toplevel); fr2.pack(pady=5)
        fr3 = tk.Frame(self.toplevel); fr3.pack(pady=5)
        fr4 = tk.Frame(self.toplevel); fr4.pack(pady=(20, 5))
        fr5 = tk.Frame(self.toplevel); fr5.pack(pady=(0, 30))
        
        Widget.Caption(fr1, "Cedula Del Cliente: ", "left")
        ttk.Entry(fr1, textvariable=self.id).pack(side="left", padx=6)
        
        ttk.Button(fr1, text="Ver Cliente", command = lambda:validar_cliente(True)).pack(side="left")

        
        Widget.InputGrid(fr2, "Nombre del cliente:", self.name, [0, 0], width=16)
        Widget.InputGrid(fr2, "Apellido del cliente:", self.last_name, [1, 0], width=16)
        
        Widget.CaptionGrid(fr3, "Comentario:", [0, 0])
        entryfeedback = ttk.Entry(fr3, textvariable=self.feedback, font=("Inter", 10),width=30)
        entryfeedback.grid(column=0, row=3, ipady = 10)
        ttk.Button(fr4, text="Añadir Cliente", width=20,command=registrar).grid(column=0, row=0)
        ttk.Button(fr5, text="Ir al carrito", width=20,command=showSaleForm).grid(column=0, row=0)

class Sale(SecForm):
    def __init__(self, main_window):
        super().__init__(main_window, "Orden de Venta")
        self.date = tk.StringVar()
        self.date.set(str(datetime.now().date()))

        self.pay = tk.StringVar()
        self.attention = tk.IntVar()

        # Lista de productos comprados
        self.products_list = []
        self.id = self.form.id
        self.name = self.form.name
        self.last_name = self.form.last_name
        
        def registrar_venta():
            if self.pay.get() != "" and self.products_list != []:
                
                self.PopUp("info", "Ventas", "Venta registrada")
            else:
                self.PopUp("error", "Error", "Debe llenar todos los campos")
        
        fr1 = tk.Frame(self.toplevel); fr1.pack(pady=10)
        fr2 = tk.Frame(self.toplevel); fr2.pack(pady=5, padx=40)
        
        
        # Mostrar el cliente
        tk.Label(fr1, text="Cliente:").pack(side="left")
        tk.Label(fr1, textvariable=self.name).pack(side="left", padx=5)
        tk.Label(fr1, textvariable=self.last_name).pack(side="left", padx=5)

        # Campos de entrada
        Widget.InputGrid(fr2, "Fecha:", self.date, [0, 0], width=16, state="readonly", js="center")
        Widget.InputGrid(fr2, "Método de pago:", self.pay, [1, 0], width=16)
        Widget.InputGrid(fr2, "Valoracion de atencion:", self.attention, [2, 0], width=16)

        # Sección de productos
        fr_products = tk.Frame(self.toplevel)
        fr_products.pack(pady=5)

        tk.Label(fr_products, text="Producto:").pack(side="left")
        self.product_entry = ttk.Entry(fr_products, font=("Inter", 10))
        self.product_entry.pack(side="left", padx=5)

        tk.Label(fr_products, text="Cantidad:").pack(side="left")
        self.quantity_entry = ttk.Entry(fr_products, font=("Inter", 10), width=5)
        self.quantity_entry.pack(side="left", padx=5)

        ttk.Button(fr_products, text="Agregar", command=self.add_product).pack(side="left")

        # Caja de texto para mostrar productos agregados
        self.products_display = tk.Text(self.toplevel, height=10, width=40, state="disabled")
        self.products_display.pack(pady=10)
        fr_facturar = tk.Frame(self.toplevel); fr_facturar.pack(pady=25)
        ttk.Button(fr_facturar,text="Facturar",width=20, command=registrar_venta
        ).grid(column=0, row=0)
        
    def add_product(self):
        """Agrega un producto con cantidad a la lista y lo muestra en la caja de texto."""
        product = self.product_entry.get().strip()
        quantity = self.quantity_entry.get().strip()

        if product and quantity.isdigit() and int(quantity) > 0:
            product_entry = f"{product} x{quantity}"  # Formato "Jamón x2"
            self.products_list.append(product_entry)

            # Mostrar en la caja de texto
            self.products_display.config(state="normal")
            self.products_display.insert(tk.END, f"{product_entry}\n")
            self.products_display.config(state="disabled")

            # Limpiar los campos de entrada
            self.product_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
        else:
            print("⚠️ Error: Ingresa un producto y una cantidad válida.") 
         