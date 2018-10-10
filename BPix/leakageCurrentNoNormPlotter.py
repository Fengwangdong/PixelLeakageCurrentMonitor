import ROOT
from ROOT import TStyle, TFile, TH1, TH1F, TCanvas, TROOT, TLegend, TLatex, TKey, TString, TAttFill, TGraphAsymmErrors, TColor
import tdrStyle
import os
from array import array
import numpy

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)

inputFileName = "HVCurrents.txt"
layer = ["LAY1","LAY2","LAY3","LAY4"]

dataPlus = {}
dataMinus = {}

for j,index in enumerate(layer):
    dataPlus[j] = [array('d'), array('d'), array('d'), array('d')]
    dataMinus[j] = [array('d'), array('d'), array('d'), array('d')]

if(os.path.exists(inputFileName)):
    fin = open(inputFileName, "r+")
    lines = fin.readlines()

    for l in lines:
        line = l.split()

        for i,ilayer in enumerate(layer):

            if ilayer in line[0]:
                if ("BpI" in line[0]) or ("BpO" in line[0]):
                    dataPlus[i][0].append(float(line[1]))
                    if line[3] == "null":
                        dataPlus[i][1].append(0)
                    else:
                        dataPlus[i][1].append(float(line[3]))
                    dataPlus[i][2].append(float(0))
                    dataPlus[i][3].append(float(line[2]))

                elif("BmI" in line[0]) or ("BmO" in line[0]):
                    dataMinus[i][0].append(float(line[1]))
                    if line[3] == "null":
                        dataMinus[i][1].append(0)
                    else:
                        dataMinus[i][1].append(float(line[3]))
                    dataMinus[i][2].append(float(0))
                    dataMinus[i][3].append(float(line[2]))

            else:
                continue


    if len(dataPlus) > 0 and len(dataMinus) > 0:

        for k,klayer in enumerate(layer):
            gr_plus = ROOT.TGraphAsymmErrors(16, dataPlus[k][0], dataPlus[k][1], dataPlus[k][3], dataPlus[k][3], dataPlus[k][2], dataPlus[k][2])
            gr_minus = ROOT.TGraphAsymmErrors(16, dataMinus[k][0], dataMinus[k][1], dataMinus[k][3], dataMinus[k][3], dataMinus[k][2], dataMinus[k][2])

            canvas = ROOT.TCanvas("leakageCurrent","leakage current",900,900)
            canvas.SetTopMargin(0.05)
            canvas.SetLeftMargin(0.2)
            canvas.SetBottomMargin(0.18)
            canvas.cd()

            frameHist = ROOT.TH1F("leakageCurrent","leakage current", 16, 0, 360)
            frameHist.SetStats(0)

            maxValue = max(dataPlus[k][1])
            if maxValue < max(dataMinus[k][1]):
                maxValue = max(dataMinus[k][1])

            minValue = min([x for x in dataPlus[k][1] if x!=0])
            if minValue > min([x for x in dataMinus[k][1] if x!=0]):
                minValue = min([x for x in dataMinus[k][1] if x!=0])

            print "MAXIMUM of", klayer, ":", maxValue, "uA"
            print "MININUM of", klayer, ":", minValue, "uA"
            print "Spread of", klayer, ":", maxValue-minValue, "uA"

            frameHist.GetYaxis().SetRangeUser(100,3000)
            frameHist.GetYaxis().SetTitle("I_{leak} [uA]")
            frameHist.GetYaxis().SetTitleOffset(1.6)
            frameHist.GetYaxis().SetTitleSize(0.06)
            frameHist.GetYaxis().SetLabelSize(0.05)

            frameHist.GetXaxis().SetTitle("#phi [*#pi/180 rad]")
            frameHist.GetXaxis().SetTitleSize(0.08)
            frameHist.GetXaxis().SetLabelSize(0.06)

            frameHist.Draw()

            gr_plus.SetLineColor(2)
            gr_plus.SetLineWidth(4)
            gr_plus.SetMarkerSize(4)
            gr_plus.SetMarkerStyle(20)
            gr_plus.SetMarkerColor(2)

            gr_minus.SetLineColor(4)
            gr_minus.SetLineWidth(4)
            gr_minus.SetMarkerSize(3)
            gr_minus.SetMarkerStyle(21)
            gr_minus.SetMarkerColor(4)

            label = ROOT.TLatex(0.25,0.9, klayer)
            label.SetNDC()

            legend = ROOT.TLegend(0.75,0.87,0.99,0.99)
            legend.SetFillColor(0)
            legend.SetTextSize(0.04)
            legend.AddEntry(gr_plus,"BPix_Bp","lpe")
            legend.AddEntry(gr_minus,"BPix_Bm","lpe")

            gr_plus.Draw("ep same")
            gr_minus.Draw("ep same")
            legend.Draw("same")
            label.Draw("same")
            canvas.SaveAs("BPix_" + klayer + "_leakageCurrents_NoNorm.pdf")
