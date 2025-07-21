# OOP-Project

Build an application that simulates an inventory management system for a warehouse.

Team Members:

- Danna Gabriela Sánchez Zambrano
- Samuel Nicolás Garzón Gómez
- David Steven Torres Garzón

This project consists of developing an application that allows the management of an auto parts warehouse inventory. It includes several `.py` files where different functionalities are defined, integrating a graphical user interface, an SQLite database, and the export of PDF reports with embedded charts.

This inventory system allows you to:
- Register products with various attributes
- Query, edit, and store inventory in an SQLite database
- Filter sales by date ranges
- Generate PDF receipts including corresponding sales charts
- Rank products by highest and lowest stock
- Interact through a graphical interface built with tkinter


Before starting with the visualization and explanation of the project, it's important to have all requirements properly installed. To verify this, run the following commands in the Windows terminal:

python
python --version
pip --version



<img width="1191" height="134" alt="Captura de pantalla 2025-07-20 230414" src="https://github.com/user-attachments/assets/ae645f88-1b62-48db-a213-7fdf9cb9059d" />


Si está correctamente instalado, ambos comandos devolverán la versión, así podemos continuar al siguiente paso

En este proyecto se hace uso de un entorno virtual, al crear la carpeta es importante que esto sea lo primero que se haga puesto que las dependencias del proyecto se instalarán en el entorno virtual, el cual se puede crear con el siguiente comando en la terminal:

python
python -m venv venv
#Aún falta activar el entorno virtual para que empiece a funcionar, este se activará usando el siguiente comando
venv\Scripts\activate


Puesto que en este proyecto se hace uso de diferentes librerías externas, también se instalarán en la terminal usando el siguiente comando

python
pip install pandas openpyxl matplotlib


Sin embargo, aún falta una librería, la cual para instalarse es necesario crear una cuenta en la página web de esta misma
- Link para registrarse (es importante consultar su nombre de usuario antes de continuar ya que este se pide durante la instalación) https://www.reportlab.com/accounts/register/

Finalmente, para la instalación de este programa se utilizará el siguiente comando en la terminal

python
pip install rlextra -i https://www.reportlab.com/pypi/


Se solicitará el nombre de usuario y la contraseña que se introdujo cuando se creó la cuenta, posteriormente iniciará la descarga

# Diagrama de clases
<img width="1329" height="3840" alt="Mermaid_Chart_-_Create_complex_visual_diagrams_with_text _A_smarter_way_of_creating_diagrams -2025-07-20-171544" src="https://github.com/user-attachments/assets/7d83d3de-85d4-4e4d-9a86-eaba15801c0a" />


# Definición y explicación de código

En nuestro archivo clases.py se encuentra toda la información de las clases del sistema de inventario

**Clase proveedor**

python
class Proveedor:
    def __init__(self, id: int, nombre, telefono: int, direccion, email):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email

    def informacion_proveedor(self):
        return f"{self.nombre} ({self.telefono})"

La clase proveedor guarda información tal como ID, nombre del proveedor, teléfono, dirección y correo electronico, adicionalmente, tiene un metodo informacion_proveedor el cual retirna el nombre y teléfono del proveedor.

**Clase producto**
python
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


Esta clase representa cada producto que se maneja en el inventario como ID, nombre, descripción, marca, modelo, fecha de compra, cantidad y precio unitario; proveedor es una instancia de la clase Proveedor. En cuanto a los metodos, sumar_stock suma una cantidad al stock actual del producto, mientras que reducir_stock le resta unidades al stock actual __solo si hay suficiente,__ si no hay inventario suficiente, no hace nada. informacion_producto devuelve un string con el nombre, marca, modelo y cantidad de un producto en inventario

**Clase inventario**

La clase inventario es el núcleo del sistema de gestión de productos, puesto que maneja la lista de productos y la base de datos SQLite


python
def crear_base_datos(self):


Este metodo crea las tablas necesarias en la base de datos SQLite si no existen,  lo cual permite inicializar la estructura para guardar la información de productos, ventas y proveedores.

python
def guardar_inventario(self):


Guarda los productos dentro de la tabla productos de la base de datos y está constantemente actualizando la base de datos.

