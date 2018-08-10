import ROOT
from ROOT import TStyle, TFile, TH1, TH1F, TCanvas, TROOT, TLegend, TLatex, TKey, TString, TAttFill, TGraphAsymmErrors, TColor
import tdrStyle
import os
from array import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)

inputFileName = "currentsLV.txt"
layer = ["LAY14","LAY23"]

dataBpI = {}
dataBpO = {}
dataBmI = {}
dataBmO = {}

for j,index in enumerate(layer):
    dataBpI[j] = [array('d'), array('d'), array('d'), array('d')]
    dataBpO[j] = [array('d'), array('d'), array('d'), array('d')]
    dataBmI[j] = [array('d'), array('d'), array('d'), array('d')]
    dataBmO[j] = [array('d'), array('d'), array('d'), array('d')]

if(os.path.exists(inputFileName)):
    fin = open(inputFileName, "r+")
    lines = fin.readlines()

    for l in lines:
        line = l.split()

        for i,ilayer in enumerate(layer):

            if ilayer in line[0]:
                if ("BpI" in line[0]):
                    dataBpI[i][0].append(float(line[0][17:18])-0.5)
                    dataBpI[i][1].append(0.5)
                    dataBpI[i][2].append(float(line[1]))
                    dataBpI[i][3].append(float(0))

                if ("BpO" in line[0]):
                    dataBpO[i][0].append(float(line[0][17:18])-0.5)
                    dataBpO[i][1].append(0.5)
                    dataBpO[i][2].append(float(line[1]))
                    dataBpO[i][3].append(float(0))

                if ("BmI" in line[0]):
                    dataBmI[i][0].append(float(line[0][17:18])-0.5)
                    dataBmI[i][1].append(0.5)
                    dataBmI[i][2].append(float(line[1]))
                    dataBmI[i][3].append(float(0))

                if ("BmO" in line[0]):
                    dataBmO[i][0].append(float(line[0][17:18])-0.5)
                    dataBmO[i][1].append(0.5)
                    dataBmO[i][2].append(float(line[1]))
                    dataBmO[i][3].append(float(0))

            else:
                continue


    if len(dataBpI) > 0 and len(dataBpO) > 0 and len(dataBmI) > 0 and len(dataBmO) > 0:

        for k,klayer in enumerate(layer):
            gr_BpI = ROOT.TGraphAsymmErrors(8, dataBpI[k][0], dataBpI[k][2], dataBpI[k][1], dataBpI[k][1], dataBpI[k][3], dataBpI[k][3])
            gr_BpO = ROOT.TGraphAsymmErrors(8, dataBpO[k][0], dataBpO[k][2], dataBpO[k][1], dataBpO[k][1], dataBpO[k][3], dataBpO[k][3])
            gr_BmI = ROOT.TGraphAsymmErrors(8, dataBmI[k][0], dataBmI[k][2], dataBmI[k][1], dataBmI[k][1], dataBmI[k][3], dataBmI[k][3])
            gr_BmO = ROOT.TGraphAsymmErrors(8, dataBmO[k][0], dataBmO[k][2], dataBmO[k][1], dataBmO[k][1], dataBmO[k][3], dataBmO[k][3])

            canvas = ROOT.TCanvas("lowVCurrent","low voltage current",900,900)
            canvas.SetTopMargin(0.07)
            canvas.SetLeftMargin(0.15)
            canvas.SetBottomMargin(0.15)
            canvas.cd()

            frameHist = ROOT.TH1F("lowVCurrent","low voltage current", 8, 0, 8)
            frameHist.SetStats(0)

            maxValue = max(dataBpI[k][2])
            if maxValue < max(max(dataBpO[k][2]), max(dataBmI[k][2]), max(dataBmO[k][2])):
                maxValue = max(max(dataBpO[k][2]), max(dataBmI[k][2]), max(dataBmO[k][2]))

            minValue = min(abs(i) for i in dataBpI[k][2])
            if minValue > min(min(abs(i) for i in dataBpO[k][2]), min(abs(i) for i in dataBmI[k][2]), min(abs(i) for i in dataBmO[k][2])):
                minValue = min(min(abs(i) for i in dataBpO[k][2]), min(abs(i) for i in dataBmI[k][2]), min(abs(i) for i in dataBmO[k][2]))

            for ibin in xrange(8):
                frameHist.GetXaxis().SetBinLabel(ibin+1, str(ibin+1))

            frameHist.GetYaxis().SetRangeUser(minValue*0.8,maxValue*1.2)
            frameHist.GetYaxis().SetTitle("I_{digital}/ROC [mA]")
            frameHist.GetYaxis().SetTitleOffset(1.)
            frameHist.GetYaxis().SetTitleSize(0.06)
            frameHist.GetYaxis().SetLabelSize(0.05)

            frameHist.GetXaxis().SetTitle("sector")
            frameHist.GetXaxis().SetTitleSize(0.07)
            frameHist.GetXaxis().SetLabelSize(0.07)

            frameHist.Draw()

            gr_BpI.SetLineColor(2)
            gr_BpI.SetLineWidth(4)
            gr_BpI.SetMarkerSize(4)
            gr_BpI.SetMarkerStyle(20)
            gr_BpI.SetMarkerColor(2)

            gr_BpO.SetLineColor(4)
            gr_BpO.SetLineWidth(4)
            gr_BpO.SetMarkerSize(4)
            gr_BpO.SetMarkerStyle(21)
            gr_BpO.SetMarkerColor(4)

            gr_BmI.SetLineColor(6)
            gr_BmI.SetLineWidth(4)
            gr_BmI.SetMarkerSize(4)
            gr_BmI.SetMarkerStyle(22)
            gr_BmI.SetMarkerColor(6)

            gr_BmO.SetLineColor(8)
            gr_BmO.SetLineWidth(4)
            gr_BmO.SetMarkerSize(4)
            gr_BmO.SetMarkerStyle(33)
            gr_BmO.SetMarkerColor(8)

            label = ROOT.TLatex(0.21,0.94, klayer)
            label.SetNDC()

            legend = ROOT.TLegend(0.77,0.77,0.99,0.99)
            legend.SetFillColor(0)
            legend.SetTextSize(0.03)
            legend.AddEntry(gr_BpI,"BPix_BpI","lpe")
            legend.AddEntry(gr_BpO,"BPix_BpO","lpe")
            legend.AddEntry(gr_BmI,"BPix_BmI","lpe")
            legend.AddEntry(gr_BmO,"BPix_BmO","lpe")

            gr_BpI.Draw("ep same")
            gr_BpO.Draw("ep same")
            gr_BmI.Draw("ep same")
            gr_BmO.Draw("ep same")
            legend.Draw("same")
            label.Draw("same")
            canvas.SaveAs("BPix_" + klayer + "_digitalCurrents.pdf")
