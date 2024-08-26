"""
optionsmenu.py - Diálogos y Funciones de Menú para M3U Organizer

Este módulo contiene funciones que implementan diálogos informativos y acciones de menú dentro de la aplicación M3U Organizer. 
Proporciona opciones para mostrar información sobre la aplicación, guías de uso, y abrir la URL del repositorio en GitHub.

Funciones:

- `show_about_dialog(main_window)`: Muestra un diálogo "Acerca de" con información sobre la aplicación M3U Organizer.
- `show_how_to_use_dialog(main_window)`: Muestra un diálogo con instrucciones sobre cómo usar la aplicación.
- `open_github_url(main_window)`: Abre la URL del repositorio de la aplicación en GitHub en el navegador web predeterminado.

Parámetros:
- `main_window (QMainWindow)`: La ventana principal de la aplicación, que se pasa como argumento para que los diálogos se abran como modales desde la ventana principal.

Dependencias:
    - PyQt5.QtWidgets: Para manejar los diálogos y la interfaz de usuario.
    - PyQt5.QtGui: Para cargar y mostrar imágenes en los diálogos.
    - webbrowser: Para abrir URLs en el navegador web predeterminado del sistema.
    - pathlib.Path: Para manejar rutas de archivos y directorios de forma segura y eficiente.

Uso:
    Este módulo se importa en `organizadorm3u.py` para proporcionar funciones de menú que permiten a los usuarios ver 
    información sobre la aplicación, aprender a usarla y acceder al código fuente en GitHub.

Autores:
    - entreunosyceros (autor principal)

Versión:
    0.5

Licencia:
    Libre para uso personal y educativo.

"""

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import webbrowser
from pathlib import Path

current_directory = Path(__file__).parent

def show_about_dialog(main_window):
    dialog = QDialog(main_window)
    dialog.setWindowTitle("Acerca de M3U Organizer")

    # Usamos un QHBoxLayout para organizar la imagen a la izquierda y el texto a la derecha
    layout = QHBoxLayout()

    # Cargar y mostrar la imagen
    image_path = current_directory / 'resources/logo.png'
    if image_path.exists():
        pixmap = QPixmap(str(image_path))
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

    # Texto de la descripción
    description_label = QLabel("M3U Organizer (V.0.5) es una herramienta para gestionar listas de reproducción en formato M3U.\n"
                               "Este es un programa escrito por entreunosyceros como un ejercicio práctico de Python.")
    description_label.setWordWrap(True)
    layout.addWidget(description_label)

    dialog.setLayout(layout)
    # Fijar el tamaño del diálogo para que no se pueda redimensionar
    dialog.setFixedSize(dialog.sizeHint())
    dialog.exec_()

def show_how_to_use_dialog(main_window):
    dialog = QDialog(main_window)
    dialog.setWindowTitle("Cómo usar M3U Organizer")

    layout = QVBoxLayout()

    # Texto de la explicación
    instruction_text = ("1. Usa 'Abrir M3U' para cargar una lista de reproducción en el lado izquierdo de la pantalla.\n"
                        "2. Utiliza la opción 'Abrir con VLC' en el menú contextual del ratón para reproducir la URL seleccionada en el lado izquierdo de la pantalla.\n"
                        "3. En el menú contextual del ratón también podrás seleccionar todo el contenido del lado izquierdo de la pantalla.\n"
                        "4. Usa 'Buscar y seleccionar' para buscar un group-title.\n"
                        "5. Arrastra el texto seleccionado de un lado a otro de la pantalla.\n Ordena el texto seleccionado del lado derecho de la pantalla arrastrando o utilizando las opciones del menú del ratón.\n"
                        "6. Puedes copiar la selección al panel derecho y guardar la lista modificada como un archivo m3u.\n")
    instruction_label = QLabel(instruction_text)
    instruction_label.setWordWrap(True)
    layout.addWidget(instruction_label)

    dialog.setLayout(layout)
    # Fijar el tamaño del diálogo para que no se pueda redimensionar
    dialog.setFixedSize(dialog.sizeHint())
    dialog.exec_()

def open_github_url(main_window):
    # URL del repositorio en GitHub
    github_url = "https://github.com/sapoclay/organizador-m3u"
    webbrowser.open(github_url)

def abrir_vpn(self):
    """
    Abre la URL para obtener una VPN gratuita durante 30 días en el navegador web predeterminado.
    """
    webbrowser.open("https://www.expressvpn.com/refer-a-friend/30-days-free?locale=es&referrer_id=40141467&utm_campaign=referrals&utm_medium=copy_link&utm_source=referral_dashboard")

def restore_window(self):
    """
    Restaura la ventana principal si está minimizada o escondida.
    """
    if self.isMinimized() or not self.isVisible():
        self.showNormal()
        self.activateWindow()