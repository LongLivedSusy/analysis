import DataFormats.FWLite as fwlite
import ROOT 
import math
import numpy as np
#from commons import findMinDr_track, invariantMassTracks, findMatch_tracktrack_new, invariantMassTracksAsPions
import os,sys
from glob import glob
from shared_utils import *
#############################################
##    Looking at secondary vertices        ##
#############################################

ROOT.TH1.SetDefaultSumw2(True)
    
try: 
    inputfiles = glob(sys.argv[1])
except: 
    #inputfiles = glob("./EDM_output_Run2017C_UL_MIH/*.root")
    inputfiles = glob("./EDM_output_DYJetsToLL_M-50_TuneCP5_Summer19UL17/*.root")
    #inputfiles = glob("./EDM_output_Run2016B_SingleElectron/*.root")
    #inputfiles = glob("./EDM_output_Run2016G_SingleElectron/edm_Run2016G*.root")
    #inputfiles = glob("./EDM_output_Run2017F_SingleElectron/*.root")
    #inputfiles = glob("./EDM_output_Run2017F_SingleElectron_more/*.root")
    #inputfiles = glob("./EDM_output_Run2018C_EGamma/*.root")
    #inputfiles = glob("./EDM_output_SMS-T2bt-LLChipm_ctau-200_mLSP-900and1000/*.root")
    #inputfiles = glob("./EDM_output_merged/edm_higgsino94x_susyall_mChipm250GeV*.root")
    #inputfiles = glob("./EDM_output_merged/edm_SUS-RunIISummer15GS-00734_T2btLLFastSim_*.root")
    #inputfiles = glob("./EDM_output_merged/edm_SUS-RunIISummer15GS-00734_T2btLLFastSim_NoPU_SVstuff.root")
    #inputfiles = glob("./EDM_output_merged/edm_SUS-RunIISummer15GS-00734_T2btLLFastSim_StandardMixing_SVstuff.root")

if not os.path.exists('./SV_rootfiles'):
    os.system('mkdir -p SV_rootfiles')

#fnew = ROOT.TFile('./SV_rootfiles/vertex_Run2016B_SingleElectron.root', 'recreate')
#fnew = ROOT.TFile('./SV_rootfiles/vertex_Run2016G_SingleElectron.root', 'recreate')
#fnew = ROOT.TFile('./SV_rootfiles/vertex_Run2017F_SingleElectron.root', 'recreate')
#fnew = ROOT.TFile('./SV_rootfiles/vertex_Run2018C_EGamma.root', 'recreate')
#fnew = ROOT.TFile('./SV_rootfiles/vertex_Run2017C_SingleMuon_UL.root', 'recreate')
fnew = ROOT.TFile('./SV_rootfiles/vertex_DYJetsToLL_M-50_UL17.root', 'recreate')


if 'Run2016B' in inputfiles[0] : 
    print 'Running Run2016B data'
    dedxcalib_barrel = DedxCorr_Pixel_barrel['Run2016B']
    dedxcalib_endcap = DedxCorr_Pixel_endcap['Run2016B']
    radDisCutHigh = 4.2
elif 'Run2016G' in inputfiles[0] : 
    print 'Running Run2016G data'
    dedxcalib_barrel = DedxCorr_Pixel_barrel['Run2016G']
    dedxcalib_endcap = DedxCorr_Pixel_endcap['Run2016G']
    radDisCutHigh = 4.2
elif 'Run2017C' in inputfiles[0] : 
    print 'Running Run2017C data'
    dedxcalib_barrel = DedxCorr_Pixel_barrel['Run2017C']
    dedxcalib_endcap = DedxCorr_Pixel_endcap['Run2017C']
    radDisCutHigh = 2.7
elif 'Run2017F' in inputfiles[0] : 
    print 'Running Run2017F data'
    dedxcalib_barrel = DedxCorr_Pixel_barrel['Run2017F']
    dedxcalib_endcap = DedxCorr_Pixel_endcap['Run2017F']
    radDisCutHigh = 2.7
