from ROOT import *
from utils import *
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)


flist = glob('RawForMask_*_PixOrStrips.root')
print flist

c1 = mkcanvas('c1')
c1.SetLogz()
c1.SetRightMargin(0.15)
cMask = mkcanvas('cMask')
cMask.SetRightMargin(0.15)
cMask.SetLogz()
fnew = TFile('Masks.root','recreate')

for fname in flist:
	print fname
	f = TFile(fname)
	hEtaVsPhi = f.Get('hEtaVsPhiDT')
	try: 
		timeperiod = fname.replace('rootfiles/','').replace('.root','').replace('RawKapps_','').replace('RawKappaMaps/','')
		timeperiod = timeperiod.replace('RawForMask_','').replace('_PixOrStrips','').replace('AllMC','MC-2016').replace('Run','Data-')
		hEtaVsPhi.SetTitle(fname.replace('rootfiles/','').replace('.root','').replace('RawKapps_','D.T. occupency ').replace('RawKappaMaps/',''))
	except:
	   print 'couldnt get', fname, 'continuing'
	   continue

	hEtaVsPhi.SetTitle(timeperiod)
	#hEtaVsPhi.Rebin2D(2,2)
	hEtaVsPhi.SetDirectory(0)
	hEtaVsPhi.GetZaxis().SetTitleOffset(1.1)
	hEtaVsPhi.GetZaxis().SetTitle('normalized/bin-area')	
	hEtaVsPhi.Draw()
	
	hEtaVsPhi.Scale(1.0/hEtaVsPhi.Integral(), 'width')
	c1.cd()
	mini, maxi = hEtaVsPhi.GetMinimum(0.000001), hEtaVsPhi.GetMaximum() 
	hEtaVsPhi.GetZaxis().SetRangeUser(mini, maxi)
	hEtaVsPhi.GetXaxis().SetTitle('#phi')
	hEtaVsPhi.GetYaxis().SetTitle('#eta')    
	hEtaVsPhi.Draw('colz')
	c1.Update()
	hMaskedEtaVsPhi = hEtaVsPhi.Clone('hEtaVsPhiDT_masked'+timeperiod)
	
	hMask = hEtaVsPhi.Clone('hEtaVsPhiDT_mask'+timeperiod)    
	hMask.Reset()
	print 'mini, maxi', mini, maxi


	#hMaskedEtaVsPhi.Reset()
	xax, yax = hMaskedEtaVsPhi.GetXaxis(), hMaskedEtaVsPhi.GetYaxis()
	for ixbin in range(1,xax.GetNbins()+1):
		for iybin in range(1,yax.GetNbins()+1):     
			if hEtaVsPhi.GetBinContent(ixbin, iybin)>0.75e-01:
				a = 1
				hMaskedEtaVsPhi.SetBinContent(ixbin, iybin, 0)
				hMask.SetBinContent(ixbin, iybin, 0)
			else:
				hMask.SetBinContent(ixbin, iybin, 1)                
				a = 1

	cMask.cd()
	hMaskedEtaVsPhi.GetZaxis().SetRangeUser(mini, maxi)
	hMaskedEtaVsPhi.SetTitle(timeperiod)
	hMaskedEtaVsPhi.GetXaxis().SetTitle('#phi')
	hMaskedEtaVsPhi.GetYaxis().SetTitle('#eta')
	hMaskedEtaVsPhi.GetZaxis().SetTitleOffset(1.1)	
	hMaskedEtaVsPhi.GetZaxis().SetTitle('normalized/bin-area')
	hMaskedEtaVsPhi.Draw('colz')       
	cMask.Update()    

	fnew.cd() 
	hEtaVsPhi.Write(hEtaVsPhi.GetName()+timeperiod)
	hMask.Write(hMask.GetName()+timeperiod)
	hMaskedEtaVsPhi.Write(hMaskedEtaVsPhi.GetName()+timeperiod)
	c1.Write('c_'+hEtaVsPhi.GetName()+timeperiod)
	c1.Print('pdfs/masks/'+'Original'+timeperiod+'.pdf')
	cMask.Write('c_'+'hEtaVsPhiDT_masked'+timeperiod)
	cMask.Print('pdfs/masks/Masked'+timeperiod+'.pdf')
	f.Close()



print 'just created', fnew.GetName()
fnew.ls()
fnew.Close()
exit(0)


