import os
import sys
import argparse
import json
from ROOT import *
from shared_utils import *

TH1.SetDefaultSumw2(True)

def passesUniversalSelection(t):
	#if not bool(t.JetID): return False
	if not t.NVtx>0: return False
	#print 'made a'
	if not  passQCDHighMETFilter(t): return False
	if not passQCDHighMETFilter2(t): return False
	#print 'made b'    
	#if not t.PFCaloMETRatio<5: return False # turned off now that we use muons
	###if not t.globalSuperTightHalo2016Filter: return False
	#print 'made c'    
	if not t.HBHENoiseFilter: return False    
	if not t.HBHEIsoNoiseFilter: return False
	if not t.eeBadScFilter: return False      
	#print 'made d'    
	if not t.BadChargedCandidateFilter: return False
	if not t.BadPFMuonFilter: return False
	#print 'made e'    
	if not t.CSCTightHaloFilter: return False
	#print 'made f'        
	if not t.EcalDeadCellTriggerPrimitiveFilter: return False      ##I think this one makes a sizeable difference    
	##if not t.ecalBadCalibReducedExtraFilter: return False
	##if not t.ecalBadCalibReducedFilter: return False      
	   
	return True

def passesUniversalSelectionFastSim(t):
 	#if not bool(t.JetID): return False
 	if not t.NVtx>0: return False
 	#print 'made a'
 	if not  passQCDHighMETFilter(t): return False
 	if not passQCDHighMETFilter2(t): return False
 	return True	