elif 'Run2018C' in inputfiles[0] : 
    print 'Running Run2018C data'
    dedxcalib_barrel = DedxCorr_Pixel_barrel['Run2018C']
    dedxcalib_endcap = DedxCorr_Pixel_endcap['Run2018C']
    radDisCutHigh = 2.7
elif 'UL17' in inputfiles[0] : 
    print 'Running UL17 MC'
    dedxcalib_barrel = 1
    dedxcalib_endcap = 1
    radDisCutHigh = 2.7
else: 
    print 'Running MC'
    dedxcalib_barrel = 1
    dedxcalib_endcap = 1
    radDisCutHigh = 4.2

print 'barrel, endcap calibs', dedxcalib_barrel, dedxcalib_endcap


events = fwlite.Events(inputfiles)


primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")
secondaryVertices_Lambda = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")
tracks_handle = fwlite.Handle("std::vector<reco::Track>")
protonIndices_handle = fwlite.Handle("std::vector<int>")

dEdxPixelTrackHandle = fwlite.Handle ("edm::ValueMap<reco::DeDxData>");
dEdxStripsTrackHandle = fwlite.Handle ("edm::ValueMap<reco::DeDxData>");

tlegend = ROOT.TLegend(0.17, 0.77, 0.51, 0.88)

# Primary
mass_primary = ROOT.TH1F("mass_primary", "primary vertex invariant mass; invariant mass [GeV];", 200, 0, 2) # invariant mass of all vertices

# Kshort
mass_highPurity = ROOT.TH1F("mass_highPurity", "Kshort mass", 1000, 0.4, 0.6)

