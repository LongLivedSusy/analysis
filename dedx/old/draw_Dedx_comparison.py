import os,sys
from ROOT import *
from glob import glob
from natsort import natsorted,ns
from shared_utils import *

gROOT.SetBatch(1)
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)

#format_c = 'pdf'
format_c = 'png'

def main(SelectedData,SelectedMC,hist,outputdir):

    print 'Drawing for ',hist
    c = mkcanvas()
    pad1 = TPad('pad1','',0,0.4,1,1.0)
    pad1.SetBottomMargin(0.0)
    pad1.SetLeftMargin(0.12)
    pad2 = TPad('pad2','',0,0.05,1,0.4)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.3)
    pad2.SetLeftMargin(0.12)
    pad2.SetGridx()
    pad2.SetGridy()
    
    c.Draw()
    pad1.Draw()
    pad2.Draw()
    #pad1.DrawFrame(0,0,10,0.15)
    #pad2.DrawFrame(0,0,10,2)

    stamp()
    pad1.cd()

    tl = mklegend(0.6,0.5,0.9,0.8)
    
    
    fin={}
    hDedx={}
    hDedx_ratio={}
     
    i = 0
    # Adding all MC
    for name,f in natsorted(SelectedMC.items()):
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
	if i==0:
	    print 'Cloning ',name
	    hDedx_MC = hDedx[name].Clone('hDedx_MC')
	else : 
	    print 'Adding ',name
	    hDedx_MC.Add(hDedx[name])
	i+=1

    hDedx_MC.SetLineWidth(2)
    hDedx_MC.Scale(1.0/hDedx_MC.Integral())
    hDedx_MC.GetXaxis().SetTitle('MeV/cm')
    hDedx_MC.GetYaxis().SetTitle('Normalized')
    hDedx_MC.SetFillStyle(3002)
    hDedx_MC.SetFillColor(kBlue)
    hDedx_MC.GetYaxis().SetRangeUser(0,0.15)
    hDedx_MC.Draw('HIST E SAME')
    
    # Get each data period
    j=0
    for name,f in natsorted(SelectedData.items()):
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
	if j==0:
	    print 'Cloning ',name
	    hDedx_data = hDedx[name].Clone('hDedx_data')
	else :
	    print 'Adding ',name
	    hDedx_data.Add(hDedx[name])
	j+=1
   
    hDedx_data.SetLineWidth(2)
    hDedx_data.SetLineColor(kBlack)
    hDedx_data.Scale(1.0/hDedx_data.Integral())
    hDedx_data.GetXaxis().SetTitle('MeV/cm')
    hDedx_data.GetYaxis().SetTitle('Normalized')
    hDedx_data.Draw('PE SAME')
    
    if SelectedData == dict_Run2016_SingleMuon:
	tl.AddEntry(hDedx_data,'Run2016','l')
    elif SelectedData == dict_Run2017_SingleMuon:
	tl.AddEntry(hDedx_data,'Run2017','l')
    elif SelectedData == dict_Run2018_SingleMuon:
	tl.AddEntry(hDedx_data,'Run2018','l')
    if SelectedMC == dict_Summer16:
	tl.AddEntry(hDedx_MC, 'Summer16 MC')
    elif SelectedMC == dict_Fall17 : 
	tl.AddEntry(hDedx_MC, 'Fall17 MC')
    
    tl.Draw('SAME')
    
    latex = TLatex()
    latex.SetTextSize(0.05)
    latex.SetTextAlign(13)
    latex.DrawLatex(4.5,.06,"#epsilon_data(0<=dE/dx<4.0 MeV/cm) = "+str(round(hDedx_data.Integral(0,39),3)))
    latex.DrawLatex(4.5,.05,"#epsilon_data(dE/dx>4.0 MeV/cm) = "+str(round(hDedx_data.Integral(40,1000),3)))
    latex.DrawLatex(4.5,.04,"#epsilon_mc(0<=dE/dx<4.0 MeV/cm) = "+str(round(hDedx_MC.Integral(0,39),3)))
    latex.DrawLatex(4.5,.03,"#epsilon_mc(dE/dx>4.0 MeV/cm) = "+str(round(hDedx_MC.Integral(40,1000),3)))


	
    pad2.cd()
    hDedx_ratio = hDedx_data.Clone('hDedx_ratio')
    hDedx_ratio.Divide(hDedx_MC)
    hDedx_ratio.GetYaxis().SetTitle('Data/MC')
    hDedx_ratio.GetYaxis().SetTitleSize(0.1)
    hDedx_ratio.GetYaxis().SetLabelSize(0.1)
    hDedx_ratio.GetYaxis().SetTitleOffset(0.5)
    hDedx_ratio.GetYaxis().CenterTitle()
    hDedx_ratio.GetYaxis().SetNdivisions(6)
    hDedx_ratio.GetYaxis().SetRangeUser(0,2)
    hDedx_ratio.GetXaxis().SetTitleSize(0.1)
    hDedx_ratio.GetXaxis().SetLabelSize(0.07)
    hDedx_ratio.Draw('e0 SAME')
        
    c.SaveAs(outputdir+'/Comparison_'+hist+'.'+format_c)
    pad1.Close()
    pad2.Close()
    c.Close()
    
if __name__ == '__main__' :

    #from Dict_datasets import *
    from Dict_datasets_doublesmear import *
    #from Dict_datasets_MIH import *

    #DataSets = ["Run2016"]
    #DataSets = ["Run2017"]
    #DataSets = ["Run2018"]
    DataSets = ["Run2016","Run2017","Run2018"]

    for	data in DataSets:
        #outputdir = './DedxComparison_'+data
        outputdir = './DedxComparison_'+data+'_doublesmear'
        #outputdir = './DedxComparison_'+data+'_lowerbound'
	#outputdir = './DedxComparison_'+data+'_MIH_lowerbound'
	if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
    	   
	if data == "Run2016":
	    SelectedMC = dict_Summer16
	    SelectedData = dict_Run2016_SingleMuon
	elif data == "Run2017":
	    #SelectedMC = dict_Summer16
	    SelectedMC = dict_Fall17
    	    SelectedData = dict_Run2017_SingleMuon
	elif data == "Run2018":
	    #SelectedMC = dict_Summer16
	    SelectedMC = dict_Fall17
    	    SelectedData = dict_Run2018_SingleMuon
	else : 
	    print 'wrong data'
	    quit()

	hists=[
		#'hTrkPixelDedx_fromZ_barrel',
		#'hTrkPixelDedx_fromZ_endcap',
		#'hTrkPixelDedxScale_fromZ_barrel',
		#'hTrkPixelDedxScale_fromZ_endcap',
		'hTrkPixelDedxScaleSmear_fromZ_barrel',
		'hTrkPixelDedxScaleSmear_fromZ_endcap',
		]
	
	# Run
	for hist in hists:
	    main(SelectedData,SelectedMC,hist,outputdir)

