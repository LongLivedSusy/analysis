import os
import sys
import argparse
import json
from ROOT import *
from shared_utils import *

TH1.SetDefaultSumw2()

def FillHisto(h, valx, weight=1.0):
    nbinsx = h.GetNbinsX()
    minvalx=h.GetXaxis().GetBinCenter(1)
    maxvalx=h.GetXaxis().GetBinCenter(nbinsx)

    newvalx=valx
    if valx<minvalx : newvalx=minvalx
    elif valx>maxvalx : newvalx=maxvalx

    h.Fill(newvalx,weight)
    return h



def prepareReader(xmlfilename, vars_training, vars_spectator, tmva_variables):

    # general set up training/spectator variables for TMVA

    reader = TMVA.Reader()
    for label in vars_training + vars_spectator:
        if label not in tmva_variables:
            tmva_variables[label] = array('f',[0])

    for label in vars_training:
        reader.AddVariable(label, tmva_variables[label])
    for label in vars_spectator:
        reader.AddSpectator(label, tmva_variables[label])
    reader.BookMVA("BDT", xmlfilename)

    return reader


def get_tmva_info(path):

    # get information about a TMVA macro

    training_variables = []
    spectator_variables = []
    preselection = ""
    method = ""
    configuration = ""
    count_mycutb = 0
    
    with open(path + "/tmva.cxx", 'r') as tmva_macro:
        for line in tmva_macro.readlines():
            if "AddVariable" in line and "//" not in line.split()[0]:
                variable = line.split('"')[1]
                training_variables.append(variable)
            elif "AddSpectator" in line and "//" not in line.split()[0]:
                spectator_variables.append(line.split('"')[1])
            elif 'mycutb=("' in line and "Entry" not in line and "//" not in line.split()[0]:
                preselection = line.split('"')[1]
            elif "BookMethod" in line and "//" not in line.split()[0]:
                method = line.split('"')[1]
                configuration = line.split('"')[3]
                configuration = configuration.replace(":", ", ")

    return {"method": method, "configuration": configuration, "variables": training_variables, "spectators": spectator_variables, "preselection": preselection}


def pass_background_stitching(current_file_name, madHT, phase):
    if (madHT>0) and \
       ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
       ("WJetsToLNu_TuneCUETP8M1" in current_file_name and madHT>100) or \
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
                

def particle_is_in_HEM_failure_region(particle):

    eta = particle.Eta()
    phi = particle.Phi()

    if -3.2<eta and eta<-1.2 and -1.77<phi and phi<-0.67:
        return True
    else:
        return False


def get_highest_HEM_object_pt(objects):

    # check HEM failure for electrons and jets:
    highestPt = 0
    for particle in objects:
        if particle_is_in_HEM_failure_region(particle):
            if particle.Pt()>highestPt:
                highestPt = particle.Pt()
    return highestPt


def get_minDeltaPhi_MHT_HEMJets(objects, MHT):

    lowestDPhi = 10
    for jet in objects:
        if not jet.Pt()>30: continue
        if particle_is_in_HEM_failure_region(jet):
            if abs(jet.DeltaPhi(mht))<lowestDPhi:
                lowestDPhi = abs(jet.DeltaPhi(mht))
    if lowestDPhi<0:
        return 10
    else:
        return lowestDPhi


def load_tmva_readers(phase):
    
    readers = {}
    if phase == 0:
        bdts = {
                #"bdt-short": "../../disappearing-track-tag/2016-short-tracks",
                #"bdt-long": "../../disappearing-track-tag/2016-long-tracks",
                "bdt_loose-short": "../../disappearing-track-tag/2016-short-tracks-loose",
                "bdt_loose-long": "../../disappearing-track-tag/2016-long-tracks-loose",
               }
               
    elif phase == 1:
        bdts = {
                #"bdt-short": "../../disappearing-track-tag/2017-short-tracks",
                #"bdt-long": "../../disappearing-track-tag/2017-long-tracks",
                "bdt_loose-short": "../../disappearing-track-tag/2017-short-tracks-loose",
                "bdt_loose-long": "../../disappearing-track-tag/2017-long-tracks-loose",
               }
    
    for label in bdts:
        readers[label] = {}
        readers[label]["tmva_variables"] = {}
        readers[label]["info"] = get_tmva_info(bdts[label])
        readers[label]["reader"] = prepareReader(bdts[label] + '/weights/TMVAClassification_BDT.weights.xml', readers[label]["info"]["variables"], readers[label]["info"]["spectators"], readers[label]["tmva_variables"])

    return readers
    

