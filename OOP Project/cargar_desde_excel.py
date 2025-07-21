import sqlite3
import pandas as pd

df = pd.read_excel("productos.xlsx", engine='openpyxl')

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

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS producto (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        marca TEXT,
        modelo TEXT,
        proveedor_id INTEGER,
        fecha_compra TEXT,
        cantidad INTEGER,
        precio_unitario REAL
    )
''')

cursor.executemany('''
    INSERT INTO producto (
        id, nombre, descripcion, marca, modelo,
        proveedor_id, fecha_compra, cantidad, precio_unitario
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', productos)

conn.commit()
conn.close()

print("Carga masiva completada correctamente.")
