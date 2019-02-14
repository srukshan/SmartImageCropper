import imageProcessor as ip

class cImage:
    def __init__(self, path, imgSize):
        self.path = path
        self.ImageArr, self.GrayImageArr, self.RealImage = ip.getImageArray(path, imgSize)
        self.setBackgroundColor()
    
    def renew(self):
        self.ImageArr, self.GrayImageArr, self.RealImage = ip.getImageArray(self.path)

    def setBackgroundColor(self):
        self.bgColor = ip.getBackground(self.ImageArr)
        self.gbgColor, self.bgDifference = ip.getGrayBackground(self.GrayImageArr)
    
    def update(self):
        self.ImageArr, self.GrayImageArr = ip.getUpdatedImageArray(self.RealImage)
        self.setBackgroundColor()
    
    