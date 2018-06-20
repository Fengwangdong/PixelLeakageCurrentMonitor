from numberOfROCs import *
from phimap import *
import os
import ROOT
from ROOT import TH1, TH1D

def getLeakageCurrent(alias, currentValue):
    rocCurrent = 0.

    for k in numberOfRocs.keys():

        if k.find(alias)!=-1:
            rocCurrent = currentValue/float(numberOfRocs[k])
            #rocCurrent = currentValue/float(numberOfRocs[k])*16.0 # each module has 16 rocs
            break

    return rocCurrent


def getPhi(alias):

    phi = -999.0

    for j in phimap.keys():
        if j.find(alias)!=-1:
            phi = float(phimap[j])
            break

    return phi


cylinder = ["BpI","BpO","BmI","BmO"]
sector   = ["S1","S2","S3","S4","S5","S6","S7","S8"]
layer    = ["LAY1","LAY2","LAY3","LAY4"]
#disk     = ["D1","D2","D3"]
#rog      = ["ROG1","ROG2","ROG3","ROG4"]
#ring     = ["RNG1","RNG2"]

#Colors = [9, 8, 7, 6, 5, 4, 3, 2]

fileName = "currentsFromDB.txt"
outputFile = "leakageCurrents.txt"

if(os.path.exists(fileName)):
    fin = open(fileName, "r+")
    lines = fin.readlines()

    fout = open(outputFile,"w")

    for index1 in cylinder:
        for index2 in sector:
            for index3 in layer:

                alias = "PixelBarrel_" + index1 + "_" + index2 + "_" + index3
                phi = getPhi(alias)
                currentHist = ROOT.TH1D("leakageCurrent", "leakageCurrent", 200, 0, 100)

                for l in lines:
                    line = l.split()

                    if "LAY1/channel002" in line[0]:
                        aliasin = line[0].replace("LAY1/channel002","LAY1")

                    elif "LAY1/channel003" in line[0]:
                        aliasin = line[0].replace("LAY1/channel003","LAY4")

                    elif "LAY3/channel002" in line[0]:
                        aliasin = line[0].replace("LAY3/channel002","LAY3")

                    elif "LAY3/channel003" in line[0]:
                        aliasin = line[0].replace("LAY3/channel003","LAY2")

                    if aliasin == alias:
                        rocCurrent = getLeakageCurrent(alias, float(line[1]))
                        currentHist.Fill(rocCurrent)

                if currentHist.GetEntries() == 0:
                    fout.write(alias + "   " + str(phi) + "   " + str(0) + "   " + str(0) + "\n")

                else:
                    averageCurrent = currentHist.GetMean()
                    uncCurrent = currentHist.GetRMS()
                    fout.write(alias + "   " + str(phi) + "   " + str(rocCurrent) + "   " + str(uncCurrent) + "\n")

                currentHist.Reset()


    fin.close()
    fout.close()
