import zipfile
import os
import glob

def unzip(zip_file_path): # 解压zip文件后，删除zip文件
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_file_path))

for zip_file_path in glob.iglob(r'./downloads/*/*.zip'):
    print(zip_file_path)
    unzip(zip_file_path)
    os.remove(zip_file_path)

