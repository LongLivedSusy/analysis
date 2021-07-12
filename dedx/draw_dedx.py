from config_FabDraw import *

draw_figure(inputfile1='output_bigchunks/Run2016.root',
	inputfile2='output_bigchunks/Summer16.TotalMC.root',
	outputdir='plot_dedxscalesmear',
	outputfile='Phase0_Dedx_barrel.png',
	hist='hTrkPixelDedx_fromZ_barrel',
	legend1='data',
	legend2='Summer16 MC',
	xtitle='MeV/cm')

draw_figure(inputfile1='output_bigchunks/Run2016.root',
	inputfile2='output_bigchunks/Summer16.TotalMC.root',
	outputdir='plot_dedxscalesmear',
	outputfile='Phase0_Dedx_endcap.png',
	hist='hTrkPixelDedx_fromZ_endcap',
	legend1='data',
	legend2='Summer16 MC',
	xtitle='MeV/cm')

draw_figure(inputfile1='output_bigchunks/Run2016.root',
	inputfile2='output_bigchunks/Summer16.TotalMC.root',
	outputdir='plot_dedxscalesmear',
	outputfile='Phase0_DedxScaleSmear_barrel.png',
	hist='hTrkPixelDedxScaleSmear_fromZ_barrel',
	legend1='data',
	legend2='Summer16 MC',
	xtitle='MeV/cm')

draw_figure(inputfile1='output_bigchunks/Run2016.root',
	inputfile2='output_bigchunks/Summer16.TotalMC.root',
	outputdir='plot_dedxscalesmear',
	outputfile='Phase0_DedxScaleSmear_endcap.png',
	hist='hTrkPixelDedxScaleSmear_fromZ_endcap',
	legend1='data',
	legend2='Summer16 MC',
	xtitle='MeV/cm')

draw_figure(inputfile1='output_bigchunks/Run2017-2018.root',
	inputfile2='output_bigchunks/Fall17.TotalMC.root',
	outputdir='plot_dedxscalesmear',
	outputfile='Phase1_Dedx_barrel.png',
	hist='hTrkPixelDedx_fromZ_barrel',
	legend1='data',
	legend2='Fall17 MC',
	xtitle='MeV/cm')

draw_figure(inputfile1='output_bigchunks/Run2017-2018.root',
	inputfile2='output_bigchunks/Fall17.TotalMC.root',
	outputdir='plot_dedxscalesmear',
	outputfile='Phase1_Dedx_endcap.png',
	hist='hTrkPixelDedx_fromZ_endcap',
	legend1='data',
	legend2='Fall17 MC',
	xtitle='MeV/cm')

draw_figure(inputfile1='output_bigchunks/Run2017-2018.root',
	inputfile2='output_bigchunks/Fall17.TotalMC.root',
	outputdir='plot_dedxscalesmear',
	outputfile='Phase1_DedxScaleSmear_barrel.png',
	hist='hTrkPixelDedxScaleSmear_fromZ_barrel',
	legend1='data',
	legend2='Fall17 MC',
	xtitle='MeV/cm')

draw_figure(inputfile1='output_bigchunks/Run2017-2018.root',
	inputfile2='output_bigchunks/Fall17.TotalMC.root',
	outputdir='plot_dedxscalesmear',
	outputfile='Phase1_DedxScaleSmear_endcap.png',
	hist='hTrkPixelDedxScaleSmear_fromZ_endcap',
	legend1='data',
	legend2='Fall17 MC',
	xtitle='MeV/cm')
