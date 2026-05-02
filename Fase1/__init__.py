import sys
import os

# 1. Obtenemos la ruta de la carpeta donde está este main.py (Fase 1)
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# 2. Obtenemos la ruta de la carpeta raíz (TEA) subiendo un nivel
ruta_raiz = os.path.join(directorio_actual, "..")

# 3. La normalizamos y la añadimos al sistema de búsqueda de Python
ruta_raiz_absoluta = os.path.abspath(ruta_raiz)
if ruta_raiz_absoluta not in sys.path:
    sys.path.insert(0, ruta_raiz_absoluta)
