from ROOT import *
from utils import *





fBenjaminSmearMC = TFile('usefulthings/FromBenjamin/Response_El_MC.root')
fBenjaminSmearData = TFile('usefulthings/FromBenjamin/Response_El_Data.root')
#fBenjaminSmear.ls()

fAkshanshSmear = TFile('usefulthings/FromAkshansh/BinnedTemplatesIIDY_WJ_TT.root')
#fAkshanshSmear.ls()
akeys = fAkshanshSmear.GetListOfKeys()



#fFileForNLayersDist = TFile('usefulthings/FromAkshansh/TagnProbe_DYJetsToLL.root')

interdudemap = {}
interdudemap['(0, 1.4442)'] = 'B'
interdudemap['(1.566, 2.4)'] = 'E'

interdudemap['(0, 20)'] = '15'
interdudemap['(20, 30)'] = '15'
interdudemap['(30, 40)'] = '30'
interdudemap['(40, 50)'] = '30'
interdudemap['(50, 70)'] = '50'
interdudemap['(70, 90)'] = '70'
interdudemap['(90, 120)'] = '90'
interdudemap['(120, 200)'] = '120'
interdudemap['(200, 300)'] = '200'
interdudemap['(300, 310)'] = '200'

rawkappafiles = ['RawKappaMaps/RawKapps_Run2016_PixAndStrips.root','RawKappaMaps/RawKapps_Run2016_PixOnly.root','RawKappaMaps/RawKapps_DYJets_PixOnly.root','RawKappaMaps/RawKapps_DYJets_PixAndStrips.root']
#rawkappafiles = ['RawKappaMaps/RawKapps_DYJets_PixOnly.root','RawKappaMaps/RawKapps_DYJets_PixAndStrips.root']
for fname in rawkappafiles:
	fFileForNLayersDist = TFile(fname)
	hNTrackerLayersDT_el = fFileForNLayersDist.Get('hNTrackerLayersDT_el')
	hNTrackerLayersDT_mu = fFileForNLayersDist.Get('hNTrackerLayersDT_mu')	
	idbit = fname.replace('RawKappaMaps/RawKapps_','').replace('.root','')
	fnew = TFile('usefulthings/DataDrivenSmear_'+idbit+'.root', 'recreate')
	if 'Run20' in fname: fBenjaminSmear = fBenjaminSmearData
	else: fBenjaminSmear = fBenjaminSmearMC	
	bkeys = fBenjaminSmear.GetListOfKeys()
	hists = []
	histDictDict={}
	histNameDict={}
	hnamekeys = []

	fnew.cd()

	for key in akeys:
		name = key.GetName()
		if not '), (' in name: 
			fAkshanshSmear.Get(name).Write()
			continue	
		if not 'htrkresp' in name: 
			#fAkshanshSmear.Get(name).Write()
			continue		
		nameArray = name.replace('htrkresp', '').replace(')','').replace('(','').split(',') 
		if not len(nameArray)==4:
			fAkshanshSmear.Get(name).Write()
			print 'skipping', name
			continue	
		
		eta_ = '('+nameArray[0].strip()+', '+nameArray[1].strip()+')'
		pt_ = '('+nameArray[2].strip()+', '+nameArray[3].strip()+')'
		if eta_=='(1.4442, 1.566)':
			fAkshanshSmear.Get(name).Write()
			continue		
		eta, pt = interdudemap[eta_], interdudemap[pt_]
		etapt = '('+eta+', '+pt+')'
		for bkey in bkeys:
			bname = bkey.GetName()
			stem = '_Tracker_LogXResponse_%s_%s_2016_'%(eta, pt)
			if not stem in bname: continue			
			hbenj = fBenjaminSmear.Get(bname)
			nlay = int(bname.split('_')[-1].replace('All','11'))
			if not name in hnamekeys: 
				hnamekeys.append(name)		
				histDictDict[name+'El'] = hbenj.Clone(name+'El')
				histDictDict[name+'El'].Reset()
				histDictDict[name+'Mu'] = hbenj.Clone(name+'Mu')
				histDictDict[name+'Mu'].Reset()				
			weight = hNTrackerLayersDT_el.GetBinContent(nlay)			
			histDictDict[name+'El'].Add(hbenj, weight)
			weight = hNTrackerLayersDT_mu.GetBinContent(nlay)			
			histDictDict[name+'Mu'].Add(hbenj, weight)			
					
		
	fnew.cd()
	print histDictDict.keys()
	for key in histDictDict:
		histDictDict[key].Write()
	fnew.ls()
	print 'just created', fnew.GetName()
	fnew.Close()
