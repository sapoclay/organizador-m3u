# M3U Organizer

M3U Organizer es una aplicación que escribí por que alguien me ha pedido una aplicación de escritorio desarrollada en Python utilizando PyQt5, diseñada para facilitar la gestión y organización de listas de reproducción en formato M3U. Este programa te permite cargar, editar, organizar, y guardar listas M3U de manera sencilla e intuitiva. Es sencillo apliar las funcionalidades de la misma, por lo que si alguien lo necesita, que no dude en hacerlo.

## Características

- **Carga y Edición de Listas M3U**: Carga listas de reproducción en formato M3U para visualizarlas y editarlas.
- **Organización de Canales**: Arrastra y suelta canales entre dos paneles de texto para organizar tu lista de reproducción.
- **Búsqueda y Selección**: Busca y selecciona rápidamente canales basados en sus `group-title` u otros criterios.
- **Reproducción con VLC**: Abre enlaces directamente en VLC desde la aplicación.
- **Exportación de Listas**: Guarda tus listas de reproducción editadas en formato M3U.
- **Menú Contextual**: Accede a funciones útiles mediante el menú contextual, como copiar, pegar, y abrir con VLC.
- **Temas Personalizados**: Cambia entre temas claros y oscuros para mejorar la experiencia visual.
- **Soporte Multilenguaje**: Disponible en varios idiomas.

## Capturas de Pantalla

![about-m3u-organ1zat0r](https://github.com/user-attachments/assets/4a926b38-134f-4cd5-ab36-08ac7cd63ae5)
![m3uorgan1zat0r-funcionando](https://github.com/user-attachments/assets/b3ee8e82-1a42-46be-afcf-ecaae940a176)

## Requisitos del Sistema

- Python 3.7 o superior
- PyQt5
- VLC Media Player (opcional, para reproducción de URLs)

## Instalación

1. **Clona el repositorio**:
    ```bash
    git clone https://github.com/sapoclay/ordenar-m3u.git
    cd ordenar-m3u
    ```

2. **Crea un entorno virtual** (opcional, pero recomendado):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. **Instala las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Ejecuta la aplicación**:
    ```bash
    python m3uorgan1zat0r.py
    ```

## Uso

1. **Cargar Lista M3U**: Usa el menú `Archivo > Abrir M3U` para cargar una lista de reproducción.
2. **Organizar Canales**: Arrastra y suelta los canales entre los dos paneles de texto para organizarlos.
3. **Buscar Canales**: Utiliza el menú `Editar > Buscar y seleccionar` para buscar canales específicos.
4. **Guardar Lista**: Una vez organizada, guarda tu lista usando `Archivo > Guardar M3U`.

## Contribuciones

¡Las contribuciones son bienvenidas! Si quieres contribuir, por favor sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza los cambios necesarios y haz commits (`git commit -am 'Añadir nueva característica'`).
4. Sube tus cambios a tu fork (`git push origin feature/nueva-caracteristica`).
5. Crea un Pull Request en este repositorio.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

- **Autor**: entreunosyceros
- **Web**: entreunosyceros.net
- **Repositorio en GitHub**: [https://github.com/sapoclay/ordenar-m3u](https://github.com/sapoclay/ordenar-m3u)

Si tienes alguna pregunta o sugerencia, no dudes en contactar.
