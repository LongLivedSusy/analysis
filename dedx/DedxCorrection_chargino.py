import os,sys
from ROOT import *
from glob import glob
from shared_utils import *
from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(False)
gStyle.SetOptFit(1111)

#format_c = 'pdf'
format_c = 'png'

rebin = 2

dict_Summer16_FullSimSignal = {
	#'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.root',
	#'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-50':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1.root',
	#'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-200':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1.root',
	#'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1.root',
	#'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-600':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1.root',
	#'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-800':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1.root',
	'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1000':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1.root',
	#'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1100':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1.root',
        }

dict_Summer16_FastSimSignal = {
	#'Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1.root',
	#'Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-50':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-50.root',
	#'Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-200':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-200.root',
	#'Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400.root',
	#'Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-600':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-600.root',
	#'Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-800':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-800.root',
	'Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1000':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1000.root',
	#'Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1100':'./output_chargino/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1100.root',
	}


def main(SelectedFastSim,SelectedFullSim,hist,outputdir):

    c = mkcanvas()
    stamp()
    tl = mklegend()
    
    fin={}
    hDedx={}
     
    # Adding Fastsim 
    i=0
    for name,f in sorted(SelectedFastSim.items()):
        fin[name] = TFile(f)
        hDedx[name] = fin[name].Get(hist)
	if i==0 :
	    print 'Cloning ',name
	    hDedx_fastsim = hDedx[name].Clone('hDedx_fastsim')
	else : 
	    print 'Adding ',name
	    hDedx_fastsim.Add(hDedx[name])
	i+=1
    
    # Adding fullsim 
    i = 0
    for name,f in sorted(SelectedFullSim.items()):
        fin[name] = TFile(f)
	hDedx[name] = fin[name].Get(hist)
	if i==0:
	    print 'Cloning ',name
	    hDedx_fullsim = hDedx[name].Clone('hDedx_fullsim')
	else : 
	    print 'Adding ',name
	    hDedx_fullsim.Add(hDedx[name])
	i+=1

    # Normalize Fastsim and Fullsim histogram
    hDedx_fullsim.Scale(1.0/hDedx_fullsim.Integral())
    hDedx_fastsim.Scale(1.0/hDedx_fastsim.Integral())

    hDedx_fullsim.Rebin(rebin)
    hDedx_fastsim.Rebin(rebin)
    
    c_fullsim = mkcanvas()
    c_fullsim.cd()
    #fitres_fullsim = hDedx_fullsim.Fit('gaus','S','',2.5,3.5) #mLSP1
    #fitres_fullsim = hDedx_fullsim.Fit('gaus','S','',2.2,3.0) #mLSP50
    #fitres_fullsim = hDedx_fullsim.Fit('gaus','S','',2.4,3.4) #mLSP200
    #fitres_fullsim = hDedx_fullsim.Fit('gaus','S','',3.6,4.2) #mLSP1100
    hDedx_fullsim.Draw('HIST E SAME')
    c_fullsim.SaveAs(outputdir+'/'+hist+'_fullsim.'+format_c)
    
    c_fastsim = mkcanvas()
    c_fastsim.cd()
    #fitres_fastsim = hDedx_fastsim.Fit('gaus','S','',4.0,4.6) #mLSP1
    #fitres_fastsim = hDedx_fastsim.Fit('gaus','S','',2.6,3.2) #mLSP50
    #fitres_fastsim = hDedx_fastsim.Fit('gaus','S','',2.6,3.2) #mLSP200
    #fitres_fastsim = hDedx_fastsim.Fit('gaus','S','',3.6,4.2) #mLSP1100
    hDedx_fastsim.Draw('HIST E SAME')
    c_fastsim.SaveAs(outputdir+'/'+hist+'_fastsim.'+format_c)

#    mean_fullsim = hDedx_fullsim.GetFunction('gaus').GetParameter(1)
#    mean_fastsim = hDedx_fastsim.GetFunction('gaus').GetParameter(1)
#    with open(outputdir+'/SF_'+hist+'.txt','w') as txt:
#	SF = round(mean_fullsim/mean_fastsim,3)
#	print 'SF : ',SF
#	txt.write('Summer16PrivateFastsim:%s,\n'%(SF))
   
    
if __name__ == '__main__' :


    #outputdir = './DedxScale_chargino_mStop1300_mLSP1'
    #outputdir = './DedxScale_chargino_mStop1300_mLSP50'
    #outputdir = './DedxScale_chargino_mStop1300_mLSP200'
    #outputdir = './DedxScale_chargino_mStop1300_mLSP400'
    #outputdir = './DedxScale_chargino_mStop1300_mLSP600'
    #outputdir = './DedxScale_chargino_mStop1300_mLSP800'
    outputdir = './DedxScale_chargino_mStop1300_mLSP1000'
    #outputdir = './DedxScale_chargino_mStop1300_mLSP1100'
    if not os.path.exists(outputdir) : os.system('mkdir -p '+outputdir)
       
    SelectedFullSim = dict_Summer16_FullSimSignal
    SelectedFastSim = dict_Summer16_FastSimSignal
    
    hists=[
    	 # before calibration
    	'hTrkPixelDedx_charginomatch_barrel',
    	'hTrkPixelDedx_charginomatch_endcap',
	#'hGenCharginoP',
	#'hGenCharginoPt',
	#'hGenCharginoEta',
	#'hGenCharginoPhi',
	#'hGenCharginoMass',
    	]
    
    # Run
    for hist in hists:
        main(SelectedFastSim,SelectedFullSim,hist,outputdir)

