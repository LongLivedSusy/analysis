from stackedplot import *
from ROOT import *

samples = {
    "DYJetsToLL": {"select": "Summer16.DYJetsToLL", "type": "bg", "color": 62},
    "QCD": {"select": "Summer16.QCD", "type": "bg", "color": 97},
    "WJetsToLNu": {"select": "Summer16.WJetsToLNu", "type": "bg", "color": 85},
    "ZJetsToNuNu": {"select": "Summer16.ZJetsToNuNu", "type": "bg", "color": 67},
    "Diboson": {"select": "Summer16.WW_TuneCUETP8M1|Summer16.WZ_TuneCUETP8M1|Summer16.ZZ_TuneCUETP8M1", "type": "bg", "color": 51},
    "TT": {"select": "Summer16.TTJets_TuneCUETP8M1_13TeV", "type": "bg", "color": 8}, 
    "signal": {"select": "g1800_chi1400_27_200970", "type": "sg", "color": kBlue},
    "rare": {"select": "Summer16.ST|Summer16.GJets", "type": "bg", "color": 15},
          }

folder = "output_skim_23_merged"

cuts_cr = "passesUniversalSelection==1 && HT>100 && PFCaloMETRatio<5 && MHT>250 && n_jets>0 && n_leptons==0 && n_DT==0"

variables = {
              "dilepton_invmass": [20, 81, 101, "passesUniversalSelection==1 && dilepton_CR==1 && HT>100"],
              "madHT": [40, 0, 1000, "madHT>0"],
              "n_jets": [25, 0, 25, cuts_cr],
              "n_btags": [25, 0, 25, cuts_cr],
              "MinDeltaPhiMhtJets": [50, 0, 2, cuts_cr],
              "HT": [40, 0, 1000, cuts_cr],
              "MHT": [40, 0, 1000, cuts_cr],
            }

for variable in variables:

    if "dilepton_invmass" in variable:
        samples["data"] = {"select": "Run2016*SingleMuon", "type": "data", "color": kBlack, "lumi": 13801}
        #samples["data"] = {"select": "Run2016*SingleElectron", "type": "data", "color": kBlack, "lumi": 6212}
    else:
        samples["data"] = {"select": "Run2016*MET", "type": "data", "color": kBlack, "lumi": 17330}

    histos = get_histograms_from_folder(folder, samples, variable, variables[variable][3], variables[variable][0], variables[variable][1], variables[variable][2])
    stack_histograms(histos, samples, variable, variable, "Events", folder)
