"""
actions.py - Funciones de Acción para M3U Organizer

Este módulo contiene las acciones relacionadas con la interacción del usuario en una aplicación PyQt5
que gestiona listas de reproducción M3U y URLs para su reproducción con VLC. 

Además, este módulo interactúa con el sistema de archivos para guardar y cargar URLs, 
y utiliza la `vlc` para reproducir vídeos fuera del programa.

Funciones:
----------
- copy_selection(main_window): Copia el texto seleccionado en el QTextEdit enfocado.
- paste_selection(main_window): Pega el texto del portapapeles en el QTextEdit enfocado.
- show_context_menu(main_window, position): Muestra un menú contextual en la posición dada 
  con opciones de copiar, pegar, abrir en VLC, previsualizar streaming y seleccionar todo.
- open_with_vlc(main_window, url): Abre la URL dada en VLC según el sistema operativo.
- handle_double_click(main_window, event): Maneja la edición de una línea de texto en un QTextEdit al hacer doble clic.
- VideoDialog(QDialog): Crea una ventana detro del programa para previsualizar un stream de video utilizando 
python-VLC en un widget de video integrado.
- load_urls(): Carga las URLs guardadas desde un archivo JSON.
- save_urls(urls): Guarda las URLs en un archivo JSON.
- guardar_url(self): Muestra un diálogo para guardar una nueva URL bajo un nombre específico.
- ver_urls_guardadas(self): Muestra un diálogo para gestionar las URLs guardadas, permitiendo editarlas, eliminarlas y copiarlas.

Clases:
-------
- VideoDialog: Clase que representa una ventana para previsualizar videos utilizando el paquete python-vlc que se instala con el archivo 
requirements.txt.

"""

from PyQt5.QtWidgets import (QAction, QDialog, QLineEdit, 
                             QApplication, QDialog, QVBoxLayout, QPushButton, QListWidget,
                            QInputDialog, QMenu, QMessageBox, QScrollArea, QWidget)
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QProcess, QTimer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
import vlc
import json
import os

def copy_selection(main_window):
    text_edit = main_window.text_left if main_window.text_left.hasFocus() else main_window.text_right
    text_edit.copy()

def paste_selection(main_window):
    text_edit = main_window.text_left if main_window.text_left.hasFocus() else main_window.text_right
    text_edit.paste()

def show_context_menu(main_window, position):
    cursor = main_window.text_left.textCursor() if main_window.text_left.hasFocus() else main_window.text_right.textCursor()
    selected_text = cursor.selectedText().strip()

    context_menu = QMenu()

    # Opción para copiar el texto seleccionado
    copy_action = QAction("Copiar", main_window)
    copy_action.triggered.connect(lambda: copy_selection(main_window))
    context_menu.addAction(copy_action)

    # Opción para pegar el texto copiado
    paste_action = QAction("Pegar", main_window)
    paste_action.triggered.connect(lambda: paste_selection(main_window))
    context_menu.addAction(paste_action)

    # Opción para abrir con VLC si el texto seleccionado es una URL válida
    if selected_text.startswith("http://") or selected_text.startswith("https://"):
        open_with_vlc_action = QAction("Abrir con VLC", main_window)
        open_with_vlc_action.triggered.connect(lambda: open_with_vlc(main_window, selected_text))
        context_menu.addAction(open_with_vlc_action)

        # Opción para previsualizar en VLC
        preview_action = QAction("Previsualizar Streaming", main_window)
        preview_action.triggered.connect(lambda: main_window.preview_stream_from_menu(selected_text))
        context_menu.addAction(preview_action)

    # Opción para seleccionar todo el texto
    select_all_action = QAction("Seleccionar Todo", main_window)
    select_all_action.triggered.connect(lambda: (main_window.text_left.selectAll() if main_window.text_left.hasFocus() else main_window.text_right.selectAll()))
    context_menu.addAction(select_all_action)

    # Mostrar el menú contextual
    context_menu.exec_(main_window.text_left.mapToGlobal(position) if main_window.text_left.hasFocus() else main_window.text_right.mapToGlobal(position))


