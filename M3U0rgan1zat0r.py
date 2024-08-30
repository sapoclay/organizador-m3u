"""
M3UOrganizer - Aplicación para la Gestión de Listas de Reproducción M3U

Este script es el punto de entrada principal para la aplicación M3UOrganizer, 
una herramienta diseñada para facilitar la gestión y organización de listas de reproducción 
en formato M3U. 

El programa utiliza PyQt5 para proporcionar una interfaz gráfica de usuario (GUI) 
que permite cargar, editar, buscar y guardar archivos M3U de manera intuitiva y rápida. 
Los usuarios pueden previsualizar, visualizar y manipular el contenido de listas de reproducción M3U 
a través de dos paneles de texto, con opciones adicionales para copiar, pegar, 
buscar títulos de grupos, y abrir URLs en VLC.

El script realiza las siguientes acciones principales:

1. Configura y lanza la aplicación PyQt5.
2. Inicializa la ventana principal del organizador de M3U (M3UOrganizer).
3. Establece un icono personalizado para la aplicación.
4. Ejecuta el bucle principal de la aplicación para manejar eventos y mantener la GUI activa.

Dependencias:
    - PyQt5: Se utiliza para la creación de la interfaz gráfica de usuario.
    - pathlib: Para manejar rutas de archivos de manera compatible entre plataformas.

Estructura del Proyecto:
    - `m3uorgan1zat0r.py`: Este archivo. El punto de entrada de la aplicación.
    - `organizadorm3u.py`: Contiene la clase principal `M3UOrganizer`, que define la interfaz y la lógica principal.
    - `actions.py`: Define las funciones para manejar acciones del usuario, como copiar, pegar, y mostrar menús contextuales.
    - `threads.py`: Define hilos para cargar archivos M3U y buscar dentro del contenido.
    - `optionsmenu.py`: Contiene funciones para mostrar diálogos de "Acerca de" y "Cómo usar".
    - `url_guardadas.json: Contiene las URL y los nombres que el usuario guarde".

Uso:
    Antes de comenzar, instala las dependencias ejecutando:
    
    ```bash
    pip install -r requirements.txt
    ```
    
    Simplemente ejecuta este script para iniciar la aplicación:

    ```bash
    python3 M3U0rgan1zat0r.py
    ```

Autor:
    - entreunosyceros

Versión:
    0.5

"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from pathlib import Path
from organizadorm3u import M3UOrganizer

# Directorio del script actual
current_directory = Path(__file__).parent

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = M3UOrganizer()
    mainWin.resize(800, 600)
    # Establecer un icono personalizado
    icon_path = current_directory / './resources/ordenar-m3u.png'
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    mainWin.show()
    sys.exit(app.exec_())