python
def hacer_backup(self):
        if not os.path.exists("backups"):
            os.makedirs("backups")
        try:
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy(self.nombre_base_datos, f"backups/inventario_backup_{fecha}.db")
        except FileNotFoundError:
            pass


Crea una copia de seguridad del archivo inventario.db dentro de una carpeta llamada backups

python
    def cargar_inventario_desde_sql(self):


Lee los productos almacenados en la base de datos y los carga al iniciar la aplicación para que estén disponibles.

**Clase venta**

Esta clase representa el sistema de transacciones de ventas en el sistema de inventario, almacenando la información detallada sobre la venta y adicionalmente permite generar registros en la base de datos por medio de comprobantes en pdf.

python
def generar_pdf(self, nombre_archivo, ventas_acumuladas=[]):


Este método genera un comprobante general en pdf que incluye:
- Detalles individuales de cada venta
- Un gráfico de barras con el resumen de los productos más vendidos.

Para el gráfico se hace uso de la librería matplotlib que fue instalada previamente, y para el pdf se usa reportlab que crea un pdf de tamaño A4

# gui_inventario.py

python
import tkinter as tk
from tkinter import messagebox
from clases import Proveedor, Producto, Inventario, Venta
import datetime


En cuanto a las importaciones, contamos con 4. tkinter crea la GUI, messagebox muestra mensajes al usuario, la importación de clases trae las clases definidas anteriormente en clases.py, en cuanto a datetime esta sirve para registrar fechas de compra y venta. 


En cuanto a la función principal iniciar_gui esta define todas las funcionalidades internas que se pueden realizar desde la ventana

python
inventario.crear_base_datos()
inventario.cargar_inventario_desde_sql()
ventas_registradas = []


- Se crea la base de datos si no existe
- Se cargan productos existentes desde SQLite
- Se inicia una lista vacia para registrar ventas en memoria

La GUI está construida de la siguiente manera:

python
ventana = tk.Tk()
ventana.title("Sistema de Inventario de Partes de Autos")
ventana.geometry("600x750")

- tk.Tk: Crea la ventana principal
- title: Define el nombre de la ventana
- geometry: Define el tamaño de la ventana

Se crea un titulo, y posteriormente se crean los campos para introducir los atributos del producto:

python
tk.Label(ventana, text="ID del producto:").pack()
entry_id = tk.Entry(ventana)
entry_id.pack()


Esto se repite con el resto del código en donde se necesite introducir información.

Finalmente un botón para añadir el producto

python
tk.Button(ventana, text="Agregar Producto", command=agregar_producto).pack(pady=10)


# Cargar_desde_excel.py

python
import sqlite3
import pandas as pd


Empezando con las librerías, se importa sqlite3 para conectarse y ejecutar comandos en la base de datos SQLite, y pandas para leer y manejar el archivo excel.

python
df = pd.read_excel("productos.xlsx", engine='openpyxl')

Aquí se lee el archivo productos.xlsx, el siguiente método se usa obligatoriamente en todos los archivos .xlsx


python
productos = [
    (
        int(row["id"]),
        str(row["nombre"]),
        str(row["descripcion"]),
        str(row["marca"]),
        str(row["modelo"]),
        int(row["proveedor_id"]),
        str(row["fecha_compra"]),
        int(row["cantidad"]),
        float(row["precio_unitario"])
    )
    for _, row in df.iterrows()
]


Se recorre cada fila haciendo uso de iterrows y cada fila se convierte en una tupla que convierte los valores en sus tipos correspondientes (int, float, str, etc)

python
cursor.executemany('''
    INSERT INTO producto (
        id, nombre, descripcion, marca, modelo,
        proveedor_id, fecha_compra, cantidad, precio_unitario
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', productos)


Se insertan las tuplas en la tabla producto y se insertan los datos en la tabla

# Main.py

Finalmente, desde el archivo main.py ocurre toda la ejecución del programa y allí será donde se use

python
def main():
    inventario = Inventario()


Crea una instancia del inventario para gestionar productos y ventas en la base de datos

python
if __name__ == "__main__":
    main()


Este archivo es una convención de python para que el archivo se ejecute directamente desde main.py

(Para una mejor visualización del programa se recomienda instalar una extensión desde vscode de lector y visualizador de archivos PDF y .xlsx, esto se hace para poder visualizar los archivos desde vscode y no tener que ir hasta la carpeta de origen para verlos)
