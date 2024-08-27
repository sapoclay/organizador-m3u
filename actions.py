"""
actions.py - Funciones de Acción para M3U Organizer

Este módulo contiene funciones que manejan diversas acciones dentro de la aplicación M3U Organizer. 
Las funciones aquí definidas se encargan de operaciones como copiar y pegar texto, mostrar menús contextuales, 
abrir URLs en VLC, y manejar eventos de doble clic para editar líneas en la interfaz de usuario.

Funciones:

- `copy_selection(main_window)`: Copia el texto seleccionado del área de texto que tiene el foco en la ventana principal.
- `paste_selection(main_window)`: Pega el texto copiado en el área de texto que tiene el foco en la ventana principal.
- `show_context_menu(main_window, position)`: Muestra un menú contextual en la posición dada, ofreciendo opciones para copiar, pegar, seleccionar todo, y abrir URLs en VLC.
- `open_with_vlc(main_window, url)`: Abre una URL en VLC, dependiendo del sistema operativo.
- `handle_double_click(main_window, event)`: Maneja el evento de doble clic en un área de texto, permitiendo al usuario editar la línea seleccionada.

Parámetros:
- `main_window (QMainWindow)`: La ventana principal de la aplicación, que contiene las áreas de texto y otros widgets.
- `position (QPoint)`: La posición donde se debe mostrar el menú contextual.
- `event (QMouseEvent)`: El evento de ratón que desencadena la acción de doble clic.
- `url (str)`: La URL que se intenta abrir con VLC.

Dependencias:
    - PyQt5.QtWidgets: Para manejar widgets y diálogos en la GUI.
    - PyQt5.QtGui: Para trabajar con cursores y eventos gráficos.
    - PyQt5.QtCore: Para manejar procesos y eventos.
    - sys: Para identificar el sistema operativo y manejar excepciones.

Uso:
    Este módulo se importa en `organizadorm3u.py` y sus funciones se conectan a eventos de usuario 
    (como clics y selecciones) para realizar las acciones correspondientes.

Autores:
    - entreunosyceros (autor principal)

Versión:
    0.5

Licencia:
    Libre para uso personal y educativo.

"""

from PyQt5.QtWidgets import QAction, QMenu, QMessageBox, QInputDialog, QMessageBox, QVBoxLayout, QDialog
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QProcess
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
import vlc

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
        preview_action = QAction("Previsualizar en VLC", main_window)
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


            # Reproducir el stream
            self.media_player.play()
            print("Reproduciendo URL:", url)  # Mensaje de depuración


        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al intentar reproducir el stream: {str(e)}")