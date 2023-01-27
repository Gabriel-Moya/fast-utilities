import os
import zipfile

def get_source_folder():
    source_folder_to_zip = input('Caminho da pasta a ser compactada: ')
    return source_folder_to_zip

def zip_folder(source, dest_zip):
    filezip = zipfile.ZipFile(f'{dest_zip}\\py_compact.zip', 'w')

    for folder, subfolders, files in os.walk(f'{source}'):
        for file in files:
            filezip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), f'{source}'), compress_type=zipfile.ZIP_DEFLATED)

    filezip.close()


source_folder_to_zip = get_source_folder()
source = os.path.join(source_folder_to_zip)
dest_zip = os.path.abspath(os.path.join(source, os.pardir))

zip_folder(source, dest_zip)
