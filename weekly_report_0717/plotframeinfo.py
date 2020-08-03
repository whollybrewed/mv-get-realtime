import sys 
import re
import matplotlib.pyplot as plt

frDict = {}
with open(sys.argv[1], 'r') as f:
    for line in f:
        splitLine = line.split(", ")
        frDict[int(splitLine[0])] = int(splitLine[1])
f.close()

with open(sys.argv[2], 'r') as f:
    i = 0
    for line in f:
        i = i + 1
        mbList = (list(map(int, re.findall('\d+', line))))
        if i in frDict:
            mbList.append(frDict[i])
        else:
            mbList.append(0)
        frDict[i] = mbList
f.close()

frame = int(sys.argv[3])
plotList = frDict[frame]

xAxis = [0,1]
xname = ["Motion Vector " + str(plotList[3]), "Macro block"]

plt.bar(0, plotList[3], color= '#ece661', edgecolor= 'w')
s1 = plt.bar(1, plotList[0], color= '#e80027', edgecolor= 'w')
s2 = plt.bar(1, plotList[1], bottom=plotList[0], color= '#337f4e', edgecolor= 'w')
s3 = plt.bar(1, plotList[2], bottom=plotList[1] + plotList[0], color= '#005295', edgecolor= 'w')


plt.xticks(xAxis, xname, fontweight='bold')
plt.xlabel("Frame:" + str(frame))
plt.legend((s1, s2, s3), 
          ("intra " + str(plotList[0]), "skip " + str(plotList[1]), "inter " + str(plotList[2])), loc=1)
plt.show()

