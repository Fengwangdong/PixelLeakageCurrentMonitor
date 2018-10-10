from phimap import *
from phiunc import *
import os
import ROOT
from ROOT import TH1, TH1F

def getPhi(alias):

    phi = -999.0

    for j in phimap.keys():
        if j.find(alias) != -1:
            phi = float(phimap[j])
            break

    return phi


def getPhiUnc(alias):

    unc = -999.0

    for j in phiunc.keys():
        if j.find(alias) != -1:
            unc = float(phiunc[j])
            break

    return unc


cylinder = ["BpI","BpO","BmI","BmO"]
sector   = ["S1","S2","S3","S4","S5","S6","S7","S8"]
layer    = ["LAY1","LAY2","LAY3","LAY4"]

fileName = "currentsFromDB.txt"
outputFile = "HVCurrents.txt"

if(os.path.exists(fileName)):
    fin = open(fileName, "r+")
    lines = fin.readlines()

    fout = open(outputFile,"w")

    for index1 in cylinder:
        for index2 in sector:
            for index3 in layer:

                alias = "PixelBarrel_" + index1 + "_" + index2 + "_" + index3
                phi = getPhi(alias)
                phiUnc = getPhiUnc(alias)
                currentHist = ROOT.TH1F("leakageCurrent", "leakageCurrent", 300, 0, 3000)

                for l in lines:
                    line = l.split()

                    aliasin = "null"

                    if "LAY14/channel002" in line[0]:
                        aliasin = line[0].replace("LAY14/channel002","LAY1")

                    elif "LAY14/channel003" in line[0]:
                        aliasin = line[0].replace("LAY14/channel003","LAY4")

                    elif "LAY23/channel002" in line[0]:
                        aliasin = line[0].replace("LAY23/channel002","LAY3")

                    elif "LAY23/channel003" in line[0]:
                        aliasin = line[0].replace("LAY23/channel003","LAY2")

                    if aliasin == alias:
                        HVCurrent = float(line[1])
                        currentHist.Fill(HVCurrent)

                if currentHist.GetEntries() == 0:
                    fout.write(alias + "   " + str(phi) + "   " + str(phiUnc) + "   " + "null" + "\n")

                else:
                    fout.write(alias + "   " + str(phi) + "   " + str(phiUnc) + "   " + str(HVCurrent) + "\n")

                currentHist.Reset()


    fin.close()
    fout.close()
