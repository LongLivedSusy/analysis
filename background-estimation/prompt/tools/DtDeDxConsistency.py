from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep
lumi = 35.9 #just for labeling. this weightw as already applied


makepdfs = True
#makepdfs = False
datamc = 'data'# should pretty much always be this way

#you could try to tighten the phase 0 Long fake BDT cut to improve the long MC mT test region in MC. everything else looks super!

tag = '2022_July4ForAnAndPaper'
tag = '2022_July5DeDxChecker'

'''
rm -rf pdfs/DeDxHighLow/dedx-highlow/* 
python tools/DtDeDxConsistency.py Summer16 MC & 
python tools/DtDeDxConsistency.py Fall17 MC &

rm -rf pdfs/DeDxHighLow/dedx-highlow/* 
python tools/DtDeDxConsistency.py Summer16 MC & 
python tools/DtDeDxConsistency.py Fall17 MC &
python tools/DtDeDxConsistency.py Run2 
sleep 5
python /afs/desy.de/user/b/beinsam/www/dir_indexer.py /afs/desy.de/user/b/beinsam/www/DisappearingTracks/ -r -t /afs/desy.de/user/b/beinsam/www/templates/default.html
python tools/bigindexer.py /afs/desy.de/user/b/beinsam/www/DisappearingTracks/DeDxHighLow


python tools/DtDeDxConsistency.py Run2017
python tools/DtDeDxConsistency.py Run2018

#after all this, you can do
hadd -f predictionRun2.root Valid_yearRun2016.root Valid_yearPhase1.root
cp predictionRun2.root /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v4/Background
'''

try: year = sys.argv[1]
except:
    year = 'Run2'
    year = 'Run2016'
    year = 'Run2017'
    year = 'Run2018'
    year = 'Phase1'    
    year = 'Summer16'    
    
try: datamc = sys.argv[2].lower()
except: datamc = 'data'

isdata = bool(datamc=='data')
if not isdata: doblinding = False

binning['DtStatus'] = [6,-3,3]
binning['FakeCrNr'] = [6,-3,3]

redoBinning = dict(binning)
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
redoBinning['DeDxAverage'] = [-0.000001,0,4.0,10.0]
redoBinning['DedxMass'] = [0,100,300,600,1000,1500,2100,2800,3600,4000]
redoBinning['ElPt'] = [30,0,300]
redoBinning['Ht']=[5,0,2000]
redoBinning['Met'] = [20,0,600]
redoBinning['HardMet'] = redoBinning['Met']
redoBinning['Mht'] = redoBinning['Met']
redoBinning['TrkEta']=[0,1.4,2.0,2.4]#tried 5 before
#redoBinning['TrkEta']=binning['TrkEta']
redoBinning['BTags'] = [-0.0000000001,0,1,4]
redoBinning['BinNumber'] = binningAnalysis['BinNumber']

makefolders = False

calm = 12
calh = 80

if year=='Run2017' or year=='Fall17': lumi = 41.8
if year=='Run2018': lumi = 55.0
if year=='Phase1': lumi = 41.8+55.0
if year=='Run2': lumi = 136



mainfilename = 'rootfiles/PromptBkgTree_promptDataDriven'+year+'_mcal'+str(calm)+'to'+str(calh)+'.root'
if datamc=='mc': mainfilename = mainfilename.replace('DataDriven','DataDrivenMC')

print 'opening', mainfilename
infile = TFile(mainfilename)
#infile.ls()



keys = infile.GetListOfKeys()


fout = 'DeDxRatioFake_year'+str(year)+'.root'
fnew = TFile(fout,'recreate')


