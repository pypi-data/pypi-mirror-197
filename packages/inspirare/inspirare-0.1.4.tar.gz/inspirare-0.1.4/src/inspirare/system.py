import os  
import shutil


def exec(command):
    os.system(command)

def open(path):
    """ 打开文件 """
    os.startfile(path)

def join(path, filename):
    return os.path.join(path,filename)

def mv(src, dst):
    shutil.move(src, dst)

def rm(file):
    os.remove(file)

def cp(src, dst):
    shutil.copyfile(src, dst)

def ls(path = '.'):
    return os.listdir(path)

def exists(path):
    return os.path.exists(path)

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def pwd():
    return os.getcwd()