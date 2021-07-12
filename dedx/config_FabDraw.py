import os as os_
import sys
from glob import glob
from ROOT import *
from shared_utils import *
import argparse

gROOT.SetBatch(True)
gStyle.SetOptStat(False)

def FabDraw(cGold,leg,hTruth,hComponents,datamc='MC',lumi=135.9, title = '', LinearScale=True, fractionthing='data/mc',xtitle=''):
	print 'datamc in FabDraw'
	cGold.cd()
	pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
	pad1.SetBottomMargin(0.0)
	pad1.SetLeftMargin(0.12)
	if not LinearScale:
		pad1.SetLogy()

	pad1.SetGridx()
	#pad1.SetGridy()
	pad1.Draw()
	pad1.cd()
	for ih in range(1,len(hComponents[1:])+1):
		hComponents[ih].Add(hComponents[ih-1])
	hComponents.reverse()        
	if abs(hComponents[0].Integral(-1,999)-1)<0.001:
		hComponents[0].GetYaxis().SetTitle('Normalized')
	else: hComponents[0].GetYaxis().SetTitle('Events/bin')
	cGold.Update()
	hTruth.GetYaxis().SetTitleOffset(1.15)
	hTruth.SetMarkerStyle(20)
	histheight = 1.5*max(hComponents[0].GetMaximum(),hTruth.GetMaximum())
	if LinearScale: low, high = 0, histheight
	else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hTruth.GetMinimum())), 1000*histheight

	title0 = hTruth.GetTitle()
	if datamc=='MC':
		for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
		leg.AddEntry(hTruth,hTruth.GetTitle(),'lpf')        
	else:
		for ihComp, hComp in enumerate(hComponents):
		    leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
		leg.AddEntry(hTruth,title0,'lp')    
	hTruth.SetTitle('')
	hComponents[0].SetTitle('')
	if LinearScale: hComponents[0].GetYaxis().SetRangeUser(0, 1.5*hTruth.GetMaximum())
	else: hComponents[0].GetYaxis().SetRangeUser(0.001, 100*hTruth.GetMaximum())
	hComponents[0].Draw('hist')

	for h in hComponents[1:]: 
		h.Draw('hist same')
		cGold.Update()
		print 'updating stack', h
	hComponents[0].Draw('same') 
	hTruth.Draw('p same')
	hTruth.Draw('e same')    
	cGold.Update()
	hComponents[0].Draw('axis same')           
	leg.Draw()        
	cGold.Update()
	#stamp2(lumi,datamc)
	cGold.Update()
	cGold.cd()
	pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
	pad2.SetTopMargin(0.0)
	pad2.SetBottomMargin(0.3)
	pad2.SetLeftMargin(0.12)
	pad2.SetGridx()
	pad2.SetGridy()
	pad2.Draw()
	pad2.cd()
	hTruthCopy = hTruth.Clone('hTruthClone'+hComponents[0].GetName())
	hRatio = hTruthCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
	hRatio.SetMarkerStyle(20)
	#hFracDiff = hComponents[0].Clone('hFracDiff')
	#hFracDiff.SetMarkerStyle(20)
	hTruthCopy.SetMarkerStyle(20)
	hTruthCopy.SetMarkerColor(1) 
	#histoStyler(hFracDiff, 1)
	histoStyler(hTruthCopy, 1)
	#hFracDiff.Add(hTruthCopy,-1)
	#hFracDiff.Divide(hTruthCopy)
	#hRatio.Divide(hTruthCopy)
	hRatio.Divide(hComponents[0])
	hRatio.GetYaxis().SetRangeUser(0.0,2.0)###
	hRatio.SetTitle('')
	if 'prediction' in title0: hRatio.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
	else: hRatio.GetYaxis().SetTitle(fractionthing)
	hRatio.GetXaxis().SetTitleSize(0.12)
	hRatio.GetXaxis().SetLabelSize(0.11)
	hRatio.GetYaxis().SetTitleSize(0.12)
	hRatio.GetYaxis().SetLabelSize(0.08)
	hRatio.GetYaxis().SetNdivisions(5)
	hRatio.GetXaxis().SetNdivisions(10)
	hRatio.GetYaxis().SetTitleOffset(0.5)
	hRatio.GetXaxis().SetTitleOffset(1.0)
	#hRatio.GetXaxis().SetTitle(hTruth.GetXaxis().GetTitle())
	hRatio.GetXaxis().SetTitle(xtitle)
	hRatio.GetYaxis().CenterTitle()
	hRatio.Draw()
	hRatio.Draw('e0')    
	pad1.cd()
    
	latex = TLatex()
    	latex.SetTextSize(0.05)
    	latex.SetTextAlign(13)
    	latex.DrawLatex(4.5,.06,"#epsilon_data(dE/dx<=4.0 MeV/cm) = "+str(round(hTruth.Integral(0,39),3)))
    	latex.DrawLatex(4.5,.05,"#epsilon_data(dE/dx>4.0 MeV/cm) = "+str(round(hTruth.Integral(40,1000),3)))
    	latex.DrawLatex(4.5,.04,"#epsilon_mc(dE/dx<=4.0 MeV/cm) = "+str(round(hComponents[0].Integral(0,39),3)))
    	latex.DrawLatex(4.5,.03,"#epsilon_mc(dE/dx>4.0 MeV/cm) = "+str(round(hComponents[0].Integral(40,1000),3)))

	hComponents.reverse()
	hTruth.SetTitle(title0)
	return hRatio, [pad1, pad2]


def draw_figure(inputfile1,inputfile2,outputdir,outputfile,hist,legend1,legend2,xtitle):
    
    if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
    
    c=mkcanvas()
    l=mklegend_(x1=.52, y1=.55, x2=.89, y2=.76, color=kWhite)
    
    fin1 = TFile(inputfile1)
    fin2 = TFile(inputfile2)
    h1 = fin1.Get(hist)
    h2 = fin2.Get(hist)
    h1.SetTitle(legend1)
    h2.SetTitle(legend2)

    h1.Scale(1.0/h1.Integral())
    h2.Scale(1.0/h2.Integral())

    hratio, [pad1, pad2]= FabDraw(c,l,h1,[h2],datamc='data',xtitle=xtitle)

    c.Update()
    c.SaveAs(outputdir+'/'+outputfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputfile1', dest='inputfile1',required=True)
    parser.add_argument('--inputfile2', dest='inputfile2',required=True)
    parser.add_argument("--outputdir",default="plot",dest="outputdir")
    parser.add_argument("--outputfile",default="output.root",dest="outputfile")
    parser.add_argument("--hist",default="",dest="hist")
    parser.add_argument("--legend1",type=str,default="",dest="legend1")
    parser.add_argument("--legend2",type=str,default="",dest="legend2")
    parser.add_argument("--xtitle",type=str,default="",dest="xtitle")

    args = parser.parse_args()
    inputfile1 = args.inputfile1
    inputfile2 = args.inputfile2
    outputdir = args.outputdir
    outputfile = args.outputfile
    hist = args.hist
    legend1 = args.legend1
    legend2 = args.legend2
    xtitle = args.xtitle
    
    draw_figure(inputfile1,inputfile2,outputdir,outputfile,hist,legend1=legend1,legend2=legend2,xtitle=xtitle)
    
