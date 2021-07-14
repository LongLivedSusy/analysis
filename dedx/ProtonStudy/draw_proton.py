from config_FabDraw import *

# 2016
#draw_figure(inputfile1='./SV_rootfiles/vertex_Run2016B_SingleElectron.root',
#	inputfile2='./SV_rootfiles/vertex_Summer16_T2bt.root',
#	outputdir='plot_proton',
#	outputfile='Run2016B_pixeldedx.png',
#	hist='dedxpixel_good_proton',
#	legend1='Run2016B',
#	legend2='Summer16 T2btLL MC',
#	xtitle='MeV/cm')
#
#draw_figure(inputfile1='./SV_rootfiles/vertex_Run2016B_SingleElectron.root',
#	inputfile2='./SV_rootfiles/vertex_Summer16_T2bt.root',
#	outputdir='plot_proton',
#	outputfile='Run2016B_pixeldedx_barrel.png',
#	hist='dedxpixel_good_proton_barrel',
#	legend1='Run2016B',
#	legend2='Summer16 T2btLL MC',
#	xtitle='MeV/cm')
#
#draw_figure(inputfile1='./SV_rootfiles/vertex_Run2016B_SingleElectron.root',
#	inputfile2='./SV_rootfiles/vertex_Summer16_T2bt.root',
#	outputdir='plot_proton',
#	outputfile='Run2016B_pixeldedx_endcap.png',
#	hist='dedxpixel_good_proton_endcap',
#	legend1='Run2016B',
#	legend2='Summer16 T2btLL MC',
#	xtitle='MeV/cm')
#
#draw_figure(inputfile1='./SV_rootfiles/vertex_Run2016B_SingleElectron.root',
#	inputfile2='./SV_rootfiles/vertex_Summer16_T2bt.root',
#	outputdir='plot_proton',
#	outputfile='Run2016B_pixeldedxCalib.png',
#	hist='dedxpixelCalib_good_proton',
#	legend1='Run2016B',
#	legend2='Summer16 T2btLL MC',
#	xtitle='MeV/cm')

draw_figure(inputfile1='./SV_rootfiles/vertex_Run2016G_SingleElectron.root',
	inputfile2='./SV_rootfiles/vertex_Summer16_T2bt.root',
	outputdir='plot_proton',
	outputfile='Phase0_pixeldedx.png',
	hist='dedxpixel_good_proton',
	legend1='Run2016G',
	legend2='Summer16 T2btLL MC',
	xtitle='MeV/cm',
	rebin=2)

draw_figure(inputfile1='./SV_rootfiles/vertex_Run2016G_SingleElectron.root',
	inputfile2='./SV_rootfiles/vertex_Summer16_T2bt.root',
	outputdir='plot_proton',
	outputfile='Phase0_pixeldedxCalib.png',
	hist='dedxpixelCalib_good_proton',
	legend1='Run2016G',
	legend2='Summer16 T2btLL MC',
	xtitle='MeV/cm',
	rebin=2)

# Phase-1
draw_figure(inputfile1='./SV_rootfiles/vertex_Phase1.root',
	inputfile2='./SV_rootfiles/vertex_Fall17_DYJetsToLL_M-50.root',
	outputdir='plot_proton',
	outputfile='Phase1_pixeldedx.png',
	hist='dedxpixel_good_proton',
	legend1='Run2017F+Run2018C',
	legend2='DYJetsToLL_M-50 Fall17 MC',
	xtitle='MeV/cm',
	rebin=2)

draw_figure(inputfile1='./SV_rootfiles/vertex_Phase1.root',
	inputfile2='./SV_rootfiles/vertex_Fall17_DYJetsToLL_M-50.root',
	outputdir='plot_proton',
	outputfile='Phase1_pixeldedxCalib.png',
	hist='dedxpixelCalib_good_proton',
	legend1='Run2017F+Run2018C',
	legend2='DYJetsToLL_M-50 Fall17 MC',
	xtitle='MeV/cm',
	rebin=2)

# Other plots
draw_figure(inputfile1='./SV_rootfiles/vertex_Run2016G_SingleElectron.root',
	inputfile2='./SV_rootfiles/vertex_Summer16_T2bt.root',
	outputdir='plot_proton',
	outputfile='Phase0_protonmass.png',
	hist='massdedxpixel_good_proton',
	legend1='Run2016G',
	legend2='Summer16 T2btLL MC',
	xtitle='GeV',
	rebin=2)

draw_figure(inputfile1='./SV_rootfiles/vertex_Run2016G_SingleElectron.root',
	inputfile2='./SV_rootfiles/vertex_Summer16_T2bt.root',
	outputdir='plot_proton',
	outputfile='Phase0_protonmassCalib.png',
	hist='massdedxpixelCalib_good_proton',
	legend1='Run2016G',
	legend2='Summer16 T2btLL MC',
	xtitle='GeV',
	rebin=2)
