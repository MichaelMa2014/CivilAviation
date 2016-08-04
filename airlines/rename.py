import os
import glob
import re
files = glob.glob('*.geojson')
for file in files:
    temp = open(file, 'r').read()
    dep = re.findall('airport1":\"(...)', temp)
    try:
        print(dep[0])
        os.rename(file, dep[0] + ".geojson")
    except:
        pass
    # os.rename(file, parts[0] + " " + file)