searchbinresults = {}
hratios = []
clist = []
directories = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
    infile.cd()
    name = key.GetName()
        
        
    if not 'hPrompt' in name: continue
    if not 'HighDeDx' in name: continue
    if not 'Truth' in name: continue
    if 'Up' in name: continue 
    if not 'CaloSideband' in name: continue
    if 'BinNumber' in name: continue
    print 'name', name
    
    kinvar = name.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
    kinvar = kinvar[kinvar.find('_')+1:]
    print 'got kinvar', kinvar, 'name', name
            

    
    hfakemethod =  infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_')) ###
    hfakemethodLowDeDx =  infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_').replace('HighDeDx','LowDeDx')) ###    
    
    if not isdata: 
        hfakemethod.Add(infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_').replace('hFake','hPrompt')))
        hfakemethodLowDeDx.Add(infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_').replace('HighDeDx','LowDeDx').replace('hFake','hPrompt')))
    histoStyler(hfakemethodLowDeDx,38) ###
    hfakemethodLowDeDx.SetFillColor(38)
    hfakemethodLowDeDx.SetFillStyle(1001)
    
        

    if len(redoBinning[kinvar])!=3: 
        nbins = len(redoBinning[kinvar])-1
        newxs = array('d',redoBinning[kinvar])
    else:
        newbinning = []
        print kinvar, name
        stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
        for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
        nbins = len(newbinning)-1
        newxs = array('d',newbinning)

    hfakemethod = hfakemethod.Rebin(nbins,'',newxs)
    hfakemethodLowDeDx = hfakemethodLowDeDx.Rebin(nbins,'',newxs)

    
    for ibin in range(1,hfakemethod.GetXaxis().GetNbins()+1):
      if (isdata or True) and (not 'BinNumber' in name):  ####systematics!
        if 'Short' in name:
            
            binc = hfakemethod.GetBinContent(ibin)
            bine = hfakemethod.GetBinError(ibin)
            hfakemethod.SetBinError(ibin, TMath.Sqrt(pow(0.3*binc,2)+pow(bine,2)))
            #toterr = TMath.Sqrt(pow(hfakemethodOneUp.GetBinContent(ibin)-hfakemethod.GetBinContent(ibin),2)+pow(hfakemethodTwoUp.GetBinContent(ibin)-hfakemethod.GetBinContent(ibin),2)+pow(bine,2))
            #hfakemethod.SetBinError(ibin, toterr)
                
        if 'Long' in name:
            binc = hfakemethod.GetBinContent(ibin)
            bine = hfakemethod.GetBinError(ibin)      
            hfakemethod.SetBinError(ibin, TMath.Sqrt(pow(0.3*binc,2)+pow(bine,2)))     
            #toterr = TMath.Sqrt(pow(hfakemethodOneUp.GetBinContent(ibin)-hfakemethod.GetBinContent(ibin),2)+pow(hfakemethodTwoUp.GetBinContent(ibin)-hfakemethod.GetBinContent(ibin),2)+pow(bine,2))
            #hfakemethod.SetBinError(ibin, toterr)            
            
        if hfakemethod.GetBinContent(ibin)<=0: 
            hfakemethod.SetBinContent(ibin, 0)
            hfakemethodLowDeDx.SetBinContent(ibin, 0)
            hfakemethod.SetBinError(ibin, 1)
            hfakemethodLowDeDx.SetBinError(ibin, 1)
        
    if year=='Run2016':
            hfakemethod.SetTitle('fakes (de/dx>4.0 MeV/cm) (ph. 0)'); 
            hfakemethodLowDeDx.SetTitle('fakes (de/dx#leq4.0 MeV/cm) (ph. 0)');             
    if year == 'Summer16':            
            hfakemethod.SetTitle('fakes (de/dx>4.0 MeV/cm) (Summer16 MC)'); 
            hfakemethodLowDeDx.SetTitle('fakes (de/dx#leq4.0 MeV/cm) (Summer16 MC)');             
    if year=='Run2017':
            hfakemethod.SetTitle('fakes (de/dx>4.0 MeV/cm) (2017)');
            hfakemethodLowDeDx.SetTitle('fakes (de/dx#leq4.0 MeV/cm) (2017)');            
    if year == 'Fall17':            
            hfakemethod.SetTitle('fakes (de/dx>4.0 MeV/cm) (Fall17 MC)');
            hfakemethodLowDeDx.SetTitle('fakes (de/dx#leq4.0 MeV/cm) (Fall17 MC)');            
    if year=='Run2018':
            hfakemethod.SetTitle('fakes (de/dx>4.0 MeV/cm) (2018)');
            hfakemethodLowDeDx.SetTitle('fakes (de/dx#leq4.0 MeV/cm) (2018)');            
    if year == 'Autumn18':
            hfakemethod.SetTitle('fakes (de/dx>4.0 MeV/cm) (Autumn18 MC)');
            hfakemethodLowDeDx.SetTitle('fakes (de/dx#leq4.0 MeV/cm) (Autumn18 MC)');            
    if year=='Phase1':
            hfakemethod.SetTitle('fakes (de/dx>4.0 MeV/cm) (ph. 1)'); 
            hfakemethodLowDeDx.SetTitle('fakes (de/dx#leq4.0 MeV/cm) (ph. 1)');             
    if year=='Run2':
            hfakemethod.SetTitle('fakes (de/dx>4.0 MeV/cm) (R. 2)'); 
            hfakemethodLowDeDx.SetTitle('fakes (de/dx#leq4.0 MeV/cm) (R. 2)');             
                        
                        
    c1 = mkcanvas('c1')
    shortname = name.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
    directory = shortname.split('_')[0].replace('hPrompt','').replace('CaloSideband','')
    if not directory in directories:
        directories.append(directory)
        if not os.path.exists('pdfs/DeDxHighLow/dedx-highlow/'+year+'/'+directory):
            os.system('mkdir -p pdfs/DeDxHighLow/dedx-highlow/'+year+'/'+directory)    

    varname = shortname.split('_')[-1]
    leg = mklegend(x1=.49, y1=.5, x2=.91, y2=.78, color=kWhite)


    themax = 150*max([hfakemethod.GetMaximum()])

    fnew.cd()
    plotname = shortname.replace('_','').replace('CaloSideband','')
                
    #hratio, hpromptmethodsyst = FabDrawSystyRatio(c1,leg,htruth,bkgs,shists,datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
    hratio, hpromptmethodsyst = FabDrawSystyRatio(c1,leg,hfakemethod,[hfakemethodLowDeDx],[],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='high / low')    
    
            
    pad1, pad2 = hpromptmethodsyst[-2:]
    hratio.GetYaxis().SetRangeUser(0.0,0.5)    
    hratio.GetYaxis().SetTitle('data/pred.')
    hratio.GetXaxis().SetTitle(kinvar)
    hratio.SetLineColor(kBlack)
    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
    hratio.SetMarkerColor(kBlack)
    hratio.SetDirectory(0)
    pad2.Update()
    
    pad1.cd()
    fnew.cd()            

    pad2.cd()
    leg2 = mklegend(x1=.68, y1=.85, x2=.94, y2=.965, color=kWhite)
    leg2.Draw()    

    pad1.cd()
    hfakemethod.GetYaxis().SetRangeUser(0.001,themax)
    hfakemethodLowDeDx.GetYaxis().SetRangeUser(0.001,themax)
    
    c1.Write('c_'+plotname)        
    shortname = shortname.replace('CaloSideband','')
    pdfname = 'pdfs/DeDxHighLow/dedx-highlow/'+year+'/'+directory+'/'+shortname.replace('_','')+'.png'
    
    c1.Print(pdfname)
    if makepdfs: c1.Print(pdfname.replace('.png','.pdf'))
    
    #clist.append(c1)
    c1.Delete()
    hratios.append([hratio, hpromptmethodsyst])

import os, sys
whippyname = 'htmlwhippy'+year+'.sh'
os.system('echo echo hello > '+whippyname)
pipe = '>'
print 'reached the end of things'
for directory_ in directories:
    os.system('echo python tools/whiphtml.py \\"pdfs/DeDxHighLow/dedx-highlow/'+year+'/'+directory_+'/*.png\\" '+pipe+' '+whippyname)
    pipe = '>>'
os.system('bash '+whippyname)
thename = fnew.GetName()
print 'just created', os.getcwd()+'/'+thename
fnew.Close()
if True:
	print 'now do'
	copycommand = 'cp -r pdfs/DeDxHighLow/dedx-highlow/'+year+' /afs/desy.de/user/b/beinsam/www/DisappearingTracks/DeDxHighLow/'+tag+'_'+year
	print copycommand
	os.system(copycommand)
	copycode = 'cp -r tools /afs/desy.de/user/b/beinsam/www/DisappearingTracks/DeDxHighLow/'+tag+'_'+year+'/'
	print copycode
	os.system(copycode)

if True: 
    print 'you might want to hadd these end products together', thename
    print 'a la'
    print 'hadd -f predictionRun2.root Valid_yearRun2016.root Valid_yearPhase1.root'
    print 'cp predictionRun2.root /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v16/Background/'
    