def open_with_vlc(main_window, url):
    if sys.platform.startswith('linux'):
        command = f"vlc {url}"
    elif sys.platform.startswith('win'):
        command = f'start vlc "{url}"'
    else:
        QMessageBox.warning(main_window, "Error", "Sistema operativo no soportado.")
        return

    try:
        QProcess.startDetached(command)
    except Exception as e:
        QMessageBox.critical(main_window, "Error", f"No se pudo abrir VLC: {str(e)}")

def handle_double_click(main_window, event):
    # Identificar cuál de los QTextEdit ha recibido el evento
    text_edit = main_window.text_left if main_window.text_left.viewport().underMouse() else main_window.text_right

    cursor = text_edit.cursorForPosition(event.pos())
    cursor.select(QTextCursor.LineUnderCursor)
    selected_text = cursor.selectedText()

    # Personalizar el tamaño de la ventana de edición
    dialog = QInputDialog(main_window)
    dialog.setWindowTitle("Editar línea")
    dialog.setLabelText("Modifica la línea:")
    dialog.setTextValue(selected_text)
    dialog.setFixedSize(400, 150)  # Ajusta el tamaño de la ventana de edición

    ok = dialog.exec_()
    new_text = dialog.textValue()

    if ok:
        cursor.insertText(new_text)
        
class VideoDialog(QDialog):
    def __init__(self, parent=None, instance=None):
        super(VideoDialog, self).__init__(parent)
        self.setWindowTitle("Video Preview")
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 480)
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        self.setLayout(layout)
        self.media_player = None
        self.instance = instance

    def closeEvent(self, event):
        if self.media_player:
            self.media_player.stop()
        event.accept()

    def play_video(self, url):
        try:
            # Crear un nuevo objeto de medios desde la URL
            media = self.instance.media_new(url)
            if not media:
                raise Exception("No se pudo crear el objeto de medios VLC.")
            
            # Establecer la opción vout en opengl
            media.add_option('vout=opengl')
            
            # Asociar el medio con el reproductor
            self.media_player = vlc.MediaPlayer()
            self.media_player.set_media(media)
            
            # Establecer el widget de salida de video según el sistema operativo
            if sys.platform.startswith('linux'):
                self.media_player.set_xwindow(int(self.video_widget.winId()))
            elif sys.platform.startswith('win'):
                self.media_player.set_hwnd(int(self.video_widget.winId()))
            elif sys.platform.startswith('darwin'):  # macOS
                self.media_player.set_nsobject(int(self.video_widget.winId()))

            # Comenzar la reproducción (sin mostrar la ventana aún)
            self.media_player.play()
            print("Reproduciendo URL:", url)  # Mensaje de depuración

            # Esperar un momento para verificar si el stream comienza
            QTimer.singleShot(3000, self.check_stream_status)  # Esperar 3 segundos antes de verificar

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al intentar reproducir el stream: {str(e)}")

    def check_stream_status(self):
        # Comprobar si el estado es Error, Stopped o Ended
        if self.media_player.get_state() in [vlc.State.Error, vlc.State.Stopped, vlc.State.Ended]:
            # Detener el reproductor y mostrar un mensaje de error
            self.media_player.stop()
            QMessageBox.warning(self, "Error de reproducción", "No se pudo reproducir el stream. La URL puede estar inactiva o ser incorrecta.")
            print("El stream no se pudo reproducir.")
            self.close()  # Cerrar la ventana si la reproducción falla
        else:
            self.show()  # Mostrar la ventana solo si la reproducción es exitosa

            
# Acciones sobre las URL a Guardar
def load_urls():
    if not os.path.exists("urls_guardadas.json"):
        return {}
    
    with open("urls_guardadas.json", "r") as file:
        return json.load(file)

def save_urls(urls):
    with open("urls_guardadas.json", "w") as file:
        json.dump(urls, file, indent=4)


