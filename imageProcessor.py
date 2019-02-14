from PIL import Image, ImageOps
import numpy
import image
import math

def saveArr2Img(img, des, qty = 70):
    tempimg = Image.fromarray(img.ImageArr.astype('uint8'))
    tempimg.save(des,optimize=True,quality=qty)

def saveImage(img, dest, qty = 70):
    img.RealImage.convert('RGB').save(dest,optimize=True,quality=qty)

def arr2rImage(img):
    img.RealImage = Image.fromarray(img.ImageArr.astype('uint8'))

def getLeftLimit(img, bgCol, diff):
    diff += 10
    minlimit = img.size
    skipper = True
    currentlimit = 0
    for x in img:
        if skipper:
            currentlimit = 0
            for y in x:
                if ((y>=(bgCol-diff)) and (y<=(bgCol+diff))):
                    currentlimit+=1
                else:
                    if currentlimit<minlimit:
                        minlimit=currentlimit
        skipper = not skipper
    return minlimit

def getHorizontalLimits(img):
    gray = numpy.asarray(img.GrayImageArr)
    llimit = getLeftLimit(gray, img.gbgColor, img.bgDifference)
    rlimit = getLeftLimit(numpy.flip(gray,1), img.gbgColor, img.bgDifference)
    return llimit, rlimit

def sliceHorizontal(img):
    left, right = getHorizontalLimits(img)
    arr = []
    for i in img.ImageArr:
        arr.append(i[left:i[:,0].size-right,:])
    img.ImageArr = numpy.asarray(arr, dtype='int64')

def getTopLimit(img, bgCol, diff):
    diff += 10
    limit = 0
    skipper = True
    for x in img:
        if skipper:
            for y in x:
                if ((y<(bgCol-diff)) or (y>(bgCol+diff))):
                    return limit
        skipper = not skipper
        limit+=1

def getVerticalLimits(img):
    gray = numpy.asarray(img.GrayImageArr)
    tlimit = getTopLimit(gray, img.gbgColor, img.bgDifference)
    blimit = getTopLimit(numpy.flip(gray,0), img.gbgColor, img.bgDifference)
    return tlimit, blimit

def sliceVertical(img):
    top, bottom = getVerticalLimits(img)
    arr = img.ImageArr[top:(img.RealImage.size[1]-bottom)]
    img.ImageArr = numpy.asarray(arr)

def sliceImg(img):
    sliceHorizontal(img)
    sliceVertical(img)

def getImage(path, imgSize):
    return image.cImage(path, imgSize)

def expand(img, size=1000, bgCol=0):
    """Expand the image object.

    Keyword arguments:

        img -- PIL Image Object
        size -- image size value (default 1000)
        bgCol -- Margin Fill Color (default White)
    
    Return the PIL Expanded Image Object
    """

    width, height = img.size

    y_border = math.floor((size - height)/2)
    x_border = math.floor((size - width)/2)

    if not isinstance(bgCol, int):
        bgCol = 'rgb({red},{green},{blue})'.format(red = bgCol[0],green = bgCol[1],blue = bgCol[2])
    return ImageOps.expand(img, (x_border,y_border,x_border,y_border), bgCol)

def resize(img, size=800):
    """Resize the image object.

    Keyword arguments:

        img -- PIL Image Object
        size -- resize value (default 800)
    
    Return the PIL Resized Image Object
    """
    width, height = img.size
    newWidth, newHeight = 0, 0
    if(width>height):
        newWidth = size
        newHeight = math.floor((size/width)*height)
    elif(height>width):
        newHeight = size
        newWidth = math.floor((size/height)*width)
    else:
        newHeight = size
        newWidth = size
    img = img.resize((newWidth, newHeight), Image.ANTIALIAS)
    return img

def getImageArray(path, imgSize = 1000):
    i = Image.open(path)
    if ((i.size[0]>imgSize) or (i.size[1]>imgSize)):
        i = resize(i, imgSize)
    gray = i.convert('L')
    return numpy.asarray(i, dtype='int64'), numpy.asarray(gray, dtype='int64'), i

def getUpdatedImageArray(img):
    return numpy.asarray(img), numpy.asarray(img.convert('L'))

