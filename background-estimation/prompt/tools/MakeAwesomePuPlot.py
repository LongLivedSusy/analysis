from ROOT import *
from utils import *
from glob import glob
gStyle.SetOptStat(0)

flist = glob('systematics/pileup/*.root')
hKappaVsPuDict = {}
hKappaVsPuNames = []


colors = [kAzure, kOrange+1, kRed, kGreen+1, kOrange+1, kGreen+2, kViolet, kViolet+1, kRed+2, kAzure+1, kTeal, kTeal-5, kYellow, kBlue+4]*2


for ifile, fname in enumerate(flist):
	if 'PuLow' in fname: pubin = 1
	elif 'PuMed' in fname: pubin = 2
	elif 'PuHigh' in fname: pubin = 3	
	else:
		print 'problem'
		exit(0)	
	file = TFile(fname)
	file.ls()
	keys = file.GetListOfKeys()
	for key in keys:
		name = key.GetName()
		if not 'ProbePtKappa_eta' in name: continue
		if '1.4442to1.566' in name: continue
		if 'Gen' in name: continue
		if not 'h'==name[:1]: continue
		nameNoPu = fname.split('/')[-1].replace('PuMed','').replace('PuHigh','').replace('PuLow','').replace('.root','')
		nameNoPu+='_'+name
		if not nameNoPu in hKappaVsPuNames:
			print 'adding', ifile, nameNoPu
			hKappaVsPuNames.append(nameNoPu)
			hKappaVsPuDict[nameNoPu] = TH1F(nameNoPu, nameNoPu, 3,1,4)
			hKappaVsPuDict[nameNoPu].GetXaxis().SetBinLabel(1, '0-14')
			hKappaVsPuDict[nameNoPu].GetXaxis().SetBinLabel(2, '14-28')
			hKappaVsPuDict[nameNoPu].GetXaxis().SetBinLabel(3, '>28')
			hKappaVsPuDict[nameNoPu].GetXaxis().SetBinLabel(4, 'inf')			
			histoStyler(hKappaVsPuDict[nameNoPu], colors[len(hKappaVsPuNames)])
			hKappaVsPuDict[nameNoPu].SetDirectory(0)			
			if 'MC'in fname: hKappaVsPuDict[nameNoPu].SetLineStyle(kDashed)
		hist = file.Get(name)
		print 'working on bin', pubin, hist.GetBinContent(1), fname, name
		hKappaVsPuDict[nameNoPu].SetBinContent(pubin, hist.GetBinContent(1))
		hKappaVsPuDict[nameNoPu].SetBinError(pubin, hist.GetBinError(1))		
	file.Close()

leg1 = mklegend(x1=.15, y1=.63, x2=.52, y2=.89, color=kWhite)
leg2 = mklegend(x1=.53, y1=.63, x2=.9, y2=.89, color=kWhite)
print hKappaVsPuDict
c1 = TCanvas(name,name,750,930)
c1.SetBottomMargin(.15)
c1.SetLeftMargin(.14)
c1.SetLogy()
arg = ''
counter = 0
num = pow(10,-len(hKappaVsPuDict.keys())/2)
for key in hKappaVsPuDict:
	hKappaVsPuDict[key].SetTitle('')
	hKappaVsPuDict[key].Draw(arg)
	hKappaVsPuDict[key].Scale(1.0*num/hKappaVsPuDict[key].GetBinContent(1))	
	hKappaVsPuDict[key].GetYaxis().SetRangeUser(pow(10,-len(hKappaVsPuDict.keys())/2-1),pow(10,len(hKappaVsPuDict)))
	legname = key.replace('Kappa','').replace('AllMC','MC-').replace('','').replace('','').replace('','')
	legname = legname.replace('hElProbePt','El').replace('hMuProbePt','Mu').replace('_','-').replace('to','-').replace('','')
	legname = legname.replace('--','-')
	if 'Run20' in key: leg1.AddEntry(hKappaVsPuDict[key], legname, 'lp')
	else: leg2.AddEntry(hKappaVsPuDict[key], legname, 'lp')	
	arg = 'same'
	num*=10
	counter+=1
leg1.Draw()
leg2.Draw()
c1.Update()
pause()