def pass_background_stitching(current_file_name, madHT, phase):
    if (madHT>0) and \
       ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
       ("WJetsToLNu_TuneCUETP8M1_13TeV" in current_file_name and madHT>100) or \
       (phase == 1 and "TTJets_Tune" in current_file_name and madHT>600) or \
       ("HT-100to200_" in current_file_name and (madHT<100 or madHT>200)) or \
       ("HT-200to300_" in current_file_name and (madHT<200 or madHT>300)) or \
       ("HT-200to400_" in current_file_name and (madHT<200 or madHT>400)) or \
       ("HT-300to500_" in current_file_name and (madHT<300 or madHT>500)) or \
       ("HT-400to600_" in current_file_name and (madHT<400 or madHT>600)) or \
       ("HT-600to800_" in current_file_name and (madHT<600 or madHT>800)) or \
       ("HT-800to1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
       ("HT-1200to2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
       ("HT-2500toInf_" in current_file_name and madHT<2500) or \
       ("HT-500to700_" in current_file_name and (madHT<500 or madHT>700)) or \
       ("HT-700to1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
       ("HT-1000to1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
       ("HT-1500to2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
       ("HT-100To200_" in current_file_name and (madHT<100 or madHT>200)) or \
       ("HT-200To300_" in current_file_name and (madHT<200 or madHT>300)) or \
       ("HT-200To400_" in current_file_name and (madHT<200 or madHT>400)) or \
       ("HT-300To500_" in current_file_name and (madHT<300 or madHT>500)) or \
       ("HT-400To600_" in current_file_name and (madHT<400 or madHT>600)) or \
       ("HT-500To700_" in current_file_name and (madHT<500 or madHT>700)) or \
       ("HT-600To800_" in current_file_name and (madHT<600 or madHT>800)) or \
       ("HT-700To1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
       ("HT-800To1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
       ("HT-1000To1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
       ("HT-1200To2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
       ("HT-1500To2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
       ("HT-2500ToInf_" in current_file_name and madHT<2500):
        return False
    else:
        return True

def main(inputfiles,output_dir,output,nev,isfast):
    
    # Adding Trees
    c = TChain("TreeMaker2/PreSelection")
    for i,inputfile in enumerate(inputfiles):
        print 'adding {}th file:{}'.format(i,inputfile)
    	c.Add(inputfile)
    
    nentries = c.GetEntries()
    if nev != -1: nentries = nev
    
    Identifiers = ['Run2016B','Run2016C','Run2016D','Run2016E','Run2016F','Run2016G','Run2016H',
		    'Run2017B','Run2017C','Run2017D','Run2017E','Run2017F',
		    'Run2018A','Run2018B','Run2018C','Run2018D',
		    'Summer16','Fall17','Summer16FastSim']
    
    FileName = c.GetFile().GetName().split('/')[-1]
    for identifier in Identifiers:
	if identifier in FileName :
	    Identifier = identifier
	if 'Summer16PrivateFastSim' in FileName :
	    Identifier = 'Summer16FastSim'

    
    # check if data:
    phase = 0
    data_period = ""
    is_data = False
    for label in ["Run2016", "Run2017", "Run2018", "Summer16", "Fall17", "Autumn18"]:
        if label in FileName:
            data_period = label
            if "Run201" in label:
                is_data = True
            if label == "Run2016" or label == "Summer16":
                phase = 0
            elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18":
                phase = 1
    
    print "FileName : ",FileName
    print "Indentifier : ",Identifier
    print "Phase:", phase
    print "IsFastSim : ",isfast 
    print "Total Entries : ",nentries 
    #c.Show(0)

    #FIXME: no special handling for Autumn18 yet
    if data_period == "Autumn18":
        data_period == "Fall17" 

    if data_period != "":
        print "data_period: %s, phase: %s" % (data_period, phase)
    else:
        print "Can't determine data/MC era!"
        quit(1)

    # load and configure data mask:
    #fMask = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/Masks_mcal10to15.root')
    fMask = TFile('../disappearing-track-tag/Masks_mcal10to15.root')
    hMask = fMask.Get('h_Mask_allyearsLongSElValidationZLLCaloSideband_EtaVsPhiDT')
    print "Loaded mask:", hMask
    
    # Output file
    fout = TFile(output_dir+'/'+output, "recreate")

    # write number of events to histogram:
    nev = c.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()


    # Histograms
    hHT_unweighted = TH1F('hHT_unweighted','hHT_unweighted',200,0,10000)
    hMET = TH1F('hMET','hMET',100,0,1000)
    hMHT = TH1F('hMHT','hMHT',100,0,1000)
    hHT = TH1F('hHT','hHT',100,0,1000)
    
    hTrkP_charginomatch = TH1F('hTrkP_charginomatch','Chargino-matched track total momentum',1000,0,10000)
    hTrkPt_charginomatch = TH1F('hTrkPt_charginomatch','Chargino-matched track transverse momentum',100,0,1000)
    hTrkEta_charginomatch = TH1F('hTrkEta_charginomatch','Chargino-matched track pseudo-rapidity',100,-2.5,2.5)
    hTrkPhi_charginomatch = TH1F('hTrkPhi_charginomatch','Chargino-matched track phi',100,-3.14,3.14)
    
    hTrkPixelDedx_charginomatch = TH1F('hTrkPixelDedx_charginomatch','Chargino-matched track pixel dedx',100,0,10)
    hTrkPixelDedx_charginomatch_barrel = TH1F('hTrkPixelDedx_charginomatch_barrel','Chargino-matched track pixel dedx at barrel region',100,0,10)
    hTrkPixelDedx_charginomatch_endcap = TH1F('hTrkPixelDedx_charginomatch_endcap','Chargino-matched track pixel dedx at endcap region',100,0,10)
    hTrkPixelDedxCalib_charginomatch_barrel = TH1F('hTrkPixelDedxCalib_charginomatch_barrel','Chargino-matched track pixel dedx at barrel region',100,0,10)
    hTrkPixelDedxCalib_charginomatch_endcap = TH1F('hTrkPixelDedxCalib_charginomatch_endcap','Chargino-matched track pixel dedx at endcap region',100,0,10)
    hTrkStripsDedx_charginomatch = TH1F('hTrkStripsDedx_charginomatch','Chargino-matched track strips dedx',100,0,10)
    hTrkStripsDedx_charginomatch_barrel = TH1F('hTrkStripsDedx_charginomatch_barrel','Chargino-matched track strips dedx at barrel region',100,0,10)
    hTrkStripsDedx_charginomatch_endcap = TH1F('hTrkStripsDedx_charginomatch_endcap','Chargino-matched track strips dedx at endcap region',100,0,10)
    hTrkStripsDedxCalib_charginomatch_barrel = TH1F('hTrkStripsDedxCalib_charginomatch_barrel','Chargino-matched track strips dedx at barrel region',100,0,10)
    hTrkStripsDedxCalib_charginomatch_endcap = TH1F('hTrkStripsDedxCalib_charginomatch_endcap','Chargino-matched track strips dedx at endcap region',100,0,10)

    hGenStopMass = TH1F('hGenStopMass','Gen-stop mass', 2500, 0, 2500)

    hGenCharginoP = TH1F('hGenCharginoP','Gen-chargino total momentum',1000,0,10000)
    hGenCharginoPt = TH1F('hGenCharginoPt','Gen-chargino transverse momentum',1000,0,1000)
    hGenCharginoEta = TH1F('hGenCharginoEta','Gen-chargino pseudo-rapidity',100,-2.5,2.5)
    hGenCharginoPhi = TH1F('hGenCharginoPhi','Gen-chargino phi',100,-3.14,3.14)
    
    # Event loop
    updateevery = 1000
    for ientry in range(nentries):
	
	if ientry%updateevery==0:
    	    print 'now processing event number', ientry, 'of', nentries
	
	c.GetEntry(ientry)
	
	# Counting histogram
	fillth1(hHT_unweighted,c.HT)

	# Weight
	#weight = c.CrossSection * c.puWeight
	weight = c.puWeight

	# MET filters, etc
	if isfast : 
	    #if not passesUniversalSelectionFastSim(c): continue
	    #if not bool(t.JetID): continue
 	    if not c.NVtx>0: continue
 	    if not  passQCDHighMETFilter(c): continue
 	    if not passQCDHighMETFilter2(c): continue
	else : 
	    #if not passesUniversalSelection(c): continue
	    #if not bool(c.JetID): continue
	    if not c.NVtx>0: continue
	    if not  passQCDHighMETFilter(c): continue
	    if not passQCDHighMETFilter2(c): continue
	    #if not c.PFCaloMETRatio<5: continue # turned off now that we use muons
	    ###if not c.globalSuperTightHalo2016Filter: continue
	    if not c.HBHENoiseFilter: continue    
	    if not c.HBHEIsoNoiseFilter: continue
	    if not c.eeBadScFilter: continue      
	    if not c.BadChargedCandidateFilter: continue
	    if not c.BadPFMuonFilter: continue
	    if not c.CSCTightHaloFilter: continue
	    if not c.EcalDeadCellTriggerPrimitiveFilter: continue      ##I think this one makes a sizeable difference    
	    ##if not c.ecalBadCalibReducedExtraFilter: continue
	    ##if not c.ecalBadCalibReducedFilter: continue      
	   
	
	# some preselection on event
	#if not c.MET>50 : continue

	fillth1(hMET,c.MET,weight)
	fillth1(hMHT,c.MHT,weight)
	fillth1(hHT,c.HT,weight)
 
	# Gen-stop
	chosenStopMass = 1250
	hasRightStopMass = True
	for igp,gp in enumerate(c.GenParticles):
	    if not abs(c.GenParticles_PdgId[igp])==1000006 : continue
	    if not abs(c.GenParticles[igp].M()-chosenStopMass)<0.1:
		hasRightStopMass = False
		break
	    fillth1(hGenStopMass,gp.M(),weight)
	if not hasRightStopMass: continue

	# Gen-chargino
	charginos=[]
	for igp,gp in enumerate(c.GenParticles):
	    if not abs(c.GenParticles_PdgId[igp])==1000024 : continue
	    if not gp.Pt() > 20 : continue
	    
	    charginos.append(gp)
	    fillth1(hGenCharginoP,gp.P(),weight)
	    fillth1(hGenCharginoPt,gp.Pt(),weight)
	    fillth1(hGenCharginoEta,gp.Eta(),weight)
	    fillth1(hGenCharginoPhi,gp.Phi(),weight)
	

	# Track
	for itrack, track in enumerate(c.tracks):
	    if not track.Pt()>20 : continue
	    if not abs(track.Eta()) < 2.4 : continue
	    if not bool(c.tracks_trackQualityHighPurity[itrack]) : continue
	    if not c.tracks_ptError[itrack]/(track.Pt()*track.Pt())<10 : continue
	    if not c.tracks_dzVtx[itrack]<0.1 : continue
	    if not c.tracks_trkRelIso[itrack]<0.01 : continue
	    if not c.tracks_trackerLayersWithMeasurement[itrack]>=2 : continue
	    if not c.tracks_nValidTrackerHits[itrack]>=2 : continue
	    if not c.tracks_nMissingInnerHits[itrack]==0 : continue
	    if not c.tracks_nValidPixelHits[itrack]>=2 : continue
	    if not bool(c.tracks_passPFCandVeto[itrack]) : continue
	    #if not isBaselineTrack(track, itrack, c, hMask): continue
	    
	    #fillth1(hTrkPt,track.Pt(),weight)
	    
	    # Gen-chargino - track matching
	    drmin=99
	    idx = -1
	    match = False
	    threshold = 0.01

	    for ichi, chi in enumerate(charginos):
                dr_track = chi.DeltaR(track)
		if dr_track < drmin:
		    drmin = dr_track
		    idx = itrack
		    track_charginomatch = track

	    if drmin < threshold : 
		match = True
		dedx_pixel = c.tracks_deDxHarmonic2pixel[idx]
		dedx_strips = c.tracks_deDxHarmonic2strips[idx]
		fillth1(hTrkP_charginomatch,track_charginomatch.P(),weight)
		fillth1(hTrkPt_charginomatch,track_charginomatch.Pt(),weight)
		fillth1(hTrkEta_charginomatch,track_charginomatch.Eta(),weight)
		fillth1(hTrkPhi_charginomatch,track_charginomatch.Phi(),weight)
		fillth1(hTrkPixelDedx_charginomatch,dedx_pixel,weight)
		fillth1(hTrkStripsDedx_charginomatch,dedx_strips,weight)
		
		if abs(track_charginomatch.Eta())<=1.5 : 
		    #print Identifier, ' barrel region(chargino matching) SF : ', DedxCorr_Pixel_barrel[Identifier]
		    SF_dedx_pixel = DedxCorr_Pixel_barrel[Identifier]
		    SF_dedx_strips = 1.0
		    fillth1(hTrkPixelDedx_charginomatch_barrel,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_charginomatch_barrel,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_charginomatch_barrel,dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_charginomatch_barrel,dedx_strips*SF_dedx_strips,weight)
		elif abs(track_charginomatch.Eta())>1.5 : 
		    #print Identifier, ' endcap region(chargino matching) SF : ', DedxCorr_Pixel_endcap[Identifier]
		    SF_dedx_pixel = DedxCorr_Pixel_endcap[Identifier]
		    SF_dedx_strips = 1.0
		    fillth1(hTrkPixelDedx_charginomatch_endcap,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_charginomatch_endcap,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_charginomatch_endcap,dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_charginomatch_endcap,dedx_strips*SF_dedx_strips,weight)
		else : print 'should not see this'
    
    fout.Write()
    fout.Close()
    print(output_dir+'/'+output+" just created")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="*", dest="inputfiles", required=True)
    parser.add_argument("--output_dir",default="outputs_smallchunks",dest="output_dir")
    parser.add_argument("--output",default="output.root",dest="output")
    parser.add_argument("--nev",default=-1,dest="nev")
    parser.add_argument("--fast",default=False,action='store_true')

    args = parser.parse_args()
    inputfiles = args.inputfiles
    output_dir = args.output_dir
    output = args.output
    nev = int(args.nev)
    isfast = args.fast
    
    main(inputfiles,output_dir,output,nev,isfast)

