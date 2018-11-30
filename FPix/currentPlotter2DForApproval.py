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
auxCylinder = ["-z Inner","-z Outer","+z Inner","+z Outer"]
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
            frameHist.GetYaxis().SetBinLabel(ibinY+1, auxCylinder[ibinY])

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
        canvas.SetLeftMargin(0.19)
        canvas.SetRightMargin(0.16)
        canvas.SetBottomMargin(0.17)
        canvas.cd()

        frameHist.GetYaxis().SetTitle("Half Cylinder")
        frameHist.GetYaxis().SetTitleOffset(2)
        frameHist.GetYaxis().SetTitleSize(0.05)
        frameHist.GetYaxis().SetLabelSize(0.07)

        frameHist.GetXaxis().SetTitle("Readout Group")
        frameHist.GetXaxis().SetTitleOffset(1.7)
        frameHist.GetXaxis().SetTitleSize(0.05)
        frameHist.GetXaxis().SetLabelSize(0.07)

        frameHist.GetZaxis().SetLabelSize(0.05)
        frameHist.GetZaxis().SetTitle("I_{leak}/ROC [#muA] (Disk " + str(i+1) + ")")
        frameHist.GetZaxis().SetTitleOffset(1)
        frameHist.GetZaxis().SetTitleSize(0.05)
        frameHist.GetZaxis().SetRangeUser(0,11)
        frameHist.SetMarkerSize(2)
        frameHist.Draw("colztext")

        label = ROOT.TLatex(0.14,0.95, "CMS")
        label.SetNDC()

        label2 = ROOT.TLatex(0.32,0.95, "Preliminary")
        label2.SetTextFont(52)
        label2.SetNDC()

        label3 = ROOT.TLatex(0.23,0.95, "2018")
        label3.SetTextFont(42)
        label3.SetNDC()

        label.Draw("same")
        label2.Draw("same")
        label3.Draw("same")
        canvas.SaveAs("FPix_Disk_" + str(i+1) + "_leakageCurrent_2D.pdf")


    fin.close()
    fout.close()
