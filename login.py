import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkinter import ttk  
from PIL import Image, ImageTk  
import mysql.connector
import csv
from datetime import datetime

# Colores
COLOR_FONDO = "#FDF6E3"    
COLOR_CAJA = "#4A3B32"     
COLOR_BOTON = "#C48F3E"    
COLOR_CABECERA = "#8A5A44" 

# Fuentes
FUENTE_TITULO = ("Georgia", 16, "bold")
FUENTE_TEXTO = ("Georgia", 12)
FUENTE_GIGANTE = ("Georgia", 28, "bold")
FUENTE_BOTON = ("Georgia", 12, "bold")

# Conexion Base de Datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin1234", 
        database="el_gran_poeta"
    )

ES_OSCURO = True  

# Interfaz principal
def construir_app_principal(id_usuario_logueado, nombre_usuario, cargo_usuario):
    contenedor_login.place_forget()
    
    frame_app = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_app.pack(fill="both", expand=True)
    
    # Barra superior
    cabecera = tk.Frame(frame_app, bg=COLOR_CABECERA, height=40)
    cabecera.pack(fill="x", side="top") 
    
    lbl_usuario_actual = tk.Label(cabecera, text=f"Usuario: {nombre_usuario.capitalize()} | Perfil: {cargo_usuario}", font=("Georgia", 11, "bold"), bg=COLOR_CABECERA, fg="white")
    lbl_usuario_actual.pack(side="left", padx=15, pady=8)
    
    def cerrar_sesion():
        if messagebox.askyesno("Confirmar", "¿Deseas cerrar sesión?"):
            frame_app.destroy() 
            caja_usuario.delete(0, tk.END)
            caja_password.delete(0, tk.END)
            aplicar_tema_login()
            contenedor_login.place(relx=0.5, rely=0.5, anchor="center")
            caja_usuario.focus()
            
    tk.Button(cabecera, text="Cerrar Sesión", font=("Georgia", 10, "bold"), bg="#E74C3C", fg="black", command=cerrar_sesion).pack(side="right", padx=15, pady=5)
    
    # Contenedor de pantallas
    tablero = tk.Frame(frame_app, bg=COLOR_FONDO)
    tablero.pack(fill="both", expand=True)
    tablero.grid_rowconfigure(0, weight=1)
    tablero.grid_columnconfigure(0, weight=1)
    
    vista_menu = tk.Frame(tablero, bg=COLOR_FONDO)
    vista_bodegas = tk.Frame(tablero, bg=COLOR_FONDO)
    vista_productos = tk.Frame(tablero, bg=COLOR_FONDO)
    vista_traslados = tk.Frame(tablero, bg=COLOR_FONDO) 
    vista_reportes = tk.Frame(tablero, bg=COLOR_FONDO) 
    vista_usuarios = tk.Frame(tablero, bg=COLOR_FONDO) 
    
    for frame in (vista_menu, vista_bodegas, vista_productos, vista_traslados, vista_reportes, vista_usuarios):
        frame.grid(row=0, column=0, sticky="nsew")

    # Cambio de modo claro y oscuro
    def aplicar_tema_app():
        bg_f = "#1E1E1E" if ES_OSCURO else "#FDF6E3"
        fg_t = "#FFFFFF" if ES_OSCURO else "black"
        bg_cab = "#111111" if ES_OSCURO else "#8A5A44"
        fg_tit = "#C48F3E" if ES_OSCURO else "#4A3B32"
        
        frame_app.configure(bg=bg_f)
        tablero.configure(bg=bg_f)
        cabecera.configure(bg=bg_cab)
        lbl_usuario_actual.configure(bg=bg_cab)
        
        def actualizar_recursivo(parent):
            for child in parent.winfo_children():
                tipo = child.winfo_class()
                
                if tipo in ("Frame", "Labelframe"):
                    if tipo == "Labelframe":
                        child.configure(bg=bg_f, fg=fg_tit)
                    else:
                        child.configure(bg=bg_f)
                        
                elif tipo == "Label":
                    if child.master == cabecera:
                        pass 
                    elif child.cget("text") in ["PANEL DE CONTROL", "ADMINISTRACIÓN DE BODEGAS", "CATÁLOGO DE LIBROS Y PRODUCTOS", "CONTROL DE INVENTARIO Y TRASLADOS", "STOCK ACTUAL GLOBAL EN TIEMPO REAL", "AUDITORÍA Y REPORTES GERENCIALES", "Filtros de Búsqueda:", "GESTIÓN DE USUARIOS", "Filtrar por Fechas:"]:
                        child.configure(bg=bg_f, fg=fg_tit)
                    else:
                        child.configure(bg=bg_f, fg=fg_t)
                        
                elif tipo == "Entry":
                    child.configure(bg="#2D2D2D" if ES_OSCURO else "white", fg="white" if ES_OSCURO else "black", insertbackground="white" if ES_OSCURO else "black")
                    
                actualizar_recursivo(child)
                
        actualizar_recursivo(frame_app)
        
        style = ttk.Style()
        if ES_OSCURO:
            style.theme_use('clam')
            style.configure("Treeview", background="#2D2D2D", foreground="white", fieldbackground="#2D2D2D", rowheight=25)
            style.configure("Treeview.Heading", background="#111111", foreground="white", borderwidth=1)
            style.map("Treeview", background=[('selected', '#C48F3E')], foreground=[('selected', 'black')])
        else:
            style.theme_use('default')
            style.configure("Treeview", background="white", foreground="black", fieldbackground="white", rowheight=20)
            style.map("Treeview", background=[('selected', '#3470A2')], foreground=[('selected', 'white')])
            
        btn_tema.configure(text="Modo Claro" if ES_OSCURO else "Modo Oscuro")

    def alternar_tema_app():
        global ES_OSCURO
        ES_OSCURO = not ES_OSCURO
        aplicar_tema_app()

    btn_tema = tk.Button(cabecera, text="Modo Oscuro", font=("Georgia", 10, "bold"), bg=COLOR_BOTON, fg="black", command=alternar_tema_app)
    btn_tema.pack(side="right", padx=5, pady=5)

    # Validacion de permisos por rol
    def ir_a_bodegas():
        if cargo_usuario == "Jefe de Bodega":
            actualizar_tabla_bodegas()
            vista_bodegas.tkraise()
        else:
            messagebox.showerror("Acceso Denegado", "Privilegios insuficientes.\nSolo el Jefe de Bodega puede administrar sucursales.")

    def ir_a_productos():
        if cargo_usuario == "Jefe de Bodega":
            cargar_editoriales()
            actualizar_tabla_productos()
            vista_productos.tkraise()
        else:
            messagebox.showerror("Acceso Denegado", "Privilegios insuficientes.\nSolo el Jefe de Bodega puede crear y editar productos.")

    def ir_a_traslados():
        if cargo_usuario == "Bodeguero":
            cargar_combos_traslados()
            actualizar_tabla_inventario()
            vista_traslados.tkraise()
        else:
            messagebox.showerror("Acceso Denegado", "Privilegios insuficientes.\nSolo el Bodeguero puede procesar movimientos de stock entre sucursales.")

    def ir_a_reportes():
        if cargo_usuario == "Jefe de Bodega":
            cargar_filtros_reportes()
            actualizar_tabla_reportes_movimientos()
            vista_reportes.tkraise()
            vista_rep_movs.tkraise() 
        else:
            messagebox.showerror("Acceso Denegado", "Privilegios insuficientes.\nSolo el Jefe de Bodega puede auditar los reportes e informes.")

    def ir_a_usuarios():
        if cargo_usuario == "Jefe de Bodega":
            cargar_perfiles_usuarios()
            actualizar_tabla_usuarios()
            vista_usuarios.tkraise()
        else:
            messagebox.showerror("Acceso Denegado", "Privilegios insuficientes.\nSolo el Jefe de Bodega puede gestionar a los usuarios del sistema.")

    # Pantalla Menu Principal
    centro_menu = tk.Frame(vista_menu, bg=COLOR_FONDO)
    centro_menu.place(relx=0.5, rely=0.5, anchor="center")
    
    if logo_img:
        tk.Label(centro_menu, image=logo_img, bg=COLOR_FONDO).pack(pady=(0, 10))
    tk.Label(centro_menu, text="PANEL DE CONTROL", font=FUENTE_GIGANTE, bg=COLOR_FONDO, fg=COLOR_CAJA).pack(pady=10)
    
    grilla_botones = tk.Frame(centro_menu, bg=COLOR_FONDO)
    grilla_botones.pack(pady=20)
    
    tk.Button(grilla_botones, text="GESTIÓN DE BODEGAS", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="black", width=25, height=2, command=ir_a_bodegas).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(grilla_botones, text="CATÁLOGO PRODUCTOS", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="black", width=25, height=2, command=ir_a_productos).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(grilla_botones, text="TRASLADOS DE STOCK", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="black", width=25, height=2, command=ir_a_traslados).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(grilla_botones, text="REPORTES Y AUDITORÍA", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="black", width=25, height=2, command=ir_a_reportes).grid(row=1, column=1, padx=10, pady=10)
    
    tk.Button(grilla_botones, text="GESTIÓN DE USUARIOS", font=FUENTE_BOTON, bg="#3498DB", fg="black", width=25, height=2, command=ir_a_usuarios).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Pantalla Gestion de Bodegas
    marco_contenido_bodegas = tk.Frame(vista_bodegas, bg=COLOR_FONDO)
    marco_contenido_bodegas.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Button(marco_contenido_bodegas, text="Volver al Menú", font=("Georgia", 10, "bold"), bg=COLOR_BOTON, fg="black", command=vista_menu.tkraise).pack(anchor="w", pady=(0, 10))
    tk.Label(marco_contenido_bodegas, text="ADMINISTRACIÓN DE BODEGAS", font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_CAJA).pack(pady=10)
    
    form_bodegas = tk.Frame(marco_contenido_bodegas, bg=COLOR_FONDO)
    form_bodegas.pack(pady=10)
    
    tk.Label(form_bodegas, text="Nombre de Sucursal:", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg="black").grid(row=0, column=0, padx=5)
    caja_bodega = tk.Entry(form_bodegas, font=FUENTE_TEXTO, width=20); caja_bodega.grid(row=0, column=1, padx=5)
    
    id_bodega_sel = tk.StringVar()

    def actualizar_tabla_bodegas():
        for item in tabla_bodegas.get_children(): tabla_bodegas.delete(item)
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("SELECT * FROM BODEGAS")
            for fila in cursor.fetchall(): tabla_bodegas.insert("", "end", values=fila)
            conexion.close(); caja_bodega.delete(0, tk.END); id_bodega_sel.set("") 
        except: pass

    def guardar_bodega():
        if not caja_bodega.get(): return
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("INSERT INTO BODEGAS (nombre_bodega) VALUES (%s)", (caja_bodega.get(),))
            conexion.commit(); conexion.close(); actualizar_tabla_bodegas()
        except: pass

    def modificar_bodega():
        if not id_bodega_sel.get() or not caja_bodega.get(): return
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("UPDATE BODEGAS SET nombre_bodega = %s WHERE id_bodega = %s", (caja_bodega.get(), id_bodega_sel.get()))
            conexion.commit(); conexion.close(); actualizar_tabla_bodegas()
            messagebox.showinfo("Éxito", "Bodega actualizada.")
        except: pass

    def eliminar_bodega():
        if not tabla_bodegas.selection(): return
        if messagebox.askyesno("Confirmar", "¿Eliminar sucursal?"):
            try:
                conexion = conectar_db(); cursor = conexion.cursor()
                cursor.execute("DELETE FROM BODEGAS WHERE id_bodega = %s", (id_bodega_sel.get(),))
                conexion.commit(); conexion.close(); actualizar_tabla_bodegas()
            except mysql.connector.Error as err:
                if err.errno == 1451: messagebox.showerror("Error", "Bodega con stock activo.")

    def clic_bodega(event):
        if tabla_bodegas.selection():
            item = tabla_bodegas.item(tabla_bodegas.selection())
            id_bodega_sel.set(item['values'][0])
            caja_bodega.delete(0, tk.END); caja_bodega.insert(0, item['values'][1])

    tk.Button(form_bodegas, text="Agregar", font=("Georgia", 10, "bold"), bg=COLOR_BOTON, fg="black", command=guardar_bodega).grid(row=0, column=2, padx=5)
    tk.Button(form_bodegas, text="Actualizar", font=("Georgia", 10, "bold"), bg="#3498DB", fg="black", command=modificar_bodega).grid(row=0, column=3, padx=5)

    tabla_bodegas = ttk.Treeview(marco_contenido_bodegas, columns=("ID", "Nombre"), show="headings", height=6)
    tabla_bodegas.heading("ID", text="ID"); tabla_bodegas.heading("Nombre", text="Nombre Sucursal")
    tabla_bodegas.column("ID", width=50, anchor="center"); tabla_bodegas.column("Nombre", width=350, anchor="center")
    tabla_bodegas.pack(pady=15); tabla_bodegas.bind("<<TreeviewSelect>>", clic_bodega)
    tk.Button(marco_contenido_bodegas, text="Eliminar Seleccionada", font=("Georgia", 10, "bold"), bg="#E74C3C", fg="black", command=eliminar_bodega).pack(pady=5)

    # Pantalla Catálogo de Productos
    marco_contenido_prod = tk.Frame(vista_productos, bg=COLOR_FONDO)
    marco_contenido_prod.place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(marco_contenido_prod, text="Volver al Menú", font=("Georgia", 10, "bold"), bg=COLOR_BOTON, fg="black", command=vista_menu.tkraise).pack(anchor="w", pady=(0, 10))
    tk.Label(marco_contenido_prod, text="CATÁLOGO DE LIBROS Y PRODUCTOS", font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_CAJA).pack(pady=10)

    form_prod = tk.Frame(marco_contenido_prod, bg=COLOR_FONDO)
    form_prod.pack(pady=10)

    tk.Label(form_prod, text="Título:", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg="black").grid(row=0, column=0, sticky="e")
    caja_titulo = tk.Entry(form_prod, font=FUENTE_TEXTO, width=25); caja_titulo.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(form_prod, text="Autor:", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg="black").grid(row=0, column=2, sticky="e")
    caja_autor = tk.Entry(form_prod, font=FUENTE_TEXTO, width=25); caja_autor.grid(row=0, column=3, padx=5, pady=5)
    
    tk.Label(form_prod, text="Tipo:", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg="black").grid(row=1, column=0, sticky="e")
    combo_tipo = ttk.Combobox(form_prod, font=FUENTE_TEXTO, width=23, state="readonly")
    combo_tipo['values'] = ["Libro", "Revista", "Enciclopedia"]
    combo_tipo.current(0)
    combo_tipo.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_prod, text="Descripción:", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg="black").grid(row=1, column=2, sticky="e")
    caja_desc = tk.Entry(form_prod, font=FUENTE_TEXTO, width=25); caja_desc.grid(row=1, column=3, padx=5, pady=5)
    
    tk.Label(form_prod, text="Editorial:", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg="black").grid(row=2, column=0, sticky="e")
    
    frame_editorial = tk.Frame(form_prod, bg=COLOR_FONDO)
    frame_editorial.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    combo_editorial = ttk.Combobox(frame_editorial, font=FUENTE_TEXTO, width=17, state="readonly")
    combo_editorial.pack(side="left")

    def agregar_nueva_editorial():
        nueva_ed = simpledialog.askstring("Nueva Editorial", "Ingresa el nombre de la nueva editorial:")
        if nueva_ed and nueva_ed.strip():
            nueva_ed = nueva_ed.strip()
            try:
                conexion = conectar_db(); cursor = conexion.cursor()
                cursor.execute("INSERT INTO EDITORIALES (nombre_editorial) VALUES (%s)", (nueva_ed,))
                conexion.commit(); conexion.close()
                cargar_editoriales() 
                if nueva_ed in combo_editorial['values']:
                    combo_editorial.current(combo_editorial['values'].index(nueva_ed))
                messagebox.showinfo("Éxito", f"La editorial '{nueva_ed}' ha sido registrada.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo guardar: {err}")

    btn_add_ed = tk.Button(frame_editorial, text="+", font=("Arial", 10, "bold"), bg="#3498DB", fg="black", command=agregar_nueva_editorial)
    btn_add_ed.pack(side="left", padx=(5, 0))

    id_producto_sel = tk.StringVar()
    mapa_editoriales = {}

    def limpiar_formulario_productos():
        caja_titulo.delete(0, tk.END); caja_autor.delete(0, tk.END)
        combo_tipo.current(0)
        caja_desc.delete(0, tk.END); id_producto_sel.set("")

    def cargar_editoriales():
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("SELECT id_editorial, nombre_editorial FROM EDITORIALES ORDER BY nombre_editorial ASC")
            nombres = []
            mapa_editoriales.clear()
            for id_ed, name_ed in cursor.fetchall():
                nombres.append(name_ed); mapa_editoriales[name_ed] = id_ed 
            combo_editorial['values'] = nombres
            if nombres: combo_editorial.current(0) 
            conexion.close()
        except: pass

    def actualizar_tabla_productos():
        for item in tabla_productos.get_children(): tabla_productos.delete(item)
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("SELECT P.id_producto, P.titulo, P.autor, P.tipo_producto, P.descripcion, E.nombre_editorial FROM PRODUCTOS P LEFT JOIN EDITORIALES E ON P.id_editorial = E.id_editorial")
            for fila in cursor.fetchall(): tabla_productos.insert("", "end", values=fila)
            conexion.close(); limpiar_formulario_productos()
        except: pass

    def guardar_producto():
        if not caja_titulo.get(): return
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("INSERT INTO PRODUCTOS (titulo, autor, tipo_producto, descripcion, id_editorial) VALUES (%s, %s, %s, %s, %s)", 
                           (caja_titulo.get(), caja_autor.get(), combo_tipo.get(), caja_desc.get(), mapa_editoriales[combo_editorial.get()]))
            conexion.commit(); conexion.close(); actualizar_tabla_productos()
            messagebox.showinfo("Éxito", "Libro registrado en el catálogo.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo guardar: {err}")

    def modificar_producto():
        if not id_producto_sel.get() or not caja_titulo.get(): return
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("UPDATE PRODUCTOS SET titulo=%s, autor=%s, tipo_producto=%s, descripcion=%s, id_editorial=%s WHERE id_producto=%s", 
                           (caja_titulo.get(), caja_autor.get(), combo_tipo.get(), caja_desc.get(), mapa_editoriales[combo_editorial.get()], id_producto_sel.get()))
            conexion.commit(); conexion.close(); actualizar_tabla_productos()
            messagebox.showinfo("Éxito", "Catálogo modificado correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo actualizar: {err}")

    def eliminar_producto():
        if not tabla_productos.selection(): return
        if messagebox.askyesno("Confirmar", "¿Eliminar del catálogo?"):
            try:
                conexion = conectar_db(); cursor = conexion.cursor()
                cursor.execute("DELETE FROM PRODUCTOS WHERE id_producto = %s", (id_producto_sel.get(),))
                conexion.commit(); conexion.close(); actualizar_tabla_productos()
            except mysql.connector.Error as err:
                if err.errno == 1451: messagebox.showerror("Error", "El registro tiene inventario activo en bodegas.")

    def clic_producto(event):
        if tabla_productos.selection():
            valores = tabla_productos.item(tabla_productos.selection())['values']
            id_producto_sel.set(valores[0])
            caja_titulo.delete(0, tk.END); caja_titulo.insert(0, valores[1])
            caja_autor.delete(0, tk.END); caja_autor.insert(0, valores[2] if valores[2] else "")
            
            tipo_guardado = str(valores[3])
            if tipo_guardado in combo_tipo['values']:
                combo_tipo.current(combo_tipo['values'].index(tipo_guardado))
            else:
                combo_tipo.set(tipo_guardado)
                
            caja_desc.delete(0, tk.END); caja_desc.insert(0, valores[4] if valores[4] else "")
            if valores[5] in combo_editorial['values']: combo_editorial.current(combo_editorial['values'].index(valores[5]))

    tk.Button(form_prod, text="Guardar Registro", font=("Georgia", 10, "bold"), bg=COLOR_BOTON, fg="black", command=guardar_producto).grid(row=2, column=2, padx=5)
    tk.Button(form_prod, text="Actualizar", font=("Georgia", 10, "bold"), bg="#3498DB", fg="black", command=modificar_producto).grid(row=2, column=3, padx=5)

    tabla_productos = ttk.Treeview(marco_contenido_prod, columns=("ID", "Título", "Autor", "Tipo", "Descripción", "Editorial"), show="headings", height=6)
    for col in tabla_productos['columns']: tabla_productos.heading(col, text=col)
    tabla_productos.column("ID", width=40, anchor="center"); tabla_productos.column("Título", width=150); tabla_productos.column("Autor", width=100); tabla_productos.column("Tipo", width=90, anchor="center"); tabla_productos.column("Descripción", width=120); tabla_productos.column("Editorial", width=100)
    tabla_productos.pack(pady=10); tabla_productos.bind("<<TreeviewSelect>>", clic_producto)
    tk.Button(marco_contenido_prod, text="Eliminar Seleccionado", font=("Georgia", 10, "bold"), bg="#E74C3C", fg="black", command=eliminar_producto).pack()


    # Pantalla Traslados de Stock
    marco_contenido_traslados = tk.Frame(vista_traslados, bg=COLOR_FONDO)
    marco_contenido_traslados.place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(marco_contenido_traslados, text="Volver al Menú", font=("Georgia", 10, "bold"), bg=COLOR_BOTON, fg="black", command=vista_menu.tkraise).pack(anchor="w", pady=(0, 10))
    tk.Label(marco_contenido_traslados, text="CONTROL DE INVENTARIO Y TRASLADOS", font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_CAJA).pack(pady=5)

    bloque_operaciones = tk.Frame(marco_contenido_traslados, bg=COLOR_FONDO)
    bloque_operaciones.pack(pady=10)

    sub_abastecer = tk.LabelFrame(bloque_operaciones, text=" Inyección de Stock Inicial ", font=("Georgia", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_CAJA, padx=10, pady=10)
    sub_abastecer.grid(row=0, column=0, padx=15, sticky="n")

    tk.Label(sub_abastecer, text="Libro/Producto:", bg=COLOR_FONDO, fg="black").pack(anchor="w")
    combo_abs_libro = ttk.Combobox(sub_abastecer, font=("Georgia", 10), width=22, state="readonly"); combo_abs_libro.pack(pady=2)
    tk.Label(sub_abastecer, text="Bodega Destino:", bg=COLOR_FONDO, fg="black").pack(anchor="w")
    combo_abs_bodega = ttk.Combobox(sub_abastecer, font=("Georgia", 10), width=22, state="readonly"); combo_abs_bodega.pack(pady=2)
    tk.Label(sub_abastecer, text="Cantidad:", bg=COLOR_FONDO, fg="black").pack(anchor="w")
    caja_abs_cant = tk.Entry(sub_abastecer, font=("Georgia", 10), width=10); caja_abs_cant.pack(pady=2)
    
    tk.Button(sub_abastecer, text="Inyectar Stock", font=("Georgia", 10, "bold"), bg="#2ECC71", fg="black", command=lambda: procesar_abastecimiento()).pack(pady=10)

    sub_transferir = tk.LabelFrame(bloque_operaciones, text=" Transferencia entre Sucursales ", font=("Georgia", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_CAJA, padx=10, pady=10)
    sub_transferir.grid(row=0, column=1, padx=15, sticky="n")

    tk.Label(sub_transferir, text="Producto a Mover:", bg=COLOR_FONDO, fg="black").grid(row=0, column=0, sticky="w")
    combo_tra_libro = ttk.Combobox(sub_transferir, font=("Georgia", 10), width=22, state="readonly"); combo_tra_libro.grid(row=0, column=1, padx=5, pady=2)
    tk.Label(sub_transferir, text="Bodega Origen:", bg=COLOR_FONDO, fg="black").grid(row=1, column=0, sticky="w")
    combo_tra_origen = ttk.Combobox(sub_transferir, font=("Georgia", 10), width=22, state="readonly"); combo_tra_origen.grid(row=1, column=1, padx=5, pady=2)
    tk.Label(sub_transferir, text="Bodega Destino:", bg=COLOR_FONDO, fg="black").grid(row=2, column=0, sticky="w")
    combo_tra_destino = ttk.Combobox(sub_transferir, font=("Georgia", 10), width=22, state="readonly"); combo_tra_destino.grid(row=2, column=1, padx=5, pady=2)
    tk.Label(sub_transferir, text="Cantidad:", bg=COLOR_FONDO, fg="black").grid(row=3, column=0, sticky="w")
    caja_tra_cant = tk.Entry(sub_transferir, font=("Georgia", 10), width=10); caja_tra_cant.grid(row=3, column=1, padx=5, pady=2, sticky="w")

    tk.Button(sub_transferir, text="Procesar Traslado", font=("Georgia", 10, "bold"), bg=COLOR_BOTON, fg="black", command=lambda: procesar_transferencia()).grid(row=4, column=0, columnspan=2, pady=10)

    dict_libros, dict_bodegas = {}, {}

    def cargar_combos_traslados():
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            dict_libros.clear(); dict_bodegas.clear()
            
            cursor.execute("SELECT id_producto, titulo FROM PRODUCTOS")
            nombres_libros = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
            for txt in nombres_libros: dict_libros[txt] = int(txt.split(" - ")[0])

            cursor.execute("SELECT id_bodega, nombre_bodega FROM BODEGAS")
            nombres_bodegas = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
            for txt in nombres_bodegas: dict_bodegas[txt] = int(txt.split(" - ")[0])

            for cb in (combo_abs_libro, combo_tra_libro): cb['values'] = nombres_libros
            for cb in (combo_abs_bodega, combo_tra_origen, combo_tra_destino): cb['values'] = nombres_bodegas
            
            for cb in (combo_abs_libro, combo_tra_libro, combo_abs_bodega, combo_tra_origen, combo_tra_destino):
                if cb['values']: cb.current(0)
            conexion.close()
        except: pass

    def actualizar_tabla_inventario():
        for item in tabla_inventario.get_children(): tabla_inventario.delete(item)
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("""
                SELECT B.nombre_bodega, P.titulo, I.cantidad 
                FROM INVENTARIO I
                JOIN BODEGAS B ON I.id_bodega = B.id_bodega
                JOIN PRODUCTOS P ON I.id_producto = P.id_producto
                ORDER BY B.nombre_bodega, P.titulo
            """)
            for fila in cursor.fetchall(): tabla_inventario.insert("", "end", values=fila)
            conexion.close()
        except: pass

    def procesar_abastecimiento():
        if not caja_abs_cant.get().isdigit():
            messagebox.showwarning("Error", "Ingresa una cantidad numérica válida.")
            return
        cant = int(caja_abs_cant.get())
        id_prod = dict_libros[combo_abs_libro.get()]
        id_bod = dict_bodegas[combo_abs_bodega.get()]

        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("SELECT id_inventario, cantidad FROM INVENTARIO WHERE id_bodega=%s AND id_producto=%s", (id_bod, id_prod))
            existe = cursor.fetchone()

            if existe:
                cursor.execute("UPDATE INVENTARIO SET cantidad=cantidad+%s WHERE id_inventario=%s", (cant, existe[0]))
            else:
                cursor.execute("INSERT INTO INVENTARIO (id_bodega, id_producto, cantidad) VALUES (%s, %s, %s)", (id_bod, id_prod, cant))

            cursor.execute("INSERT INTO MOVIMIENTOS (id_usuario, bodega_origen, bodega_destino, id_producto, cantidad) VALUES (%s, NULL, %s, %s, %s)", 
                           (id_usuario_logueado, id_bod, id_prod, cant))
            
            conexion.commit(); conexion.close(); caja_abs_cant.delete(0, tk.END)
            actualizar_tabla_inventario()
            messagebox.showinfo("Éxito", "Inventario abastecido correctamente.")
        except mysql.connector.Error as e: messagebox.showerror("Error", f"Fallo: {e}")

    def procesar_transferencia():
        if not caja_tra_cant.get().isdigit():
            messagebox.showwarning("Error", "Cantidad inválida.")
            return
        cant = int(caja_tra_cant.get())
        id_prod = dict_libros[combo_tra_libro.get()]
        id_ori = dict_bodegas[combo_tra_origen.get()]
        id_des = dict_bodegas[combo_tra_destino.get()]

        if id_ori == id_des:
            messagebox.showwarning("Atención", "La bodega de origen y destino no pueden ser iguales.")
            return

        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            
            cursor.execute("SELECT id_inventario, cantidad FROM INVENTARIO WHERE id_bodega=%s AND id_producto=%s", (id_ori, id_prod))
            stock_origen = cursor.fetchone()

            if not stock_origen or stock_origen[1] < cant:
                messagebox.showerror("Stock Insuficiente", f"Operación denegada. Stock disponible en origen: {stock_origen[1] if stock_origen else 0} unidades.")
                conexion.close()
                return

            cursor.execute("UPDATE INVENTARIO SET cantidad=cantidad-%s WHERE id_inventario=%s", (cant, stock_origen[0]))

            cursor.execute("SELECT id_inventario FROM INVENTARIO WHERE id_bodega=%s AND id_producto=%s", (id_des, id_prod))
            stock_destino = cursor.fetchone()
            if stock_destino:
                cursor.execute("UPDATE INVENTARIO SET cantidad=cantidad+%s WHERE id_inventario=%s", (cant, stock_destino[0]))
            else:
                cursor.execute("INSERT INTO INVENTARIO (id_bodega, id_producto, cantidad) VALUES (%s, %s, %s)", (id_des, id_prod, cant))

            cursor.execute("INSERT INTO MOVIMIENTOS (id_usuario, bodega_origen, bodega_destino, id_producto, cantidad) VALUES (%s, %s, %s, %s, %s)", 
                           (id_usuario_logueado, id_ori, id_des, id_prod, cant))

            conexion.commit(); conexion.close(); caja_tra_cant.delete(0, tk.END)
            actualizar_tabla_inventario()
            messagebox.showinfo("Éxito", "Traslado de stock procesado con éxito.")
        except mysql.connector.Error as e: messagebox.showerror("Error", f"Error crítico: {e}")

    tk.Label(marco_contenido_traslados, text="STOCK ACTUAL GLOBAL EN TIEMPO REAL", font=("Georgia", 11, "bold"), bg=COLOR_FONDO, fg=COLOR_CAJA).pack(pady=(10,0))
    tabla_inventario = ttk.Treeview(marco_contenido_traslados, columns=("Bodega", "Libro", "Cantidad"), show="headings", height=6)
    tabla_inventario.heading("Bodega", text="Bodega / Sucursal"); tabla_inventario.heading("Libro", text="Libro / Catálogo"); tabla_inventario.heading("Cantidad", text="Stock Disponible")
    tabla_inventario.column("Bodega", width=180, anchor="center"); tabla_inventario.column("Libro", width=250, anchor="w"); tabla_inventario.column("Cantidad", width=100, anchor="center")
    tabla_inventario.pack(pady=10)


    # Pantalla Reportes y Auditoria
    marco_contenido_reportes = tk.Frame(vista_reportes, bg=COLOR_FONDO)
    marco_contenido_reportes.place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(marco_contenido_reportes, text="Volver al Menú", font=("Georgia", 10, "bold"), bg=COLOR_BOTON, fg="black", command=vista_menu.tkraise).pack(anchor="w", pady=(0, 10))
    tk.Label(marco_contenido_reportes, text="AUDITORÍA Y REPORTES GERENCIALES", font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_CAJA).pack(pady=5)

    marco_botones_reportes = tk.Frame(marco_contenido_reportes, bg=COLOR_FONDO)
    marco_botones_reportes.pack(pady=5)
    
    contenedor_vistas_reportes = tk.Frame(marco_contenido_reportes, bg=COLOR_FONDO)
    contenedor_vistas_reportes.pack(fill="both", expand=True)
    
    vista_rep_movs = tk.Frame(contenedor_vistas_reportes, bg=COLOR_FONDO)
    vista_rep_stock = tk.Frame(contenedor_vistas_reportes, bg=COLOR_FONDO)
    vista_rep_movs.grid(row=0, column=0, sticky="nsew")
    vista_rep_stock.grid(row=0, column=0, sticky="nsew")

    tk.Button(marco_botones_reportes, text="Ver Historial de Movimientos", font=("Georgia", 10, "bold"), bg="#3498DB", fg="black", command=vista_rep_movs.tkraise).grid(row=0, column=0, padx=10)
    tk.Button(marco_botones_reportes, text="Ver Inventario Filtrado (Jefe)", font=("Georgia", 10, "bold"), bg="#2ECC71", fg="black", command=vista_rep_stock.tkraise).grid(row=0, column=1, padx=10)

    # SECCION A: Historial de Movimientos

    marco_filtros_movs = tk.Frame(vista_rep_movs, bg=COLOR_FONDO)
    marco_filtros_movs.pack(pady=5)
    
    tk.Label(marco_filtros_movs, text="Filtrar por Fechas:", font=("Georgia", 10, "bold"), bg=COLOR_FONDO, fg="black").grid(row=0, column=0, columnspan=4, pady=5)
    
    tk.Label(marco_filtros_movs, text="Desde (YYYY-MM-DD):", font=("Georgia", 10), bg=COLOR_FONDO, fg="black").grid(row=1, column=0, padx=5)
    caja_fecha_inicio = tk.Entry(marco_filtros_movs, font=("Georgia", 10), width=12)
    caja_fecha_inicio.grid(row=1, column=1, padx=5)
    
    tk.Label(marco_filtros_movs, text="Hasta (YYYY-MM-DD):", font=("Georgia", 10), bg=COLOR_FONDO, fg="black").grid(row=1, column=2, padx=5)
    caja_fecha_fin = tk.Entry(marco_filtros_movs, font=("Georgia", 10), width=12)
    caja_fecha_fin.grid(row=1, column=3, padx=5)

    def actualizar_tabla_reportes_movimientos():
        for item in tabla_reportes.get_children(): tabla_reportes.delete(item)
        
        f_inicio = caja_fecha_inicio.get().strip()
        f_fin = caja_fecha_fin.get().strip()
        
        query = """
            SELECT 
                M.id_movimiento, DATE_FORMAT(M.fecha_movimiento, '%Y-%m-%d %H:%i:%s'), 
                U.username, IFNULL(B1.nombre_bodega, 'Abastecimiento Externo'), 
                B2.nombre_bodega, P.titulo, M.cantidad
            FROM MOVIMIENTOS M
            JOIN USUARIOS U ON M.id_usuario = U.id_usuario
            LEFT JOIN BODEGAS B1 ON M.bodega_origen = B1.id_bodega
            JOIN BODEGAS B2 ON M.bodega_destino = B2.id_bodega
            JOIN PRODUCTOS P ON M.id_producto = P.id_producto
            WHERE 1=1
        """
        params = []
        
        if f_inicio:
            query += " AND DATE(M.fecha_movimiento) >= %s"
            params.append(f_inicio)
        if f_fin:
            query += " AND DATE(M.fecha_movimiento) <= %s"
            params.append(f_fin)
            
        query += " ORDER BY M.fecha_movimiento DESC"
        
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute(query, tuple(params))
            for fila in cursor.fetchall(): tabla_reportes.insert("", "end", values=fila)
            conexion.close()
        except: pass

    def exportar_auditoria_excel():
        if not tabla_reportes.get_children():
            messagebox.showwarning("Atención", "No hay datos en la tabla para exportar.")
            return

        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H%M")
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            title="Guardar Reporte de Movimientos",
            initialfile=f"Movimientos_{fecha_actual}"
        )
        if not archivo: return

        try:
            with open(archivo, mode="w", newline="", encoding="utf-8-sig") as f:
                escritor = csv.writer(f, delimiter=";") 
                escritor.writerow(["ID Movimiento", "Fecha / Hora", "Operador", "Bodega Origen", "Bodega Destino", "Producto", "Cantidad"])
                for item in tabla_reportes.get_children():
                    fila_datos = tabla_reportes.item(item)['values']
                    escritor.writerow(fila_datos)
            messagebox.showinfo("Éxito", "Reporte exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

    tk.Button(marco_filtros_movs, text="Buscar / Refrescar", font=("Georgia", 10, "bold"), bg="#3498DB", fg="black", command=actualizar_tabla_reportes_movimientos).grid(row=1, column=4, padx=10)
    tk.Button(marco_filtros_movs, text="Exportar a Excel", font=("Georgia", 10, "bold"), bg="#2ECC71", fg="black", command=exportar_auditoria_excel).grid(row=1, column=5, padx=10)

    tabla_reportes = ttk.Treeview(vista_rep_movs, columns=("ID", "Fecha", "Usuario", "Origen", "Destino", "Libro", "Cant"), show="headings", height=8)
    tabla_reportes.heading("ID", text="ID"); tabla_reportes.heading("Fecha", text="Fecha / Hora"); tabla_reportes.heading("Usuario", text="Operador")
    tabla_reportes.heading("Origen", text="Bodega Origen"); tabla_reportes.heading("Destino", text="Bodega Destino"); tabla_reportes.heading("Libro", text="Libro / Producto"); tabla_reportes.heading("Cant", text="Cant")
    tabla_reportes.column("ID", width=40, anchor="center"); tabla_reportes.column("Fecha", width=140, anchor="center"); tabla_reportes.column("Usuario", width=90, anchor="center")
    tabla_reportes.column("Origen", width=140, anchor="w"); tabla_reportes.column("Destino", width=140, anchor="w"); tabla_reportes.column("Libro", width=160, anchor="w"); tabla_reportes.column("Cant", width=50, anchor="center")
    tabla_reportes.pack(pady=10)


    # SECCION B: Stock Filtrado

    marco_filtros = tk.Frame(vista_rep_stock, bg=COLOR_FONDO)
    marco_filtros.pack(pady=5)
    
    tk.Label(marco_filtros, text="Filtros de Búsqueda:", font=("Georgia", 10, "bold"), bg=COLOR_FONDO, fg="black").grid(row=0, column=0, columnspan=4, pady=5)
    
    combo_filtro_bodega = ttk.Combobox(marco_filtros, font=("Georgia", 10), width=20, state="readonly")
    combo_filtro_bodega.grid(row=1, column=0, padx=5)
    combo_filtro_editorial = ttk.Combobox(marco_filtros, font=("Georgia", 10), width=20, state="readonly")
    combo_filtro_editorial.grid(row=1, column=1, padx=5)

    def cargar_filtros_reportes():
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("SELECT nombre_bodega FROM BODEGAS")
            combo_filtro_bodega['values'] = ["Todas las Bodegas"] + [r[0] for r in cursor.fetchall()]
            combo_filtro_bodega.current(0)
            
            cursor.execute("SELECT nombre_editorial FROM EDITORIALES")
            combo_filtro_editorial['values'] = ["Todas las Editoriales"] + [r[0] for r in cursor.fetchall()]
            combo_filtro_editorial.current(0)
            conexion.close()
            generar_informe_stock() 
        except: pass

    def generar_informe_stock():
        for item in tabla_stock_filtro.get_children(): tabla_stock_filtro.delete(item)
        bodega_sel = combo_filtro_bodega.get()
        editorial_sel = combo_filtro_editorial.get()
        
        query = """
            SELECT B.nombre_bodega, P.tipo_producto, P.titulo, E.nombre_editorial, I.cantidad
            FROM INVENTARIO I
            JOIN BODEGAS B ON I.id_bodega = B.id_bodega
            JOIN PRODUCTOS P ON I.id_producto = P.id_producto
            JOIN EDITORIALES E ON P.id_editorial = E.id_editorial
            WHERE 1=1
        """
        params = []
        if bodega_sel != "Todas las Bodegas":
            query += " AND B.nombre_bodega = %s"
            params.append(bodega_sel)
        if editorial_sel != "Todas las Editoriales":
            query += " AND E.nombre_editorial = %s"
            params.append(editorial_sel)
            
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute(query, tuple(params))
            for fila in cursor.fetchall(): tabla_stock_filtro.insert("", "end", values=fila)
            conexion.close()
        except: pass

    def exportar_stock_excel():
        if not tabla_stock_filtro.get_children():
            messagebox.showwarning("Atención", "No hay datos en la tabla para exportar.")
            return

        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H%M")
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            title="Guardar Reporte de Stock",
            initialfile=f"Stock_{fecha_actual}"
        )
        if not archivo: return

        try:
            with open(archivo, mode="w", newline="", encoding="utf-8-sig") as f:
                escritor = csv.writer(f, delimiter=";") 
                escritor.writerow(["Bodega", "Tipo", "Titulo", "Editorial", "Cantidad"])
                for item in tabla_stock_filtro.get_children():
                    fila_datos = tabla_stock_filtro.item(item)['values']
                    escritor.writerow(fila_datos)
            messagebox.showinfo("Éxito", "Reporte de stock exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

    tk.Button(marco_filtros, text="Buscar", font=("Georgia", 10, "bold"), bg="#F1C40F", fg="black", command=generar_informe_stock).grid(row=1, column=2, padx=10)
    tk.Button(marco_filtros, text="Exportar a Excel", font=("Georgia", 10, "bold"), bg="#2ECC71", fg="black", command=exportar_stock_excel).grid(row=1, column=3, padx=10)

    tabla_stock_filtro = ttk.Treeview(vista_rep_stock, columns=("Bodega", "Tipo", "Título", "Editorial", "Cant"), show="headings", height=8)
    tabla_stock_filtro.heading("Bodega", text="Bodega"); tabla_stock_filtro.heading("Tipo", text="Tipo de Producto")
    tabla_stock_filtro.heading("Título", text="Título / Nombre"); tabla_stock_filtro.heading("Editorial", text="Editorial"); tabla_stock_filtro.heading("Cant", text="Stock")
    tabla_stock_filtro.column("Bodega", width=150, anchor="w"); tabla_stock_filtro.column("Tipo", width=100, anchor="center")
    tabla_stock_filtro.column("Título", width=200, anchor="w"); tabla_stock_filtro.column("Editorial", width=120, anchor="center"); tabla_stock_filtro.column("Cant", width=60, anchor="center")
    tabla_stock_filtro.pack(pady=10)


    # Pantalla Gestion de Usuarios
    marco_contenido_usuarios = tk.Frame(vista_usuarios, bg=COLOR_FONDO)
    marco_contenido_usuarios.place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(marco_contenido_usuarios, text="Volver al Menú", font=("Georgia", 10, "bold"), bg=COLOR_BOTON, fg="black", command=vista_menu.tkraise).pack(anchor="w", pady=(0, 10))
    tk.Label(marco_contenido_usuarios, text="GESTIÓN DE USUARIOS", font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_CAJA).pack(pady=10)

    form_usuarios = tk.Frame(marco_contenido_usuarios, bg=COLOR_FONDO)
    form_usuarios.pack(pady=10)

    tk.Label(form_usuarios, text="Nombre Usuario:", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg="black").grid(row=0, column=0, sticky="e", padx=5)
    caja_usu_nombre = tk.Entry(form_usuarios, font=FUENTE_TEXTO, width=20)
    caja_usu_nombre.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(form_usuarios, text="Contraseña:", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg="black").grid(row=0, column=2, sticky="e", padx=5)
    caja_usu_pass = tk.Entry(form_usuarios, font=FUENTE_TEXTO, width=20, show="*")
    caja_usu_pass.grid(row=0, column=3, padx=5, pady=5)
    
    tk.Label(form_usuarios, text="Perfil/Rol:", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg="black").grid(row=1, column=0, sticky="e", padx=5)
    combo_usu_perfil = ttk.Combobox(form_usuarios, font=FUENTE_TEXTO, width=18, state="readonly")
    combo_usu_perfil.grid(row=1, column=1, padx=5, pady=5)

    id_usuario_sel = tk.StringVar()
    mapa_perfiles = {}

    def limpiar_form_usuarios():
        caja_usu_nombre.delete(0, tk.END)
        caja_usu_pass.delete(0, tk.END)
        id_usuario_sel.set("")
        if combo_usu_perfil['values']:
            combo_usu_perfil.current(0)

    def cargar_perfiles_usuarios():
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("SELECT id_perfil, nombre_perfil FROM PERFILES")
            nombres = []
            mapa_perfiles.clear()
            for id_perf, name_perf in cursor.fetchall():
                nombres.append(name_perf)
                mapa_perfiles[name_perf] = id_perf
            combo_usu_perfil['values'] = nombres
            if nombres: 
                combo_usu_perfil.current(0)
            conexion.close()
        except: pass

    def actualizar_tabla_usuarios():
        for item in tabla_usuarios.get_children(): tabla_usuarios.delete(item)
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("SELECT U.id_usuario, U.username, P.nombre_perfil FROM USUARIOS U JOIN PERFILES P ON U.id_perfil = P.id_perfil")
            for fila in cursor.fetchall(): tabla_usuarios.insert("", "end", values=fila)
            conexion.close()
            limpiar_form_usuarios()
        except: pass

    def guardar_usuario():
        if not caja_usu_nombre.get() or not caja_usu_pass.get() or not combo_usu_perfil.get(): 
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            cursor.execute("INSERT INTO USUARIOS (username, password, id_perfil) VALUES (%s, %s, %s)", 
                           (caja_usu_nombre.get(), caja_usu_pass.get(), mapa_perfiles[combo_usu_perfil.get()]))
            conexion.commit(); conexion.close(); actualizar_tabla_usuarios()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        except mysql.connector.Error as err:
            if err.errno == 1062: 
                messagebox.showerror("Error", "Ese nombre de usuario ya existe en el sistema.")
            else:
                messagebox.showerror("Error", f"No se pudo guardar: {err}")

    def modificar_usuario():
        if not id_usuario_sel.get() or not caja_usu_nombre.get(): return
        try:
            conexion = conectar_db(); cursor = conexion.cursor()
            if not caja_usu_pass.get():
                cursor.execute("UPDATE USUARIOS SET username=%s, id_perfil=%s WHERE id_usuario=%s", 
                               (caja_usu_nombre.get(), mapa_perfiles[combo_usu_perfil.get()], id_usuario_sel.get()))
            else:
                cursor.execute("UPDATE USUARIOS SET username=%s, password=%s, id_perfil=%s WHERE id_usuario=%s", 
                               (caja_usu_nombre.get(), caja_usu_pass.get(), mapa_perfiles[combo_usu_perfil.get()], id_usuario_sel.get()))
            conexion.commit(); conexion.close(); actualizar_tabla_usuarios()
            messagebox.showinfo("Éxito", "Usuario modificado correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo actualizar: {err}")

    def eliminar_usuario():
        if not tabla_usuarios.selection(): return
        
        if id_usuario_sel.get() == str(id_usuario_logueado):
            messagebox.showerror("Operación Denegada", "No puedes eliminar el usuario con el que tienes la sesión activa.")
            return
            
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar al usuario {caja_usu_nombre.get()}?"):
            try:
                conexion = conectar_db(); cursor = conexion.cursor()
                cursor.execute("DELETE FROM USUARIOS WHERE id_usuario = %s", (id_usuario_sel.get(),))
                conexion.commit(); conexion.close(); actualizar_tabla_usuarios()
            except mysql.connector.Error as err:
                if err.errno == 1451: 
                    messagebox.showerror("Error", "No puedes borrar a este usuario porque ya tiene registros de movimientos de stock asociados.")
                else:
                    messagebox.showerror("Error", f"Error al eliminar: {err}")

    def clic_usuario(event):
        if tabla_usuarios.selection():
            valores = tabla_usuarios.item(tabla_usuarios.selection())['values']
            id_usuario_sel.set(valores[0])
            caja_usu_nombre.delete(0, tk.END); caja_usu_nombre.insert(0, valores[1])
            caja_usu_pass.delete(0, tk.END) 
            
            perfil_guardado = str(valores[2])
            if perfil_guardado in combo_usu_perfil['values']:
                combo_usu_perfil.current(combo_usu_perfil['values'].index(perfil_guardado))

    botones_usu = tk.Frame(form_usuarios, bg=COLOR_FONDO)
    botones_usu.grid(row=1, column=2, columnspan=2, pady=5)
    tk.Button(botones_usu, text="Guardar Nuevo", font=("Georgia", 10, "bold"), bg=COLOR_BOTON, fg="black", command=guardar_usuario).pack(side="left", padx=5)
    tk.Button(botones_usu, text="Actualizar", font=("Georgia", 10, "bold"), bg="#3498DB", fg="black", command=modificar_usuario).pack(side="left", padx=5)

    tabla_usuarios = ttk.Treeview(marco_contenido_usuarios, columns=("ID", "Usuario", "Perfil"), show="headings", height=6)
    tabla_usuarios.heading("ID", text="ID"); tabla_usuarios.heading("Usuario", text="Nombre de Usuario"); tabla_usuarios.heading("Perfil", text="Rol / Perfil")
    tabla_usuarios.column("ID", width=50, anchor="center"); tabla_usuarios.column("Usuario", width=200, anchor="center"); tabla_usuarios.column("Perfil", width=200, anchor="center")
    tabla_usuarios.pack(pady=10); tabla_usuarios.bind("<<TreeviewSelect>>", clic_usuario)
    tk.Button(marco_contenido_usuarios, text="Eliminar Seleccionado", font=("Georgia", 10, "bold"), bg="#E74C3C", fg="black", command=eliminar_usuario).pack()

    aplicar_tema_app() 
    vista_menu.tkraise()

# Interfaz Tema Login
def aplicar_tema_login():
    if ES_OSCURO:
        ventana.configure(bg="#1E1E1E")
        contenedor_login.configure(bg="#1E1E1E")
        if not logo_img:
            lbl_titulo_libreria.configure(bg="#1E1E1E", fg="#C48F3E")
        else:
            lbl_logo_login.configure(bg="#1E1E1E")
        frame_login.configure(bg="#2D2D2D")
        lbl_inicio.configure(bg="#2D2D2D", fg="white")
        lbl_u.configure(bg="#2D2D2D", fg="white")
        lbl_p.configure(bg="#2D2D2D", fg="white")
        caja_usuario.configure(bg="#3A3A3A", fg="white", insertbackground="white")
        caja_password.configure(bg="#3A3A3A", fg="white", insertbackground="white")
        btn_tema_login.configure(text="Modo Claro", bg=COLOR_BOTON, fg="black")
    else:
        ventana.configure(bg="#FDF6E3")
        contenedor_login.configure(bg="#FDF6E3")
        if not logo_img:
            lbl_titulo_libreria.configure(bg="#FDF6E3", fg="#C48F3E")
        else:
            lbl_logo_login.configure(bg="#FDF6E3")
        frame_login.configure(bg="#4A3B32")
        lbl_inicio.configure(bg="#4A3B32", fg="white")
        lbl_u.configure(bg="#4A3B32", fg="white")
        lbl_p.configure(bg="#4A3B32", fg="white")
        caja_usuario.configure(bg="white", fg="black", insertbackground="black")
        caja_password.configure(bg="white", fg="black", insertbackground="black")
        btn_tema_login.configure(text="Modo Oscuro", bg=COLOR_BOTON, fg="black")

def alternar_tema_login():
    global ES_OSCURO
    ES_OSCURO = not ES_OSCURO
    aplicar_tema_login()

# Autenticacion de Login
def validar_ingreso(event=None):
    try:
        conexion = conectar_db(); cursor = conexion.cursor()
        cursor.execute("SELECT U.id_usuario, U.username, P.nombre_perfil FROM USUARIOS U JOIN PERFILES P ON U.id_perfil = P.id_perfil WHERE U.username = %s AND U.password = %s", (caja_usuario.get(), caja_password.get()))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado:
            construir_app_principal(resultado[0], resultado[1], resultado[2])
        else:
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Sin conexión a BD: {error}")

# Configuracion base de Ventana Principal
ventana = tk.Tk()
ventana.title("El Gran Poeta - Control de Stock")
ventana.geometry("1024x768")
ventana.minsize(450, 500)

try:
    img = Image.open("logo.png")
    img.thumbnail((400, 400)) 
    logo_img = ImageTk.PhotoImage(img)
except Exception:
    logo_img = None

contenedor_login = tk.Frame(ventana)
contenedor_login.place(relx=0.5, rely=0.5, anchor="center")

if logo_img:
    lbl_logo_login = tk.Label(contenedor_login, image=logo_img)
    lbl_logo_login.pack(pady=(0, 20))
else:
    lbl_titulo_libreria = tk.Label(contenedor_login, text="LIBRERÍA EL GRAN POETA", font=("Georgia", 36, "bold"))
    lbl_titulo_libreria.pack(pady=(0, 20))

frame_login = tk.Frame(contenedor_login, padx=50, pady=40)
frame_login.pack()

lbl_inicio = tk.Label(frame_login, text="INICIO DE SESIÓN", font=FUENTE_TITULO)
lbl_inicio.pack(pady=(0, 20))

lbl_u = tk.Label(frame_login, text="Usuario:", font=FUENTE_TEXTO)
lbl_u.pack(pady=5)
caja_usuario = tk.Entry(frame_login, font=FUENTE_TEXTO, justify="center"); caja_usuario.pack(pady=5)

lbl_p = tk.Label(frame_login, text="Contraseña:", font=FUENTE_TEXTO)
lbl_p.pack(pady=5)
caja_password = tk.Entry(frame_login, font=FUENTE_TEXTO, justify="center", show="*"); caja_password.pack(pady=5)

tk.Button(frame_login, text="INGRESAR", font=FUENTE_BOTON, command=validar_ingreso).pack(pady=(30, 0))

btn_tema_login = tk.Button(contenedor_login, font=("Georgia", 10, "bold"), command=alternar_tema_login)
btn_tema_login.pack(pady=(15, 0))

aplicar_tema_login()

caja_usuario.bind("<Return>", validar_ingreso); caja_password.bind("<Return>", validar_ingreso); caja_usuario.focus()
ventana.mainloop()