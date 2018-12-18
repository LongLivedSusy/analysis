import ROOT

# from within CMSSW:
#ROOT.gSystem.Load('libCondFormatsBTauObjects') 
#ROOT.gSystem.Load('libCondToolsBTau') 

# OR using standalone code:
ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+') 

# get the sf data loaded
#calib = ROOT.BTagCalibration('csvv1', 'CSVV1.csv')
calib = ROOT.BTagCalibration('csvv2', 'CSVv2_Moriond17_B_H.csv')

# making a std::vector<std::string>> in python is a bit awkward, 
# but works with root (needed to load other sys types):
v_sys = getattr(ROOT, 'vector<string>')()
v_sys.push_back('up')
v_sys.push_back('down')

# make a reader instance and load the sf data
reader = ROOT.BTagCalibrationReader(
    0,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
    "central",      # central systematic type
    v_sys,          # vector of other sys. types
) 
print reader
reader.load(
    calib, 
    0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
    "comb"      # measurement type
)
# reader.load(...)     # for FLAV_C
# reader.load(...)     # for FLAV_UDSG



f = ROOT.TFile("../../samples/Summer16.TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_53_RA2AnalysisTree.root","READ")
t = f.Get("TreeMaker2/PreSelection")
nentries = t.GetEntries()
print nentries

# for data 2016 and 80X MC
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
csv_b_looseWP = 0.5426
csv_b_mediumWP = 0.8484
csv_b_tightWP = 0.9535

#for ientry in nentries :
for ientry in range(10) :
    t.GetEntry(ientry)

    weight = 1
    weight_up = 1
    weight_down = 1
    for ijet, jet in enumerate(t.Jets) :
	if t.Jets_bDiscriminatorCSV[ijet] < csv_b_looseWP : continue
	if 20 < jet.Pt() < 1000. :
	    sf = reader.eval_auto_bounds(
	        'central',      # systematic (here also 'up'/'down' possible)
	        0,              # jet flavor
	        jet.Eta(),      # absolute value of eta
	        jet.Pt()        # pt
	    )
	    sf_up = reader.eval_auto_bounds(
	        'up',	        # systematic (here also 'up'/'down' possible)
	        0,              # jet flavor
	        jet.Eta(),      # absolute value of eta
	        jet.Pt()        # pt
	    )
	    sf_down = reader.eval_auto_bounds(
	        'down',	        # systematic (here also 'up'/'down' possible)
	        0,              # jet flavor
	        jet.Eta(),      # absolute value of eta
	        jet.Pt()        # pt
	    )
	    weight *= sf
	    weight_up *= sf_up
	    weight_down *= sf_down
	else : 
	    weight *= reader.eval_auto_bounds('central',0,jet.Eta(),999.)
	    weight_up *= reader.eval_auto_bounds('up',0,jet.Eta(),999.)
	    weight_down *= reader.eval_auto_bounds('down',0,jet.Eta(),999.)
	
    print ientry,'th event weight :', weight, '\tup :', weight_up, '\tdown :', weight_down
    
