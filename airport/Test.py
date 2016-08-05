import sys
import os
import re

fromfile = open("airport.txt","r",encoding = "utf-8")
inputtext = fromfile.read()

pattern = re.compile(r"{.*?}")
result = pattern.findall(inputtext)

for i in range (len(result)):
    temp = result[i]
    patternname = re.compile(r'"国际航空运输协会编号":".*?"')
    resultname = patternname.findall(temp)
    Name = resultname[0][14:17]#机场编号
    temp = list(temp)
    for j in range (len(temp)):
        if(temp[j]=='"' or temp[j]=='{' or temp[j]=='}'):
            temp[j] = ''
        if(temp[j]==','):
            temp[j] = '\n\n'
    temp = ''.join(temp)

    if(Name=="AUX" or Name=="PRN"):
        continue
    tofile = open(Name+""+".txt","w",encoding="utf-8")
    tofile.write(temp)
    tofile.close()

fromfile.close()
