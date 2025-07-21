import sqlite3
from datetime import datetime
import shutil
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from matplotlib import pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

class Proveedor:
    def __init__(self, id: int, nombre, telefono: int, direccion, email):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email

    def informacion_proveedor(self):
        return f"{self.nombre} ({self.telefono})"

class Producto:
    def __init__(self, id: int, nombre, descripcion, marca, modelo, proveedor: Proveedor, fecha_compra: datetime, cantidad, precio_unitario):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.marca = marca
        self.modelo = modelo
        self.proveedor = proveedor
        self.fecha_compra = fecha_compra
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def sumar_stock(self, cantidad):
        self.cantidad += cantidad

    def reducir_stock(self, cantidad):
        if self.cantidad < cantidad:
            return
        self.cantidad -= cantidad

    def informacion_producto(self):
        return f"{self.nombre} - {self.marca} {self.modelo} ({self.cantidad} unidades)"

class Inventario:
    def __init__(self):
        self.productos = []
        self.nombre_base_datos = "inventario.db"

    def buscar_por_id(self, id_producto):
        for producto in self.productos:
            if producto.id == id_producto:
                return producto
        return None

    def crear_base_datos(self):
        conexion = sqlite3.connect(self.nombre_base_datos)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ventas (
                id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER,
                producto_nombre TEXT,
                cantidad_vendida INTEGER,
                precio_unitario REAL,
                total REAL,
                fecha_venta TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Proveedores (
                id INTEGER,
                nombre TEXT,
                telefono INTEGER,
                direccion TEXT,
                email TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                marca TEXT,
                modelo TEXT,
                proveedor_id INTEGER,
                proveedor_nombre TEXT,
                proveedor_telefono INTEGER,
                proveedor_direccion TEXT,
                proveedor_email TEXT,
                fecha_compra TEXT,
                cantidad INTEGER,
                precio_unitario REAL
            )
        ''')
        conexion.commit()
        conexion.close()

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def guardar_inventario(self):
        conexion = sqlite3.connect(self.nombre_base_datos)
        cursor = conexion.cursor()
        for producto in self.productos:
            cursor.execute('''
                INSERT OR REPLACE INTO Productos (
                    id, nombre, descripcion, marca, modelo,
                    proveedor_id, proveedor_nombre, proveedor_telefono,
                    proveedor_direccion, proveedor_email,
                    fecha_compra, cantidad, precio_unitario
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                producto.id,
                producto.nombre,
                producto.descripcion,
                producto.marca,
                producto.modelo,
                producto.proveedor.id,
                producto.proveedor.nombre,
                producto.proveedor.telefono,
                producto.proveedor.direccion,
                producto.proveedor.email,
                producto.fecha_compra.strftime("%Y-%m-%d %H:%M:%S"),
                producto.cantidad,
                producto.precio_unitario
            ))
        conexion.commit()
        conexion.close()

    def hacer_backup(self):
        if not os.path.exists("backups"):
            os.makedirs("backups")
        try:
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy(self.nombre_base_datos, f"backups/inventario_backup_{fecha}.db")
        except FileNotFoundError:
            pass

    
    def cargar_inventario_desde_sql(self):
        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, nombre, descripcion, marca, modelo,
                proveedor_id, proveedor_nombre, fecha_compra,
                cantidad, precio_unitario
            FROM Productos
        """)
        filas = cursor.fetchall()
        self.productos = []
        for fila in filas:
            (
                id_producto, nombre, descripcion, marca, modelo,
                proveedor_id, proveedor_nombre, fecha_compra,
                cantidad, precio_unitario
            ) = fila

            proveedor = Proveedor(proveedor_id, proveedor_nombre, 0, "", "")
            fecha = datetime.fromisoformat(fecha_compra)

            producto = Producto(
                id_producto, nombre, descripcion, marca, modelo,
                proveedor, fecha, cantidad, precio_unitario
            )
            self.productos.append(producto)
        conexion.close()

    def obtener_ventas(self):
        conexion = sqlite3.connect(self.nombre_base_datos)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Ventas")
        ventas = cursor.fetchall()
        conexion.close()
        return ventas

class Venta:
    def __init__(self, id, producto, cantidad, precio_unitario, fecha_venta):
        self.id = id
        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.fecha_venta = fecha_venta
        self.precio_total = 0

        if self.cantidad > self.producto.cantidad:
            raise ValueError(f"Stock insuficiente para el producto {self.producto.nombre}.")
        self.precio_total += self.precio_unitario * self.cantidad
        self.guardar_venta()

    def guardar_venta(self):
        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()
        total_producto = self.precio_unitario * self.cantidad
        cursor.execute('''
            INSERT INTO Ventas (producto_id, producto_nombre, cantidad_vendida, precio_unitario, total, fecha_venta)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.producto.id,
            self.producto.nombre,
            self.cantidad,
            self.precio_unitario,
            total_producto,
            self.fecha_venta.isoformat()
        ))
        conexion.commit()
        conexion.close()

    def generar_pdf(self, nombre_archivo, ventas_acumuladas=[]):
        resumen = {}
        for venta in ventas_acumuladas:
            nombre = venta.producto.nombre
            resumen[nombre] = resumen.get(nombre, 0) + venta.cantidad

        productos = list(resumen.keys())
        cantidades = list(resumen.values())

        plt.figure(figsize=(6, 3))
        plt.bar(productos, cantidades, color='skyblue')
        plt.title("Histórico de productos vendidos")
        plt.ylabel("Unidades vendidas")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("grafico_ventas.png")
        plt.close()

        c = canvas.Canvas(nombre_archivo, pagesize=A4)
        width, height = A4
        margin = 50
        y = height - margin

        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, y, "Comprobante general de ventas")
        y -= 40

        c.setFont("Helvetica", 12)
        line_spacing = 18

        for venta in ventas_acumuladas:
            detalles = [
                f"Fecha: {venta.fecha_venta.strftime('%Y-%m-%d %H:%M:%S')}",
                f"Producto: {venta.producto.nombre}",
                f"Descripción: {venta.producto.descripcion}",
                f"Marca: {venta.producto.marca} | Modelo: {venta.producto.modelo}",
                f"Proveedor: {venta.producto.proveedor.nombre} ({venta.producto.proveedor.telefono})",
                f"Cantidad vendida: {venta.cantidad}",
                f"Precio unitario: ${venta.precio_unitario:,.2f}",
                f"Total: ${venta.cantidad * venta.precio_unitario:,.2f}",
                f"Stock restante: {venta.producto.cantidad}",
                "-" * 80
            ]

            for linea in detalles:
                if y < margin + 100:
                    c.showPage()
                    y = height - margin
                    c.setFont("Helvetica", 12)
                c.drawString(margin, y, linea)
                y -= line_spacing
                
        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, height - margin, "Gráfico de productos más vendidos")

        if os.path.exists("grafico_ventas.png"):
            try:
                img = ImageReader("grafico_ventas.png")
                c.drawImage(img, margin, height - 400, width=480, height=300, preserveAspectRatio=True)
            except Exception as e:
                c.drawString(margin, height - 100, f"No se pudo cargar el gráfico: {str(e)}")

        c.save()
