3D Pipeline - Level Editor

Una herramienta ligera y eficiente basada en PySide6 diseñada para el diseño de niveles (mapas) basados en grillas. Permite configurar dimensiones, definir tipos de terreno mediante ciclos de colores y exportar la configuración a archivos JSON.
Características

    Redimensionamiento Dinámico: Ajusta el ancho y alto del mapa en tiempo real.

    Interfaz Interactiva: Sistema de clics para alternar entre diferentes tipos de tiles (0-7).

    Exportación JSON: Genera archivos de configuración personalizados con la estructura de tu mapa.

    Auto-ajuste: La ventana se ajusta automáticamente al tamaño del mapa para una experiencia de usuario limpia.

    Referencia Visual: Incluye una leyenda de colores para identificar rápidamente el tipo de tile.

Requisitos

    Python 3.x

    PySide6

Instalación

    Clona este repositorio en tu máquina local:
    Bash

    git clone <url-de-tu-repositorio>
    cd <nombre-de-tu-carpeta>

    Crea y activa un entorno virtual (recomendado):
    Bash

    python3 -m venv venv
    source venv/bin/activate

    Instala las dependencias necesarias:
    Bash

    pip install -r requirements.txt

Uso

Para ejecutar el editor, simplemente lanza el script principal:
Bash

python editor.py

Al abrir la ventana, puedes:

    Ajustar el tamaño (Width/Height) y pulsar Resize Map.

    Hacer clic en los cuadros para cambiar su valor y color.

    Ingresar un nombre de archivo en la caja de texto y pulsar Export Level to JSON.

Leyenda de Colores
Valor	Tipo
0	Empty (Blanco)
1	Wall (Negro)
2	Floor (Gris)
3	Health (Rojo oscuro)
4	Ammo (Azul)
5	To be asigned (Verde)
6	To be asigned (Oro)
7	Portal (Púrpura)
8 To be Asigned (Verde oscuro)
9 Enemy (Rojo)
Estructura del JSON generado

El archivo exportado sigue este formato:
JSON

{
    "version": "1.1",
    "width": 10,
    "height": 10,
    "map": [
    [0, 0, 1, ...],
        [0, 2, 2, ...]
    ]
}
