from clases import Inventario
from gui_inventario import iniciar_gui

def main():
    inventario = Inventario()
    inventario.crear_base_datos()
    inventario.cargar_inventario_desde_sql()
    iniciar_gui(inventario)

if __name__ == "__main__":
    main()
