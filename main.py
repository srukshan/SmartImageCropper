import imageProcessor
import pathManager

print('    ************************************************************************    ')
print('                             Welcome to Image Resizer                           ')
print('    ************************************************************************    ')
print()

while True:
    loc = input('    Images Folder Path : ')
    if pathManager.confirmPath(loc) != '':
        break
    print('    Warning! Path Entered Was Invalid')
loc = pathManager.confirmPath(loc)

while True:
    desc = input('    Destination Path : ')
    if pathManager.confirmPath(desc) != '':
        break
    if pathManager.confirmPath(desc) == '':
        pathManager.makeDir(desc)
        break
desc = pathManager.confirmPath(desc)

while True:
    imgSize = int(input('    Image Size : '))
    if imgSize >= 0:
        break
    print('    Warning! Invalid Image Size')

while True:
    imgMargin = int(input('    Image Margin : '))
    if imgMargin >= 0:
        break
    print('    Warning! Invalid Image Margin')

imgQuality = input('    Image Quality : ')
if imgQuality == '':
    imgQuality = 70
else:
    imgQuality = int(imgQuality)

print()
print('    ************************************************************************    ')
print()
print('    Processing (0% Completed)', end='\r')

#Initialize Path Manager
path = pathManager.pathManager(loc, desc)

while path.hasNext():
    mpath = path.getNext()
    print('    Processing ('+str(path.getPercentage())+'% Completed) - {0} - Image Uploading'.format(path.getCurrentFileName()), end='\r')

    im = imageProcessor.getImage(mpath,imgSize)
    print('    Processing ('+str(path.getPercentage())+'% Completed) - {0} - Image Uploaded           '.format(path.getCurrentFileName()), end='\r')

    imageProcessor.sliceImg(im)
    print('    Processing ('+str(path.getPercentage())+'% Completed) - {0} - Smart Cropping Completed     '.format(path.getCurrentFileName()), end='\r')

    imageProcessor.arr2rImage(im)
    im.RealImage = imageProcessor.resize(im.RealImage, (imgSize-(imgMargin*2)))
    im.RealImage = imageProcessor.expand(im.RealImage, imgSize, im.bgColor)
    print('    Processing ('+str(path.getPercentage())+'% Completed) - {0} - Smart Resizing Completed      '.format(path.getCurrentFileName()), end='\r')

    imageProcessor.saveImage(im, path.getCurrentDestination(), imgQuality)
    print('                                                                                                ', end='\r')
    print('    {0} Processed and saved as {1}'.format(path.getCurrentFileName(),path.getCurrentDestination()))

    if im.bgDifference>50:
        path.moveProcessed('error')
    elif im.bgDifference>20:
        path.moveProcessed('check')
    else:
        path.moveProcessed()

print('    Processing (100% Completed)')