import zipfile
import os
def create_zip_folder(zip_file_path, folder_path):
    if os.path.isfile(zip_file_path) is True:
        os.remove(zip_file_path)
    if os.path.isdir(folder_path) is False:
        return
    zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            zip_file.write(os.path.join(root, file))
    zip_file.close()
    print('Zip file created successfully')
    return zip_file

folder_path = '../backend/'
zip_file_path = '../backend.zip'
create_zip_folder(zip_file_path, folder_path)