def guardar_url(self):
    # Mostrar un cuadro de diálogo para obtener el nombre y la URL
    nombre, ok_pressed = QInputDialog.getText(self, "Guardar URL", "Ingrese un nombre para la URL:")
    if not ok_pressed or not nombre:
        return  # Si el usuario cancela o no ingresa un nombre, salir
    
    url, ok_pressed = QInputDialog.getText(self, "Guardar URL", "Ingrese la URL:")
    if not ok_pressed or not url:
        return  # Si el usuario cancela o no ingresa una URL, salir
    
    urls = load_urls()
    urls[nombre] = url
    save_urls(urls)

    QMessageBox.information(self, "Acción completada", f"URL guardada bajo el nombre '{nombre}'")


def ver_urls_guardadas(self):
    urls = load_urls()

    if not urls:
        QMessageBox.information(self, "Información", "No hay URLs guardadas.")
        return

    # Crear un diálogo para mostrar y gestionar URLs
    dialog = QDialog(self)
    dialog.setWindowTitle("URLs Guardadas")
    layout = QVBoxLayout(dialog)

    # Crear un área de desplazamiento
    scroll_area = QScrollArea(dialog)
    scroll_area.setWidgetResizable(True)

    # Crear un widget contenedor para el área de desplazamiento
    container_widget = QWidget()
    container_layout = QVBoxLayout(container_widget)

    list_widget = QListWidget(container_widget)
    for nombre in urls:
        list_widget.addItem(nombre)

    container_layout.addWidget(list_widget)
    container_widget.setLayout(container_layout)
    scroll_area.setWidget(container_widget)

    layout.addWidget(scroll_area)

    # Añadir botones para editar, eliminar y copiar URL
    edit_button = QPushButton("Editar URL", dialog)
    delete_button = QPushButton("Eliminar URL", dialog)
    copy_button = QPushButton("Copiar URL", dialog)

    def edit_url():
        current_item = list_widget.currentItem()
        if current_item:
            nombre_original = current_item.text()

            # Editar el nombre
            nuevo_nombre, ok_pressed = QInputDialog.getText(dialog, "Editar Nombre", "Modifica el nombre:", text=nombre_original)
            if not ok_pressed or not nuevo_nombre:
                QMessageBox.warning(dialog, "Advertencia", "El nombre no puede estar vacío.")
                return

            # Editar la URL
            nueva_url, ok_pressed = QInputDialog.getText(dialog, "Editar URL", "Modifica la URL:", text=urls[nombre_original])
            if not ok_pressed or not nueva_url:
                QMessageBox.warning(dialog, "Advertencia", "La URL no puede estar vacía.")
                return

            # Actualizar el registro y guardar
            del urls[nombre_original]  # Eliminar el antiguo nombre
            urls[nuevo_nombre] = nueva_url
            save_urls(urls)

            # Actualizar la lista en la UI
            current_item.setText(nuevo_nombre)

            QMessageBox.information(dialog, "Éxito", f"'{nombre_original}' actualizado correctamente a '{nuevo_nombre}'.")

    def delete_url():
        current_item = list_widget.currentItem()
        if current_item:
            nombre = current_item.text()
            del urls[nombre]
            save_urls(urls)
            list_widget.takeItem(list_widget.row(current_item))
            QMessageBox.information(dialog, "Éxito", f"URL '{nombre}' eliminada correctamente.")

    def copy_url():
        current_item = list_widget.currentItem()
        if current_item:
            nombre = current_item.text()
            url = urls[nombre]
            clipboard = QApplication.clipboard()
            clipboard.setText(url)
            QMessageBox.information(dialog, "Éxito", f"URL '{url}' copiada al portapapeles.")

    edit_button.clicked.connect(edit_url)
    delete_button.clicked.connect(delete_url)
    copy_button.clicked.connect(copy_url)

    layout.addWidget(edit_button)
    layout.addWidget(delete_button)
    layout.addWidget(copy_button)

    dialog.setLayout(layout)
    dialog.exec_()