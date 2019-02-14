import pathManager

print('    ************************************************************************    ')
print('                               Welcome to CSVify                                ')
print('    ************************************************************************    ')
print()

while True:
    loc = input('    Files Folder Path : ')
    if pathManager.confirmPath(loc) != '':
        break
    print('    Warning! Path Entered Was Invalid')
loc = pathManager.confirmPath(loc)

desc = input('    CSV Destination Path : ')

path = pathManager.pathManager(loc, desc)

path.CSVify()