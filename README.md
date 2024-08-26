# organizador-m3u

M3U Organizer es una herramienta escrita en Python utilizando PyQt5 para gestionar listas de reproducción en formato M3U. Este programa permite cargar, editar, y guardar listas de reproducción, además de ofrecer funcionalidades adicionales como la búsqueda y la reproducción de URLs.

## Características

- **Cargar y guardar listas M3U**: Permite cargar archivos M3U y guardarlos después de realizar modificaciones.
- **Búsqueda y selección**: Busca y resalta grupos o títulos específicos dentro del archivo.
- **Reproducción de URLs**: Reproduce URLs seleccionadas directamente en VLC.
- **Interfaz intuitiva**: Arrastra y suelta canales para reorganizarlos, y utiliza menús contextuales para opciones rápidas.

# Instalar dependencias

Asegúrate de tener Python 3.x y pip instalados. Luego, ejecuta:

```pip install -r requirements.txt```

Nota: Si no hay un archivo requirements.txt, instala PyQt5 manualmente:

```pip install PyQt5```

# Uso

- Ejecutar el programa:

```python3 nombre_del_script.py```

- Cargar un archivo M3U. Utiliza la opción Archivo > Abrir M3U para cargar una lista de reproducción en el lado izquierdo de la pantalla.

- Editar y reorganizar. Arrastra el texto seleccionado entre los paneles o utiliza las opciones del menú contextual del ratón. Doble clic sobre una línea para editarla directamente.

- Guardar el archivo M3U. Utiliza la opción Archivo > Guardar M3U para guardar tus cambios en un nuevo archivo M3U.

- Reproducir URLs. Haz clic derecho en una URL y selecciona Abrir con VLC para reproducirla.

# Créditos

M3U Organizer fue desarrollado por entreunosyceros como un ejercicio práctico de Python.