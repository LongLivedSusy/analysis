import FWCore.ParameterSet.Config as cms
import os,sys

process = cms.Process("DisplacedThings")

try: 
    fname = sys.argv[2]
    outputdir = sys.argv[3]
except: 
    #fname = "root://cmsxrootd.fnal.gov//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/F219C63C-8A8A-E911-A7CA-008CFAF292B2.root"#run over
    #fname = "/store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/ECF10E5A-6B8A-E911-BB0D-3417EBE528B5.root"#run over
    #fname = "root://cmsxrootd.fnal.gov//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/B6BB1B78-9D8A-E911-B1E0-2047478D3908.root" # done
    #fname = "root://cmsxrootd.fnal.gov//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/ECF10E5A-6B8A-E911-BB0D-3417EBE528B5.root"
    #fname = "file:/afs/desy.de/user/s/spak/dust/DisappearingTracks/CMSSW_9_4_17/src/SUS-RunIISummer15GS-00734-fragment_py_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO.root"
    #fname = "file:/afs/desy.de/user/s/spak/dust/DisappearingTracks/CMSSW_9_4_17/src/SUS-RunIISummer15GS-00734-fragment_py_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_premix10000_10000evt.root"
    #fname = "file:/afs/desy.de/user/s/spak/dust/DisappearingTracks/CMSSW_9_4_17/src/SUS-RunIISummer15GS-00734-fragment_py_GEN_SIM_RECOBEFMIX_DIGI_L1_DIGI2RAW_L1Reco_RECO_NoPU.root"
    #fname = "file:/afs/desy.de/user/s/spak/dust/DisappearingTracks/FastSim/output/smallchunks/SUS-RunIISummer15GS-00734_T2btLLFastSim_200of200.root"
    #fname = "file:/afs/desy.de/user/s/spak/dust/DisappearingTracks/FastSim/CMSSW_9_4_17/src/20200831_040129897445869/SUS-RunIISummer15GS-00734_T2btLLFastSim_StandardMixing_1of1.root"
    #fname = "root://xrootd-cms.infn.it//store/data/Run2017F/SingleElectron/AOD/17Nov2017-v1/60000/B289F8E0-AEDE-E711-9D11-0CC47A7C3430.root"
    fname = "root://xrootd-cms.infn.it///store/data/Run2017C/SingleMuon/AOD/09Aug2019_UL2017-v1/50000/D335A134-4746-D542-97C7-CE1591F12BFF.root"
    #fname = "file:./AODs/B289F8E0-AEDE-E711-9D11-0CC47A7C3430.root"
    outputdir = "EDM_output_UL"

print 'will use', fname

fnameout = outputdir+"/edm_"+(fname.split('/')[-1]).replace('.root','_SVstuff.root')
if 'Run2' in fname:
    fnameout = fnameout.replace('edm_', 'edm_'+fname.split('/')[-6])
else:
    if 'Summer16' in fname:
	fnameout = fnameout.replace('edm_', 'edm_Summer16_')

# Use the tracks_and_vertices.root file as input.
process.source = cms.Source("PoolSource",
fileNames =  cms.untracked.vstring(fname)
    )

#more data file names for the example SingleEl 2016G are in the fileinfo directory

#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

# Suppress messages that are less important than ERRORs.
process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring("cout"),
    cout = cms.untracked.PSet(threshold = cms.untracked.string("ERROR")))

# Load part of the CMSSW reconstruction sequence to make vertexing possible.
# We'll need the CMS geometry and magnetic field to follow the true, non-helical
# shapes of tracks through the detector.
process.load("Configuration/StandardSequences/FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
if '/mc/' in fname or 'T2' in fname or 'higgsino' in fname or 'SUS' in fname or 'SMS' in fname: process.GlobalTag =  GlobalTag(process.GlobalTag, "auto:run2_mc")
else: process.GlobalTag =  GlobalTag(process.GlobalTag, "auto:run2_data")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

# Copy most of the vertex producer's parameters, but accept tracks with
# progressively more strict quality.
process.load("RecoVertex.V0Producer.generalV0Candidates_cfi")

# loose
process.SecondaryVerticesFromLooseTracks = process.generalV0Candidates.clone(
    trackRecoAlgorithm = cms.InputTag("generalTracks"),
    doKshorts = cms.bool(True),
    doLambdas = cms.bool(True),
    trackQualities = cms.string("loose"),
    innerHitPosCut = cms.double(-1.),
    vtxDecaySigXYCut = cms.double(-1.),
    )

# tight
process.SecondaryVerticesFromTightTracks = process.SecondaryVerticesFromLooseTracks.clone(
    trackQualities = cms.string("tight"),
    )

# highPurity
process.SecondaryVerticesFromHighPurityTracks = process.SecondaryVerticesFromLooseTracks.clone(
    trackQualities = cms.string("highPurity"),
    )


'''
process.dedxPixelHarmonic2 = cms.EDProducer("DeDxEstimatorProducer",
    tracks                     = cms.InputTag("generalTracks"), 
    estimator      = cms.string('generic'),
    fraction       = cms.double(0.4),        #Used only if estimator='truncated'
    exponent       = cms.double(-2.0),       #Used only if estimator='generic'
    UseStrip       = cms.bool(True),
    UsePixel       = cms.bool(False),
    ShapeTest      = cms.bool(True),
    MeVperADCStrip = cms.double(3.61e-06*265),
    MeVperADCPixel = cms.double(3.61e-06),
    Reccord            = cms.string("SiStripDeDxMip_3D_Rcd"), #used only for discriminators : estimators='productDiscrim' or 'btagDiscrim' or 'smirnovDiscrim' or 'asmirnovDiscrim'
    ProbabilityMode    = cms.string("Accumulation"),          #used only for discriminators : estimators='productDiscrim' or 'btagDiscrim' or 'smirnovDiscrim' or 'asmirnovDiscrim'
    UseCalibration  = cms.bool(False),
    calibrationPath = cms.string(""),
)


#process.dedxHarmonic2,     process.dedxPixelHarmonic2
'''

# Run all three versions of the algorithm.
process.path = cms.Path(process.SecondaryVerticesFromLooseTracks *
                        process.SecondaryVerticesFromTightTracks *
                        process.SecondaryVerticesFromHighPurityTracks 
                        )

# Writer to a new file called output.root.  Save only the new K-shorts and the
# primary vertices (for later exercises).
process.output = cms.OutputModule(
    "PoolOutputModule",
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("path")),
    outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_*_*_DisplacedThings",
        "keep *_offlineBeamSpot_*_*",
        "keep *_generalTracks_*_*",
        "keep *_offlinePrimaryVertices_*_*",
        "keep *_offlinePrimaryVerticesWithBS_*_*",
        "keep *_dedxPixelHarmonic2_*_*",
        "keep *_dedxHarmonic2_*_*",        
        ),
    fileName = cms.untracked.string(fnameout)
    )
process.endpath = cms.EndPath(process.output)
