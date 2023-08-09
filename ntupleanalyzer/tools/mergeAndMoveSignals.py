from ROOT import *
import os, sys
from glob import glob
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
import time


shutterLeps = False

istest = False

binningAnalysis['MatchedCalo'] = [100,0,100]
binningAnalysis['DtStatus'] = [6,-3,3]
binningAnalysis['FakeCrNr'] = [6,-3,3]
#redoBinning = binningAnalysis
redoBinning = binning
redoBinning['BinNumber'] = binningAnalysis['BinNumber']

try: infiles = sys.argv[1]
except: infiles = 'holdingbay/Hists*.root'

try: outdir = sys.argv[2]
except: 
    #outdir = '../interpretation/HistsBkgObsSig/Piano/Signal/'
    outdir = '/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Signal/T1qqqqLL'
    outdir = '/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Signal/T2btLL'
    outdir = '/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Xenon/v2/Signal/T2btLL'
    outdir = '/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v8NoPreFireWeight/T1qqqqLL'

bayname = infiles.split('/')[0]

#lumi = 137
if 'Summer16' in outdir: lumi = 36.5
elif 'Fall17' in outdir: lumi = 41.5
elif 'Autumn18' in outdir: lumi = 59.0
else: lumi = 41.5+59.0


finaldestin = outdir.split('/')[-1]
tempfolder = str(time.time())+'_'+finaldestin


#tempfolder = '1678426436.41_T2btLLAutumn18'####
os.system('mkdir '+tempfolder)

if not os.path.isdir(outdir):
    dircmd = 'mkdir -p '+outdir
    print dircmd
    os.system(dircmd)

infilelist = glob(infiles)


if 'higgsino' in infilelist[0].lower():
    higgsinoEventNumbersFile = TFile("usefulthings/simEventNumbers_FullSim_AOD_v2.root")
    higgsinoEventNumbersHist = higgsinoEventNumbersFile.Get('simEventNumbers_FullSim_AOD_v2')
    xax = higgsinoEventNumbersHist.GetXaxis()
    yax = higgsinoEventNumbersHist.GetYaxis()    


keywords = []

for fname in infilelist:
    fkey = fname.split('/')[-1].split('_time')[0].replace('Hists_','')
    fkey = fkey.split('_part')[0]
    if not fkey in keywords:
        keywords.append(fkey)

print 'we have the following keywords'
print keywords


for fkey in keywords:
    
    cmd = 'python tools/ahadd.py -j 10 -f '+tempfolder+'/ctrw'+fkey.replace('_Autumn18','').replace('_Fall17','')+'.root '+bayname+'/*'+fkey+'_*.root'
    print cmd    
    if istest: exit(0)
    else: os.system(cmd)

    #pause()
    fintermediate = TFile(tempfolder+'/ctrw'+fkey.replace('_Autumn18','').replace('_Fall17','')+'.root')
    keys = fintermediate.GetListOfKeys()    
    if len(keys)==0: 
        print 'couldnt make sense of', fkey.replace('_Autumn18','').replace('_Fall17','')
        continue
    ffinal = TFile(outdir+'/'+fkey.replace('_Autumn18','').replace('_Fall17','')+'.root', 'recreate')
    hHt = fintermediate.Get('hHt')

    if 'higgsino' in infilelist[0].lower(): ##what, don't you want this to actually know about the m??
        print fkey
        m  = float('higgsino94x_susyall_mChipm200GeV_dm0p8GeV'.split('mChipm')[-1].split('GeV')[0].replace('p','.'))
        dm = float('higgsino94x_susyall_mChipm200GeV_dm0p8GeV'.split('_dm')[-1].split('GeV')[0].replace('p','.'))        
        print m, dm, higgsinoEventNumbersHist.GetBinContent(xax.FindBin(m), yax.FindBin(dm))
        nentries = higgsinoEventNumbersHist.GetBinContent(xax.FindBin(m), yax.FindBin(dm))
        #continue
        
    else:
        nentries = hHt.GetEntries()
    for key in keys:
        name = key.GetName()
        if name=='hHt': 
            hHt = fintermediate.Get(name)
            ffinal.cd()
            hHt.Write()
            continue
        if name=='hHtWeighted': 
            hHt = fintermediate.Get(name)
            ffinal.cd()
            hHt.Write()        
            continue
        if 'hShort' in name and 'BinNumber' in name: continue
        
        #if not 'hLongBaseline' in name: continue
        #if not 'BinNumber' in name: continue
        hist = fintermediate.Get(name)
        
        if 'hLongBaseline' in name and 'BinNumber' in name:
            hist2 = fintermediate.Get(name.replace('Long','Short'))
            hist.Add(hist2)
        if not ('hLong' in name or 'hShort' in name):
            h = fintermediate.Get(name)
            h.Write()
            continue        
        
        if 'BinNumber' in name:
            if shutterLeps:
                for ibin in range(1, hist.GetXaxis().GetNbins()+1):
                    xval = int(hist.GetXaxis().GetBinLowEdge(ibin))
                    if (xval>=25 and xval<=48) or xval in [51,52,53,54]: 
                        hist.SetBinContent(ibin, 0)
                        hist.SetBinError(ibin, 0)                            
            hist = merge6dtbins(hist)                    
                
        
        kinvar = name.replace('Method','').replace('Truth','').replace('Method','')
        kinvar = kinvar[kinvar.find('_')+1:]
        #print 'got kinvar', kinvar, 'name', name
            
        if len(redoBinning[kinvar])!=3: 
            nbins = len(redoBinning[kinvar])-1
            newxs = array('d',redoBinning[kinvar])
            hist = hist.Rebin(nbins,'',newxs)    
        else:
            newbinning = []
            #print kinvar, name
            stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
            for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
            nbins = len(newbinning)-1
            newxs = array('d',newbinning)
            hist = hist.Rebin(nbins,'',newxs)
        
        hist.Scale(1.0*1000*lumi/nentries)
        ffinal.cd()
        if 'BinNumber' in name: hist.Write(hist.GetName().replace('hLong','h'))
        else: hist.Write(hist.GetName())
    fintermediate.Close()
    print 'just created', ffinal.GetName()
    ffinal.Close()    
    
    
    
    
    
    

    