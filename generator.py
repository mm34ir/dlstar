import compileall

#compileall.compile_dir('.', force=True)

import shutil
import os

dir = 'build'
if os.path.exists(dir):
    shutil.rmtree(dir)
    
os.mkdir(dir)

def copy(dir):
    os.mkdir(f"build/{dir}")
    
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        dir = root.replace(startpath,"")
        print('{}/'.format(dir))
        if not dir.startswith('.'): copy(dir)
        for f in files:
            print('{}'.format( f))

list_files(".")