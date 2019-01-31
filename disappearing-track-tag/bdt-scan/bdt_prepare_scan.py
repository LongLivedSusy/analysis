#!/bin/env python
import glob
import os
import uuid

n_trees = [2, 3, 4]
n_depth = [50, 100, 150, 200]

# possible variables are
# 'chargedPtSum', 'chi2perNdof', 'deDxHarmonic2', 'dxyVtx', 'dzVtx', 'matchedCaloEnergy', 'matchedCaloEnergyJets', 'neutralPtSum', 'neutralWithoutGammaPtSum', 'nMissingInnerHits', 'nMissingMiddleHits', 'nMissingOuterHits', 'nValidPixelHits', 'nValidTrackerHits', 'passExo16044DeadNoisyECALVeto', 'passExo16044GapsVeto', 'passExo16044JetIso', 'passExo16044LepIso', 'passExo16044Tag', 'passPFCandVeto', 'pixelLayersWithMeasurement', 'ptError', 'trackerLayersWithMeasurement', 'trackJetIso', 'trackLeptonIso', 'trackQualityConfirmed', 'trackQualityDiscarded', 'trackQualityGoodIterative', 'trackQualityHighPurity', 'trackQualityHighPuritySetWithPV', 'trackQualityLoose', 'trackQualityLooseSetWithPV', 'trackQualitySize', 'trackQualityTight', 'trackQualityUndef', 'trkMiniRelIso', 'trkRelIso'

basic_preselection = [
               "pt>15 && abs(eta)<2.4 && passPFCandVeto==1 && trackQualityHighPurity==1",
               "pt>30 && abs(eta)<2.4 && passPFCandVeto==1 && trackQualityHighPurity==1",
               "pt>30 && abs(eta)<2.4 && passPFCandVeto==1 && nMissingMiddleHits==0 && trackQualityHighPurity==1",
               "pt>30 && abs(eta)<2.4 && passPFCandVeto==1 && nMissingInnerHits==0 && trackQualityHighPurity==1",
               "pt>30 && abs(eta)<2.4 && passPFCandVeto==1 && nMissingMiddleHits==0 && nMissingInnerHits==0 && trackQualityHighPurity==1",
                     ]

variables = {
             "short": [
                         [ ("dxyVtx","F", "<0.1"), ("dzVtx","F", "<0.1"), ("matchedCaloEnergy", "F"), ("trkRelIso","F", "<0.2"), ("nValidPixelHits", "I"), ("nValidTrackerHits", "I"), ("ptErrOverPt2","F", "<0.5") ],
                         [ ("dxyVtx","F", "<0.1"), ("dzVtx","F", "<0.1"), ("matchedCaloEnergy", "F"), ("trkRelIso","F", "<0.2"), ("nValidPixelHits", "I"), ("nValidTrackerHits", "I"), ("ptErrOverPt2","F", "<0.5"), ("trackJetIso", "F", ">0.45") ],
                         [ ("dxyVtx","F", "<0.1"), ("dzVtx","F", "<0.1"), ("matchedCaloEnergy", "F", "<50"), ("trkRelIso","F", "<0.2"), ("nValidPixelHits", "I"), ("nValidTrackerHits", "I"), ("ptErrOverPt2","F", "<0.5") ],
                         [ ("dxyVtx","F", "<0.1"), ("dzVtx","F", "<0.1"), ("matchedCaloEnergy", "F", "<50"), ("trkRelIso","F", "<0.2"), ("nValidPixelHits", "I"), ("nValidTrackerHits", "I"), ("ptErrOverPt2","F", "<0.5"), ("chargedPtSum", "F", "<50"), ("neutralPtSum", "F", "<50") ],
                ],
             "medium": [
                         [ ("dxyVtx","F", "<0.1"), ("dzVtx","F", "<0.1"), ("matchedCaloEnergy", "F"), ("trkRelIso","F", "<0.2"), ("nValidPixelHits", "I"), ("nValidTrackerHits", "I"), ("ptErrOverPt2","F", "<0.5") ],
                         [ ("dxyVtx","F", "<0.1"), ("dzVtx","F", "<0.1"), ("matchedCaloEnergy", "F"), ("trkRelIso","F", "<0.2"), ("nValidPixelHits", "I"), ("nValidTrackerHits", "I"), ("ptErrOverPt2","F", "<0.5"), ("trackJetIso", "F", ">0.45") ],
                         [ ("dxyVtx","F", "<0.1"), ("dzVtx","F", "<0.1"), ("matchedCaloEnergy", "F", "<50"), ("trkRelIso","F", "<0.2"), ("nValidPixelHits", "I"), ("nValidTrackerHits", "I"), ("ptErrOverPt2","F", "<0.5") ],
                         [ ("dxyVtx","F", "<0.1"), ("dzVtx","F", "<0.1"), ("matchedCaloEnergy", "F", "<50"), ("trkRelIso","F", "<0.2"), ("nValidPixelHits", "I"), ("nValidTrackerHits", "I"), ("ptErrOverPt2","F", "<0.5"), ("chargedPtSum", "F", "<50"), ("neutralPtSum", "F", "<50") ],
                         [ ("dxyVtx","F", "<0.1"), ("dzVtx","F", "<0.1"), ("matchedCaloEnergy", "F", "<50"), ("trkRelIso","F", "<0.2"), ("nValidPixelHits", "I"), ("nValidTrackerHits", "I"), ("ptErrOverPt2","F", "<0.5"), ("nMissingOuterHits", "F", ">=2") ],
                ]
            }

