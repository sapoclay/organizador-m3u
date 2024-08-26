"""
organizadorm3u.py - Interfaz principal de M3U Organizer

Este módulo define la clase `M3UOrganizer`, que representa la ventana principal de la aplicación M3U Organizer. 
La clase gestiona la interfaz gráfica de usuario (GUI), incluyendo la carga y guardado de archivos M3U, 
la interacción del usuario a través de menús, y la ejecución de hilos para tareas en segundo plano.

Clases:

- `M3UOrganizer`: Hereda de `QMainWindow` y proporciona la funcionalidad principal de la aplicación, 
  permitiendo al usuario gestionar listas de reproducción en formato M3U.

Métodos:

- `__init__(self)`: Constructor que inicializa la interfaz de usuario y los componentes principales.
- `initUI(self)`: Configura la interfaz gráfica, crea menús y establece las conexiones para los eventos de usuario.
- `load_m3u(self)`: Abre un diálogo para seleccionar y cargar un archivo M3U en el editor de texto izquierdo.
- `update_progress(self, value)`: Actualiza el progreso de la carga del archivo en un diálogo de progreso.
- `append_text_to_left(self, text)`: Añade texto al editor de texto izquierdo, ignorando líneas específicas.
- `on_file_loaded(self)`: Maneja la finalización de la carga del archivo, cerrando el diálogo de progreso.
- `cancel_loading(self)`: Cancela la carga del archivo si el usuario así lo indica.
- `append_lines_to_text_edit(self, text_edit, lines)`: Añade líneas de texto al editor con formato de color según el tipo de contenido.
- `append_colored_text_with_cursor(self, cursor, text, color)`: Inserta texto coloreado en la posición actual del cursor.
- `on_lines_loaded(self, line)`: Maneja la carga de líneas en grupos para evitar sobrecargar la UI.
- `save_m3u(self)`: Guarda el contenido del editor de texto derecho en un archivo M3U.
- `search_group_title(self)`: Busca y resalta un término específico en el editor de texto izquierdo.
- `on_search_finished(self, positions)`: Resalta todas las coincidencias encontradas durante la búsqueda.
- `closeEvent(self, event)`: Pregunta al usuario si desea cerrar la aplicación y maneja el cierre seguro de hilos.
- `close_all_threads_and_processes(self)`: Cierra todos los hilos y procesos en ejecución antes de salir de la aplicación.

Dependencias:
    - PyQt5.QtWidgets: Para manejar la ventana principal, menús, diálogos y otros widgets.
    - PyQt5.QtGui: Para trabajar con cursores, formatos de texto y colores.
    - PyQt5.QtCore: Para gestionar hilos, señales y otros eventos.
    - pathlib.Path: Para manejar rutas de archivos y directorios.
    - `optionsmenu`: Importa funciones para mostrar diálogos de opciones y abrir URLs.
    - `actions`: Importa funciones que manejan acciones como copiar, pegar y mostrar menús contextuales.
    - `threads`: Importa clases que gestionan tareas de carga de archivos y búsqueda en segundo plano.

Uso:
    Este módulo se ejecuta como la ventana principal cuando se inicia la aplicación M3U Organizer, proporcionando 
    todas las funcionalidades necesarias para gestionar listas de reproducción M3U.

Autores:
    - entreunosyceros (autor principal)

Versión:
    0.5

Licencia:
    Libre para uso personal y educativo.

"""

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QHBoxLayout, QWidget, QAction, QFileDialog, QMessageBox, QInputDialog,  QProgressDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QBrush, QColor
from pathlib import Path
from optionsmenu import show_about_dialog, show_how_to_use_dialog, open_github_url
from actions import copy_selection, paste_selection, show_context_menu, open_with_vlc, handle_double_click
from threads import LoadFileThread, SearchThread
import requests  # Importa la librería requests para realizar la descarga

# Directorio del script actual
current_directory = Path(__file__).parent

