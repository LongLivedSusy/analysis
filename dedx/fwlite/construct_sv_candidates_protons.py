import FWCore.ParameterSet.Config as cms
import os,sys

process = cms.Process("DisplacedThings")



try: 
    fname = sys.argv[2]
    output_folder = sys.argv[3]
except: 
    #fname = "root://cmsxrootd.fnal.gov//store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/8678DD46-3DB2-E611-A53A-008CFA1974D8.root"
    fname = "file:/nfs/dust/cms/user/wolfmor/Run2016GSingleElectronAOD07Aug17-v1/D25CC9A3-5787-E711-AD38-20CF3027A589.root"
    #fname = "file:T2bt-AOD_F219C63C-8A8A-E911-A7CA-008CFAF292B2.root"
    #fname = "root://cmsxrootd.fnal.gov//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/F219C63C-8A8A-E911-A7CA-008CFAF292B2.root"#run over
    #fname = "/store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/ECF10E5A-6B8A-E911-BB0D-3417EBE528B5.root"#run over
    #fname = "root://cmsxrootd.fnal.gov//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/B6BB1B78-9D8A-E911-B1E0-2047478D3908.root" # done
    #fname = "root://cmsxrootd.fnal.gov//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/ECF10E5A-6B8A-E911-BB0D-3417EBE528B5.root"
    output_folder = './EDM_output'

print 'will use', fname

fnameout = output_folder+"/edm_"+(fname.split('/')[-1]).replace('.root','SVstuff.root')
if 'Run2' in fname:
    fnameout = fnameout.replace('edm_', 'edm_'+fname.split('/')[-6])
else:
    #if 'Summer16' in fname:
    #fnameout = fnameout.replace('edm_', 'edm_'+'Summer16')
    print 'MC'

# Use the tracks_and_vertices.root file as input.
process.source = cms.Source("PoolSource",
#fileNames = cms.untracked.vstring()
#fileNames = cms.untracked.vstring("file:/nfs/dust/cms/user/beinsam/CommonSamples/MC_BSM/CompressedHiggsino/RadiativeMu_2016Fast/v2/higgsino94x_susyall_mChipm500GeV_dm5p33GeV_pu35_part12of25.root")
#fileNames = cms.untracked.vstring("root://cmsxrootd.fnal.gov//store/data/Run2016G/SingleElectron/AOD/07Aug17-v1/110000/D25CC9A3-5787-E711-AD38-20CF3027A589.root")
fileNames =  cms.untracked.vstring(fname)
    )

#more data file names for the example SingleEl 2016G are in the fileinfo directory

#SUSY FullSim signals
#root://cmsxrootd.fnal.gov//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/F219C63C-8A8A-E911-A7CA-008CFAF292B2.root
#/store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/ECF10E5A-6B8A-E911-BB0D-3417EBE528B5.root
#/store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-50_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/40000/B6BB1B78-9D8A-E911-B1E0-2047478D3908.root


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))

# Suppress messages that are less important than ERRORs.
process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring("cout"),
    cout = cms.untracked.PSet(threshold = cms.untracked.string("ERROR")))

# Load part of the CMSSW reconstruction sequence to make vertexing possible.
# We'll need the CMS geometry and magnetic field to follow the true, non-helical
# shapes of tracks through the detector.
process.load("Configuration/StandardSequences/FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
if '/mc/' in fname or 'T2' in fname or 'higgsino' in fname: process.GlobalTag =  GlobalTag(process.GlobalTag, "auto:run2_mc")
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
