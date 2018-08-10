import os
from numberOfROCs import *

def getRocCurrent(alias, currentValue):
    rocCurrent = 0.0
    sumRoc = 0
    auxAlias1 = "null"
    auxAlias2 = "null"

    if "LAY14" in alias:
        auxAlias1 = alias.replace("LAY14","LAY1")
        auxAlias2 = alias.replace("LAY14","LAY4")

    if "LAY23" in alias:
        auxAlias1 = alias.replace("LAY23","LAY2")
        auxAlias2 = alias.replace("LAY23","LAY3")

    for k in numberOfRocs.keys():

        if (auxAlias1.find(k)!=-1) or (auxAlias2.find(k)!=-1):
            sumRoc += float(numberOfRocs[k])

    rocCurrent = currentValue/sumRoc
    return rocCurrent


cylinder = ["BpI","BpO","BmI","BmO"]
sector   = ["S1","S2","S3","S4","S5","S6","S7","S8"]
layer    = ["LAY14","LAY23"]

fileName = "currentsFromDB.txt"
outputFile = "currentsLV.txt"

if(os.path.exists(fileName)):
    fin = open(fileName, "r+")
    lines = fin.readlines()

    fout = open(outputFile,"w")

    for index1 in cylinder:
        for index2 in sector:
            for index3 in layer:

                alias = "PixelBarrel_" + index1 + "_" + index2 + "_" + index3
                anaCurrent = -999.
                digCurrent = -999.

                for l in lines:
                    line = l.split()

                    aliasLV = "null"

                    if "LAY14/channel000" in line[0]:
                        aliasLV = line[0].replace("LAY14/channel000","LAY14Dig")

                    if "LAY14/channel001" in line[0]:
                        aliasLV = line[0].replace("LAY14/channel001","LAY14Ana")

                    if "LAY23/channel000" in line[0]:
                        aliasLV = line[0].replace("LAY23/channel000","LAY23Dig")

                    if "LAY23/channel001" in line[0]:
                        aliasLV = line[0].replace("LAY23/channel001","LAY23Ana")

                    if (alias in aliasLV):
                        if ("Dig" in aliasLV):
                            digCurrent = float(line[1]) * 1000.0
                            digCurrent = getRocCurrent(aliasLV, digCurrent)
                        if ("Ana" in aliasLV):
                            anaCurrent = float(line[1]) * 1000.0
                            anaCurrent = getRocCurrent(aliasLV, anaCurrent)


                if digCurrent == -999. or anaCurrent == -999.:
                    print alias, " has empty content!  Dig: ", digCurrent, "  Ana: ", anaCurrent

                fout.write(alias + "   " + str(digCurrent) + "   " + str(anaCurrent) + "\n")


    fin.close()
    fout.close()
