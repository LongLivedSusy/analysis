import os,sys
from ROOT import *
gROOT.SetBatch(1)

def main(inputfile,hist,outputdir) :

    if not os.path.exists(outputdir):
	os.system('mkdir -p '+outputdir)

    histname = hist[0]
    xtitle = hist[1]
    ytitle = hist[2]
    LogZ = hist[3]
    rebinx = hist[4]
    rebiny = hist[5]
    
    c=TCanvas('c','',800,600)
    
    f = TFile(inputfile)
    
    h = f.Get(histname)
    
    h.GetXaxis().SetTitle(xtitle)
    h.GetYaxis().SetTitle(ytitle)
    h.RebinX(rebinx)
    h.RebinY(rebiny)

    h.Draw('COLZ')
    
    c.SetLogz(LogZ)
    outputname = inputfile.split('/')[-1].replace('.root','').replace('vertex_','')
    c.SaveAs(outputdir+'/'+outputname+'_'+histname+'.png')

if __name__ == '__main__' :

    inputfiles = [
	    "./SV_rootfiles/vertex_Run2016B_SingleElectron.root",
	    "./SV_rootfiles/vertex_Run2016G_SingleElectron.root",
	    "./SV_rootfiles/vertex_Run2017F_SingleElectron.root",
	    "./SV_rootfiles/vertex_Run2018C_EGamma.root",
	    "./SV_rootfiles/vertex_Summer16_T2bt.root",
	    ]
    rebinx=1
    rebiny=1
    hists = [
	    ["h2_proton_P_vs_DeDxPixel","Total momentum[GeV]","harmonic-2 dE/dx",False,rebinx,rebiny],
	    ["h2_proton_P_vs_DeDxPixelCalib","Total momentum[GeV]","harmonic-2 dE/dx",False,rebinx,rebiny],
	    ["h2_proton_P_vs_DeDxStrips","Total momentum[GeV]","harmonic-2 dE/dx",False,rebinx,rebiny],
	    ]

    outputdir = './2Dplots/'

    for inputfile in inputfiles :
	for hist in hists:
	    main(inputfile,hist,outputdir)
