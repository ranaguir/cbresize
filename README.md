# cbresize
Modifica el tamaño de las paginas de un comic .cbr o .cbz para que pueda ser leído con más comodidad.

Actualmente procesa correctamente los archivos .cbr y .cbz.  No procesa los comprimidos con 7z y muestra un mensaje de error.

El ancho default de las páginas será **1280**.

##Dependencias
- Wand
- Send2Trash
- rarfile

##TODO
1. Permitir especificar en un archivo de configuración, el directorio de dónde se toman los archivos fuentes y el directorio donde se copian los archivos destino.  También si deben moverse los archivos fuentes a algún otro directorio.
2. Poder indicar mediante un parámetro o un archivo de configuración el ancho de las páginas.
3. Procesar archivos comprimidos con 7z
4. Interfaz gráfica para procesar los archivos.
