# OOP-Project

Build an application that simulates an inventory management system for a warehouse.

(We've made 2 versions of repositorys, one in english and another one in spanish)

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

```python
python --version
pip --version
```


<img width="1191" height="134" alt="Captura de pantalla 2025-07-20 230414" src="https://github.com/user-attachments/assets/ae645f88-1b62-48db-a213-7fdf9cb9059d" />


If installed correctly, both commands will return their respective versions. Once confirmed, you may proceed.

This project uses a virtual environment. It is important to create it first, as all dependencies will be installed there. You can create the environment using the following command:

```python
python -m venv venv
#Then activate the virtual environment using the command below:
venv\Scripts\activate
```

Since this project uses external libraries, they must be installed with:

```python
pip install pandas openpyxl matplotlib
```

However, one additional library requires account registration.
To install it, you must create an account at: https://www.reportlab.com/accounts/register/
(Make sure to check your username, as it will be required during installation)

To install the package, run:

```python
pip install rlextra -i https://www.reportlab.com/pypi/
```

You’ll be prompted to enter your username and password, after which the download will begin.

# Class diagram
<img width="1329" height="3840" alt="Mermaid_Chart_-_Create_complex_visual_diagrams_with_text _A_smarter_way_of_creating_diagrams -2025-07-20-171544" src="https://github.com/user-attachments/assets/7d83d3de-85d4-4e4d-9a86-eaba15801c0a" />


# Code Definition and Explanation

In the clases.py file, you’ll find all the class definitions for the inventory system

**Class proveedor (or supplier in english but in code terms we'll use the original names in spanish)**

```python
class Proveedor:
    def __init__(self, id: int, nombre, telefono: int, direccion, email):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email

    def informacion_proveedor(self):
        return f"{self.nombre} ({self.telefono})"
```
This class stores the supplier's ID, name, phone number, address, and email. It also includes a method `informacion_proveedor` which returns the name and phone number.

**Clase producto**
```python
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
```

This class represents each product in the inventory, storing attributes like ID, name, description, brand, model, purchase date, quantity, and unit price. The supplier is an instance of the Proveedor class. `sumar_stock` increases the stock while `reducir_stock` decreases the stock __only if there is enough inventory.__ `informacion_producto` returns a string summarizing product info.

**Class inventario**

This is the core of the system, managing the product list and the SQLite database.

```python
def crear_base_datos(self):
```

Creates the necessary tables in the database if they don’t already exist.

```python
def guardar_inventario(self):
```

Saves the products to the productos table and keeps the database up to date..

```python
def hacer_backup(self):
        if not os.path.exists("backups"):
            os.makedirs("backups")
        try:
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy(self.nombre_base_datos, f"backups/inventario_backup_{fecha}.db")
        except FileNotFoundError:
            pass
```

creates a backup of the inventario.db file in a folder named `backups`.
`
```python
    def cargar_inventario_desde_sql(self):
```

Loads products from the database when the app starts..

**Class venta**

This class manages transactions and sales, storing detailed sale information and allowing database registration via PDF receipts.

```python
def generar_pdf(self, nombre_archivo, ventas_acumuladas=[]):
```

This method generates a general PDF receipt with:
- Sale details
- A bar chart summarizing the most sold products

`matplotlib` is used for the chart, and `reportlab` is used to generate the A4-sized PDF.

# gui_inventario.py

```python
import tkinter as tk
from tkinter import messagebox
from clases import Proveedor, Producto, Inventario, Venta
import datetime
```

- `tkinter` is used for the GUI
- `messagebox` shows messages in the screen
- The imported classes are from `clases.py`
- `datetime` manages date fields for purchases and sales

The `iniciar_gui` function defines all interactive functionalities in the main window.

```python
inventario.crear_base_datos()
inventario.cargar_inventario_desde_sql()
ventas_registradas = []
```

- Initializes the database
- Loads existing inventory
- Starts an empty list to track sales in memory

La GUI está construida de la siguiente manera:

```python
ventana = tk.Tk()
ventana.title("Sistema de Inventario de Partes de Autos")
ventana.geometry("600x750")
```
- tk.Tk: Creates the main window
- title: Creates window's name
- geometry: Creates window's size

Then, labels and input fields are created to enter product attributes, like this:

```python
tk.Label(ventana, text="ID del producto:").pack()
entry_id = tk.Entry(ventana)
entry_id.pack()
```

The same applies to the rest of the code where information needs to be entered.

Finally, a button is added to insert the product:

```python
tk.Button(ventana, text="Agregar Producto", command=agregar_producto).pack(pady=10)
```

# Cargar_desde_excel.py

```python
import sqlite3
import pandas as pd
```

Starting with the librarys, we import sqlite3 which allows database access, and pandas which reads the Excel file.

```python
df = pd.read_excel("productos.xlsx", engine='openpyxl')
```
Reads the `productos.xlsx file.` openpyxl is required for .xlsx files.


```python
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
```

Then, each row is processed using `iterrows` and converted into a tuple with their values (int, float, str, etc)

```python
cursor.executemany('''
    INSERT INTO producto (
        id, nombre, descripcion, marca, modelo,
        proveedor_id, fecha_compra, cantidad, precio_unitario
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', productos)
```

Finally, they are inserted into the producto table

# Main.py

This file is where the full program execution begins:

```python
def main():
    inventario = Inventario()
```

Creates an instance of the Inventario class.

```python
if __name__ == "__main__":
    main()
```

This is a Python convention that ensures the file runs only when executed directly.

(For better project visualization, it's recommended to install a PDF and Excel viewer extension in VSCode. This allows you to open files directly within the editor instead of browsing through folders.)