# Lambda
P_Lambda = ROOT.TH1F("P_Lambda","Total momentum of Lambda",300,0,30)
P_good_Lambda = ROOT.TH1F("P_good_Lambda","Total momentum of Lambda",300,0,30)
P_good_Lambda_nodedx = ROOT.TH1F("P_good_Lambda_nodedx","Total momentum of Lambda",300,0,30)
P_good_Lambda_NoMassWindow = ROOT.TH1F("P_good_Lambda_NoMassWindow","Total momentum of Lambda",300,0,30)
pt_Lambda = ROOT.TH1F("pt_Lambda","Transverse momentum of Lambda",300,0,30)
pt_good_Lambda = ROOT.TH1F("pt_good_Lambda","Transverse momentum of Lambda",300,0,30)
pt_good_Lambda_nodedx = ROOT.TH1F("pt_good_Lambda_nodedx","Transverse momentum of Lambda",300,0,30)
pt_good_Lambda_NoMassWindow = ROOT.TH1F("pt_good_Lambda_NoMassWindow","Transverse momentum of Lambda",300,0,30)
eta_Lambda = ROOT.TH1F("eta_Lambda","Pseudorapidity of Lambda",100,-2.5,2.5)
eta_good_Lambda = ROOT.TH1F("eta_good_Lambda","Pseudorapidity of Lambda",100,-2.5,2.5)
eta_good_Lambda_nodedx = ROOT.TH1F("eta_good_Lambda_nodedx","Pseudorapidity of Lambda",100,-2.5,2.5)
eta_good_Lambda_NoMassWindow = ROOT.TH1F("eta_good_Lambda_NoMassWindow","Pseudorapidity of Lambda",100,-2.5,2.5)
mass_Lambda = ROOT.TH1F("mass_Lambda", "reconstructed #Lambda^{0} invariant mass; invariant mass [GeV]; no. of reconstructed SV", 1000, 1.08, 1.16) # invariant mass of all vertices
mass_good_Lambda = ROOT.TH1F("mass_good_Lambda", "invariant mass [GeV];no. of reconstructed SV;", 100,  1.08, 1.16) 
mass_good_Lambda_nodedx = ROOT.TH1F("mass_good_Lambda_nodedx", "invariant mass [GeV];no. of reconstructed SV;", 1000,  1.08, 1.16) 
mass_good_Lambda_NoMassWindow = ROOT.TH1F("mass_good_Lambda_NoMassWindow", "invariant mass [GeV];no. of reconstructed SV;", 1000,  1.08, 1.16) 
radialDistance_Lambda= ROOT.TH1F("radialDistance_Lambda", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
radialDistance_good_Lambda= ROOT.TH1F("radialDistance_good_Lambda", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
radialDistance_good_Lambda_nodedx= ROOT.TH1F("radialDistance_good_Lambda_nodedx", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
radialDistance_good_Lambda_NoMassWindow= ROOT.TH1F("radialDistance_good_Lambda_NoMassWindow", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
CosAngle = ROOT.TH1F("bestCosAngle","best cosine angle between displacement vector and Lambda momentum", 100,0.99999,1)
CosAngle_good_Lambda = ROOT.TH1F("bestCosAngle_good_Lambda","best cosine angle between displacement vector and Lambda momentum", 100,0.99999,1)
CosAngle_good_Lambda_nodedx = ROOT.TH1F("bestCosAngle_good_Lambda_nodedx","best cosine angle between displacement vector and Lambda momentum", 100,0.99999,1)
CosAngle_good_Lambda_NoMassWindow = ROOT.TH1F("bestCosAngle_good_Lambda_NoMassWindow","best cosine angle between displacement vector and Lambda momentum", 100,0.99999,1)

# Proton
P_proton = ROOT.TH1F("P_proton","Total momentum[GeV]|proton",300,0,30)
P_good_proton = ROOT.TH1F("P_good_proton", "Total momentum[GeV]|proton;", 300, 0, 30) 
P_good_proton_nodedx = ROOT.TH1F("P_good_proton_nodedx", "Total momentum[GeV]|proton;", 300, 0, 30) 
P_good_proton_barrel = ROOT.TH1F("P_good_proton_barrel", "Total momentum[GeV]|proton;", 300, 0, 30) 
P_good_proton_endcap = ROOT.TH1F("P_good_proton_endcap", "Total momentum[GeV]|proton;", 300, 0, 30) 

pt_proton = ROOT.TH1F("pt_proton","Transverse momentum[GeV]|proton",300,0,30)
pt_good_proton = ROOT.TH1F("pt_good_proton", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
pt_good_proton_nodedx = ROOT.TH1F("pt_good_proton_nodedx", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
pt_good_proton_barrel = ROOT.TH1F("pt_good_proton_barrel", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
pt_good_proton_endcap = ROOT.TH1F("pt_good_proton_endcap", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
eta_good_proton = ROOT.TH1F("eta_good_proton", "Pseudorapidity|proton;", 100,-2.5,2.5) 
eta_good_proton_nodedx = ROOT.TH1F("eta_good_proton_nodedx", "Pseudorapidity|proton;", 100,-2.5,2.5) 

#pixel dedx
dedxpixel_proton = ROOT.TH1F("dedxpixel_proton", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_proton = ROOT.TH1F("dedxpixelCalib_proton", "Calibrated pixel dedx|proton;", 200, 0, 10) 

dedxpixel_good_proton = ROOT.TH1F("dedxpixel_good_proton", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_nodedx = ROOT.TH1F("dedxpixel_good_proton_nodedx", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P0to1 = ROOT.TH1F("dedxpixel_good_proton_P0to1", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P1to2 = ROOT.TH1F("dedxpixel_good_proton_P1to2", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P2to3 = ROOT.TH1F("dedxpixel_good_proton_P2to3", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P3to4 = ROOT.TH1F("dedxpixel_good_proton_P3to4", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P4to5 = ROOT.TH1F("dedxpixel_good_proton_P4to5", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P5to6 = ROOT.TH1F("dedxpixel_good_proton_P5to6", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P6toInf = ROOT.TH1F("dedxpixel_good_proton_P6toInf", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_barrel = ROOT.TH1F("dedxpixel_good_proton_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P0to1_barrel = ROOT.TH1F("dedxpixel_good_proton_P0to1_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P1to2_barrel = ROOT.TH1F("dedxpixel_good_proton_P1to2_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P2to3_barrel = ROOT.TH1F("dedxpixel_good_proton_P2to3_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P3to4_barrel = ROOT.TH1F("dedxpixel_good_proton_P3to4_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P4to5_barrel = ROOT.TH1F("dedxpixel_good_proton_P4to5_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P5to6_barrel = ROOT.TH1F("dedxpixel_good_proton_P5to6_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P6toInf_barrel = ROOT.TH1F("dedxpixel_good_proton_P6toInf_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_endcap = ROOT.TH1F("dedxpixel_good_proton_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P0to1_endcap = ROOT.TH1F("dedxpixel_good_proton_P0to1_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P1to2_endcap = ROOT.TH1F("dedxpixel_good_proton_P1to2_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P2to3_endcap = ROOT.TH1F("dedxpixel_good_proton_P2to3_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P3to4_endcap = ROOT.TH1F("dedxpixel_good_proton_P3to4_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P4to5_endcap = ROOT.TH1F("dedxpixel_good_proton_P4to5_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P5to6_endcap = ROOT.TH1F("dedxpixel_good_proton_P5to6_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_P6toInf_endcap = ROOT.TH1F("dedxpixel_good_proton_P6toInf_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton = ROOT.TH1F("dedxpixelCalib_good_proton", "Calibrated pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P0to1 = ROOT.TH1F("dedxpixelCalib_good_proton_P0to1", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P1to2 = ROOT.TH1F("dedxpixelCalib_good_proton_P1to2", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P2to3 = ROOT.TH1F("dedxpixelCalib_good_proton_P2to3", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P3to4 = ROOT.TH1F("dedxpixelCalib_good_proton_P3to4", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P4to5 = ROOT.TH1F("dedxpixelCalib_good_proton_P4to5", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P5to6 = ROOT.TH1F("dedxpixelCalib_good_proton_P5to6", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P6toInf = ROOT.TH1F("dedxpixelCalib_good_proton_P6toInf", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_barrel = ROOT.TH1F("dedxpixelCalib_good_proton_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P0to1_barrel = ROOT.TH1F("dedxpixelCalib_good_proton_P0to1_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P1to2_barrel = ROOT.TH1F("dedxpixelCalib_good_proton_P1to2_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P2to3_barrel = ROOT.TH1F("dedxpixelCalib_good_proton_P2to3_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P3to4_barrel = ROOT.TH1F("dedxpixelCalib_good_proton_P3to4_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P4to5_barrel = ROOT.TH1F("dedxpixelCalib_good_proton_P4to5_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P5to6_barrel = ROOT.TH1F("dedxpixelCalib_good_proton_P5to6_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P6toInf_barrel = ROOT.TH1F("dedxpixelCalib_good_proton_P6toInf_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_endcap = ROOT.TH1F("dedxpixelCalib_good_proton_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P0to1_endcap = ROOT.TH1F("dedxpixelCalib_good_proton_P0to1_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P1to2_endcap = ROOT.TH1F("dedxpixelCalib_good_proton_P1to2_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P2to3_endcap = ROOT.TH1F("dedxpixelCalib_good_proton_P2to3_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P3to4_endcap = ROOT.TH1F("dedxpixelCalib_good_proton_P3to4_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P4to5_endcap = ROOT.TH1F("dedxpixelCalib_good_proton_P4to5_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P5to6_endcap = ROOT.TH1F("dedxpixelCalib_good_proton_P5to6_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_P6toInf_endcap = ROOT.TH1F("dedxpixelCalib_good_proton_P6toInf_endcap", "pixel dedx|proton;", 200, 0, 10) 

# strips dedx
dedxstrips_proton = ROOT.TH1F("dedxstrips_proton", "strips dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton = ROOT.TH1F("dedxstrips_good_proton", "strips dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton_nodedx = ROOT.TH1F("dedxstrips_good_proton_nodedx", "strips dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton_barrel = ROOT.TH1F("dedxstrips_good_proton_barrel", "strips dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton_endcap = ROOT.TH1F("dedxstrips_good_proton_endcap", "strips dedx|proton;", 200, 0, 10) 

massdedxpixel_proton = ROOT.TH1F("massdedxpixel_proton", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixelCalib_proton = ROOT.TH1F("massdedxpixelCalib_proton", "Calibrated pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_proton = ROOT.TH1F("massdedxstrips_proton", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 

massdedxpixel_good_proton = ROOT.TH1F("massdedxpixel_good_proton", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixel_good_proton_nodedx = ROOT.TH1F("massdedxpixel_good_proton_nodedx", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixelCalib_good_proton = ROOT.TH1F("massdedxpixelCalib_good_proton", "Calibrated pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_good_proton = ROOT.TH1F("massdedxstrips_good_proton", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_good_proton_nodedx = ROOT.TH1F("massdedxstrips_good_proton_nodedx", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 


rho_z_histogram = ROOT.TH2F("rho_z", "rho_z", 100, 0.0, 30.0, 100, 0.0, 10.0) # horizontal axis will represent z, the direction parallel to the beamline, and the vertical axis will represent rho, the distance from the beamline
h2_proton_P_vs_DeDxPixel = ROOT.TH2F("h2_proton_P_vs_DeDxPixel", "proton total momentum VS pixel dedx", 100, 0, 10, 100, 0, 10) 
h2_proton_P_vs_DeDxPixelCalib = ROOT.TH2F("h2_proton_P_vs_DeDxPixelCalib", "proton total momentum VS calibrated pixel dedx", 100, 0, 10, 100, 0, 10) 
h2_proton_P_vs_DeDxStrips = ROOT.TH2F("h2_proton_P_vs_DeDxStrips", "proton total momentum VS strip dedx", 100, 0, 10, 100, 0, 10) 


events.toBegin()
findMatch = 0
for i, event in enumerate(events):

    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    event.getByLabel("SecondaryVerticesFromHighPurityTracks", "Kshort", secondaryVertices)
    event.getByLabel("SecondaryVerticesFromHighPurityTracks", "Lambda", secondaryVertices_Lambda)
    event.getByLabel("SecondaryVerticesFromHighPurityTracks", "ProtonTrackIndices", protonIndices_handle)
    event.getByLabel("generalTracks", tracks_handle)
    event.getByLabel("dedxPixelHarmonic2", dEdxPixelTrackHandle)
    event.getByLabel("dedxHarmonic2", dEdxStripsTrackHandle)
    
    #print i,' th event pv:{}, sv:{}'.format(primaryVertices,secondaryVertices_Lambda)
    #print i,' th event len(pv.product):{} len(sv.product):{}'.format(len(primaryVertices.product()),len(secondaryVertices_Lambda.product()))

    if i > 9999999: break
    #if i > 500000: break
    #if i > 2000: break
    
    if i%1000==0:print 'passing {}th event'.format(i)
    #if i%1==0: print i, "   Primary vertices per event:", primaryVertices.product().size()
    #if i%1==0: print i, "   Secondary vertices per event:", secondaryVertices_Lambda.product().size()

    tracks = tracks_handle.product()
    dEdxPixelTrack = dEdxPixelTrackHandle.product()
    dEdxStripsTrack = dEdxStripsTrackHandle.product()
    protonIndices = protonIndices_handle.product()

    # particle mass from primary vertex		
    #for pv in primaryVertices.product():
	#mass_primary.Fill(pv.mass())
    
    # kShort
    for sv in secondaryVertices.product():
        mass_highPurity.Fill(sv.mass())	
    
    # Lambda loop		
    for j, secondary in enumerate(secondaryVertices_Lambda.product()):
        ## invariant mass of all vertices	
	P_Lambda.Fill(secondary.p())
	pt_Lambda.Fill(secondary.pt())
        mass_Lambda.Fill(secondary.mass())
	
	# compute displacement vectors and compare them with Lambda momentum vectors
        px = secondary.px()
        py = secondary.py()
        pz = secondary.pz()
        p = secondary.p()
        bestCosAngle = -1 
        radDis = -1
	
	for primary in primaryVertices.product():
            dx = secondary.vx() - primary.x()
            dy = secondary.vy() - primary.y()
            dz = secondary.vz() - primary.z()
            dl = math.sqrt(dx**2 + dy**2 + dz**2)
            dxy = math.sqrt(dx**2 + dy**2)
            #if i % 100 == 0: print "Normalized momentum:", px/p, py/p, pz/p,
            #if i % 100 == 0: print "Normalized displacement:", dx/dl, dy/dl, dz/dl
            dotProduct = px*dx + py*dy + pz*dz
	    if p==0 or dl==0 : continue
            cosAngle = dotProduct / p / dl
            if cosAngle > bestCosAngle:
                bestCosAngle = cosAngle # update it if you've found a better one
                radDis = dxy
	radialDistance_Lambda.Fill(radDis)
	CosAngle.Fill(bestCosAngle)

	# proton track and dEdx
        protonIdx = protonIndices[j]
        protrack = tracks[protonIdx]
        #if not protrack.charge()>0: continue
        
        P, pt, eta = protrack.p(),  protrack.pt(), protrack.eta()
	dedxpixel = dEdxPixelTrack.get(protonIdx).dEdx()
	dedxstrips = dEdxStripsTrack.get(protonIdx).dEdx()
	
        massfromdedxpixel = ROOT.TMath.Sqrt((dedxpixel-2.557)*pow(pt*ROOT.TMath.CosH(eta),2)/2.579)
        massfromdedxstrips = ROOT.TMath.Sqrt((dedxstrips-2.557)*pow(pt*ROOT.TMath.CosH(eta),2)/2.579)
	
	if abs(eta)<1.5: 
	    dedxpixelCalib = dedxcalib_barrel*dedxpixel
	    massfromdedxpixelCalib = ROOT.TMath.Sqrt((dedxpixelCalib-2.557)*pow(pt*ROOT.TMath.CosH(eta),2)/2.579)
        else: 
	    dedxpixelCalib = dedxcalib_endcap*dedxpixel
	    massfromdedxpixelCalib = ROOT.TMath.Sqrt((dedxpixelCalib-2.557)*pow(pt*ROOT.TMath.CosH(eta),2)/2.579)
                
	P_proton.Fill(protrack.p())
	pt_proton.Fill(protrack.pt())
	
	#print 'pdgid:',secondary.pdgId(), '\t number of daughters:',secondary.numberOfDaughters()
	#print 'secondary pT:%.2f \tsv daughter(0) pT:%.2f \tsv daughter(1) pT:%.2f \tproton pT:%.2f'%(secondary.pt(),secondary.daughter(0).pt(),secondary.daughter(1).pt(),protrack.pt())
	
	# more tight selection without Lambda mass window
        if (radDis > 0.5) and (radDis <= radDisCutHigh) and bestCosAngle > 0.999994 and abs(protrack.eta()) < 2.4 and dedxpixel>0 and dedxstrips>0 : 
	    radialDistance_good_Lambda_NoMassWindow.Fill(radDis)
    	    CosAngle_good_Lambda_NoMassWindow.Fill(bestCosAngle)
            P_good_Lambda_NoMassWindow.Fill(secondary.p())
            pt_good_Lambda_NoMassWindow.Fill(secondary.pt())
            eta_good_Lambda_NoMassWindow.Fill(secondary.eta())
            mass_good_Lambda_NoMassWindow.Fill(secondary.mass())
	    
	# more tight selection
        if (radDis > 0.5) and (radDis <= radDisCutHigh) and abs(secondary.mass()-1.11604e+00)<2.13880e-03 and bestCosAngle > 0.999994 and abs(protrack.eta()) < 2.4:
	    if dedxpixel>0 and dedxstrips>0 : 
		#print 'both pixel/strips dedx exist'
		radialDistance_good_Lambda.Fill(radDis)
	    	CosAngle_good_Lambda.Fill(bestCosAngle)
	        P_good_Lambda.Fill(secondary.p())
	        pt_good_Lambda.Fill(secondary.pt())
	        eta_good_Lambda.Fill(secondary.eta())
	        mass_good_Lambda.Fill(secondary.mass())
	        P_good_proton.Fill(protrack.p())
	        pt_good_proton.Fill(protrack.pt())
	        eta_good_proton.Fill(protrack.eta())
		dedxpixel_good_proton.Fill(dedxpixel)
		dedxpixelCalib_good_proton.Fill(dedxpixelCalib)
		dedxstrips_good_proton.Fill(dedxstrips)
            	massdedxpixel_good_proton.Fill(massfromdedxpixel)
	    	massdedxpixelCalib_good_proton.Fill(massfromdedxpixelCalib)
            	massdedxstrips_good_proton.Fill(massfromdedxstrips)
		
		if protrack.p() >=0 and protrack.p() < 1.0: 
		    dedxpixel_good_proton_P0to1.Fill(dedxpixel)
		    dedxpixelCalib_good_proton_P0to1.Fill(dedxpixelCalib)
		elif protrack.p() >=1.0 and protrack.p() < 2.0: 
		    dedxpixel_good_proton_P1to2.Fill(dedxpixel)
		    dedxpixelCalib_good_proton_P1to2.Fill(dedxpixelCalib)
		elif protrack.p() >=2.0 and protrack.p() < 3.0: 
		    dedxpixel_good_proton_P2to3.Fill(dedxpixel)
		    dedxpixelCalib_good_proton_P2to3.Fill(dedxpixelCalib)
		elif protrack.p() >=3.0 and protrack.p() < 4.0: 
		    dedxpixel_good_proton_P3to4.Fill(dedxpixel)
		    dedxpixelCalib_good_proton_P3to4.Fill(dedxpixelCalib)
		elif protrack.p() >=4.0 and protrack.p() < 5.0: 
		    dedxpixel_good_proton_P4to5.Fill(dedxpixel)
		    dedxpixelCalib_good_proton_P4to5.Fill(dedxpixelCalib)
		elif protrack.p() >=5.0 and protrack.p() < 6.0: 
		    dedxpixel_good_proton_P5to6.Fill(dedxpixel)
		    dedxpixelCalib_good_proton_P5to6.Fill(dedxpixelCalib)
		elif protrack.p() >=6.0: 
		    dedxpixel_good_proton_P6toInf.Fill(dedxpixel)
		    dedxpixelCalib_good_proton_P6toInf.Fill(dedxpixelCalib)
            	
		if abs(protrack.eta()) < 1.5 :
		    P_good_proton_barrel.Fill(protrack.p())
	            pt_good_proton_barrel.Fill(protrack.pt())
		    dedxpixel_good_proton_barrel.Fill(dedxpixel)
		    dedxstrips_good_proton_barrel.Fill(dedxstrips)
		    if protrack.p() >=0 and protrack.p() < 1.0: 
		        dedxpixel_good_proton_P0to1_barrel.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P0to1_barrel.Fill(dedxpixelCalib)
		    elif protrack.p() >=1.0 and protrack.p() < 2.0: 
		        dedxpixel_good_proton_P1to2_barrel.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P1to2_barrel.Fill(dedxpixelCalib)
		    elif protrack.p() >=2.0 and protrack.p() < 3.0: 
		        dedxpixel_good_proton_P2to3_barrel.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P2to3_barrel.Fill(dedxpixelCalib)
		    elif protrack.p() >=3.0 and protrack.p() < 4.0: 
		        dedxpixel_good_proton_P3to4_barrel.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P3to4_barrel.Fill(dedxpixelCalib)
		    elif protrack.p() >=4.0 and protrack.p() < 5.0: 
		        dedxpixel_good_proton_P4to5_barrel.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P4to5_barrel.Fill(dedxpixelCalib)
		    elif protrack.p() >=5.0 and protrack.p() < 6.0: 
		        dedxpixel_good_proton_P5to6_barrel.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P5to6_barrel.Fill(dedxpixelCalib)
		    elif protrack.p() >=6.0: 
		        dedxpixel_good_proton_P6toInf_barrel.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P6toInf_barrel.Fill(dedxpixelCalib)
		elif abs(protrack.eta()) >= 1.5 and abs(protrack.eta()) < 2.4 :
		    P_good_proton_endcap.Fill(protrack.p())
	            pt_good_proton_endcap.Fill(protrack.pt())
		    dedxpixel_good_proton_endcap.Fill(dedxpixel)
		    dedxstrips_good_proton_endcap.Fill(dedxstrips)
		    if protrack.p() >=0 and protrack.p() < 1.0: 
		        dedxpixel_good_proton_P0to1_endcap.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P0to1_endcap.Fill(dedxpixelCalib)
		    elif protrack.p() >=1.0 and protrack.p() < 2.0: 
		        dedxpixel_good_proton_P1to2_endcap.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P1to2_endcap.Fill(dedxpixelCalib)
		    elif protrack.p() >=2.0 and protrack.p() < 3.0: 
		        dedxpixel_good_proton_P2to3_endcap.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P2to3_endcap.Fill(dedxpixelCalib)
		    elif protrack.p() >=3.0 and protrack.p() < 4.0: 
		        dedxpixel_good_proton_P3to4_endcap.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P3to4_endcap.Fill(dedxpixelCalib)
		    elif protrack.p() >=4.0 and protrack.p() < 5.0: 
		        dedxpixel_good_proton_P4to5_endcap.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P4to5_endcap.Fill(dedxpixelCalib)
		    elif protrack.p() >=5.0 and protrack.p() < 6.0: 
		        dedxpixel_good_proton_P5to6_endcap.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P5to6_endcap.Fill(dedxpixelCalib)
		    elif protrack.p() >=6.0: 
		        dedxpixel_good_proton_P6toInf_endcap.Fill(dedxpixel)
		        dedxpixelCalib_good_proton_P6toInf_endcap.Fill(dedxpixelCalib)
		else : print 'out of eta range, shouldnt see this message'
		
		h2_proton_P_vs_DeDxPixel.Fill(protrack.p(),dedxpixel)
            	h2_proton_P_vs_DeDxPixelCalib.Fill(protrack.p(),dedxpixelCalib)
            	h2_proton_P_vs_DeDxStrips.Fill(protrack.p(),dedxstrips)
    	
	    
	    elif dedxpixel==0 or dedxstrips==0 : # when there are no dedx 
		#print 'dedx doesnt exist at least one of pixel or strips'
		radialDistance_good_Lambda_nodedx.Fill(radDis)
	    	CosAngle_good_Lambda_nodedx.Fill(bestCosAngle)
		P_good_Lambda_nodedx.Fill(secondary.p())
		pt_good_Lambda_nodedx.Fill(secondary.pt())
		eta_good_Lambda_nodedx.Fill(secondary.eta())
               	mass_good_Lambda_nodedx.Fill(secondary.mass())
               	P_good_proton_nodedx.Fill(protrack.p())
               	pt_good_proton_nodedx.Fill(protrack.pt())
               	eta_good_proton_nodedx.Fill(protrack.eta())
		dedxpixel_good_proton_nodedx.Fill(dedxpixel)
            	dedxstrips_good_proton_nodedx.Fill(dedxstrips)
            	massdedxpixel_good_proton_nodedx.Fill(massfromdedxpixel)
            	massdedxstrips_good_proton_nodedx.Fill(massfromdedxstrips)

	    else : print 'What is this?'

fnew.cd()
fnew.Write()
print 'just created', fnew.GetName()
fnew.Close()
