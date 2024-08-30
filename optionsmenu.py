"""
optionsmenu.py - Diálogos y Funciones de Menú para M3U Organizer

Este módulo contiene las funciones relacionadas con el menú de opciones de la aplicación M3U Organizer, 
incluyendo diálogos informativos y enlaces a recursos en línea.

Funciones:
----------
- show_about_dialog(main_window): Muestra un cuadro de diálogo con información sobre la aplicación, 
  incluyendo una breve descripción y un logotipo.
- show_how_to_use_dialog(main_window): Muestra un cuadro de diálogo con instrucciones detalladas sobre 
  cómo usar M3U Organizer, incluyendo el formato de listas M3U y las funcionalidades principales de la aplicación.
- open_github_url(main_window): Abre la página del repositorio GitHub del proyecto en el navegador web predeterminado.
- abrir_vpn(self): Abre una URL en el navegador para obtener una VPN gratuita durante 30 días.
- restore_window(self): Restaura la ventana principal si está minimizada o no visible, devolviéndola a su estado normal.

Este módulo está diseñado para proporcionar acceso a recursos adicionales y 
ayuda al usuario, así como para manejar algunas acciones relacionadas con la interfaz de usuario.

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
    image_path = current_directory / './resources/logo.png'
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
    instruction_text = ("0. Formato de lista .m3u válido:\n"
                        "#EXTM3U\n"
                        "#EXTINF:-1 ETIQUETAS\n"
                        "http://URL-DEL-STREAMING\n"
                        "#EXTINF:-1 ETIQUETAS\n"
                        "http://URL-DEL-STREAMING\n"
                        "---------------------------\n"
                        "1. Usa 'Abrir M3U' para cargar una lista de reproducción en el lado izquierdo de la pantalla.\n"
                        "2. Utiliza la opción 'Abrir con VLC' en el menú contextual del ratón para reproducir la URL seleccionada en el lado izquierdo de la pantalla.\n"
                        "3. En el menú contextual del ratón también podrás seleccionar todo el contenido del lado izquierdo de la pantalla.\n"
                        "4. Usa 'Buscar y seleccionar' para buscar un group-title.\n"
                        "5. El usuario podrá previsualizar el streaming de la URL seleccionada en el lado izquierdo de pantalla.\n También podrá directamente abrir la URL con VLC para ver el streaming."
                        "6. Arrastra el texto seleccionado de un lado a otro de la pantalla.\n Ordena el texto seleccionado del lado derecho de la pantalla arrastrando o utilizando las opciones del menú del ratón.\n"
                        "7. Puedes copiar la selección al panel derecho y guardar la lista modificada como un archivo m3u.\n")
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
        
