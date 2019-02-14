import os
import numpy as np
import pandas as pd

def makeDir(path):
    os.makedirs(path)

def confirmPath(path):
    if os.path.isdir(path):
        if(path.endswith('/')):
            path = path[:-1]
        return path
    return ''

def change2jpeg(file):
    filename = file.split('.')[0]
    return filename+'.jpeg'

class pathManager:
    def __init__(self, root_dir, dest_dir):
        self.root_dir = confirmPath(root_dir)
        self.dest_dir = confirmPath(dest_dir)
        try:
            self.files = [item for item in os.listdir(self.root_dir) if os.path.isfile(os.path.join(self.root_dir, item))]
        except Exception:
            print('Invalid Path')
            exit(-1)
        
        self.currentFile = 0
    
    # def CSVify(self):
    #     files = np.asarray(self.files)
    #     pd.DataFrame(files).to_csv("files.csv",header=False,index=False)

    def getPercentage(self):
        return ((self.currentFile-1)/self.files.__len__())*100

    def getNext(self):
        file = self.files[self.currentFile]
        self.currentFile+=1
        return self.root_dir + '/' + file

    def hasNext(self):
        return ((self.files.__len__())!=self.currentFile)

    def getCurrentDestination(self):
        file = self.files[self.currentFile-1]
        return self.dest_dir + '/' + change2jpeg(file)
    
    def getCurrentFileName(self):
        return self.files[self.currentFile-1]

    def getIndex(self, id):
        return self.root_dir + '/' + self.files[id]

    def moveProcessed(self, folder = ''):
        if folder=='':
            folder = 'originals'
        else:
            folder = 'originals/'+folder
        file = self.files[self.currentFile-1]
        des = self.dest_dir + '/'+folder+'/'+file
        if confirmPath(self.dest_dir + '/'+folder+'/')=='':
            makeDir(self.dest_dir + '/'+folder+'/')
        os.rename(self.root_dir + '/' + file, des)