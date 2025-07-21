import tkinter as tk
from tkinter import messagebox
from clases import Proveedor, Producto, Inventario, Venta
import datetime

def iniciar_gui(inventario):
    inventario.crear_base_datos()
    inventario.cargar_inventario_desde_sql()

    
    ventas_registradas = []

    def agregar_producto():
        try:
            id_producto = int(entry_id.get())
            nombre = entry_nombre.get()
            descripcion = entry_descripcion.get()
            marca = entry_marca.get()
            modelo = entry_modelo.get()
            proveedor = Proveedor(1, "N/A", "N/A", "", "")
            fecha_compra = datetime.datetime.now()
            cantidad = int(entry_cantidad.get())
            precio_unitario = float(entry_precio.get())

            producto = Producto(id_producto, nombre, descripcion, marca, modelo, proveedor, fecha_compra, cantidad, precio_unitario)
            inventario.agregar_producto(producto)
            inventario.guardar_inventario()
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado al inventario.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def registrar_venta():
        try:
            id_producto = int(entry_id_venta.get())
            cantidad = int(entry_cantidad_venta.get())
            producto = inventario.buscar_por_id(id_producto)
            if producto is None:
                messagebox.showerror("Error", "Producto no encontrado.")
                return
            if cantidad > producto.cantidad:
                messagebox.showerror("Error", "Cantidad no disponible en inventario.")
                return

            fecha_venta = datetime.datetime.now()
            venta = Venta(len(ventas_registradas)+1, producto, cantidad, producto.precio_unitario, fecha_venta)
            producto.cantidad -= cantidad
            venta.guardar_venta()
            ventas_registradas.append(venta)
            # nombre_pdf = f"comprobante_venta_{len(ventas_registradas)}.pdf"
            # venta.generar_pdf(nombre_pdf)
            inventario.guardar_inventario()
            messagebox.showinfo("Venta registrada", f"Venta registrada")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def filtrar_ventas_por_fecha():
        try:
            inicio = datetime.datetime.strptime(entry_fecha_inicio.get(), "%Y-%m-%d")
            fin = datetime.datetime.strptime(entry_fecha_fin.get(), "%Y-%m-%d")

            print([str(v) for v in ventas_registradas]) 
            ventas_en_rango = [
                v for v in ventas_registradas 
                if inicio.date() <= v.fecha_venta.date() <= fin.date()
            ]

            if not ventas_en_rango:
                messagebox.showinfo("Sin resultados", "No hay ventas en ese rango de fechas.")
                return
            resultado = "\n\n".join([
                f"{v.fecha_venta.strftime('%Y-%m-%d %H:%M:%S')} - {v.producto.nombre} x{v.cantidad} = ${v.cantidad * v.precio_unitario:,.2f}"
                for v in ventas_en_rango
            ])
            messagebox.showinfo("Ventas en rango", resultado)

        except ValueError:
            messagebox.showerror("Formato incorrecto", "Usa el formato YYYY-MM-DD para las fechas.")

    def generar_comprobante_general():
        if not ventas_registradas:
            messagebox.showinfo("Sin datos", "No hay ventas registradas aún.")
            return
        try:
            ventas_registradas[-1].generar_pdf("comprobante_general.pdf", ventas_acumuladas=ventas_registradas)
            messagebox.showinfo("Comprobante generado", "Se ha creado 'comprobante_general.pdf'.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_ranking_stock():
        productos = inventario.productos
        if not productos:
            messagebox.showinfo("Inventario vacío", "No hay productos en el inventario.")
            return

        stock_list = [(p.nombre, p.cantidad) for p in productos]
        stock_list.sort(key=lambda x: x[1], reverse=True)

        top_3 = stock_list[:3]
        bottom_3 = stock_list[-3:]

        mensaje = "Productos con más stock:\n" + "\n".join([f"{p[0]}: {p[1]}" for p in top_3]) + "\n\n"
        mensaje += "Productos con menos stock:\n" + "\n".join([f"{p[0]}: {p[1]}" for p in bottom_3])

        messagebox.showinfo("Ranking de stock", mensaje)

    # --- GUI ---
    ventana = tk.Tk()
    ventana.title("Sistema de Inventario de Partes de Autos")
    ventana.geometry("600x750")

    tk.Label(ventana, text="Agregar Producto al Inventario", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(ventana, text="ID del producto:").pack()
    entry_id = tk.Entry(ventana)
    entry_id.pack()
    tk.Label(ventana, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()
    tk.Label(ventana, text="Descripción:").pack()
    entry_descripcion = tk.Entry(ventana)
    entry_descripcion.pack()
    tk.Label(ventana, text="Marca:").pack()
    entry_marca = tk.Entry(ventana)
    entry_marca.pack()
    tk.Label(ventana, text="Modelo:").pack()
    entry_modelo = tk.Entry(ventana)
    entry_modelo.pack()
    tk.Label(ventana, text="Cantidad:").pack()
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.pack()
    tk.Label(ventana, text="Precio unitario:").pack()
    entry_precio = tk.Entry(ventana)
    entry_precio.pack()
    tk.Button(ventana, text="Agregar Producto", command=agregar_producto).pack(pady=10)

    tk.Label(ventana, text="Registrar Venta", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(ventana, text="ID del producto a vender:").pack()
    entry_id_venta = tk.Entry(ventana)
    entry_id_venta.pack()
    tk.Label(ventana, text="Cantidad a vender:").pack()
    entry_cantidad_venta = tk.Entry(ventana)
    entry_cantidad_venta.pack()
    tk.Button(ventana, text="Registrar Venta", command=registrar_venta).pack(pady=10)
    tk.Button(ventana, text="Generar comprobante general", command=generar_comprobante_general).pack(pady=10)
    tk.Label(ventana, text="Ver ventas por rango de fechas", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(ventana, text="Fecha inicio (YYYY-MM-DD):").pack()
    entry_fecha_inicio = tk.Entry(ventana)
    entry_fecha_inicio.pack()

    tk.Label(ventana, text="Fecha fin (YYYY-MM-DD):").pack()
    entry_fecha_fin = tk.Entry(ventana)
    entry_fecha_fin.pack()

    tk.Button(ventana, text="Filtrar ventas por fecha", command=filtrar_ventas_por_fecha).pack(pady=5)
    tk.Button(ventana, text="Mostrar ranking de stock", command=mostrar_ranking_stock).pack(pady=5)

    ventana.mainloop()
