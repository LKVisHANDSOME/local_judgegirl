import os

origindir = 'C:\\Users\\a2320\\Desktop\\judgegirl'
basedir = os.getcwd()

def replace(filename):
    s = ""
    with open(filename,'r+',encoding='utf-8') as f:
        s = f.read()
        s = s.replace(origindir,basedir)
    with open(filename,'w+',encoding='utf-8') as f:
        f.write(s)

def get_filelist(dir, Filelist):
    newDir = dir
    if os.path.isfile(dir):
        if dir != os.path.join(basedir,'init.py') and dir != os.path.join(basedir,'init.exe'):
            Filelist.append(dir)
    elif os.path.isdir(dir):
        if dir != os.path.join(basedir,'downloads') and dir != os.path.join(basedir,'images'):
            for s in os.listdir(dir):
                newDir = os.path.join(dir,s)
                get_filelist(newDir,Filelist)
    return Filelist

if __name__ == '__main__':
    filelist = get_filelist(basedir,[])
    print(len(filelist))
    for file in filelist:
        print(file)
        replace(file)