import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from venta import Venta
from auth import AuthUser
from handledb import DB
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from reporte import Reporte
from inventario import Inventario
COLOR1 = "#225270"
COLOR1_SOFT = "#C4DDED"

class Widget:
    @staticmethod
    def MainLabel(parent, text):
        tk.Label(parent, text=text,foreground=COLOR1, font=("Inter ExtraBold", 24)
        ).pack(padx=90, pady=(30, 0))

    @staticmethod
    def SecLabel(parent, text):
        tk.Label(parent, text=text, font=("Inter", 10)
        ).pack()

    @staticmethod
    def Caption(parent, text):
        tk.Label(parent, text=text, foreground=COLOR1, font=("Inter SemiBold", 10)
        ).pack()
    
    @staticmethod
    def CaptionGrid(parent, text, arr, cspan=1, rspan=1):
        tk.Label(parent, text=text, foreground=COLOR1, font=("Inter SemiBold", 10)
        ).grid(column=arr[0], row=arr[1], columnspan=cspan, rowspan=rspan, sticky="w")

    @staticmethod
    def Input(parent, text, var, fs=11):
        Widget.Caption(parent, text)
        tk.Entry(parent, textvariable=var, font=("Inter", fs)
        ).pack()

    @staticmethod
    def InputGrid(parent, text, var, arr, cspan=1, rspan=1, width=None, fs=11):
        fr = tk.Frame(parent)
        Widget.CaptionGrid(fr, text, arr, cspan, rspan)
        et = None
        if width:
            et = tk.Entry(fr, textvariable=var, font=("Inter", fs), width=width)
        else:
            et = tk.Entry(fr, textvariable=var, font=("Inter", fs))

        et.grid(column=arr[0], row=(arr[1]+1), columnspan=cspan, rowspan=rspan)
        fr.grid(column=arr[0], row=arr[1], padx=8)

class Form:
    def __init__(self, main_window, title):
        self.main_window = main_window
        self.toplevel = tk.Toplevel(main_window)
        self.toplevel.title(f"{title} - MeatFlow")
        Widget.MainLabel(self.toplevel, title)
        self.toplevel.withdraw()  # Inicialmente oculto
        self.toplevel.resizable(False, False)


        self.toplevel.protocol("WM_DELETE_WINDOW", self.handleQuit)

    def show(self):
        self.toplevel.deiconify()  # Mostrar el formulario

    def hide(self):
        self.toplevel.destroy()  # Mostrar el formulario

    #- NOTA: ESTE METODO ES SOLO PARA EL <<LOGINFORM>>, CAMBIARLO ANTES DE PRODUCC
    def handleQuit(self):
        self.toplevel.destroy()
        self.main_window.destroy()

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
        tk.Entry(fUser, textvariable=self.userVar, justify="center", font=("Inter", 11)
        ).pack()
        
        Widget.Caption(fPassw, "Contraseña:")
        tk.Entry(fPassw, textvariable=self.passVar, justify="center", show="*", font=("Inter", 11)
        ).pack()

        # Button (Limpiar)
        tk.Button(fBtns, foreground=COLOR1, text="Limpiar", relief="groove", width=10, font=("Inter", 11), command=self.handleClean).grid(column=1, row=0, padx=5)
        # Button (Ingresar)
        tk.Button(fBtns, foreground=COLOR1, text="Ingresar...", relief="groove", width=15, font=("Inter Bold", 11), command=self.handleLoginSubmit).grid(column=0, row=0, padx=5)
        self.toplevel.bind("<Return>", self.handleLoginSubmit)

    def userLogout(self):
        self.user.logout()

    def handleLoginSubmit(self, event=None):
        if self.userVar.get() and self.passVar.get():
            self.user = AuthUser(self.userVar.get())
            try:
                if self.user.login(self.passVar.get()):
                    self.hide()
                    self.main_window.deiconify()
            except Exception as e:
                messagebox.showwarning("Error al iniciar sesión", str(e))

    def handleClean(self):
        self.userVar.set("")
        self.passVar.set("")