class M3UOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.threads = []  # Inicializa el atributo threads

    def initUI(self):
        self.loaded_lines = []  # Inicializar lista para acumular líneas cargadas
        self.setWindowTitle('M3U 0rgan1zat0r')

        # Crear los widgets
        self.text_left = QTextEdit()
        self.text_right = QTextEdit()

        # Hacer que ambos cuadros de texto acepten arrastrar y soltar
        self.text_left.setAcceptDrops(True)
        self.text_right.setAcceptDrops(True)

        # Crear el diseño
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.text_left)
        h_layout.addWidget(self.text_right)

        container = QWidget()
        container.setLayout(h_layout)
        self.setCentralWidget(container)

        # Crear el menú
        menubar = self.menuBar()

        # Menú Archivo
        file_menu = menubar.addMenu('Archivo')
        open_action = QAction('Abrir M3U local', self)
        open_from_url_action = QAction('Abrir M3U desde URL', self)  
        save_action = QAction('Guardar M3U', self)
        exit_action = QAction('Salir', self)
        open_action.triggered.connect(self.load_m3u)
        open_from_url_action.triggered.connect(self.load_m3u_from_url) 
        save_action.triggered.connect(self.save_m3u)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(open_action)
        file_menu.addAction(open_from_url_action)  
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        # Menú Editar
        edit_menu = menubar.addMenu('Editar')
        search_action = QAction('Buscar y seleccionar', self)
        copy_action = QAction('Copiar selección', self)
        paste_action = QAction('Pegar', self)
        search_action.triggered.connect(self.search_group_title)
        copy_action.triggered.connect(lambda: copy_selection(self))
        paste_action.triggered.connect(lambda: paste_selection(self))
        edit_menu.addAction(search_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        # Menú Opciones
        options_menu = menubar.addMenu('Opciones')

        # Subopción Acerca de
        about_action = QAction('Acerca de', self)
        about_action.triggered.connect(lambda: show_about_dialog(self))
        options_menu.addAction(about_action)

        # Subopción Cómo usar
        how_to_use_action = QAction('Cómo usar', self)
        how_to_use_action.triggered.connect(lambda: show_how_to_use_dialog(self))
        options_menu.addAction(how_to_use_action)

        # Subopción Abrir URL del repositorio en GitHub
        open_github_action = QAction('Abrir URL del repositorio en GitHub', self)
        open_github_action.triggered.connect(lambda: open_github_url(self))
        options_menu.addAction(open_github_action)

        # Conectar el menú contextual del texto izquierdo
        self.text_left.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_left.customContextMenuRequested.connect(lambda position: show_context_menu(self, position))

        # Conectar el menú contextual del texto derecho
        self.text_right.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_right.customContextMenuRequested.connect(lambda position: show_context_menu(self, position))

        # Conectar la señal de doble clic a una función
        self.text_left.mouseDoubleClickEvent = lambda event: handle_double_click(self, event)
        self.text_right.mouseDoubleClickEvent = lambda event: handle_double_click(self, event)


    def load_m3u(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir M3U", "", "M3U Files (*.m3u);;All Files (*)", options=options)
        if file_path:
            self.start_loading_m3u(file_path)

    def load_m3u_from_url(self):
        # Solicita al usuario la URL del archivo M3U
        url, ok = QInputDialog.getText(self, 'Abrir M3U desde URL', 'Introduce la URL del archivo M3U:')
        
        if ok and url:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()  # Verifica que la solicitud fue exitosa

                # Guardar temporalmente el archivo M3U descargado
                temp_file_path = str(current_directory / "temp_downloaded.m3u")
                with open(temp_file_path, 'wb') as temp_file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # Filtra los keep-alive chunks
                            temp_file.write(chunk)

                self.start_loading_m3u(temp_file_path)

            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, "Error", f"No se pudo descargar el archivo: {str(e)}")

    def start_loading_m3u(self, file_path):
        """Inicia la carga del archivo M3U, ya sea desde un archivo local o desde una URL."""
        self.text_left.clear()  # Borra el texto actual antes de cargar el nuevo archivo

        self.progress_dialog = QProgressDialog("Cargando archivo...", "Cancelar", 0, 100, self)
        self.progress_dialog.setWindowTitle("Cargando")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setValue(0)

        self.thread = LoadFileThread(file_path)
        self.threads.append(self.thread)

        # Conexiones
        self.thread.progress.connect(self.update_progress)
        self.thread.lines_loaded.connect(self.append_text_to_left)
        self.thread.finished.connect(self.on_file_loaded)
        self.progress_dialog.canceled.connect(self.cancel_loading)

        self.thread.start()

    def update_progress(self, value):
        self.progress_dialog.setValue(value)

    def append_text_to_left(self, text):
        # Ignora la línea #EXTM3U
        if not text.startswith("#EXTM3U"):
            # Aquí pasamos una lista con una sola línea a la función que maneja el coloreado
            self.append_lines_to_text_edit(self.text_left, [text])

    def on_file_loaded(self):
        self.progress_dialog.close()  # Cerrar el QProgressDialog cuando todo haya terminado
        self.threads.remove(self.sender())
        
    def cancel_loading(self):
        if self.thread.isRunning():
            self.thread.terminate()
            self.progress_dialog.close()
            QMessageBox.information(self, "Cancelado", "La carga del archivo ha sido cancelada.")


    def append_lines_to_text_edit(self, text_edit, lines):
        cursor = text_edit.textCursor()
        for line in lines:
            if line.startswith("#EXTINF:") or line.startswith("http"):
                self.append_colored_text_with_cursor(cursor, line, QColor('black'))
            else:
                self.append_colored_text_with_cursor(cursor, line, QColor('red'))
        text_edit.setTextCursor(cursor)  # Asegura que el cursor esté al final

    def append_colored_text_with_cursor(self, cursor, text, color):
        fmt = QTextCharFormat()
        fmt.setForeground(QBrush(color))
        cursor.movePosition(QTextCursor.End)
        cursor.insertBlock()
        cursor.insertText(text, fmt)
        cursor.setCharFormat(QTextCharFormat())  # Resetear el formato
        
    def on_lines_loaded(self, line):
        # Acumula las líneas cargadas
        self.loaded_lines.append(line)
        # Muestra las líneas en grupos (por ejemplo, de 10,000) para evitar recargar la UI
        if len(self.loaded_lines) >= 10000:
            self.append_lines_to_text_edit(self.text_left, self.loaded_lines)
            self.loaded_lines.clear()

    def save_m3u(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar M3U", "", "M3U Files (*.m3u);;All Files (*)", options=options)
        if file_path:
            content = self.text_right.toPlainText()
            with open(file_path, 'w') as file:
                # Añadir #EXTM3U al principio del archivo
                file.write("#EXTM3U\n")
                file.write(content)

    def search_group_title(self):
        search_term, ok = QInputDialog.getText(self, 'Buscar', 'Escribe el contenido de group-title a buscar:')
        if ok and search_term:
            self.thread = SearchThread(self.text_left.toPlainText(), search_term)
            self.thread.result.connect(self.on_search_finished)
            self.thread.start()

    def on_search_finished(self, positions):
        if not positions:
            QMessageBox.warning(self, "Advertencia", "No hay resultados para el concepto buscado.")
        else:
            fmt = QTextCharFormat()
            fmt.setBackground(QBrush(QColor('yellow')))
            cursor = self.text_left.textCursor()

            # Resaltar todas las posiciones encontradas
            for pos in positions:
                cursor.setPosition(pos)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(positions[pos]))
                cursor.mergeCharFormat(fmt)

    def closeEvent(self, event):
        # Preguntar al usuario si está seguro de cerrar
        reply = QMessageBox.question(self, 'Confirmar salida', '¿Está seguro de que desea salir?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Cerrar todos los hilos y procesos en ejecución
            self.close_all_threads_and_processes()
            event.accept()
        else:
            event.ignore()

    def close_all_threads_and_processes(self):
        # Aquí deberías cerrar todos los hilos y procesos que estén en ejecución
        for thread in self.threads:
            if thread.isRunning():
                thread.quit()
                thread.wait()
        self.threads.clear()

