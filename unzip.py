import os
import glob
from ehentai.settings import DOWNLOAD_DIR

__dirname = os.path.dirname(os.path.abspath(__file__))

xzip_exe = os.path.join(__dirname, 'bin', '7-zip', '7z.exe')

if(not os.path.exists(xzip_exe)):
    print(f'文件不存在: {xzip_exe}')
    exit(1)


def unzips(gp):
    '''
    7-Zip 命令行文档 https://7ziphelp.com/7zip-command-line
    解压文件后，删除文件
    '''
    for p in glob.iglob(gp):
        print(p)
        outdir = os.path.dirname(p)
        os.system(f'{xzip_exe} x -bso0 -o"{outdir}" "{p}"')
        os.remove(p)


for p in 'zip|rar|7z'.split('|'):
    unzips(os.path.join(DOWNLOAD_DIR, f'*/*.{p}'))
