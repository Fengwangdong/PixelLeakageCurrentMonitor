import ROOT
from ROOT import TStyle, TFile, TH1, TH1F, TCanvas, TROOT, TLegend, TLatex, TKey, TString, TAttFill, TGraphAsymmErrors, TColor
import tdrStyle
import os
from array import array
import numpy

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)

inputFileName1 = "BeforeChangeFlow/HVCurrents.txt"
inputFileName2 = "AfterChangeFlow/HVCurrents.txt"
layer = ["LAY1","LAY2","LAY3","LAY4"]

dataPlus = {}
dataMinus = {}

for j,index in enumerate(layer):
    dataPlus[j] = [array('d'), array('d'), array('d'), array('d')]
    dataMinus[j] = [array('d'), array('d'), array('d'), array('d')]

if(os.path.exists(inputFileName1) and os.path.exists(inputFileName2)):
    fin1 = open(inputFileName1, "r+")
    fin2 = open(inputFileName2, "r+")
    lines1 = fin1.readlines()
    lines2 = fin2.readlines()

    for l1 in lines1:
        line1 = l1.split()

        for l2 in lines2:
            line2 = l2.split()

            for i,ilayer in enumerate(layer):

                if ilayer in line1[0] and ilayer in line2[0]:
                    if (("BpI" in line1[0]) or ("BpO" in line1[0])) and (line1[0] == line2[0]):
                        dataPlus[i][0].append(float(line1[1]))
                        if line1[3] == "null" and line2[3] == "null":
                            dataPlus[i][1].append(0)
                        elif line1[3] == "null":
                            dataPlus[i][1].append(float(line2[3]))
                        elif line2[3] == "null":
                            dataPlus[i][1].append(float(line1[3]))
                        else:
                            dataPlus[i][1].append(float(line1[3]) - float(line2[3]))
                        dataPlus[i][2].append(float(0))
                        dataPlus[i][3].append(float(line1[2]))

                    elif(("BmI" in line1[0]) or ("BmO" in line1[0])) and (line1[0] == line2[0]):
                        dataMinus[i][0].append(float(line1[1]))
                        if line1[3] == "null" and line2[3] == "null":
                            dataMinus[i][1].append(0)
                        elif line1[3] == "null":
                            dataMinus[i][1].append(float(line2[3]))
                        elif line2[3] == "null":
                            dataMinus[i][1].append(float(line1[3]))
                        else:
                            dataMinus[i][1].append(float(line1[3]) - float(line2[3]))
                        dataMinus[i][2].append(float(0))
                        dataMinus[i][3].append(float(line1[2]))

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

            frameHist.GetYaxis().SetRangeUser(0,1000)
            #frameHist.GetYaxis().SetRangeUser(0,400)
            frameHist.GetYaxis().SetTitle("I_{leak}(before) - I_{leak}(after) [uA]")
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
            canvas.SaveAs("BPix_" + klayer + "_leakageSpread_NoNorm.pdf")