def inplace_change(filename, old_string, new_string):

    with open(filename) as f:
        s = f.read()
        if str(old_string) not in s:
            return

    with open(filename, 'w') as f:
        s = s.replace(str(old_string), str(new_string))
        f.write(s)


def create_tmva_folder(template_folder, output_name, tree_path, n_depth, n_trees, preselection, variables):
    
    # create new TMVA folder for training:

    if not os.path.exists("tmva"):
        os.mkdir("tmva")

    if not os.path.exists("tmva/%s" % output_name):
        os.mkdir("tmva/%s" % output_name)

    os.system("cp -r %s/* tmva/%s/" % (template_folder, output_name))

    # replace variables in TMVA configuration:

    variables_statements = ""
    for variable in variables:
        variables_statements += """    factory->AddVariable("%s", '%s');\n""" % (variable[0], variable[1])
        if len(variable)>2:
            preselection += " && %s%s" % (variable[0], variable[2])

    inplace_change("tmva/%s/runTMVA.sh" % output_name, "$TREEPATH", tree_path)
    inplace_change("tmva/%s/tmva.cxx" % output_name, "$PRESELECTION", preselection)
    inplace_change("tmva/%s/tmva.cxx" % output_name, "$LUMI", "150000")
    inplace_change("tmva/%s/tmva.cxx" % output_name, "$VARIABLES", variables_statements)
    inplace_change("tmva/%s/tmva.cxx" % output_name, "$MAXDEPTH", n_depth)
    inplace_change("tmva/%s/tmva.cxx" % output_name, "$NTREES", n_trees)

    variable_names = [item[0] for item in variables]
    identifier = output_name + ": " + str(variable_names) + ", " + preselection + ", n_depth=" + str(n_depth) + ", n_trees=" + str(n_trees) + ", " + tree_path + "\n"
    with open("tmva/tmva_catalogue", 'a') as f:
        f.write(identifier)


def create_tmva_folders():

    count = 0

    for version in ["cmssw10"]:
        for category in ["short", "medium"]:
            for i_depth in n_depth:
                for i_trees in n_trees:
                    for preselection in basic_preselection:
                        for training_variables in variables[category]:

                            if version == "cmssw8":
                                tree_path = "/nfs/dust/cms/user/kutznerv/DisappTrksNtuple-cmssw8/tracks-mini-%s" % category
                                template_folder = "templates/cmssw8"
                            elif version == "cmssw10":
                                tree_path = "/nfs/dust/cms/user/kutznerv/DisappTrksNtuple-cmssw10/tracks-%s" % category
                                template_folder = "templates/cmssw10"

                            output_name = version + "-" + category + "-" + str(i_trees) + "-" + str(i_depth) + "-" + str(uuid.uuid4())[:8]

                            print template_folder, output_name, tree_path, i_depth, i_trees, preselection, training_variables
                            count += 1

                            create_tmva_folder(template_folder, output_name, tree_path, i_depth, i_trees, preselection, training_variables)

    print count

create_tmva_folders()
