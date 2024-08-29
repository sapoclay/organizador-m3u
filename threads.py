"""
threads.py - Hilos para operaciones en segundo plano en M3U Organizer

Este módulo contiene dos clases que heredan de QThread y están diseñadas para realizar operaciones en segundo plano 
en una aplicación PyQt5. Las clases `LoadFileThread` y `SearchThread` proporcionan hilos para cargar archivos 
y buscar términos específicos en texto, respectivamente.

Classes:
--------
- LoadFileThread(QThread):
    Hilo para cargar un archivo grande en segmentos, emitiendo señales de progreso y las líneas cargadas.

    Signals:
    - progress (int): Señal emitida con el porcentaje de progreso de la carga del archivo.
    - lines_loaded (str): Señal emitida con las líneas cargadas del archivo.
    - finished (): Señal emitida cuando la carga del archivo ha finalizado.

    Methods:
    - run(): Ejecuta la carga del archivo línea por línea, emitiendo el progreso y las líneas cargadas.
    - process_lines(lines): Procesa las líneas cargadas, aplicando color según el tipo de línea (EXTINF o URL).

- SearchThread(QThread):
    Hilo para buscar un término en un texto dado, emitiendo las posiciones encontradas.

    Signals:
    - result (dict): Señal emitida con un diccionario que contiene las posiciones de los términos encontrados.

    Methods:
    - run(): Ejecuta la búsqueda del término dentro del texto, almacenando las posiciones encontradas.
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
        
