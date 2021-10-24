'''Renames all files within a folder (and subfolders if you'd be so inclined)
to their respective comicbook archive extensions.\n

In order to run this script, open a commandline prompt and input the following:
$ python <this script> --loc <folderpath>
Where:\n
\t<this script> is the full path leading to this script\n
\t<folderpath> is the full path of the folder you want to run the script on\n\n

You may also attach the flag '--sf' to have the script run on all subfolders
of <folderpath>
'''

import sys
import os
import time
import argparse

extOG = ('.rar','.zip','.7z','.ace','.tar')
extNU = ('.cbr','.cbz','.cb7','.cba','.cbt')
# extNU = ('.rar','.zip','.7z','.ace','.tar')
# extOG = ('.cbr','.cbz','.cb7','.cba','.cbt')


def addSubFolders(path):
    '''Adds a given folder's subfolders' compressed files to a list and return it

    This function fetches the directory given in the 'path' argument, makes a list
    of all subfolders found within it, and to each one of those, recusively calls this
    function itself and the addFiles function.

    Will return a list of all fetched compressed files with each subfolder.
    '''
    folders = list(filter(lambda p: os.path.isdir(path+'\\'+p),os.listdir(path)))
    files = []
    for f in folders:
        filepath = path+'\\'+f
        files += addFiles(filepath) + addSubFolders(filepath)
    return files

def addFiles(path):
    '''Returns a list of all the compressed files within a given folder
    
    This function fetches the list of all files found within the folder in the
    'path' argument, filters the list to contain only the compressed files 
    within it and returns said list, with the path leading to the folder
    added to the front of it.
    '''
    files = list(filter(lambda p: p.endswith(extOG),os.listdir(path))) # list of all compressed files
    extlist = [os.path.splitext(p)[1] for p in files] #the file extensions
    filenames = [os.path.splitext(p)[0] for p in files] #the file names

    files2 = (list(filter(lambda p: p.endswith(extNU),os.listdir(path))))
    filenames2 = [os.path.splitext(p)[0] for p in files2] #the file names of all cba files

    # filter for files that don't have a cba version
    files=[]
    for i in range(len(filenames)):
        if not filenames[i] in filenames2:
            files.append(filenames[i]+extlist[i])
    
    files =  [path + '\\' + e for e in files]
    return files

def rename(file):
    '''Rename a compressed file to its respective comicbook archive extension    
    '''
    base = os.path.splitext(file)[0]
    ext = extNU[extOG.index(os.path.splitext(file)[1])]
    os.rename(file, base + ext)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('-sf',action='store_true',help="When this flag is present, will also explore and"+
    " change files in subfolders")
    parser.add_argument('--log',action='store_true',help="When this flag is present, will create a log file")
    parser.add_argument('--loc','-l',nargs='*',help="Location of initial folder")
    parser.add_argument('--rev','-r',nargs='*',action='store_true',help="Reverse compression")
    args = parser.parse_args()

    path = args.loc
    if isinstance(path,list):
        path = ' '.join(args.loc)
    elif path == None:
        path = os.getcwd()
    sf = args.sf

    if (args.rev):
        extNU = ('.rar','.zip','.7z','.ace','.tar')
        extOG = ('.cbr','.cbz','.cb7','.cba','.cbt')

    tic = time.time()    
    files = (addFiles(path))
    if sf:
        fileAdd = addSubFolders(path)
        files = files+fileAdd
    if len(files) == 0:
        files="No renamable files found."
        print(files)
    else:
        for p in files:
            rename(p)
        print(f"Renaming done. Renamed {len(files)} compressed files.")
    toc = time.time()
    worktime = f'Work time: {toc - tic} seconds'
    
    print(f"{worktime} Closing Program.")
    
    if args.log:
        import datetime
        with open(f'log cbrz {datetime.datetime.now().strftime("%d.%m.%Y %H.%M.%S")}.txt','w',encoding="utf-8") as f:
            l = 0
            if isinstance(files,list):
                l = len(files)
                files = '\n'.join(files)
            f.write(f'Total number of files converted: {l}.\n\nList of files converted:\n')
            f.write(files)
            f.write(f'\n{worktime}')
    
main()