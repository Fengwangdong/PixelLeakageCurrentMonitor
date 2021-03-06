from numberOfROCs import *
import ROOT
from ROOT import TStyle, TH2, TH2F, TCanvas, TROOT, TLatex, TAttFill, TColor
import tdrStyle
import os
from array import array

def getLeakageCurrent(alias, currentValue):
    rocCurrent = 0.

    for k in numberOfRocs.keys():

        if k.find(alias)!=-1:
            rocCurrent = currentValue/float(numberOfRocs[k])
            break

    return rocCurrent

tdrStyle.setTDRStyle()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.1f")
ROOT.gStyle.SetPalette(87)

inputFileName = "currentsFromDB.txt"
cylinder = ["BmI","BmO","BpI","BpO"]
rog = ["ROG1","ROG2","ROG3","ROG4"]
disk = ["D1","D2","D3"]
outputFileName = "leakageCurrents.txt"

if(os.path.exists(inputFileName)):
    fin = open(inputFileName, "r+")
    lines = fin.readlines()
    fout = open(outputFileName,"w")

    for i,idisk in enumerate(disk):
        frameHist = ROOT.TH2F("leakageCurrent","leakageCurrent",8,0,8,4,0,4)
        for ibinX in xrange(4):
            frameHist.GetXaxis().SetBinLabel(ibinX*2+1, str(ibinX+1)+"(RING1)")
            frameHist.GetXaxis().SetBinLabel(ibinX*2+2, str(ibinX+1)+"(RING2)")

        for ibinY in xrange(4):
            frameHist.GetYaxis().SetBinLabel(ibinY+1, cylinder[ibinY])

        for j,jhc in enumerate(cylinder):

            for k,krog in enumerate(rog):

                for l in lines:
                    line = l.split()

                    if (idisk in line[0]) and (jhc in line[0]) and (krog in line[0]):

                        rocCurrent = getLeakageCurrent(line[0], float(line[1]))
                        fout.write(line[0] + "  " + str(rocCurrent) + "\n")

                        if "RNG1" in line[0]:
                            frameHist.SetBinContent(k*2+1,j+1,rocCurrent)

                        if "RNG2" in line[0]:
                            frameHist.SetBinContent(k*2+2,j+1,rocCurrent)

                    else:
                        continue

        canvas = ROOT.TCanvas("leakageCurrent","leakageCurrent",1300,1000)
        canvas.SetTopMargin(0.07)
        canvas.SetLeftMargin(0.1)
        canvas.SetRightMargin(0.14)
        canvas.SetBottomMargin(0.14)
        canvas.cd()

        frameHist.GetYaxis().SetTitle("Cylinder")
        frameHist.GetYaxis().SetTitleOffset(0.9)
        frameHist.GetYaxis().SetTitleSize(0.05)
        frameHist.GetYaxis().SetLabelSize(0.05)

        frameHist.GetXaxis().SetTitle("Readout Group")
        frameHist.GetXaxis().SetTitleOffset(1.2)
        frameHist.GetXaxis().SetTitleSize(0.05)
        frameHist.GetXaxis().SetLabelSize(0.04)

        frameHist.GetZaxis().SetLabelSize(0.03)
        frameHist.GetZaxis().SetTitle("I_{leak}/ROC [uA] (Disk " + str(i+1) + ")")
        frameHist.GetZaxis().SetTitleOffset(0.75)
        frameHist.GetZaxis().SetTitleSize(0.05)
        frameHist.GetZaxis().SetRangeUser(0,11)
        frameHist.SetMarkerSize(1.5)
        frameHist.Draw("colztext")

        label = ROOT.TLatex(0.17,0.95, "CMS  2018")
        label.SetNDC()

        label2 = ROOT.TLatex(0.37,0.95, "Preliminary")
        label2.SetTextFont(52)
        label2.SetNDC()

        label.Draw("same")
        label2.Draw("same")
        canvas.SaveAs("FPix_Disk_" + str(i+1) + "_leakageCurrent_2D.pdf")


    fin.close()
    fout.close()
