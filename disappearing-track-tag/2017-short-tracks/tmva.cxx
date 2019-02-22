#include "TApplication.h"
#include <cstdlib>
#include <iostream>
#include <map>
#include <stdio.h>
#include <string>
#include "TApplication.h"
#include "TChain.h"
#include "TFile.h"
#include "TH1D.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#include "TMVA/TMVAGui.h"
#include "TMVA/TMVARegGui.h"

int tmva(const char* signalFileName, const char* outFileName, const char* backgroundPath, const char* maxTreeEntries) {

    std::string path = backgroundPath;
    std::string maxTreeEntriesString = maxTreeEntries;
    std::cout << "Background path: " << path << std::endl;

    const char* treename = "PreSelection";

    gROOT->SetBatch(kTRUE);

    TMVA::Tools::Instance();

    TFile* outputFile = TFile::Open(outFileName, "RECREATE");

    TMVA::Factory *factory = new TMVA::Factory("TMVAClassification",outputFile,"V:!Silent:Color:Transformations=I:DrawProgressBar:AnalysisType=Classification"); 

    Double_t weight;
    Double_t lumi = 35900;  // 1/pb
    TH1D* Nev;

    TFile* fsignal = new TFile(signalFileName);
    TTree* sgTree = (TTree*)(fsignal->Get(treename));
    Nev = (TH1D*)(fsignal->Get("Nev"));
    weight = 0.00276133 * lumi / Nev->GetBinContent(1);
    factory->AddSignalTree(sgTree, weight);
    
    TFile* fbackground_wjets_100To200 = new TFile((path + "/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_wjets_100To200 = (TTree*)(fbackground_wjets_100To200->Get(treename));
    Nev = (TH1D*)(fbackground_wjets_100To200->Get("Nev"));
    weight = 1395.0 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_wjets_100To200, weight);

    TFile* fbackground_wjets_200To400 = new TFile((path + "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_wjets_200To400 = (TTree*)(fbackground_wjets_200To400->Get(treename));
    Nev = (TH1D*)(fbackground_wjets_200To400->Get("Nev"));
    weight = 407.9 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_wjets_200To400, weight);

    TFile* fbackground_wjets_400To600 = new TFile((path + "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_wjets_400To600 = (TTree*)(fbackground_wjets_400To600->Get(treename));
    Nev = (TH1D*)(fbackground_wjets_400To600->Get("Nev"));
    weight = 57.48 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_wjets_400To600, weight);

    TFile* fbackground_wjets_600To800 = new TFile((path + "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_wjets_600To800 = (TTree*)(fbackground_wjets_600To800->Get(treename));
    Nev = (TH1D*)(fbackground_wjets_600To800->Get("Nev"));
    weight = 12.87 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_wjets_600To800, weight);

    TFile* fbackground_wjets_800To1200 = new TFile((path + "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_wjets_800To1200 = (TTree*)(fbackground_wjets_800To1200->Get(treename));
    Nev = (TH1D*)(fbackground_wjets_800To1200->Get("Nev"));
    weight = 5.366 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_wjets_800To1200, weight);

    //TFile* fbackground_wjets_1200To2500 = new TFile((path + "/Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RA2AnalysisTree.root").c_str());
    //TTree* bgTree_wjets_1200To2500 = (TTree*)(fbackground_wjets_1200To2500->Get(treename));
    //Nev = (TH1D*)(fbackground_wjets_1200To2500->Get("Nev"));
    //weight = 1.608 * lumi / Nev->GetBinContent(1);
    //factory->AddBackgroundTree(bgTree_wjets_1200To2500, weight);

    TFile* fbackground_wjets_2500ToInf = new TFile((path + "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_wjets_2500ToInf = (TTree*)(fbackground_wjets_2500ToInf->Get(treename));
    Nev = (TH1D*)(fbackground_wjets_2500ToInf->Get("Nev"));
    weight = 5.366 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_wjets_2500ToInf, weight);

    TFile* fbackground_ttjets = new TFile((path + "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root").c_str());
    TTree* bgTree_ttjets = (TTree*)(fbackground_ttjets->Get(treename));
    Nev = (TH1D*)(fbackground_ttjets->Get("Nev"));
    weight = 722.8 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_ttjets, weight);

    TFile* fbackground_dyjets_100To200 = new TFile((path + "/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_dyjets_100To200 = (TTree*)(fbackground_dyjets_100To200->Get(treename));
    Nev = (TH1D*)(fbackground_dyjets_100To200->Get("Nev"));
    weight = 161.1 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_dyjets_100To200, weight);

    TFile* fbackground_dyjets_200To400 = new TFile((path + "/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_dyjets_200To400 = (TTree*)(fbackground_dyjets_200To400->Get(treename));
    Nev = (TH1D*)(fbackground_dyjets_200To400->Get("Nev"));
    weight = 48.66 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_dyjets_200To400, weight);

    TFile* fbackground_dyjets_400To600 = new TFile((path + "/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_dyjets_400To600 = (TTree*)(fbackground_dyjets_400To600->Get(treename));
    Nev = (TH1D*)(fbackground_dyjets_400To600->Get("Nev"));
    weight = 6.968 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_dyjets_400To600, weight);

    //TFile* fbackground_dyjets_600To800 = new TFile((path + "/Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RA2AnalysisTree.root").c_str());
    //TTree* bgTree_dyjets_600To800 = (TTree*)(fbackground_dyjets_600To800->Get(treename));
    //Nev = (TH1D*)(fbackground_dyjets_600To800->Get("Nev"));
    //weight = 1.681 * lumi / Nev->GetBinContent(1);
    //factory->AddBackgroundTree(bgTree_dyjets_600To800, weight);

    TFile* fbackground_dyjets_800To1200 = new TFile((path + "/DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_dyjets_800To1200 = (TTree*)(fbackground_dyjets_800To1200->Get(treename));
    Nev = (TH1D*)(fbackground_dyjets_800To1200->Get("Nev"));
    weight = 0.8052 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_dyjets_800To1200, weight);

    TFile* fbackground_dyjets_1200To2500 = new TFile((path + "/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8.root").c_str());
    TTree* bgTree_dyjets_1200To2500 = (TTree*)(fbackground_dyjets_1200To2500->Get(treename));
    Nev = (TH1D*)(fbackground_dyjets_1200To2500->Get("Nev"));
    weight = 0.1933 * lumi / Nev->GetBinContent(1);
    factory->AddBackgroundTree(bgTree_dyjets_1200To2500, weight);

    //TFile* fbackground_dyjets_2500ToInf = new TFile((path + "/Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RA2AnalysisTree.root").c_str());
    //TTree* bgTree_dyjets_2500ToInf = (TTree*)(fbackground_dyjets_2500ToInf->Get(treename));
    //Nev = (TH1D*)(fbackground_dyjets_2500ToInf->Get("Nev"));
    //weight = 0.004385 * lumi / Nev->GetBinContent(1);
    //factory->AddBackgroundTree(bgTree_dyjets_2500ToInf, weight);

    // track-related variables:
    factory->AddVariable("dxyVtx",'F');
    factory->AddVariable("dzVtx",'F');
    factory->AddVariable("matchedCaloEnergy",'F');
    factory->AddVariable("trkRelIso",'F');
    factory->AddVariable("nValidPixelHits",'I');
    factory->AddVariable("nValidTrackerHits",'I');
    factory->AddVariable("ptErrOverPt2",'F');

    // If no numbers of events are given, half of the events in the tree are used 
    // for training, and the other half for testing:
    TCut mycuts;
    TCut mycutb;
    if (strcmp(maxTreeEntriesString.c_str(), "-1")) {
        // maxTreeEntriesString is set to a different value than -1
        mycuts=("pt>15 && abs(eta)<2.4 && passPFCandVeto==1 && trkRelIso<0.2 && dxyVtx<0.1 && dzVtx<0.1 && ptErrOverPt2<10 && nMissingMiddleHits==0 && trackQualityHighPurity==1 && Entry$<" + maxTreeEntriesString).c_str();
        mycutb=("pt>15 && abs(eta)<2.4 && passPFCandVeto==1 && trkRelIso<0.2 && dxyVtx<0.1 && dzVtx<0.1 && ptErrOverPt2<10 && nMissingMiddleHits==0 && trackQualityHighPurity==1 && Entry$<" + maxTreeEntriesString).c_str();
    } else {
        mycuts=("pt>15 && abs(eta)<2.4 && passPFCandVeto==1 && trkRelIso<0.2 && dxyVtx<0.1 && dzVtx<0.1 && ptErrOverPt2<10 && nMissingMiddleHits==0 && trackQualityHighPurity==1");
        mycutb=("pt>15 && abs(eta)<2.4 && passPFCandVeto==1 && trkRelIso<0.2 && dxyVtx<0.1 && dzVtx<0.1 && ptErrOverPt2<10 && nMissingMiddleHits==0 && trackQualityHighPurity==1");
    }

    factory->PrepareTrainingAndTestTree(mycuts, mycutb, "SplitMode=random:!V");

    factory->BookMethod(TMVA::Types::kBDT, "BDT", "NTrees=200:MaxDepth=4");

    factory->TrainAllMethods();
    factory->TestAllMethods();
    factory->EvaluateAllMethods();
    outputFile->Close();

    if (!gROOT->IsBatch()) TMVA::TMVAGui( outFileName );

    return 0;

}


int main( int argc, char** argv )
{
   return tmva(argv[1], argv[2], argv[3], argv[4]);
}

