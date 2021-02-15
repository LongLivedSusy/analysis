import os,sys
from ROOT import *
from glob import glob
from natsort import natsorted,ns

gROOT.SetBatch(1)
gStyle.SetOptStat(1)
gStyle.SetOptFit(1111)


def main(f,hist,outputdir='./plots_DedxCorrection_proton'):

    c = TCanvas('c','',800,600)
    tl = TLegend(0.5,0.6,0.9,0.9)
    
    fin=TFile(f)
    h=hist[0]
    hXtitle=str(hist[1])
    setLogy=bool(hist[2])
    rebin=int(hist[3])

    c.cd()
    
    hDedx = fin.Get(h)
    print hDedx.Integral()
    if hDedx.GetEntries() == 0 : 
	print 'Empty' 
	return 0

    hDedx.SetTitle('')
    hDedx.Rebin(rebin)
    hDedx.Scale(1.0/hDedx.Integral())
    
    fitres = hDedx.Fit('gaus','S','',1.5,3.0)
    if 'T2bt' in f :
	fitres = hDedx.Fit('gaus','S','',2,4.0)

    fitres.Print()
    
    mean = hDedx.GetFunction('gaus').GetParameter(1)
    hDedx.GetXaxis().SetTitle(hXtitle)
    hDedx.GetYaxis().SetTitle('Normalized')
    hDedx.Draw('HIST E SAME')
    
    if not os.path.exists(outputdir):
	os.system('mkdir -p '+outputdir)
    c.SaveAs(outputdir+'/ProtonDedxCalib_'+h+'.'+format_c)
    c.Close()

    print 'mean : ',mean
    with open(outputdir+'/mean_'+h+'.txt','w') as txt :
	txt.write(str(mean))
    
    
if __name__ == '__main__' :

    #format_c = 'pdf'
    format_c = 'png'
    
    f_data_2017C = "./SV_rootfiles/vertex_Run2017C_SingleMuon_UL.root" 
    f_sim = "./SV_rootfiles_old/vertex_Summer16_T2bt.root" 

    rebin=2

    hists=[
	# ['HISTNAME','X-axis title',logy,rebin],
	#['dedxpixel_good_proton_P0to0p5','Proton(P 0-0.5) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P0p5to1','Proton(P 0.5~1) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P1to1p5','Proton(P 1~1.5) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P1p5to2','Proton(P 1.5~2) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P2to3','Proton(P 2~3) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P3to4','Proton(P 3~4) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P4to5','Proton(P 4-5) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P5to6','Proton(P 5-6) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P6toInf','Proton(P 6-Inf) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P0to0p5_barrel','Proton(P 0-0.5) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P0p5to1_barrel','Proton(P 0.5~1) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P1to1p5_barrel','Proton(P 1~1.5) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P1p5to2_barrel','Proton(P 1.5~2) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P2to3_barrel','Proton(P 2~3) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P3to4_barrel','Proton(P 3~4) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P4to5_barrel','Proton(P 4-5) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P5to6_barrel','Proton(P 5-6) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P6toInf_barrel','Proton(P 6-Inf) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P0to0p5_endcap','Proton(P 0-0.5) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P0p5to1_endcap','Proton(P 0.5~1) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P1to1p5_endcap','Proton(P 1~1.5) pixel dEdx [MeV]',False,rebin],
	#['dedxpixel_good_proton_P1p5to2_endcap','Proton(P 1.5~2) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P2to3_endcap','Proton(P 2~3) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P3to4_endcap','Proton(P 3~4) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P4to5_endcap','Proton(P 4-5) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P5to6_endcap','Proton(P 5-6) pixel dEdx [MeV]',False,rebin],
	['dedxpixel_good_proton_P6toInf_endcap','Proton(P 6-Inf) pixel dEdx [MeV]',False,rebin],
    ]
    
    # Run
    for hist in hists:
        #main(f_data_2016G, hist, outputdir='./plots_DedxCorrection_proton_data_2016G')
        main(f_data_2017C, hist, outputdir='./plots_DedxCorrection_proton_data_2017C')
        #main(f_sim, hist, outputdir='./plots_DedxCorrection_proton_sim')