class ProductForm (Form):
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

        tk.Button(fr5, foreground=COLOR1, text="Añadir", relief="groove", width=20, height=2, font=("Inter Bold", 10), command=self.addProduct
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
                DB.save("productos", data)
                messagebox.showinfo("Producto agregado!", "Se agrego correctamente!")
                self.setDefault()
            except:
                messagebox.showwarning("Error en producto!", "No se completo el registro!")
        else:
            messagebox.showwarning("Campos requeridos", "Todos los campos son requeridos")

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
        tk.Entry(ftfr, textvariable=self.namefl).pack(side="left", padx=10)
        tk.Button(ftfr, text="Filtrar", relief="groove", font=("Inter", 9), command=handleFilter).pack(side="left")
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
        if data == None:
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

class SupplierForm (Form):
    def __init__(self, main_window):
        super().__init__(main_window, "Proveedores")
        Widget.SecLabel(self.toplevel, "Registra a un nuevo Proveerdor")

        fr1 = tk.Frame(self.toplevel); fr1.pack(pady=5)
        fr2 = tk.Frame(self.toplevel); fr2.pack(pady=5)
        fr3 = tk.Frame(self.toplevel); fr3.pack(pady=5)
        fr4 = tk.Frame(self.toplevel); fr4.pack(pady=5)
        fr5 = tk.Frame(self.toplevel); fr5.pack(pady=5)

        self.nameVar = tk.StringVar()
        Widget.InputGrid(fr2, "Nombre proveedor:", self.nameVar, [0,0])

        def handleSearch(event):
            self.prodNameList.delete(0, tk.END)
            

        self.prodNameList = tk.Listbox(fr2, height=6)
        self.prodSearch = tk.StringVar()
        Widget.CaptionGrid(fr2, "Producto suministrado:", [0, 2])
        entrySearch = tk.Entry(fr2, textvariable=self.prodSearch, font=("Inter", 10))
        entrySearch.grid(column=0, row=3)
        entrySearch.bind("<KeyPress>", handleSearch)

        prods = DB.get("productos")
        for prod in prods:
            self.prodNameList.insert(tk.END, prod["name"])

        self.prodNameList.grid(column=0, row=4)




class ReporteForm(Form):
    def __init__(self, main_window):
        super().__init__(main_window, "Reporte de Ventas")
        Widget.SecLabel(self.toplevel, "Visualiza el reporte de ventas y tendencias")

        # Cargar datos usando handledb.DB
        self.reporte = self.cargar_datos_reporte()

        # Filtro de búsqueda
        self.namefl = tk.StringVar()
        tk.Label(self.toplevel, text="Filtros").pack()
        ftfr = tk.Frame(self.toplevel)
        tk.Label(ftfr, text="Producto: ").pack(side="left")
        tk.Entry(ftfr, textvariable=self.namefl).pack(side="left", padx=10)
        tk.Button(ftfr, text="Filtrar", relief="groove", font=("Inter", 9), command=self.handleFilter).pack(side="left")
        ftfr.pack(pady=(0, 20))

        # Contenedor de reportes
        self.report_frame = tk.Frame(self.toplevel)
        self.report_frame.pack(pady=(0, 20))

        # Botón para graficar tendencias
        tk.Button(self.toplevel, text="Graficar Tendencias", command=self.graficar_tendencias).pack()

        # Contenedor del gráfico
        self.graph_frame = tk.Frame(self.toplevel)
        self.graph_frame.pack()

        self.setData()

    def cargar_datos_reporte(self):
        """Carga solo los productos y cantidades vendidos desde la base de datos JSON y crea el objeto Reporte."""

        ventas_data = DB.get("ventas")  # Cargar ventas desde JSON 
        if not ventas_data:
            pass

        # Extraer solo productos y cantidades
        ventas = []
        for data in ventas_data:
            try:
                venta = Venta(
                    fecha=data["fecha"],
                    productos_vendidos=data["productos_vendidos"],
                    metodo_pago=data["metodo_pago"],
                    puntuacion_atencion=data["puntuacion_atencion"]
                )
                ventas.append(venta)
            except KeyError as e:
                pass
        inventario = Inventario()
        inventario.products = DB.get("productos")
        if not inventario.products:
            pass

        return Reporte(inventario, ventas)

    def handleFilter(self):
    
        """Filtra los productos vendidos según el nombre ingresado en la barra de búsqueda."""
        filtro = self.namefl.get().strip().lower()

        if not filtro:
            self.setData(self.reporte.generar_reporte_ventas())
            return

        # Obtener todas las ventas
        ventas_data = DB.get("ventas")
        ventas_filtradas = {}

        for venta in ventas_data:
            for item in venta["productos_vendidos"]:
                nombre_producto = item["producto"].lower()
                if filtro in nombre_producto:
                    ventas_filtradas[item["producto"]] = ventas_filtradas.get(item["producto"], 0) + item["cantidad"]

        if ventas_filtradas:
            pass
        else:
            pass
        self.setData(ventas_filtradas)

    def setData(self, data=None):
        """Muestra el reporte de ventas en la interfaz."""
        for widget in self.report_frame.winfo_children():
            widget.destroy()  # Limpia el frame antes de agregar nuevos datos

        if data is None:
            data = self.reporte.generar_reporte_ventas()

        # Encabezado
        tk.Label(self.report_frame, text="Producto", font=("Inter Semibold", 10)).grid(row=0, column=0)
        tk.Label(self.report_frame, text="Cantidad Vendida", font=("Inter Semibold", 10)).grid(row=0, column=1)

        # Mostrar los productos
        for i, (producto, cantidad) in enumerate(data.items()):
            bg = COLOR1_SOFT if i%2==0 else None
            tk.Label(self.report_frame,background=bg, text=producto, font=("Inter", 9)).grid(row=i + 1, column=0)
            tk.Label(self.report_frame,background=bg, text=str(cantidad), font=("Inter", 9)).grid(row=i + 1, column=1)


    def graficar_tendencias(self):
        """Genera y muestra un gráfico de tendencias dentro de Tkinter."""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4))
        tendencias = self.reporte.graficar_tendencias()

        for producto, valores in tendencias.items():
            ax.plot(valores['fechas'], valores['cantidades'], label=producto)

        ax.set_xlabel('Fecha')
        ax.set_ylabel('Cantidad Vendida')
        ax.set_title('Tendencias de Ventas')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()