def get_disappearing_track_score(dt_tag_label, event, itrack, readers, loose = False):
    
    # check TMVA preselection and evaluate BDT score
    
    category = "short"
    is_pixel_track = True
    if event.tracks_trackerLayersWithMeasurement[itrack] > event.tracks_pixelLayersWithMeasurement[itrack]:
        category = "long"
        is_pixel_track = False

    if "loose" in dt_tag_label:
	use_dxy = False
	use_dz = True
	bdt = readers["bdt_loose-%s" % category]
    else:
	use_dxy = True
	use_dz = True
	bdt = readers["bdt-%s" % category]
                
    ptErrOverPt2 = event.tracks_ptError[itrack] / (event.tracks[itrack].Pt()**2)
    
    # check TMVA preselection:
    if is_pixel_track and not (event.tracks[itrack].Pt() > 30 and \
        abs(event.tracks[itrack].Eta()) < 2.4 and \
        event.tracks_trkRelIso[itrack] < 0.2 and \
        (not use_dxy or event.tracks_dxyVtx[itrack] < 0.1) and \
        (not use_dz or event.tracks_dzVtx[itrack] < 0.1) and \
        ptErrOverPt2 < 10 and \
        event.tracks_nMissingMiddleHits[itrack] == 0 and \
        bool(event.tracks_trackQualityHighPurity[itrack]) == 1):
            return -10

    if not is_pixel_track and not (event.tracks[itrack].Pt() > 30 and \
        abs(event.tracks[itrack].Eta()) < 2.4 and \
        event.tracks_trkRelIso[itrack] < 0.2 and \
        (not use_dxy or event.tracks_dxyVtx[itrack] < 0.1) and \
        (not use_dz or event.tracks_dzVtx[itrack] < 0.1) and \
        ptErrOverPt2 < 10 and \
        event.tracks_nMissingOuterHits[itrack] >= 2 and \
        event.tracks_nMissingMiddleHits[itrack] == 0 and \
        bool(event.tracks_trackQualityHighPurity[itrack]) == 1):
            return -10
    
    if not loose:
        bdt = readers["bdt-%s" % category]
    else:
        bdt = readers["bdt_loose-%s" % category]

    if use_dxy:
        bdt["tmva_variables"]["dxyVtx"][0] = event.tracks_dxyVtx[itrack]
    if use_dz:
        bdt["tmva_variables"]["dzVtx"][0] = event.tracks_dzVtx[itrack]
    bdt["tmva_variables"]["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[itrack]
    bdt["tmva_variables"]["trkRelIso"][0] = event.tracks_trkRelIso[itrack]
    bdt["tmva_variables"]["nValidPixelHits"][0] = event.tracks_nValidPixelHits[itrack]
    bdt["tmva_variables"]["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[itrack]
    bdt["tmva_variables"]["ptErrOverPt2"][0] = ptErrOverPt2           

    score = bdt["reader"].EvaluateMVA("BDT")
    
    return score
    
    
def check_is_reco_lepton(event, itrack, deltaR = 0.01):

    reco_lepton = False
    for k in range(len(event.Muons)):
        if event.tracks[itrack].DeltaR(event.Muons[k]) < deltaR:
            reco_lepton = True
    for k in range(len(event.Electrons)):
        if event.tracks[itrack].DeltaR(event.Electrons[k]) < deltaR:
            reco_lepton = True
    return reco_lepton


def pass_pion_veto(event, itrack, deltaR = 0.03):

    # check for nearby pions:
    passpionveto = True
    for k in range(len(event.TAPPionTracks)):
        if event.tracks[itrack].DeltaR(event.TAPPionTracks[k]) < deltaR:
            passpionveto = False
            break
    return passpionveto

def myround(x, base=5):
    return int(base * round(float(x)/base))


def main(inputfiles,output_dir,output,nev):
    
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
		    'Summer16','Fall17']
    FileName = c.GetFile().GetName().split('/')[-1]
    for identifier in Identifiers:
	if identifier in FileName :
	    Identifier = identifier 

    print "FileName : ",FileName
    print "Indentifier : ",Identifier
    print "Total Entries : ",nentries 
    #c.Show(0)
    
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
    print "Phase:", phase

    #FIXME: no special handling for Autumn18 yet
    if data_period == "Autumn18":
        data_period == "Fall17" 

    if data_period != "":
        print "data_period: %s, phase: %s" % (data_period, phase)
    else:
        print "Can't determine data/MC era!"
        quit(1)

    # load BDTs and fetch list of DT tag labels
    #readers = load_tmva_readers(phase)
    if phase==0:
    	pixelXml = '../disappearing-track-tag/2016-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
    	pixelstripsXml = '../disappearing-track-tag/2016-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
    else:
    	pixelXml = '../disappearing-track-tag/2017-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
    	pixelstripsXml = '../disappearing-track-tag/2017-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml'	

    #readerPixelOnly = TMVA.Reader()
    #readerPixelStrips = TMVA.Reader()
    #prepareReaderPixelStrips_loose(readerPixelStrips, pixelstripsXml)
    #prepareReaderPixel_loose(readerPixelOnly, pixelXml)
    
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
    hNlepton = TH1F('Nlepton','Nlepton',10,0,10)
    
    hTrkP = TH1F('hTrkP','hTrkP',100,0,10000)
    hTrkP_tightmumatch =	TH1F('hTrkP_tightmumatch','P of track matched with tight muon',100,0,10000)
    hTrkP_tightmumatch_barrel = TH1F('hTrkP_tightmumatch_barrel','P of track matched with tight muon in barrel region',100,0,10000)
    hTrkP_tightmumatch_endcap = TH1F('hTrkP_tightmumatch_endcap','P of track matched with tight muon in endcap region',100,0,10000)
    hTrkP_tightgenmumatch =	TH1F('hTrkP_tightgenmumatch','P of track matched with gen-matched muon',100,0,10000)
    hTrkP_tightgenmumatch_barrel =  TH1F('hTrkP_tightgenmumatch_barrel','P of track matched with gen-matched muon in barrel region',100,0,10000)
    hTrkP_tightgenmumatch_endcap =  TH1F('hTrkP_tightgenmumatch_endcap','P of track matched with gen-matched muon in endcap region',100,0,10000)
    hTrkP_tightmumatch_fromZ =	TH1F('hTrkP_tightmumatch_fromZ','P of track matched with tight muon',100,0,10000)
    hTrkP_tightmumatch_fromZ_barrel = TH1F('hTrkP_tightmumatch_fromZ_barrel','P of track matched with tight muon in barrel region',100,0,10000)
    hTrkP_tightmumatch_fromZ_endcap = TH1F('hTrkP_tightmumatch_fromZ_endcap','P of track matched with tight muon in endcap region',100,0,10000)
    hTrkP_tightelematch =	TH1F('hTrkP_tightelematch','P of track matched with tight electron',100,0,10000)
    hTrkP_tightelematch_barrel = TH1F('hTrkP_tightelematch_barrel','P of track matched with tight electron in barrel region',100,0,10000)
    hTrkP_tightelematch_endcap = TH1F('hTrkP_tightelematch_endcap','P of track matched with tight electron in endcap region',100,0,10000)
    hTrkP_tightgenelematch = TH1F('hTrkP_tightgenelematch','P of track matched with gen-matched electron',100,0,10000)
    hTrkP_tightgenelematch_barrel = TH1F('hTrkP_tightgenelematch_barrel','P of track matched with gen-matched electron in barrel region',100,0,10000)
    hTrkP_tightgenelematch_endcap = TH1F('hTrkP_tightgenelematch_endcap','P of track matched with gen-matched electron in endcap region',100,0,10000)
    hTrkP_tightelematch_fromZ =	TH1F('hTrkP_tightelematch_fromZ','P of track matched with tight electron',100,0,10000)
    hTrkP_tightelematch_fromZ_barrel = TH1F('hTrkP_tightelematch_fromZ_barrel','P of track matched with tight electron in barrel region',100,0,10000)
    hTrkP_tightelematch_fromZ_endcap = TH1F('hTrkP_tightelematch_fromZ_endcap','P of track matched with tight electron in endcap region',100,0,10000)
    
    hTrkPt = TH1F('hTrkPt','pT of track',100,0,1000)
    hTrkPt_mumatch = TH1F('hTrkPt_mumatch','pT of track matched with muon',100,0,1000)
    hTrkPt_tightmumatch = TH1F('hTrkPt_tightmumatch','pT of track matched with tight muon',100,0,1000)
    hTrkPt_tightmumatch_barrel = TH1F('hTrkPt_tightmumatch_barrel','pT of track matched with tight muon in barrel region',100,0,1000)
    hTrkPt_tightmumatch_endcap = TH1F('hTrkPt_tightmumatch_endcap','hTrkPt_tightmumatch_endcap',100,0,1000)
    hTrkPt_tightgenmumatch = TH1F('hTrkPt_tightgenmumatch','hTrkPt_tightgenmumatch',100,0,1000)
    hTrkPt_tightgenmumatch_barrel = TH1F('hTrkPt_tightgenmumatch_barrel','hTrkPt_tightgenmumatch_barrel',100,0,1000)
    hTrkPt_tightgenmumatch_endcap = TH1F('hTrkPt_tightgenmumatch_endcap','hTrkPt_tightgenmumatch_endcap',100,0,1000)
    hTrkPt_tightmumatch_fromZ = TH1F('hTrkPt_tightmumatch_fromZ','pT of track matched with tight muon',100,0,1000)
    hTrkPt_tightmumatch_fromZ_barrel = TH1F('hTrkPt_tightmumatch_fromZ_barrel','pT of track matched with tight muon in barrel region',100,0,1000)
    hTrkPt_tightmumatch_fromZ_endcap = TH1F('hTrkPt_tightmumatch_fromZ_endcap','hTrkPt_tightmumatch_endcap',100,0,1000)
    
    hTrkEta_tightmumatch = TH1F('hTrkEta_tightmumatch','hTrkEta_tightmumatch',100,0,1000)
    hTrkEta_tightmumatch_barrel = TH1F('hTrkEta_tightmumatch_barrel','hTrkEta_tightmumatch_barrel',100,0,1000)
    hTrkEta_tightmumatch_endcap = TH1F('hTrkEta_tightmumatch_endcap','hTrkEta_tightmumatch_endcap',100,0,1000)
    hTrkEta_tightgenmumatch = TH1F('hTrkEta_tightgenmumatch','hTrkEta_tightgenmumatch',100,0,1000)
    hTrkEta_tightgenmumatch_barrel = TH1F('hTrkEta_tightgenmumatch_barrel','hTrkEta_tightgenmumatch_barrel',100,0,1000)
    hTrkEta_tightgenmumatch_endcap = TH1F('hTrkEta_tightgenmumatch_endcap','hTrkEta_tightgenmumatch_endcap',100,0,1000)
    
    hTrkPt_elematch = TH1F('hTrkPt_elematch','hTrkPt_elematch',100,0,1000)
    hTrkPt_tightelematch = TH1F('hTrkPt_tightelematch','hTrkPt_tightelematch',100,0,1000)
    hTrkPt_tightelematch_barrel = TH1F('hTrkPt_tightelematch_barrel','hTrkPt_tightelematch_barrel',100,0,1000)
    hTrkPt_tightelematch_endcap = TH1F('hTrkPt_tightelematch_endcap','hTrkPt_tightelematch_endcap',100,0,1000)
    hTrkPt_tightgenelematch = TH1F('hTrkPt_tightgenelematch','hTrkPt_tightgenelematch',100,0,1000)
    hTrkPt_tightgenelematch_barrel = TH1F('hTrkPt_tightgenelematch_barrel','hTrkPt_tightgenelematch_barrel',100,0,1000)
    hTrkPt_tightgenelematch_endcap = TH1F('hTrkPt_tightgenelematch_endcap','hTrkPt_tightgenelematch_endcap',100,0,1000)
    hTrkPt_tightelematch_fromZ = TH1F('hTrkPt_tightelematch_fromZ','hTrkPt_tightelematch',100,0,1000)
    hTrkPt_tightelematch_fromZ_barrel = TH1F('hTrkPt_tightelematch_fromZ_barrel','hTrkPt_tightelematch_barrel',100,0,1000)
    hTrkPt_tightelematch_fromZ_endcap = TH1F('hTrkPt_tightelematch_fromZ_endcap','hTrkPt_tightelematch_endcap',100,0,1000)
    hTrkEta_tightelematch = TH1F('hTrkEta_tightelematch','hTrkEta_tightelematch',100,0,1000)
    hTrkEta_tightelematch_barrel = TH1F('hTrkEta_tightelematch_barrel','hTrkEta_tightelematch_barrel',100,0,1000)
    hTrkEta_tightelematch_endcap = TH1F('hTrkEta_tightelematch_endcap','hTrkEta_tightelematch_endcap',100,0,1000)
    hTrkEta_tightgenelematch = TH1F('hTrkEta_tightgenelematch','hTrkEta_tightgenelematch',100,0,1000)
    hTrkEta_tightgenelematch_barrel = TH1F('hTrkEta_tightgenelematch_barrel','hTrkEta_tightgenelematch_barrel',100,0,1000)
    hTrkEta_tightgenelematch_endcap = TH1F('hTrkEta_tightgenelematch_endcap','hTrkEta_tightgenelematch_endcap',100,0,1000)
    
    hTrkPixelDedx_mumatch = TH1F('hTrkPixelDedx_mumatch','hTrkPixelDedx_mumatch',100,0,10)
    hTrkPixelDedx_tightmumatch = TH1F('hTrkPixelDedx_tightmumatch','hTrkPixelDedx_tightmumatch',100,0,10)
    hTrkPixelDedx_tightmumatch_barrel = TH1F('hTrkPixelDedx_tightmumatch_barrel','hTrkPixelDedx_tightmumatch_barrel',100,0,10)
    hTrkPixelDedx_tightmumatch_endcap = TH1F('hTrkPixelDedx_tightmumatch_endcap','hTrkPixelDedx_tightmumatch_endcap',100,0,10)
    hTrkPixelDedx_tightgenmumatch = TH1F('hTrkPixelDedx_tightgenmumatch','hTrkPixelDedx_tightgenmumatch',100,0,10)
    hTrkPixelDedx_tightgenmumatch_barrel = TH1F('hTrkPixelDedx_tightgenmumatch_barrel','hTrkPixelDedx_tightgenmumatch_barrel',100,0,10)
    hTrkPixelDedx_tightgenmumatch_endcap = TH1F('hTrkPixelDedx_tightgenmumatch_endcap','hTrkPixelDedx_tightgenmumatch_endcap',100,0,10)
    hTrkPixelDedx_tightmumatch_fromZ = TH1F('hTrkPixelDedx_tightmumatch_fromZ','hTrkPixelDedx_tightmumatch',100,0,10)
    hTrkPixelDedx_tightmumatch_fromZ_barrel = TH1F('hTrkPixelDedx_tightmumatch_fromZ_barrel','hTrkPixelDedx_tightmumatch_barrel',100,0,10)
    hTrkPixelDedx_tightmumatch_fromZ_endcap = TH1F('hTrkPixelDedx_tightmumatch_fromZ_endcap','hTrkPixelDedx_tightmumatch_endcap',100,0,10)
    hTrkPixelDedxCalib_tightmumatch = TH1F('hTrkPixelDedxCalib_tightmumatch','hTrkPixelDedxCalib_tightmumatch',100,0,10)
    hTrkPixelDedxCalib_tightmumatch_barrel = TH1F('hTrkPixelDedxCalib_tightmumatch_barrel','hTrkPixelDedxCalib_tightmumatch_barrel',100,0,10)
    hTrkPixelDedxCalib_tightmumatch_endcap = TH1F('hTrkPixelDedxCalib_tightmumatch_endcap','hTrkPixelDedxCalib_tightmumatch_endcap',100,0,10)
    
    hTrkPixelDedx_elematch = TH1F('hTrkPixelDedx_elematch','hTrkPixelDedx_elematch',100,0,10)
    hTrkPixelDedx_tightelematch = TH1F('hTrkPixelDedx_tightelematch','hTrkPixelDedx_tightelematch',100,0,10)
    hTrkPixelDedx_tightelematch_barrel = TH1F('hTrkPixelDedx_tightelematch_barrel','hTrkPixelDedx_tightelematch_barrel',100,0,10)
    hTrkPixelDedx_tightelematch_endcap = TH1F('hTrkPixelDedx_tightelematch_endcap','hTrkPixelDedx_tightelematch_endcap',100,0,10)
    hTrkPixelDedx_tightgenelematch = TH1F('hTrkPixelDedx_tightgenelematch','hTrkPixelDedx_tightgenelematch',100,0,10)
    hTrkPixelDedx_tightgenelematch_barrel = TH1F('hTrkPixelDedx_tightgenelematch_barrel','hTrkPixelDedx_tightgenelematch_barrel',100,0,10)
    hTrkPixelDedx_tightgenelematch_endcap = TH1F('hTrkPixelDedx_tightgenelematch_endcap','hTrkPixelDedx_tightgenelematch_endcap',100,0,10)
    hTrkPixelDedx_tightelematch_fromZ = TH1F('hTrkPixelDedx_tightelematch_fromZ','hTrkPixelDedx_tightelematch',100,0,10)
    hTrkPixelDedx_tightelematch_fromZ_barrel = TH1F('hTrkPixelDedx_tightelematch_fromZ_barrel','hTrkPixelDedx_tightelematch_barrel',100,0,10)
    hTrkPixelDedx_tightelematch_fromZ_endcap = TH1F('hTrkPixelDedx_tightelematch_fromZ_endcap','hTrkPixelDedx_tightelematch_endcap',100,0,10)
    hTrkPixelDedxCalib_tightelematch = TH1F('hTrkPixelDedxCalib_tightelematch','hTrkPixelDedxCalib_tightelematch',100,0,10)
    hTrkPixelDedxCalib_tightelematch_barrel = TH1F('hTrkPixelDedxCalib_tightelematch_barrel','hTrkPixelDedxCalib_tightelematch_barrel',100,0,10)
    hTrkPixelDedxCalib_tightelematch_endcap = TH1F('hTrkPixelDedxCalib_tightelematch_endcap','hTrkPixelDedxCalib_tightelematch_endcap',100,0,10)
    
    hTrkStripsDedx_mumatch = TH1F('hTrkStripsDedx_mumatch','hTrkStripsDedx_mumatch',100,0,10)
    hTrkStripsDedx_tightmumatch = TH1F('hTrkStripsDedx_tightmumatch','hTrkStripsDedx_tightmumatch',100,0,10)
    hTrkStripsDedx_tightmumatch_barrel = TH1F('hTrkStripsDedx_tightmumatch_barrel','hTrkStripsDedx_tightmumatch_barrel',100,0,10)
    hTrkStripsDedx_tightmumatch_endcap = TH1F('hTrkStripsDedx_tightmumatch_endcap','hTrkStripsDedx_tightmumatch_endcap',100,0,10)
    hTrkStripsDedx_tightgenmumatch = TH1F('hTrkStripsDedx_tightgenmumatch','hTrkStripsDedx_tightgenmumatch',100,0,10)
    hTrkStripsDedx_tightgenmumatch_barrel = TH1F('hTrkStripsDedx_tightgenmumatch_barrel','hTrkStripsDedx_tightgenmumatch_barrel',100,0,10)
    hTrkStripsDedx_tightgenmumatch_endcap = TH1F('hTrkStripsDedx_tightgenmumatch_endcap','hTrkStripsDedx_tightgenmumatch_endcap',100,0,10)
    hTrkStripsDedx_tightmumatch_fromZ = TH1F('hTrkStripsDedx_tightmumatch_fromZ','hTrkStripsDedx_tightmumatch',100,0,10)
    hTrkStripsDedx_tightmumatch_fromZ_barrel = TH1F('hTrkStripsDedx_tightmumatch_fromZ_barrel','hTrkStripsDedx_tightmumatch_barrel',100,0,10)
    hTrkStripsDedx_tightmumatch_fromZ_endcap = TH1F('hTrkStripsDedx_tightmumatch_fromZ_endcap','hTrkStripsDedx_tightmumatch_endcap',100,0,10)
    hTrkStripsDedxCalib_tightmumatch = TH1F('hTrkStripsDedxCalib_tightmumatch','hTrkStripsDedxCalib_tightmumatch',100,0,10)
    hTrkStripsDedxCalib_tightmumatch_barrel = TH1F('hTrkStripsDedxCalib_tightmumatch_barrel','hTrkStripsDedxCalib_tightmumatch_barrel',100,0,10)
    hTrkStripsDedxCalib_tightmumatch_endcap = TH1F('hTrkStripsDedxCalib_tightmumatch_endcap','hTrkStripsDedxCalib_tightmumatch_endcap',100,0,10)
    
    hTrkStripsDedx_elematch = TH1F('hTrkStripsDedx_elematch','hTrkStripsDedx_elematch',100,0,10)
    hTrkStripsDedx_tightelematch = TH1F('hTrkStripsDedx_tightelematch','hTrkStripsDedx_tightelematch',100,0,10)
    hTrkStripsDedx_tightelematch_barrel = TH1F('hTrkStripsDedx_tightelematch_barrel','hTrkStripsDedx_tightelematch_barrel',100,0,10)
    hTrkStripsDedx_tightelematch_endcap = TH1F('hTrkStripsDedx_tightelematch_endcap','hTrkStripsDedx_tightelematch_endcap',100,0,10)
    hTrkStripsDedx_tightgenelematch = TH1F('hTrkStripsDedx_tightgenelematch','hTrkStripsDedx_tightgenelematch',100,0,10)
    hTrkStripsDedx_tightgenelematch_barrel = TH1F('hTrkStripsDedx_tightgenelematch_barrel','hTrkStripsDedx_tightgenelematch_barrel',100,0,10)
    hTrkStripsDedx_tightgenelematch_endcap = TH1F('hTrkStripsDedx_tightgenelematch_endcap','hTrkStripsDedx_tightgenelematch_endcap',100,0,10)
    hTrkStripsDedx_tightelematch_fromZ = TH1F('hTrkStripsDedx_tightelematch_fromZ','hTrkStripsDedx_tightelematch',100,0,10)
    hTrkStripsDedx_tightelematch_fromZ_barrel = TH1F('hTrkStripsDedx_tightelematch_fromZ_barrel','hTrkStripsDedx_tightelematch_barrel',100,0,10)
    hTrkStripsDedx_tightelematch_fromZ_endcap = TH1F('hTrkStripsDedx_tightelematch_fromZ_endcap','hTrkStripsDedx_tightelematch_endcap',100,0,10)
    hTrkStripsDedxCalib_tightelematch = TH1F('hTrkStripsDedxCalib_tightelematch','hTrkStripsDedxCalib_tightelematch',100,0,10)
    hTrkStripsDedxCalib_tightelematch_barrel = TH1F('hTrkStripsDedxCalib_tightelematch_barrel','hTrkStripsDedxCalib_tightelematch_barrel',100,0,10)
    hTrkStripsDedxCalib_tightelematch_endcap = TH1F('hTrkStripsDedxCalib_tightelematch_endcap','hTrkStripsDedxCalib_tightelematch_endcap',100,0,10)
    
    hMuP = TH1F('hMuP','hMuP',100,0,10000)
    hMuPt = TH1F('hMuPt','hMuPt',100,0,1000)
    hMuPt_genmatch = TH1F('hMuPt_genmatch','hMuPt_genmatch',100,0,1000)
    hMuPt_fromZ_leading = TH1F('hMuPt_fromZ_leading','Leading muon from Z decay',100,0,1000)
    hMuPt_fromZ_trailing = TH1F('hMuPt_fromZ_trailing','Trailing muon from Z decay',100,0,1000)
    hMuEta = TH1F('hMuEta','hMuEta',100,-3,3)
    hMuPhi = TH1F('hMuPhi','hMuPhi',100,-3.14,3.14)
    hGamma_mu = TH1F('hGamma_mu','hGamma_mu',100,0,10000)
    
    hEleP = TH1F('hEleP','hEleP',100,0,10000)
    hElePt = TH1F('hElePt','hElePt',100,0,1000)
    hElePt_genmatch = TH1F('hElePt_genmatch','hElePt_genmatch',100,0,1000)
    hElePt_fromZ_leading = TH1F('hElePt_fromZ_leading','Leading electron from Z decay',100,0,1000)
    hElePt_fromZ_trailing = TH1F('hElePt_fromZ_trailing','Trailing electron from Z decay',100,0,1000)
    hEleEta = TH1F('hEleEta','hEleEta',100,-3,3)
    hElePhi = TH1F('hElePhi','hElePhi',100,-3.14,3.14)
    hGamma_ele = TH1F('hGamma_ele','hGamma_ele',100,0,200000)

    h2_TrkMu_P_Dedx = TH2F('h2_TrkMu_P_Dedx','Muon P vs Dedx', 100,0,2000,100,0,10)
    h2_TrkEle_P_Dedx = TH2F('h2_TrkEle_P_Dedx','Electron P vs Dedx', 100,0,2000,100,0,10)
    h2_TrkChi_P_Dedx = TH2F('h2_TrkChi_P_Dedx','Chargino P vs Dedx', 200,0,4000,100,0,10)

    h3_TrkMu_P_Eta_Dedx = TH3F('h3_TrkMu_P_Eta_Dedx','Muon P vs Eta vs Dedx', 100,0,2000,10,0,2.5,100,0,10)
    h3_TrkEle_P_Eta_Dedx = TH3F('h3_TrkEle_P_Eta_Dedx','Electron P vs Eta vs Dedx', 100,0,2000,10,0,2.5,100,0,10)
    h3_TrkChi_P_Eta_Dedx = TH3F('h3_TrkChi_P_Eta_Dedx','Chargino P vs Eta vs Dedx', 200,0,4000,10,0,2.5,100,0,10)
    
    # Event loop
    updateevery = 10000
    for ientry in range(nentries):
	
	if ientry%updateevery==0:
    	    print 'now processing event number', ientry, 'of', nentries
	
	c.GetEntry(ientry)
	
	# Counting histogram
	FillHisto(hHT_unweighted,c.HT)

	# store runs for JSON output:
    	runs = {}

	# Weight
	if is_data:
            runnum = c.RunNum
            lumisec = c.LumiBlockNum
            if runnum not in runs:
                runs[runnum] = []
            if lumisec not in runs[runnum]:
                runs[runnum].append(lumisec)
	    weight = 1.0
	else : 
	    weight = c.CrossSection * c.puWeight

	# data trigger and mc madHT check
	if is_data and "MET" in FileName :
	    if not PassTrig(c,'MhtMet6pack') : continue
	elif is_data and "SingleMuon" in FileName :
	    if not PassTrig(c,'SingleMuon') : continue
	elif is_data and ("SingleElectron" in FileName or "EGamma" in FileName) :
	    if not PassTrig(c,'SingleElectron') : continue
	else :
	    # madHT check
	    if c.GetBranch("madHT"):
		madHT = c.madHT
	    	if not pass_background_stitching(FileName, madHT, phase): continue
	    
	# MET filters, etc
	if not passesUniversalSelection(c): continue

	# some preselection on event
	#if not c.MET>50 : continue

	FillHisto(hMET,c.MET,weight)
	FillHisto(hMHT,c.MHT,weight)
	FillHisto(hHT,c.HT,weight)
  
	# Electrons
	n_tightelectron =0
	tightelectrons=[]
	tightelectrons_genmatch=[]
	n_electron = len(c.Electrons)
	for iele, ele in enumerate(c.Electrons):
	    if not (ele.Pt()>30): continue
	    if not abs(ele.Eta())<2.4: continue
	    if not (abs(ele.Eta()) > 1.566 or abs(ele.Eta()) < 1.4442): continue
	    if not c.Electrons_passIso[iele]: continue
	    if not c.Electrons_tightID[iele]: continue
	    n_tightelectron+=1
	    tightelectrons.append(ele)
	    #gamma_ele = ele.Pt()*TMath.CosH(ele.Eta())/0.000511
	    gamma_ele = ele.P()/0.000511
	    FillHisto(hEleP,ele.P(),weight)
	    FillHisto(hElePt,ele.Pt(),weight)
	    FillHisto(hEleEta,ele.Eta(),weight)
	    FillHisto(hElePhi,ele.Phi(),weight)
	    FillHisto(hGamma_ele,gamma_ele,weight)
	    
	    # Gen-electron matching
	    if not is_data:
		drele_gen=99
		for igp,gp in enumerate(c.GenParticles):
		    if not abs(c.GenParticles_PdgId[igp])==11 : continue
		    drele_gen = min(drele_gen, ele.DeltaR(gp))
		    if drele_gen<0.01 : 
			#print 'Electron matched with GenElectron : elePt:%s genelePt:%s'%(ele.Pt(),gp.Pt())
			FillHisto(hElePt_genmatch,ele.Pt(),weight)
			tightelectrons_genmatch.append(ele)
			break
	
	# Electrons from Z
	tightelectrons_fromZ=[]
	if n_tightelectron == 2:  
	    ele1 = c.Electrons[0]
	    ele2 = c.Electrons[1]
	    if not c.Electrons_charge[0] * c.Electrons_charge[1] == -1 : continue
	    invmass = (ele1+ele2).M()
	    if not (invmass >= 70 and invmass <= 110) : continue 
	    #print '{}th event Z invmass:{}, ele1 pT:{}, ele2 pT:{}, {}'.format(ientry, invmass,ele1.Pt(),ele2.Pt(), True if ele1.Pt()>ele2.Pt() else False)
	    FillHisto(hElePt_fromZ_leading,ele1.Pt(),weight)
	    FillHisto(hElePt_fromZ_trailing,ele2.Pt(),weight)
	    tightelectrons_fromZ.append(ele1)
	    tightelectrons_fromZ.append(ele2)

	# Muons
	n_tightmuon = 0
	tightmuons=[]
	tightmuons_genmatch=[]
	for imu, mu in enumerate(c.Muons):
	    if not (mu.Pt()>30): continue
	    if not abs(mu.Eta())<2.4: continue
	    if not (abs(mu.Eta()) > 1.566 or abs(mu.Eta()) < 1.4442): continue
	    if not c.Muons_passIso[imu]: continue
	    if not c.Muons_tightID[imu]: continue
	    n_tightmuon+=1
	    tightmuons.append(mu)
	    #gamma_mu = mu.Pt()*TMath.CosH(mu.Eta())/0.105
	    gamma_mu = mu.P()/0.105
	    FillHisto(hMuPt,mu.P(),weight)
	    FillHisto(hMuPt,mu.Pt(),weight)
	    FillHisto(hMuEta,mu.Eta(),weight)
	    FillHisto(hMuPhi,mu.Phi(),weight)
	    FillHisto(hGamma_mu,gamma_mu,weight)
	    
	    # Gen-muon matching
	    if not is_data:
		drmu_gen=99
		for igp,gp in enumerate(c.GenParticles):
		    if not abs(c.GenParticles_PdgId[igp])==13 : continue
		    drmu_gen = min(drmu_gen, mu.DeltaR(gp))
		    if drmu_gen<0.01 : 
			#print 'Muon matched with GenMuon : muPt:%s genmuPt:%s'%(mu.Pt(),gp.Pt())
			FillHisto(hMuPt_genmatch,mu.Pt(),weight)
			tightmuons_genmatch.append(mu)
			break

	# Muons from Z
	tightmuons_fromZ=[]
	if n_tightmuon == 2:  
	    mu1 = c.Muons[0]
	    mu2 = c.Muons[1]
	    if not c.Muons_charge[0] * c.Muons_charge[1] == -1 : continue
	    invmass = (mu1+mu2).M()
	    if not (invmass >= 70 and invmass <= 110) : continue 
	    #print '{}th event Z invmass:{}, mu1 pT:{}, mu2 pT:{}, {}'.format(ientry, invmass,mu1.Pt(),mu2.Pt(), True if mu1.Pt()>mu2.Pt() else False)
	    FillHisto(hMuPt_fromZ_leading,mu1.Pt(),weight)
	    FillHisto(hMuPt_fromZ_trailing,mu2.Pt(),weight)
	    tightmuons_fromZ.append(mu1)
	    tightmuons_fromZ.append(mu2)


	# JETS
	n_recojets=0
	for ijet, jet in enumerate(c.Jets):
	    if not abs(jet.Eta())<2.4: continue
	    if not (jet.Pt()>30): continue
	    if not c.Jets_ID[ijet]: continue
	    n_recojets+=1

	n_lepton = n_tightmuon + n_tightelectron

	FillHisto(hNlepton,n_lepton,weight)

	# Track
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):
	    if not track.Pt()>20 : continue
	    if not abs(track.Eta()) < 2.4 : continue
	    if not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
	    if not isBaselineTrack(track, itrack, c, hMask): continue
	    FillHisto(hTrkPt,track.Pt(),weight)

	    # Muon-track matching
	    drmu = 99
	    for imu, mu in enumerate(tightmuons):
                drmu = min(drmu, mu.DeltaR(track))
		pTdiff_rel = abs(mu.Pt()-track.Pt())/mu.Pt()
                if drmu<0.01 and pTdiff_rel<0.1: 
		    dedx_pixel = c.tracks_deDxHarmonic2pixel[itrack]
		    dedx_strips = c.tracks_deDxHarmonic2strips[itrack]
		    #FillHisto(hTrkPt_mumatch,track.Pt(),weight)
		    #FillHisto(hTrkPixelDedx_mumatch,dedx,weight)
		    FillHisto(hTrkP_tightmumatch,track.P(),weight)
		    FillHisto(hTrkPt_tightmumatch,track.Pt(),weight)
		    FillHisto(hTrkPixelDedx_tightmumatch,dedx_pixel,weight)
		    FillHisto(hTrkStripsDedx_tightmumatch,dedx_strips,weight)
		    if abs(track.Eta())<=1.5 : 
			#print 'barrel region(mu matching)'
			SF_dedx_pixel = Dedxcalibdict_Muon_barrel[Identifier]
			SF_dedx_strips = 1.0
			FillHisto(hTrkP_tightmumatch_barrel,track.P(),weight)
			FillHisto(hTrkPt_tightmumatch_barrel,track.Pt(),weight)
			FillHisto(hTrkEta_tightmumatch_barrel,track.Eta(),weight)
		    	FillHisto(hTrkPixelDedx_tightmumatch_barrel,dedx_pixel,weight)
		    	FillHisto(hTrkPixelDedxCalib_tightmumatch_barrel,dedx_pixel*SF_dedx_pixel,weight)
		    	FillHisto(hTrkPixelDedxCalib_tightmumatch,dedx_pixel*SF_dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightmumatch_barrel,dedx_strips,weight)
		    	FillHisto(hTrkStripsDedxCalib_tightmumatch_barrel,dedx_strips*SF_dedx_strips,weight)
		    	FillHisto(hTrkStripsDedxCalib_tightmumatch,dedx_strips*SF_dedx_strips,weight)
		    elif abs(track.Eta())>1.5 : 
			#print 'endcap region(mu matching)'
			SF_dedx_pixel = Dedxcalibdict_Muon_endcap[Identifier]
			SF_dedx_strips = 1.0
			FillHisto(hTrkP_tightmumatch_endcap,track.P(),weight)
			FillHisto(hTrkPt_tightmumatch_endcap,track.Pt(),weight)
			FillHisto(hTrkEta_tightmumatch_endcap,track.Eta(),weight)
		    	FillHisto(hTrkPixelDedx_tightmumatch_endcap,dedx_pixel,weight)
		    	FillHisto(hTrkPixelDedxCalib_tightmumatch_endcap,dedx_pixel*SF_dedx_pixel,weight)
			FillHisto(hTrkPixelDedxCalib_tightmumatch,dedx_pixel*SF_dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightmumatch_endcap,dedx_strips,weight)
		    	FillHisto(hTrkStripsDedxCalib_tightmumatch_endcap,dedx_strips*SF_dedx_strips,weight)
			FillHisto(hTrkStripsDedxCalib_tightmumatch,dedx_strips*SF_dedx_strips,weight)
		    else : print 'should not see this'
	
		    break

	    # Gen-matched Muon matching
	    dr = 99
	    for imu, mu in enumerate(tightmuons_genmatch):
                dr = min(dr, mu.DeltaR(track))
		pTdiff_rel = abs(mu.Pt()-track.Pt())/mu.Pt()
                if dr<0.01 and pTdiff_rel<0.1: 
		    #print 'track - genmatched muon matching'
		    dedx_pixel = c.tracks_deDxHarmonic2pixel[itrack]
		    dedx_strips = c.tracks_deDxHarmonic2strips[itrack]
		    FillHisto(hTrkP_tightgenmumatch,track.P(),weight)
		    FillHisto(hTrkPt_tightgenmumatch,track.Pt(),weight)
		    FillHisto(hTrkPixelDedx_tightgenmumatch,dedx_pixel,weight)
		    FillHisto(hTrkStripsDedx_tightgenmumatch,dedx_strips,weight)
		    h2_TrkMu_P_Dedx.Fill(track.P(),dedx_pixel,weight)
		    h3_TrkMu_P_Eta_Dedx.Fill(track.P(),track.Eta(),dedx_pixel,weight)
		    
		    if abs(track.Eta())<=1.5 : 
			#print 'barrel region(gen-mu matching)'
			FillHisto(hTrkP_tightgenmumatch_barrel,track.P(),weight)
			FillHisto(hTrkPt_tightgenmumatch_barrel,track.Pt(),weight)
			FillHisto(hTrkEta_tightgenmumatch_barrel,track.Eta(),weight)
		    	FillHisto(hTrkPixelDedx_tightgenmumatch_barrel,dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightgenmumatch_barrel,dedx_strips,weight)
		    elif abs(track.Eta())>1.5 : 
			#print 'endcap region(gen-mu matching)'
			FillHisto(hTrkP_tightgenmumatch_endcap,track.P(),weight)
			FillHisto(hTrkPt_tightgenmumatch_endcap,track.Pt(),weight)
			FillHisto(hTrkEta_tightgenmumatch_endcap,track.Eta(),weight)
		    	FillHisto(hTrkPixelDedx_tightgenmumatch_endcap,dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightgenmumatch_endcap,dedx_strips,weight)
		    else : print 'should not see this'
		    
		    break
	
	    # Muon from Z matching
	    dr = 99
	    for imu, mu in enumerate(tightmuons_fromZ):
                dr = min(dr, mu.DeltaR(track))
		pTdiff_rel = abs(mu.Pt()-track.Pt())/mu.Pt()
                if dr<0.01 and pTdiff_rel<0.1: 
		    #print 'track - muon from Z matching'
		    dedx_pixel = c.tracks_deDxHarmonic2pixel[itrack]
		    dedx_strips = c.tracks_deDxHarmonic2strips[itrack]
		    FillHisto(hTrkP_tightmumatch_fromZ,track.P(),weight)
		    FillHisto(hTrkPt_tightmumatch_fromZ,track.Pt(),weight)
		    FillHisto(hTrkPixelDedx_tightmumatch_fromZ,dedx_pixel,weight)
		    FillHisto(hTrkStripsDedx_tightmumatch_fromZ,dedx_strips,weight)
		    
		    if abs(track.Eta())<=1.5 : 
			#print 'barrel region(mu_fromZ matching)'
			FillHisto(hTrkP_tightmumatch_fromZ_barrel,track.P(),weight)
			FillHisto(hTrkPt_tightmumatch_fromZ_barrel,track.Pt(),weight)
		    	FillHisto(hTrkPixelDedx_tightmumatch_fromZ_barrel,dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightmumatch_fromZ_barrel,dedx_strips,weight)
		    elif abs(track.Eta())>1.5 : 
			#print 'endcap region(mu_fromZ matching)'
			FillHisto(hTrkP_tightmumatch_fromZ_endcap,track.P(),weight)
			FillHisto(hTrkPt_tightmumatch_fromZ_endcap,track.Pt(),weight)
		    	FillHisto(hTrkPixelDedx_tightmumatch_fromZ_endcap,dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightmumatch_fromZ_endcap,dedx_strips,weight)
		    else : print 'should not see this'
		    
		    break
	    
	    # Electron-track matching
	    drele = 99
	    for iele, ele in enumerate(tightelectrons):
                drele = min(drele, ele.DeltaR(track))
		pTdiff_rel = abs(ele.Pt()-track.Pt())/ele.Pt()
                if drele<0.01 and pTdiff_rel<0.1: 
		    dedx_pixel = c.tracks_deDxHarmonic2pixel[itrack]
		    dedx_strips = c.tracks_deDxHarmonic2strips[itrack]
		    #FillHisto(hTrkPt_elematch,track.Pt(),weight)
		    #FillHisto(hTrkPixelDedx_elematch,dedx_pixel,weight)
		    FillHisto(hTrkP_tightelematch,track.P(),weight)
		    FillHisto(hTrkPt_tightelematch,track.Pt(),weight)
		    FillHisto(hTrkPixelDedx_tightelematch,dedx_pixel,weight)
		    FillHisto(hTrkStripsDedx_tightelematch,dedx_strips,weight)
		    
		    if abs(track.Eta())<=1.5 : 
			#print 'barrel region(ele matching)'
			SF_dedx_pixel = Dedxcalibdict_Electron_barrel[Identifier]
			SF_dedx_strips = 1.0
			FillHisto(hTrkP_tightelematch_barrel,track.P(),weight)
			FillHisto(hTrkPt_tightelematch_barrel,track.Pt(),weight)
			FillHisto(hTrkEta_tightelematch_barrel,track.Eta(),weight)
		    	FillHisto(hTrkPixelDedx_tightelematch_barrel,dedx_pixel,weight)
		    	FillHisto(hTrkPixelDedxCalib_tightelematch_barrel,dedx_pixel*SF_dedx_pixel,weight)
			FillHisto(hTrkPixelDedxCalib_tightelematch,dedx_pixel*SF_dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightelematch_barrel,dedx_strips,weight)
		    	FillHisto(hTrkStripsDedxCalib_tightelematch_barrel,dedx_strips*SF_dedx_strips,weight)
			FillHisto(hTrkStripsDedxCalib_tightelematch,dedx_strips*SF_dedx_strips,weight)
		    elif abs(track.Eta())>1.5 : 
			#print 'endcap region(ele matching)'
			SF_dedx_pixel = Dedxcalibdict_Electron_endcap[Identifier]
			SF_dedx_strips = 1.0
			FillHisto(hTrkP_tightelematch_endcap,track.P(),weight)
			FillHisto(hTrkPt_tightelematch_endcap,track.Pt(),weight)
			FillHisto(hTrkEta_tightelematch_endcap,track.Eta(),weight)
		    	FillHisto(hTrkPixelDedx_tightelematch_endcap,dedx_pixel,weight)
		    	FillHisto(hTrkPixelDedxCalib_tightelematch_endcap,dedx_pixel*SF_dedx_pixel,weight)
			FillHisto(hTrkPixelDedxCalib_tightelematch,dedx_pixel*SF_dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightelematch_endcap,dedx_strips,weight)
		    	FillHisto(hTrkStripsDedxCalib_tightelematch_endcap,dedx_strips*SF_dedx_strips,weight)
			FillHisto(hTrkStripsDedxCalib_tightelematch,dedx_strips*SF_dedx_strips,weight)
		    else : print 'should not see this'
	    
	    # Gen-matched Electron matching
	    dr = 99
	    for iele, ele in enumerate(tightelectrons_genmatch):
                dr = min(dr, ele.DeltaR(track))
		pTdiff_rel = abs(ele.Pt()-track.Pt())/ele.Pt()
                if dr<0.01 and pTdiff_rel<0.1: 
		    #print 'track - genmatched electron matching'
		    dedx_pixel = c.tracks_deDxHarmonic2pixel[itrack]
		    dedx_strips = c.tracks_deDxHarmonic2strips[itrack]
		    FillHisto(hTrkP_tightgenelematch,track.P(),weight)
		    FillHisto(hTrkPt_tightgenelematch,track.Pt(),weight)
		    FillHisto(hTrkPixelDedx_tightgenelematch,dedx_pixel,weight)
		    FillHisto(hTrkStripsDedx_tightgenelematch,dedx_strips,weight)
		    h2_TrkEle_P_Dedx.Fill(track.P(),dedx_pixel,weight)
		    h3_TrkEle_P_Eta_Dedx.Fill(track.P(),track.Eta(),dedx_pixel,weight)
		    
		    if abs(track.Eta())<=1.5 : 
			#print 'barrel region(ele matching)'
			FillHisto(hTrkP_tightelematch_barrel,track.P(),weight)
			FillHisto(hTrkPt_tightelematch_barrel,track.Pt(),weight)
			FillHisto(hTrkEta_tightelematch_barrel,track.Eta(),weight)
		    	FillHisto(hTrkPixelDedx_tightelematch_barrel,dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightelematch_barrel,dedx_strips,weight)
		    elif abs(track.Eta())>1.5 : 
			#print 'endcap region(ele matching)'
			FillHisto(hTrkP_tightelematch_endcap,track.P(),weight)
			FillHisto(hTrkPt_tightelematch_endcap,track.Pt(),weight)
			FillHisto(hTrkEta_tightelematch_endcap,track.Eta(),weight)
		    	FillHisto(hTrkPixelDedx_tightelematch_endcap,dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightelematch_endcap,dedx_strips,weight)
		    else : print 'should not see this'
		    
		    break
	    
	    # Electron from Z matching
	    dr = 99
	    for iele, ele in enumerate(tightelectrons_fromZ):
                dr = min(dr, ele.DeltaR(track))
		pTdiff_rel = abs(ele.Pt()-track.Pt())/ele.Pt()
                if dr<0.01 and pTdiff_rel<0.1: 
		    #print 'track - electron from Z matching'
		    dedx_pixel = c.tracks_deDxHarmonic2pixel[itrack]
		    dedx_strips = c.tracks_deDxHarmonic2strips[itrack]
		    FillHisto(hTrkP_tightelematch_fromZ,track.P(),weight)
		    FillHisto(hTrkPt_tightelematch_fromZ,track.Pt(),weight)
		    FillHisto(hTrkPixelDedx_tightelematch_fromZ,dedx_pixel,weight)
		    FillHisto(hTrkStripsDedx_tightelematch_fromZ,dedx_strips,weight)
		    
		    if abs(track.Eta())<=1.5 : 
			#print 'barrel region(ele_fromZ matching)'
			FillHisto(hTrkP_tightelematch_fromZ_barrel,track.P(),weight)
			FillHisto(hTrkPt_tightelematch_fromZ_barrel,track.Pt(),weight)
		    	FillHisto(hTrkPixelDedx_tightelematch_fromZ_barrel,dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightelematch_fromZ_barrel,dedx_strips,weight)
		    elif abs(track.Eta())>1.5 : 
			#print 'endcap region(ele_fromZ matching)'
			FillHisto(hTrkP_tightelematch_fromZ_endcap,track.P(),weight)
			FillHisto(hTrkPt_tightelematch_fromZ_endcap,track.Pt(),weight)
		    	FillHisto(hTrkPixelDedx_tightelematch_fromZ_endcap,dedx_pixel,weight)
		    	FillHisto(hTrkStripsDedx_tightelematch_fromZ_endcap,dedx_strips,weight)
		    else : print 'should not see this'
		    
		    break
	    
	    
	    # Gen-chargino matching
	    if not is_data:
	        drchi_gen=99
	        for igp,gp in enumerate(c.GenParticles):
	            if not abs(c.GenParticles_PdgId[igp])==1000024 : continue #Gen-Chargino
	            drchi_gen = min(drchi_gen, track.DeltaR(gp))
		    pTdiff_rel = abs(gp.Pt()-track.Pt())/track.Pt()
	            if drchi_gen<0.01 and pTdiff_rel<0.1: 
			dedx_pixel = c.tracks_deDxHarmonic2pixel[itrack]
		    	dedx_strips = c.tracks_deDxHarmonic2strips[itrack]
	        	#print 'Track matched with Gen-Chargino : trackPt:%s genchiPt:%s'%(track.Pt(),gp.Pt())
			h2_TrkChi_P_Dedx.Fill(track.P(),dedx_pixel,weight)
		    	h3_TrkChi_P_Eta_Dedx.Fill(track.P(),track.Eta(),dedx_pixel,weight)
	        	break



    fout.Write()
    fout.Close()
    print("DONE")
    
    #FIXME
    # write JSON containing lumisections:
    if len(runs) > 0:
        runs_compacted = {}
        for run in runs:
            if run not in runs_compacted:
                runs_compacted[run] = []
            for lumisec in runs[run]:
                if len(runs_compacted[run]) > 0 and lumisec == runs_compacted[run][-1][-1]+1:
                    runs_compacted[run][-1][-1] = lumisec
                else:
                    runs_compacted[run].append([lumisec, lumisec])
	print runs_compacted

        json_content = json.dumps(runs_compacted)
        with open(output_dir+'/'+output.replace(".root", ".json"), "w") as fjson:
            fjson.write(json_content)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="*", dest="inputfiles", required=True)
    parser.add_argument("--output_dir",default="outputs_smallchunks",dest="output_dir")
    parser.add_argument("--output",default="output.root",dest="output")
    parser.add_argument("--nev",default=-1,dest="nev")

    args = parser.parse_args()
    inputfiles = args.inputfiles
    output_dir = args.output_dir
    output = args.output
    nev = int(args.nev)

    main(inputfiles,output_dir,output,nev)

