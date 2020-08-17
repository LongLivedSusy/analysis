from ROOT import *
from utils import *
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)




#filenames = glob('rootfiles/PromptBkgTree_*Run*_mcal10to15.root')
filenames = glob('rootfiles/PromptBkgTree_*Run*_mcal10to12.root')

#filenames = glob('rootfiles/HemLook*mcal25to40.root')
histnames = ['TrackShortSElValidationZLLCaloSideband_EtaVsPhiDT', 'TrackLongSElValidationZLLCaloSideband_EtaVsPhiDT','TrackLongSMuValidationMTCaloSideband_EtaVsPhiDT']



c1 = mkcanvas('c1')
c1.SetRightMargin(0.15)
#c1.SetLogz()
if 'HemLook' in filenames[0]: fnew = TFile('MasksHemmy_mcal25to40.root','recreate')
else: fnew = TFile('Masks_mcal10to13.root','recreate')

for histname in histnames:
	isfirstrun = True
	for ifname, fname in enumerate(filenames):
		f = TFile(fname)
		quickname_ = fname.split('DataDriven')[-1].split('_mcal')[0]
			
		h = f.Get(histname)
		if ifname==0: 
			f.ls()
			
		if 'Run' in fname:
			if isfirstrun: 
				hallyearsdata = h.Clone()
				hallyearsdata.SetDirectory(0)	
				isfirstrun = False
			else: hallyearsdata.Add(h)
		h.Draw('colz')
		c1.Update()
		fnew.cd()
		h.Write()
		c1.Write(histname.replace('Track','c_'+quickname_))
		c1.Print('pdfs/masks/'+histname.replace('Track',quickname_)+'.pdf')
		f.Close()
	hallyearsdata.Draw('colz')
	c1.Update()
	fnew.cd()
	c1.Write(histname.replace('Track','c_allyears'))
	c1.Print('pdfs/masks/'+histname.replace('Track','allyears')+'.pdf')
	hallyearsdata.Write(histname.replace('Track','Trackallyears'))
	hmaskdata = hallyearsdata.Clone(histname.replace('Track','h_Mask_allyears'))
	hmaskdata.Reset()
	xax, yax = hallyearsdata.GetXaxis(), hallyearsdata.GetYaxis()
	ntot = 0
	nblacked = 0
	for ix in range(1,xax.GetNbins()+1):
		for iy in range(1,yax.GetNbins()+1):
			ntot+=1
			if hallyearsdata.GetBinContent(ix,iy)>1:
				print 'zeroing out', ix, iy
				nblacked+=1
				hmaskdata.SetBinContent(ix,iy,0)
			else: hmaskdata.SetBinContent(ix,iy,1)
	hmaskdata.GetZaxis().SetRangeUser(0,1.2)
	hmaskdata.Draw('colz')
	tl.DrawLatex(0.16,0.912,'masked fraction: '+str(round(nblacked*1./ntot,5)))
	c1.Update()
	c1.Write('c_'+hmaskdata.GetName())
	c1.Print('pdfs/masks/'+hmaskdata.GetName()+'.pdf')	
	hmaskdata.Write()


import os as os_		
print 'just created', os_.getcwd()+'/'+fnew.GetName()
fnew.Close()

exit(0)
		