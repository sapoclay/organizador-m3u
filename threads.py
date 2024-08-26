"""
threads.py - Hilos para operaciones en segundo plano en M3U Organizer

Este módulo define dos clases de hilos (`QThread`) que se utilizan para realizar operaciones en segundo plano 
en la aplicación M3U Organizer. Estas operaciones incluyen la carga de archivos grandes y la búsqueda de términos 
en textos extensos, permitiendo que la interfaz gráfica de usuario (GUI) permanezca responsiva mientras se ejecutan.

Clases:

- `LoadFileThread(QThread)`: Hilo que carga un archivo M3U línea por línea, emitiendo señales de progreso, 
  líneas cargadas y finalización del proceso.
  - `__init__(self, file_path, chunk_size=10000)`: Constructor que inicializa el hilo con la ruta del archivo 
    y un tamaño de lote (chunk_size) para la carga progresiva.
  - `run(self)`: Método principal del hilo que carga el archivo, emite señales de progreso y las líneas leídas.
  - `process_lines(self, lines)`: Procesa un lote de líneas y les aplica formato HTML para colorearlas 
    según su contenido.

- `SearchThread(QThread)`: Hilo que busca un término en un texto grande y emite la posición de todas las coincidencias.
  - `__init__(self, text, search_term)`: Constructor que inicializa el hilo con el texto completo y el término 
    de búsqueda.
  - `run(self)`: Método principal del hilo que busca el término y emite un diccionario con las posiciones 
    de las coincidencias.

Señales (pyqtSignal):

- `LoadFileThread.progress`: Emite un entero representando el progreso de la carga en porcentaje.
- `LoadFileThread.lines_loaded`: Emite una cadena con cada línea cargada del archivo.
- `LoadFileThread.finished`: Señala que el proceso de carga ha finalizado.
- `SearchThread.result`: Emite un diccionario con las posiciones de todas las coincidencias encontradas en la búsqueda.

Dependencias:
    - PyQt5.QtCore: Para el manejo de hilos y señales (QThread, pyqtSignal).

Uso:
    Estos hilos son utilizados en la aplicación principal (`organizadorm3u.py`) para manejar la carga de archivos 
    M3U y la búsqueda de términos sin bloquear la interfaz gráfica.

Ejemplo:
    En `M3UOrganizer`, estos hilos se inician para cargar archivos y buscar términos, con sus señales conectadas 
    a métodos que actualizan la UI o realizan otras acciones en respuesta a los eventos emitidos.

Autores:
    - entreunosyceros (autor principal)

Versión:
    0.5

Licencia:
    Libre para uso personal y educativo.

"""

from PyQt5.QtCore import QThread, pyqtSignal

class LoadFileThread(QThread):
    progress = pyqtSignal(int)
    lines_loaded = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, file_path, chunk_size=10000):  # chunk_size aumentado
        super().__init__()
        self.file_path = file_path
        self.chunk_size = chunk_size

    def run(self):
        total_lines = 0
        with open(self.file_path, 'r') as file:
            while file.readline():
                total_lines += 1

        with open(self.file_path, 'r') as file:
            for i, line in enumerate(file):
                if i % self.chunk_size == 0:
                    self.progress.emit(int((i / total_lines) * 100))
                self.lines_loaded.emit(line.strip())

        self.finished.emit()

    def process_lines(self, lines):
        processed_lines = []
        for line in lines:
            line = line.strip()
            color = 'black' if line.startswith("#EXTINF:") or line.startswith("http") else 'red'
            processed_lines.append(f"<span style='color:{color}'>{line}</span>")
        return "\n".join(processed_lines)

class SearchThread(QThread):
    result = pyqtSignal(dict)

    def __init__(self, text, search_term):
        super().__init__()
        self.text = text
        self.search_term = search_term

    def run(self):
        positions = {}
        current_pos = 0
        while current_pos >= 0:
            current_pos = self.text.find(self.search_term, current_pos)
            if (current_pos >= 0):
                positions[current_pos] = self.search_term
                current_pos += len(self.search_term)
        self.result.emit(positions)