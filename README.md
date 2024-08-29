<p style="text-align:center;"># M3U Organizer</p>
<p>![ordenar-m3u](https://github.com/user-attachments/assets/115f63ed-0579-4074-a681-f18a05f8ead8)</p>

M3U Organizer es una aplicación que escribí por que alguien me ha pedido una aplicación de escritorio desarrollada en Python utilizando PyQt5, diseñada para facilitar la gestión y organización de listas de reproducción en formato M3U. Este programa te permite cargar, editar, organizar, y guardar listas M3U de manera sencilla e intuitiva. Es sencillo apliar las funcionalidades de la misma, por lo que si alguien lo necesita, que no dude en hacerlo.

## Características

- **Carga y Edición de Listas M3U**: Carga listas de reproducción en formato M3U o M3U8, desde un archivo local o desde una URL, para visualizarlas y editarlas.
- **Organización de Canales**: Arrastra y suelta canales entre dos paneles de texto para organizar tu lista de reproducción.
- **Búsqueda y Selección**: Busca y selecciona rápidamente canales basados en sus `group-title` u otros criterios.
- **Reproducción con VLC**: Abre enlaces directamente en VLC desde la aplicación.
- **Exportación de Listas**: Guarda tus listas de reproducción editadas en formato M3U.
- **Listas**: Nos va a permitir guardar nuestras listas m3u preferidas. Podremos guardar la URL, y añadir un nombre identificativo. Se podrá copiar la URL para utilizarla para poder trabajar o ver la lista m3u. El listado de URL se guardará como archivo .JSON en el mismo directorio del programa.
- **Menú Contextual**: Accede a funciones útiles mediante el menú contextual, como copiar, pegar, previsualizar y abrir con VLC.

## Capturas de Pantalla

![about-m3u-organ1zat0r](https://github.com/user-attachments/assets/4a926b38-134f-4cd5-ab36-08ac7cd63ae5)
![m3uorgan1zat0r-funcionando](https://github.com/user-attachments/assets/b3ee8e82-1a42-46be-afcf-ecaae940a176)
![previsualizacion-video](https://github.com/user-attachments/assets/6a4a5003-81ab-41c2-86bf-ff9cfd20fa81)

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
    python3 m3uorgan1zat0r.py
    ```

## Uso

1. **Cargar Lista M3U Local**: Usa el menú `Archivo > Abrir M3U local` para cargar una lista de reproducción desde un archivo descargado en tu equipo.
2. **Cargar Lista M3U desde URL**: Usa el menú `Archivo > Abrir M3U desde URL` para cargar una lista de reproducción desde una URL en la que se encuentre el archivo m3u.
3. **Filtros y ordenación**: Puedes ordenar los canales utilizando los filtros las opciones de orden disponibles.
4. **Organizar Canales**: Arrastra y suelta los canales entre los dos paneles de texto para organizarlos. También podrás copiar y pegar los canales.
5. **Buscar Canales**: Utiliza el menú `Editar > Buscar y seleccionar` para buscar canales específicos.
6. **Guardar Lista**: Una vez organizada, guarda tu lista usando `Archivo > Guardar M3U`.
7. **Previsualizar**: En el menú contextual del ratón, sobre una URL, tendremos la posibilidad de previsualizar la emisión de la URL desde el propio programa. Así podremos saber si la URL tiene la emisión en activo y poder añadir la URL a nuestra lista sabiendo que está operativa.

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