def getAverageBgColor(
    topleft, 
    topleft1, 
    topleft2, 
    topleft3, 
    topright, 
    topright1, 
    topright2, 
    topright3, 
    bottomleft, 
    bottomleft1, 
    bottomleft2, 
    bottomleft3, 
    bottomright, 
    bottomright1, 
    bottomright2, 
    bottomright3
    ):
    avgColor = numpy.array([0,0,0])
    for x in range(3):
        val = (
            topleft[x]+
            topleft1[x]+
            topleft2[x]+
            topleft3[x]+
            topright[x]+
            topright1[x]+
            topright2[x]+
            topright3[x]+
            bottomleft[x]+
            bottomleft1[x]+
            bottomleft2[x]+
            bottomleft3[x]+
            bottomright[x]+
            bottomright1[x]+
            bottomright2[x]+
            bottomright3[x]
            )/16
        avgColor[x] = val
    return avgColor

def mod(x):
    if x>0:
        return x
    else:
        return (x*(-1))

def maxDifference(avg, i,j,k,l):
    maximum = 0
    if mod(avg-i)>maximum :
        maximum = mod(avg-i)
    if mod(avg-j)>maximum :
        maximum = mod(avg-j)
    if mod(avg-k)>maximum :
        maximum = mod(avg-k)
    if mod(avg-l)>maximum :
        maximum = mod(avg-l)
    return maximum

def getBackground(ImageArr):
    topleft = ImageArr[0,0]
    topleft1 = ImageArr[5,0]
    topleft2 = ImageArr[0,5]
    topleft3 = ImageArr[5,5]
    topright = ImageArr[0,len(ImageArr[0])-1]
    topright1 = ImageArr[5,len(ImageArr[0])-6]
    topright2 = ImageArr[0,len(ImageArr[0])-6]
    topright3 = ImageArr[5,len(ImageArr[0])-1]
    bottomleft = ImageArr[len(ImageArr)-1,0]
    bottomleft1 = ImageArr[len(ImageArr)-6,0]
    bottomleft2 = ImageArr[len(ImageArr)-1,5]
    bottomleft3 = ImageArr[len(ImageArr)-6,5]
    bottomright = ImageArr[len(ImageArr)-1,len(ImageArr[0])-1]
    bottomright1 = ImageArr[len(ImageArr)-6,len(ImageArr[0])-1]
    bottomright2 = ImageArr[len(ImageArr)-1,len(ImageArr[0])-6]
    bottomright3 = ImageArr[len(ImageArr)-6,len(ImageArr[0])-6]
    avgBgCol = getAverageBgColor(
        topleft, 
        topleft1, 
        topleft2, 
        topleft3, 
        topright, 
        topright1, 
        topright2, 
        topright3, 
        bottomleft, 
        bottomleft1, 
        bottomleft2, 
        bottomleft3, 
        bottomright, 
        bottomright1, 
        bottomright2, 
        bottomright3
        )
    
    return avgBgCol

def getGrayBackground(ImageArr):
    topleft = ImageArr[0,0]
    topleft1 = ImageArr[5,0]
    topleft2 = ImageArr[0,5]
    topleft3 = ImageArr[5,5]
    topright = ImageArr[0,len(ImageArr[0])-1]
    topright1 = ImageArr[5,len(ImageArr[0])-6]
    topright2 = ImageArr[0,len(ImageArr[0])-6]
    topright3 = ImageArr[5,len(ImageArr[0])-1]
    bottomleft = ImageArr[len(ImageArr)-1,0]
    bottomleft1 = ImageArr[len(ImageArr)-6,0]
    bottomleft2 = ImageArr[len(ImageArr)-1,5]
    bottomleft3 = ImageArr[len(ImageArr)-6,5]
    bottomright = ImageArr[len(ImageArr)-1,len(ImageArr[0])-1]
    bottomright1 = ImageArr[len(ImageArr)-6,len(ImageArr[0])-1]
    bottomright2 = ImageArr[len(ImageArr)-1,len(ImageArr[0])-6]
    bottomright3 = ImageArr[len(ImageArr)-6,len(ImageArr[0])-6]
    avgBgCol = ((
        topleft+
        topleft1+
        topleft2+
        topleft3+
        topright+
        topright1+
        topright2+
        topright3+
        bottomleft+
        bottomleft1+
        bottomleft2+
        bottomleft3+
        bottomright+
        bottomright1+
        bottomright2+
        bottomright3
        )/16)

    bgDifference = maxDifference(avgBgCol, topleft, topright, bottomleft, bottomright)
    
    return avgBgCol, bgDifference