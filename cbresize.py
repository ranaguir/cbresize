import os
import zipfile
import rarfile

from send2trash import send2trash
from wand.image import Image

# Set to full path of unrar.exe if it is not in PATH
rarfile.UNRAR_TOOL = "C:\\Program Files\\WinRAR\\UnRAR.exe"

# definicion de variables globales
base_dir = 'D:\\comics\\modificaciones'
dir_modificados = os.path.join(base_dir,'modificados')
# el ancho de la pagina deseado
ancho = 1280
s_ancho = str(ancho) + 'x'
doble_ancho = ancho * 2
s_doble_ancho = str(doble_ancho) + 'x'
factor_compresion = 85

# funcion para determinar el tipo de archivo
def Tipo_Archivo (archivo):
    # identificadores de archivo
    _RAR5_ID = b"Rar!\x1a\x07\x01\x00"
    _RAR_ID = b"Rar!\x1a\x07\x00"
    _ZIP_ID = b"PK"
    _7Z_ID = b"7z\xbc\xaf\x27\x1c"
    # abre el archivo para obtener los primeros bytes
    with open(archivo, 'rb') as f:
        buf = f.read(len(_RAR5_ID))
    # determina el tipo
    if buf.startswith(_RAR_ID):
        tipo = 'RAR'
    elif buf.startswith(_RAR5_ID):
        tipo = 'RAR'
    elif buf.startswith(_ZIP_ID):
        tipo = 'ZIP'
    elif buf.startswith(_7Z_ID):
        tipo = '7Z'
    else:
        tipo = 'XX'
    # retorna el valor
    return tipo

# procesar el .jpg
def procesar_imagen (archivo):
    (_,extension) = os.path.splitext(archivo)
    # solo los .jpg, ignora el resto de archivos
    if extension.lower() in ('.jpg', '.jpeg'):
        with Image(filename = archivo, resolution = 72) as img:
            (width, height) = img.size
            # verifica que no sea una pagina doble
            if width < height:
                # si ya el ancho de la pagina es menor, no hace nada
                if width > ancho:
                    img.transform(resize = s_ancho)
            else:
                if width > doble_ancho:
                    img.transform(resize = s_doble_ancho)
            # reduce el tamaño del archivo
            img.strip()
            img.interlace_scheme = 'plane'
            img.compression_quality = factor_compresion
            img.save(filename = archivo)

def procesar_archivo (archivo):
    (nombre,_) = os.path.splitext(archivo)
    # lista para almacenar los archivos del comprimido
    lista_archivos = []
    # crea un directorio para descomprimir
    if not os.path.exists (nombre):
        os.makedirs(nombre)
    # determina el tipo del archivo
    # no se hace por extension porque a veces lo nombran cbr, pero por dentro
    # en realidad es un cbz
    tipo_archivo = Tipo_Archivo (archivo)
    # si es un .zip o un .cbz, crea un directorio con el nombre y
    # extrae los archivos que contiene
    if tipo_archivo == 'ZIP':
        zip = zipfile.ZipFile(archivo)
        # primero descomprime todo
        zip.extractall(path = nombre)
        # luego recorre el contenido del .zip y procesa las imagenes
        os.chdir (nombre)
        for archivo_imagen in zip.namelist():
            lista_archivos.append(os.path.sep.join(archivo_imagen.split('/')))
            procesar_imagen (os.path.sep.join(archivo_imagen.split('/')))
        zip.close()
    # si es un .rar o un .cbr, crea un directorio con el nombre y
    # extrae los archivos que contiene
    elif tipo_archivo == 'RAR':
        rar = rarfile.RarFile(archivo)
        # primero descomprime todo
        rar.extractall(path = nombre)
        # luego recorre el contenido del .zip y procesa las imagenes
        os.chdir (nombre)
        for archivo_imagen in rar.namelist():
            lista_archivos.append(os.path.sep.join(archivo_imagen.split('/')))
            procesar_imagen (os.path.sep.join(archivo_imagen.split('/')))
        rar.close()
    elif tipo_archivo == '7Z':
        print('El archivo es un 7z - no se puede procesar')
    else:
        print('No es posible determinar el tipo de archivo')

    # crear el nuevo zip con las imagenes modificadas
    new_zip = zipfile.ZipFile(os.path.join(dir_modificados,nombre) + '.cbz', 'w')
    for nuevo_archivo in lista_archivos:
        new_zip.write(nuevo_archivo, compress_type=zipfile.ZIP_DEFLATED)
    new_zip.close()
    # se cambia al directorio principal y elimina el directorio
    # donde se descomprimieron las imagenes
    os.chdir(base_dir)
    send2trash(nombre)

def main():
    # inicio
    list_files = []
    if os.path.exists (base_dir):
        os.chdir(base_dir)
        # si no existe el directorio destino, entonces se crea
        if not os.path.exists (dir_modificados):
            os.makedirs (dir_modificados)
        # recorre el directorio base en busqueda de los archivos de comics
        for archivo in os.listdir():
            (_,extension) = os.path.splitext(archivo)
            if (extension in ('.cbz','.zip','.cbr','.rar')):
                list_files.append(archivo)

    # proces los archivos de comics
    for file in list_files:
        try:
            print ("Procesando archivo " + file)
            procesar_archivo (file)
        except:
            print ("Error en archivo " + file)

if __name__ == '__main__':
    main()
