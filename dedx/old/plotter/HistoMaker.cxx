#include <iostream>
#include <string>
#include <fstream>
#include "TApplication.h"
#include "TROOT.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TMath.h"
#include "TChain.h"
#include <vector>
#include "TLorentzVector.h"
#include "TBranch.h"
#include "TSystem.h"

using namespace std;

int FillHisto(TH1D* hist, double valx, double weight)
{
    // filling histogram with overflow/underflow bins
    int nbinsx = hist->GetNbinsX();
    double minvalx=hist->GetXaxis()->GetBinCenter(1);
    double maxvalx=hist->GetXaxis()->GetBinCenter(nbinsx);
    
    double newvalx = valx;
    
    if(valx< minvalx) newvalx=minvalx;
    else if(valx>maxvalx) newvalx=maxvalx;
    
    hist->Fill(newvalx, weight);
}

int FillHisto(TH2D* hist, double valx, double valy, double weight)
{
    // filling histogram with overflow/underflow bins
    int nbinsx = hist->GetNbinsX();
    double minvalx=hist->GetXaxis()->GetBinCenter(1);
    double maxvalx=hist->GetXaxis()->GetBinCenter(nbinsx);
    
    double newvalx = valx;
    
    int nbinsy = hist->GetNbinsY();
    double minvaly=hist->GetYaxis()->GetBinCenter(1);
    double maxvaly=hist->GetYaxis()->GetBinCenter(nbinsy);
    
    double newvaly = valy;
    
    if(valx< minvalx) newvalx=minvalx;
    else if(valx>maxvalx) newvalx=maxvalx;
    
    if(valy< minvaly) newvaly=minvaly;
    else if(valy>maxvaly) newvaly=maxvaly;
    
    hist->Fill(newvalx, newvaly, weight);
}

int HistoMaker(const char* inputfile, const char* outdir, const char* outputfile, const char* isData, const char* isSignal)
{
    cout << "Running HistoMaker" << endl;
    cout << "Input file : " << inputfile << endl;
    cout << "Output Directory : " << outdir << endl;
    cout << "Output file : " << outputfile << endl;
    cout << "isData : " << isData << endl;
    cout << "isSignal : " << isSignal << endl;

    bool IsData = 0;
    if (strcmp(isData,"True")==0){IsData = true;}
    else if (strcmp(isData,"False")==0){IsData = false;}
    else {
        cout << "IsData not correctly defined" << endl;
        return 0;
    }
    cout << "(Converted)IsData : " << IsData << endl;
    
    bool IsSignal = 0;
    if (strcmp(isSignal,"True")==0){IsSignal = true;}
    else if (strcmp(isSignal,"False")==0){IsSignal = false;}
    else {
        cout << "IsSignal not correctly defined" << endl;
        return 0;
    }
    cout << "(Converted)IsSignal : " << IsSignal << endl;

    TFile *f = new TFile(inputfile);
    TTree *fChain = (TTree*)f->Get("Events");
    fChain->SetBranchStatus("*",1);  // enable all branches
    //fChain->SetBranchStatus("*",0);  // disable all branches

    // Declaration of leaf types
    Float_t         weight;
    Float_t         MET;
    Float_t         METPhi;
    Float_t         MHT;
    Float_t         HT;
    Float_t         MinDeltaPhiMhtJets;
    Float_t         PFCaloMETRatio;
    Float_t         madHT;
    Float_t         CrossSection;
    Float_t         puWeight;
    Float_t         MHT_cleaned;
    Float_t         HT_cleaned;
    Float_t         MinDeltaPhiMhtJets_cleaned;
    Int_t           n_jets;
    Int_t           n_btags;
    Int_t           n_leptons;
    Int_t           n_allvertices;
    Int_t           n_NVtx;
    Int_t           passesUniversalSelection;
    Int_t           n_genLeptons;
    Int_t           n_genElectrons;
    Int_t           n_genMuons;
    Int_t           n_genTaus;
    Int_t           n_jets_cleaned;
    Int_t           n_btags_cleaned;
    vector<TLorentzVector> *tracks;
    vector<int>     *tracks_is_pixel_track;
    vector<int>     *tracks_pixelLayersWithMeasurement;
    vector<int>     *tracks_trackerLayersWithMeasurement;
    vector<int>     *tracks_nMissingInnerHits;
    vector<int>     *tracks_nMissingMiddleHits;
    vector<int>     *tracks_nMissingOuterHits;
    vector<int>     *tracks_trackQualityHighPurity;
    vector<int>     *tracks_nValidPixelHits;
    vector<int>     *tracks_nValidTrackerHits;
    vector<int>     *tracks_fake;
    vector<int>     *tracks_prompt_electron;
    vector<int>     *tracks_prompt_muon;
    vector<int>     *tracks_prompt_tau;
    vector<int>     *tracks_prompt_tau_widecone;
    vector<int>     *tracks_prompt_tau_leadtrk;
    vector<int>     *tracks_passpionveto;
    vector<int>     *tracks_is_reco_lepton;
    vector<int>     *tracks_passPFCandVeto;
    vector<int>     *tracks_charge;
    vector<int>     *tracks_tagged_bdt;
    vector<int>     *tracks_tagged_bdt_loose;
    vector<double>  *tracks_dxyVtx;
    vector<double>  *tracks_dzVtx;
    vector<double>  *tracks_matchedCaloEnergy;
    vector<double>  *tracks_trkRelIso;
    vector<double>  *tracks_ptErrOverPt2;
    vector<double>  *tracks_P;
    vector<double>  *tracks_pt;
    vector<double>  *tracks_eta;
    vector<double>  *tracks_phi;
    vector<double>  *tracks_chargino_P;
    vector<double>  *tracks_chargino_pt;
    vector<double>  *tracks_chargino_eta;
    vector<double>  *tracks_chargino_phi;
    vector<double>  *tracks_trkMiniRelIso;
    vector<double>  *tracks_trackJetIso;
    vector<double>  *tracks_ptError;
    vector<double>  *tracks_neutralPtSum;
    vector<double>  *tracks_neutralWithoutGammaPtSum;
    vector<double>  *tracks_minDrLepton;
    vector<double>  *tracks_matchedCaloEnergyJets;
    vector<double>  *tracks_deDxHarmonic2pixel;
    vector<double>  *tracks_deDxHarmonic2strips;
    vector<double>  *tracks_chi2perNdof;
    vector<double>  *tracks_chargedPtSum;
    vector<double>  *tracks_chiCandGenMatchingDR;
    vector<double>  *tracks_LabXYcm;
    vector<double>  *tracks_mva_bdt;
    vector<double>  *tracks_mva_bdt_loose;
    
    vector<TLorentzVector> *muons;
    vector<int>     *muons_charge;
    vector<int>     *muons_mediumID;
    vector<int>     *muons_tightID;
    vector<int>     *muons_passIso;
    vector<double>  *muons_MiniIso;
    vector<double>  *muons_pt;
    vector<double>  *muons_eta;
    vector<double>  *muons_phi;
    
    vector<TLorentzVector> *electrons;
    vector<int>     *electrons_charge;
    vector<int>     *electrons_mediumID;
    vector<int>     *electrons_tightID;
    vector<int>     *electrons_passIso;
    vector<double>  *electrons_MiniIso;
    vector<double>  *electrons_pt;
    vector<double>  *electrons_eta;
    vector<double>  *electrons_phi;

    // List of branches
    TBranch        *b_weight;   //!
    TBranch        *b_MET;   //!
    TBranch        *b_METPhi;   //!
    TBranch        *b_MHT;   //!
    TBranch        *b_HT;   //!
    TBranch        *b_MinDeltaPhiMhtJets;   //!
    TBranch        *b_PFCaloMETRatio;   //!
    TBranch        *b_madHT;   //!
    TBranch        *b_CrossSection;   //!
    TBranch        *b_puWeight;   //!
    TBranch        *b_MHT_cleaned;   //!
    TBranch        *b_HT_cleaned;   //!
    TBranch        *b_MinDeltaPhiMhtJets_cleaned;   //!
    TBranch        *b_n_jets;   //!
    TBranch        *b_n_btags;   //!
    TBranch        *b_n_leptons;   //!
    TBranch        *b_n_allvertices;   //!
    TBranch        *b_n_NVtx;   //!
    TBranch        *b_passesUniversalSelection;   //!
    TBranch        *b_n_genLeptons;   //!
    TBranch        *b_n_genElectrons;   //!
    TBranch        *b_n_genMuons;   //!
    TBranch        *b_n_genTaus;   //!
    TBranch        *b_n_jets_cleaned;   //!
    TBranch        *b_n_btags_cleaned;   //!
    TBranch        *b_tracks;   //!
    TBranch        *b_tracks_is_pixel_track;   //!
    TBranch        *b_tracks_pixelLayersWithMeasurement;   //!
    TBranch        *b_tracks_trackerLayersWithMeasurement;   //!
    TBranch        *b_tracks_nMissingInnerHits;   //!
    TBranch        *b_tracks_nMissingMiddleHits;   //!
    TBranch        *b_tracks_nMissingOuterHits;   //!
    TBranch        *b_tracks_trackQualityHighPurity;   //!
    TBranch        *b_tracks_nValidPixelHits;   //!
    TBranch        *b_tracks_nValidTrackerHits;   //!
    TBranch        *b_tracks_fake;   //!
    TBranch        *b_tracks_prompt_electron;   //!
    TBranch        *b_tracks_prompt_muon;   //!
    TBranch        *b_tracks_prompt_tau;   //!
    TBranch        *b_tracks_prompt_tau_widecone;   //!
    TBranch        *b_tracks_prompt_tau_leadtrk;   //!
    TBranch        *b_tracks_passpionveto;   //!
    TBranch        *b_tracks_is_reco_lepton;   //!
    TBranch        *b_tracks_passPFCandVeto;   //!
    TBranch        *b_tracks_charge;   //!
    TBranch        *b_tracks_tagged_bdt;   //!
    TBranch        *b_tracks_tagged_bdt_loose;   //!
    TBranch        *b_tracks_dxyVtx;   //!
    TBranch        *b_tracks_dzVtx;   //!
    TBranch        *b_tracks_matchedCaloEnergy;   //!
    TBranch        *b_tracks_trkRelIso;   //!
    TBranch        *b_tracks_ptErrOverPt2;   //!
    TBranch        *b_tracks_P;   //!
    TBranch        *b_tracks_pt;   //!
    TBranch        *b_tracks_eta;   //!
    TBranch        *b_tracks_phi;   //!
    TBranch        *b_tracks_chargino_P;   //!
    TBranch        *b_tracks_chargino_pt;   //!
    TBranch        *b_tracks_chargino_eta;   //!
    TBranch        *b_tracks_chargino_phi;   //!
    TBranch        *b_tracks_trkMiniRelIso;   //!
    TBranch        *b_tracks_trackJetIso;   //!
    TBranch        *b_tracks_ptError;   //!
    TBranch        *b_tracks_neutralPtSum;   //!
    TBranch        *b_tracks_neutralWithoutGammaPtSum;   //!
    TBranch        *b_tracks_minDrLepton;   //!
    TBranch        *b_tracks_matchedCaloEnergyJets;   //!
    TBranch        *b_tracks_deDxHarmonic2pixel;   //!
    TBranch        *b_tracks_deDxHarmonic2strips;   //!
    TBranch        *b_tracks_chi2perNdof;   //!
    TBranch        *b_tracks_chargedPtSum;   //!
    TBranch        *b_tracks_chiCandGenMatchingDR;   //!
    TBranch        *b_tracks_LabXYcm;   //!
    TBranch        *b_tracks_mva_bdt;   //!
    TBranch        *b_tracks_mva_bdt_loose;   //!
    TBranch        *b_muons;   //!
    TBranch        *b_muons_charge;   //!
    TBranch        *b_muons_mediumID;   //!
    TBranch        *b_muons_tightID;   //!
    TBranch        *b_muons_passIso;   //!
    TBranch        *b_muons_MiniIso;   //!
    TBranch        *b_muons_pt;   //!
    TBranch        *b_muons_eta;   //!
    TBranch        *b_muons_phi;   //!
    TBranch        *b_electrons;   //!
    TBranch        *b_electrons_charge;   //!
    TBranch        *b_electrons_mediumID;   //!
    TBranch        *b_electrons_tightID;   //!
    TBranch        *b_electrons_passIso;   //!
    TBranch        *b_electrons_MiniIso;   //!
    TBranch        *b_electrons_pt;   //!
    TBranch        *b_electrons_eta;   //!
    TBranch        *b_electrons_phi;   //!

    cout << "Initialize variables at HistMaker" << endl;
    // Set object pointer
    tracks = 0;
    tracks_is_pixel_track = 0;
    tracks_pixelLayersWithMeasurement = 0;
    tracks_trackerLayersWithMeasurement = 0;
    tracks_nMissingInnerHits = 0;
    tracks_nMissingMiddleHits = 0;
    tracks_nMissingOuterHits = 0;
    tracks_trackQualityHighPurity = 0;
    tracks_nValidPixelHits = 0;
    tracks_nValidTrackerHits = 0;
    tracks_fake = 0;
    tracks_prompt_electron = 0;
    tracks_prompt_muon = 0;
    tracks_prompt_tau = 0;
    tracks_prompt_tau_widecone = 0;
    tracks_prompt_tau_leadtrk = 0;
    tracks_passpionveto = 0;
    tracks_is_reco_lepton = 0;
    tracks_passPFCandVeto = 0;
    tracks_charge = 0;
    tracks_tagged_bdt = 0;
    tracks_tagged_bdt_loose = 0;
    tracks_dxyVtx = 0;
    tracks_dzVtx = 0;
    tracks_matchedCaloEnergy = 0;
    tracks_trkRelIso = 0;
    tracks_ptErrOverPt2 = 0;
    tracks_P = 0;
    tracks_pt = 0;
    tracks_eta = 0;
    tracks_phi = 0;
    tracks_chargino_P = 0;
    tracks_chargino_pt = 0;
    tracks_chargino_eta = 0;
    tracks_chargino_phi = 0;
    tracks_trkMiniRelIso = 0;
    tracks_trackJetIso = 0;
    tracks_ptError = 0;
    tracks_neutralPtSum = 0;
    tracks_neutralWithoutGammaPtSum = 0;
    tracks_minDrLepton = 0;
    tracks_matchedCaloEnergyJets = 0;
    tracks_deDxHarmonic2pixel = 0;
    tracks_deDxHarmonic2strips = 0;
    tracks_chi2perNdof = 0;
    tracks_chargedPtSum = 0;
    tracks_chiCandGenMatchingDR = 0;
    tracks_LabXYcm = 0;
    tracks_mva_bdt = 0;
    tracks_mva_bdt_loose = 0;
    muons = 0;
    muons_mediumID = 0;
    muons_tightID = 0;
    muons_passIso = 0;
    muons_MiniIso = 0;
    muons_pt = 0;
    muons_eta = 0;
    muons_phi = 0;
    electrons = 0;
    electrons_mediumID = 0;
    electrons_tightID = 0;
    electrons_passIso = 0;
    electrons_MiniIso = 0;
    electrons_pt = 0;
    electrons_eta = 0;
    electrons_phi = 0;

    
    // Set branch addresses and branch pointers
    fChain->SetMakeClass(1);

    if (!IsData)
    {
	fChain->SetBranchAddress("madHT", &madHT, &b_madHT);
    	fChain->SetBranchAddress("CrossSection", &CrossSection, &b_CrossSection);
    	fChain->SetBranchAddress("puWeight", &puWeight, &b_puWeight);
    }
    fChain->SetBranchAddress("weight", &weight, &b_weight);
    fChain->SetBranchAddress("MET", &MET, &b_MET);
    fChain->SetBranchAddress("METPhi", &METPhi, &b_METPhi);
    fChain->SetBranchAddress("MHT", &MHT, &b_MHT);
    fChain->SetBranchAddress("HT", &HT, &b_HT);
    fChain->SetBranchAddress("MinDeltaPhiMhtJets", &MinDeltaPhiMhtJets, &b_MinDeltaPhiMhtJets);
    fChain->SetBranchAddress("PFCaloMETRatio", &PFCaloMETRatio, &b_PFCaloMETRatio);
    fChain->SetBranchAddress("MHT_cleaned", &MHT_cleaned, &b_MHT_cleaned);
    fChain->SetBranchAddress("HT_cleaned", &HT_cleaned, &b_HT_cleaned);
    fChain->SetBranchAddress("MinDeltaPhiMhtJets_cleaned", &MinDeltaPhiMhtJets_cleaned, &b_MinDeltaPhiMhtJets_cleaned);
    fChain->SetBranchAddress("n_jets", &n_jets, &b_n_jets);
    fChain->SetBranchAddress("n_btags", &n_btags, &b_n_btags);
    fChain->SetBranchAddress("n_leptons", &n_leptons, &b_n_leptons);
    fChain->SetBranchAddress("n_allvertices", &n_allvertices, &b_n_allvertices);
    fChain->SetBranchAddress("n_NVtx", &n_NVtx, &b_n_NVtx);
    fChain->SetBranchAddress("passesUniversalSelection", &passesUniversalSelection, &b_passesUniversalSelection);
    fChain->SetBranchAddress("n_genLeptons", &n_genLeptons, &b_n_genLeptons);
    fChain->SetBranchAddress("n_genElectrons", &n_genElectrons, &b_n_genElectrons);
    fChain->SetBranchAddress("n_genMuons", &n_genMuons, &b_n_genMuons);
    fChain->SetBranchAddress("n_genTaus", &n_genTaus, &b_n_genTaus);
    fChain->SetBranchAddress("n_jets_cleaned", &n_jets_cleaned, &b_n_jets_cleaned);
    fChain->SetBranchAddress("n_btags_cleaned", &n_btags_cleaned, &b_n_btags_cleaned);
    fChain->SetBranchAddress("tracks", &tracks, &b_tracks);
    fChain->SetBranchAddress("tracks_is_pixel_track", &tracks_is_pixel_track, &b_tracks_is_pixel_track);
    fChain->SetBranchAddress("tracks_pixelLayersWithMeasurement", &tracks_pixelLayersWithMeasurement, &b_tracks_pixelLayersWithMeasurement);
    fChain->SetBranchAddress("tracks_trackerLayersWithMeasurement", &tracks_trackerLayersWithMeasurement, &b_tracks_trackerLayersWithMeasurement);
    fChain->SetBranchAddress("tracks_nMissingInnerHits", &tracks_nMissingInnerHits, &b_tracks_nMissingInnerHits);
    fChain->SetBranchAddress("tracks_nMissingMiddleHits", &tracks_nMissingMiddleHits, &b_tracks_nMissingMiddleHits);
    fChain->SetBranchAddress("tracks_nMissingOuterHits", &tracks_nMissingOuterHits, &b_tracks_nMissingOuterHits);
    fChain->SetBranchAddress("tracks_trackQualityHighPurity", &tracks_trackQualityHighPurity, &b_tracks_trackQualityHighPurity);
    fChain->SetBranchAddress("tracks_nValidPixelHits", &tracks_nValidPixelHits, &b_tracks_nValidPixelHits);
    fChain->SetBranchAddress("tracks_nValidTrackerHits", &tracks_nValidTrackerHits, &b_tracks_nValidTrackerHits);
    fChain->SetBranchAddress("tracks_fake", &tracks_fake, &b_tracks_fake);
    fChain->SetBranchAddress("tracks_prompt_electron", &tracks_prompt_electron, &b_tracks_prompt_electron);
    fChain->SetBranchAddress("tracks_prompt_muon", &tracks_prompt_muon, &b_tracks_prompt_muon);
    fChain->SetBranchAddress("tracks_prompt_tau", &tracks_prompt_tau, &b_tracks_prompt_tau);
    fChain->SetBranchAddress("tracks_prompt_tau_widecone", &tracks_prompt_tau_widecone, &b_tracks_prompt_tau_widecone);
    fChain->SetBranchAddress("tracks_prompt_tau_leadtrk", &tracks_prompt_tau_leadtrk, &b_tracks_prompt_tau_leadtrk);
    fChain->SetBranchAddress("tracks_passpionveto", &tracks_passpionveto, &b_tracks_passpionveto);
    fChain->SetBranchAddress("tracks_is_reco_lepton", &tracks_is_reco_lepton, &b_tracks_is_reco_lepton);
    fChain->SetBranchAddress("tracks_passPFCandVeto", &tracks_passPFCandVeto, &b_tracks_passPFCandVeto);
    fChain->SetBranchAddress("tracks_charge", &tracks_charge, &b_tracks_charge);
    fChain->SetBranchAddress("tracks_tagged_bdt", &tracks_tagged_bdt, &b_tracks_tagged_bdt);
    fChain->SetBranchAddress("tracks_tagged_bdt_loose", &tracks_tagged_bdt_loose, &b_tracks_tagged_bdt_loose);
    fChain->SetBranchAddress("tracks_dxyVtx", &tracks_dxyVtx, &b_tracks_dxyVtx);
    fChain->SetBranchAddress("tracks_dzVtx", &tracks_dzVtx, &b_tracks_dzVtx);
    fChain->SetBranchAddress("tracks_matchedCaloEnergy", &tracks_matchedCaloEnergy, &b_tracks_matchedCaloEnergy);
    fChain->SetBranchAddress("tracks_trkRelIso", &tracks_trkRelIso, &b_tracks_trkRelIso);
    fChain->SetBranchAddress("tracks_ptErrOverPt2", &tracks_ptErrOverPt2, &b_tracks_ptErrOverPt2);
    fChain->SetBranchAddress("tracks_P", &tracks_P, &b_tracks_P);
    fChain->SetBranchAddress("tracks_pt", &tracks_pt, &b_tracks_pt);
    fChain->SetBranchAddress("tracks_eta", &tracks_eta, &b_tracks_eta);
    fChain->SetBranchAddress("tracks_phi", &tracks_phi, &b_tracks_phi);
    fChain->SetBranchAddress("tracks_chargino_P", &tracks_chargino_P, &b_tracks_chargino_P);
    fChain->SetBranchAddress("tracks_chargino_pt", &tracks_chargino_pt, &b_tracks_chargino_pt);
    fChain->SetBranchAddress("tracks_chargino_eta", &tracks_chargino_eta, &b_tracks_chargino_eta);
    fChain->SetBranchAddress("tracks_chargino_phi", &tracks_chargino_phi, &b_tracks_chargino_phi);
    fChain->SetBranchAddress("tracks_trkMiniRelIso", &tracks_trkMiniRelIso, &b_tracks_trkMiniRelIso);
    fChain->SetBranchAddress("tracks_trackJetIso", &tracks_trackJetIso, &b_tracks_trackJetIso);
    fChain->SetBranchAddress("tracks_ptError", &tracks_ptError, &b_tracks_ptError);
    fChain->SetBranchAddress("tracks_neutralPtSum", &tracks_neutralPtSum, &b_tracks_neutralPtSum);
    fChain->SetBranchAddress("tracks_neutralWithoutGammaPtSum", &tracks_neutralWithoutGammaPtSum, &b_tracks_neutralWithoutGammaPtSum);
    fChain->SetBranchAddress("tracks_minDrLepton", &tracks_minDrLepton, &b_tracks_minDrLepton);
    fChain->SetBranchAddress("tracks_matchedCaloEnergyJets", &tracks_matchedCaloEnergyJets, &b_tracks_matchedCaloEnergyJets);
    fChain->SetBranchAddress("tracks_deDxHarmonic2pixel", &tracks_deDxHarmonic2pixel, &b_tracks_deDxHarmonic2pixel);
    fChain->SetBranchAddress("tracks_deDxHarmonic2strips", &tracks_deDxHarmonic2strips, &b_tracks_deDxHarmonic2strips);
    fChain->SetBranchAddress("tracks_chi2perNdof", &tracks_chi2perNdof, &b_tracks_chi2perNdof);
    fChain->SetBranchAddress("tracks_chargedPtSum", &tracks_chargedPtSum, &b_tracks_chargedPtSum);
    fChain->SetBranchAddress("tracks_chiCandGenMatchingDR", &tracks_chiCandGenMatchingDR, &b_tracks_chiCandGenMatchingDR);
    fChain->SetBranchAddress("tracks_LabXYcm", &tracks_LabXYcm, &b_tracks_LabXYcm);
    fChain->SetBranchAddress("tracks_mva_bdt", &tracks_mva_bdt, &b_tracks_mva_bdt);
    fChain->SetBranchAddress("tracks_mva_bdt_loose", &tracks_mva_bdt_loose, &b_tracks_mva_bdt_loose);
    fChain->SetBranchAddress("muons", &muons, &b_muons);
    fChain->SetBranchAddress("muons_mediumID", &muons_mediumID, &b_muons_mediumID);
    fChain->SetBranchAddress("muons_tightID", &muons_tightID, &b_muons_tightID);
    fChain->SetBranchAddress("muons_passIso", &muons_passIso, &b_muons_passIso);
    fChain->SetBranchAddress("muons_MiniIso", &muons_MiniIso, &b_muons_MiniIso);
    fChain->SetBranchAddress("muons_pt", &muons_pt, &b_muons_pt);
    fChain->SetBranchAddress("muons_eta", &muons_eta, &b_muons_eta);
    fChain->SetBranchAddress("muons_phi", &muons_phi, &b_muons_phi);
    fChain->SetBranchAddress("electrons", &electrons, &b_electrons);
    fChain->SetBranchAddress("electrons_mediumID", &electrons_mediumID, &b_electrons_mediumID);
    fChain->SetBranchAddress("electrons_tightID", &electrons_tightID, &b_electrons_tightID);
    fChain->SetBranchAddress("electrons_passIso", &electrons_passIso, &b_electrons_passIso);
    fChain->SetBranchAddress("electrons_MiniIso", &electrons_MiniIso, &b_electrons_MiniIso);
    fChain->SetBranchAddress("electrons_pt", &electrons_pt, &b_electrons_pt);
    fChain->SetBranchAddress("electrons_eta", &electrons_eta, &b_electrons_eta);
    fChain->SetBranchAddress("electrons_phi", &electrons_phi, &b_electrons_phi);
   
    // Output root file
    TFile* fout = new TFile(Form("./%s/%s",outdir,outputfile),"recreate");
    
    // Histogram
    TH1::SetDefaultSumw2();
    TH1D* h_MET = new TH1D("MET","MET",100,0,1000);
    TH1D* h_MHT = new TH1D("MHT","MHT",100,0,1000);
    TH1D* h_HT = new TH1D("HT","HT",200,0,2000);
    TH1D* h_MinDeltaPhiMhtJets = new TH1D("dPhiMhtJets","dPhiMhtJets",100,0,1);
    TH1D* h_n_jets = new TH1D("n_jets","n_jets",20,0,20);
    TH1D* h_n_btags = new TH1D("n_btags","n_btags",10,0,10);
    TH1D* h_n_leptons = new TH1D("n_leptons","n_leptons",10,0,10);
    TH1D* h_n_DT_short = new TH1D("n_DT_short","n_DT_short",5,0,5);
    TH1D* h_n_DT_long = new TH1D("n_DT_long","n_DT_long",5,0,5);
    TH1D* h_n_DT = new TH1D("n_DT","n_DT",5,0,5);
    TH1D* h_TrackP_pixel = new TH1D("TrackP_pixel","Track_P",50,0,1000);
    TH1D* h_TrackP_pixel_chargino = new TH1D("TrackP_pixel_chargino","Track_P_chargino",50,0,1000);
    TH1D* h_TrackP_pixel_GenMatch = new TH1D("TrackP_pixel_GenMatch","Track_P_GenMatch",50,0,1000);
    TH1D* h_TrackPt_pixel = new TH1D("TrackPt_pixel","TrackPt",50,0,1000);
    TH1D* h_TrackPt_pixel_chargino = new TH1D("TrackPt_pixel_chargino","TrackPt_chargino",50,0,1000);
    TH1D* h_TrackPt_pixel_GenMatch = new TH1D("TrackPt_pixel_GenMatch","TrackPt_GenMatch",50,0,1000);
    TH1D* h_TrackP_strips = new TH1D("TrackP_strips","TrackP",50,0,1000);
    TH1D* h_TrackP_strips_chargino = new TH1D("TrackP_strips_chargino","TrackP_chargino",50,0,1000);
    TH1D* h_TrackP_strips_GenMatch = new TH1D("TrackP_strips_GenMatch","TrackP_GenMatch",50,0,1000);
    TH1D* h_TrackPt_strips = new TH1D("TrackPt_strips","TrackPt",50,0,1000);
    TH1D* h_TrackPt_strips_chargino = new TH1D("TrackPt_strips_chargino","TrackPt_chargino",50,0,1000);
    TH1D* h_TrackPt_strips_GenMatch = new TH1D("TrackPt_strips_GenMatch","TrackPt_GenMatch",50,0,1000);
    TH1D* h_TrackDedx_pixel = new TH1D("TrackDedx_pixel","TrackDedx",20,0,20);
    TH1D* h_TrackDedx_pixel_chargino = new TH1D("TrackDedx_pixel_chargino","TrackDedx_chargino",20,0,20);
    TH1D* h_TrackMass_pixel = new TH1D("TrackMass_pixel","Log10(TrackMass_pixel)",50,0,5.5);
    TH1D* h_TrackMass_pixel_calib = new TH1D("TrackMass_pixel_calib","Log10(TrackMass_pixel_calib)",50,0,5.5);
    TH1D* h_TrackMass_pixel_charginoMomentum = new TH1D("TrackMass_pixel_charginoMomentum","Log10(TrackMass_pixel_charginoMomentum)",50,0,5.5);
    TH1D* h_TrackMass_pixel_GenMatch = new TH1D("TrackMass_pixel_GenMatch","Log10(TrackMass_pixel_GenMatch)",50,0,5.5);
    
    TH1D* h_TrackDedx_strips = new TH1D("TrackDedx_strips","TrackDedx_strips",20,0,20);
    TH1D* h_TrackDedx_strips_chargino = new TH1D("TrackDedx_strips_chargino","TrackDedx_strips_chargino",20,0,20);
    TH1D* h_TrackMass_strips = new TH1D("TrackMass_strips","Log10(TrackMass_strips)",50,0,5.5);
    TH1D* h_TrackMass_strips_calib = new TH1D("TrackMass_strips_calib","Log10(TrackMass_strips_calib)",50,0,5.5);
    TH1D* h_TrackMass_strips_charginoMomentum = new TH1D("TrackMass_strips_charginoMomentum","Log10(TrackMass_strips_charginoMomentum)",50,0,5.5);
    TH1D* h_TrackMass_strips_GenMatch = new TH1D("TrackMass_strips_GenMatch","Log10(TrackMass_strips_GenMatch)",50,0,5.5);
    TH1D* h_TrackMass_weightedPixelStripsMass = new TH1D("TrackMass_weightedPixelStripsMass","Log10(TrackMass_weightedPixelStripsMass)",50,0,5.5);
    
    TH1D* h_Track_deltaR_with_chargino_pixel = new TH1D("Track_deltaR_with_chargino_pixel","Track_deltaR__with_chargino_pixel",20,0,0.1);
    TH1D* h_Track_deltaR_with_chargino_strips = new TH1D("Track_deltaR_with_chargino_strips","Track_deltaR_with_chargino_strips",20,0,0.1);
    
    TH1D* h_CR_noDT_MET = new TH1D("MET_CR_noDT","MET",100,0,1000);
    TH1D* h_CR_noDT_MHT = new TH1D("MHT_CR_noDT","MHT",100,0,1000);
    TH1D* h_CR_noDT_HT = new TH1D("HT_CR_noDT","HT",200,0,2000);
    TH1D* h_CR_noDT_MinDeltaPhiMhtJets = new TH1D("dPhiMhtJets_CR_noDT","dPhiMhtJets",100,0,1);
    TH1D* h_CR_noDT_n_jets = new TH1D("n_jets_CR_noDT","n_jets",20,0,20);
    TH1D* h_CR_noDT_n_btags = new TH1D("n_btags_CR_noDT","n_btags",10,0,10);
    TH1D* h_CR_noDT_n_leptons = new TH1D("n_leptons_CR_noDT","n_leptons",10,0,10);
    TH1D* h_CR_noDT_n_DT = new TH1D("n_DT_CR_noDT","n_DT",5,0,5);
    TH1D* h_CR_noDT_TrackP = new TH1D("TrackP_CR_noDT","TrackP",20,0,1000);
    TH1D* h_CR_noDT_TrackPt = new TH1D("TrackPt_CR_noDT","TrackPt",20,0,1000);
    TH1D* h_CR_noDT_TrackDedx_pixel = new TH1D("TrackDedx_pixel_CR_noDT","TrackDedx",20,0,20);
    TH1D* h_CR_noDT_TrackDedx_strips = new TH1D("TrackDedx_strips_CR_noDT","TrackDedx",20,0,20);
    
    TH1D* h_CR1muon_MET = new TH1D("MET_CR1muon","MET",50,0,1000);
    TH1D* h_CR1muon_MHT = new TH1D("MHT_CR1muon","MHT",50,0,1000);
    TH1D* h_CR1muon_HT = new TH1D("HT_CR1muon","HT",50,0,2000);
    TH1D* h_CR1muon_MinDeltaPhiMhtJets = new TH1D("dPhiMhtJets_CR1muon","dPhiMhtJets",100,0,1);
    TH1D* h_CR1muon_n_jets = new TH1D("n_jets_CR1muon","n_jets",20,0,20);
    TH1D* h_CR1muon_n_btags = new TH1D("n_btags_CR1muon","n_btags",10,0,10);
    TH1D* h_CR1muon_n_leptons = new TH1D("n_leptons_CR1muon","n_leptons",10,0,10);
    TH1D* h_CR1muon_n_track_short = new TH1D("n_track_short_CR1muon","n_track_short",5,0,5);
    TH1D* h_CR1muon_n_track_long = new TH1D("n_track_long_CR1muon","n_track_long",5,0,5);
    TH1D* h_CR1muon_n_track = new TH1D("n_track_CR1muon","n_track",5,0,5);
    TH1D* h_CR1muon_TrackP_pixel = new TH1D("TrackP_pixel_CR1muon","TrackP",20,0,1000);
    TH1D* h_CR1muon_TrackPt_pixel = new TH1D("TrackPt_pixel_CR1muon","TrackPt",20,0,1000);
    TH1D* h_CR1muon_TrackP_strips = new TH1D("TrackP_strips_CR1muon","TrackP",20,0,1000);
    TH1D* h_CR1muon_TrackPt_strips = new TH1D("TrackPt_strips_CR1muon","TrackPt",20,0,1000);
    TH1D* h_CR1muon_TrackDedx_pixel = new TH1D("TrackDedx_pixel_CR1muon","TrackDedx",20,0,20);
    TH1D* h_CR1muon_TrackDedx_strips = new TH1D("TrackDedx_strips_CR1muon","TrackDedx",20,0,20);
    TH1D* h_n_muon = new TH1D("n_muon","n_muon",10,0,10);
    TH1D* h_muonPt = new TH1D("muonPt","muonPt",30,0,300);
    TH1D* h_CR1muonPt = new TH1D("muonPt_CR1muon","muonPt",30,0,300);
    TH1D* h_muonEta = new TH1D("muonEta","muonEta",30,-3,3);
    TH1D* h_muonPhi = new TH1D("muonPhi","muonPhi",30,-3,3);
    
    TH1D* h_CR1electron_MET = new TH1D("MET_CR1electron","MET",50,0,1000);
    TH1D* h_CR1electron_MHT = new TH1D("MHT_CR1electron","MHT",50,0,1000);
    TH1D* h_CR1electron_HT = new TH1D("HT_CR1electron","HT",50,0,2000);
    TH1D* h_CR1electron_MinDeltaPhiMhtJets = new TH1D("dPhiMhtJets_CR1electron","dPhiMhtJets",100,0,1);
    TH1D* h_CR1electron_n_jets = new TH1D("n_jets_CR1electron","n_jets",20,0,20);
    TH1D* h_CR1electron_n_btags = new TH1D("n_btags_CR1electron","n_btags",10,0,10);
    TH1D* h_CR1electron_n_leptons = new TH1D("n_leptons_CR1electron","n_leptons",10,0,10);
    TH1D* h_CR1electron_n_track_short = new TH1D("n_track_short_CR1electron","n_track_short",5,0,5);
    TH1D* h_CR1electron_n_track_long = new TH1D("n_track_long_CR1electron","n_track_long",5,0,5);
    TH1D* h_CR1electron_n_track = new TH1D("n_track_CR1electron","n_track",5,0,5);
    TH1D* h_CR1electron_TrackP_pixel = new TH1D("TrackP_pixel_CR1electron","TrackP",20,0,1000);
    TH1D* h_CR1electron_TrackPt_pixel = new TH1D("TrackPt_pixel_CR1electron","TrackPt",20,0,1000);
    TH1D* h_CR1electron_TrackP_strips = new TH1D("TrackP_strips_CR1electron","TrackP",20,0,1000);
    TH1D* h_CR1electron_TrackPt_strips = new TH1D("TrackPt_strips_CR1electron","TrackPt",20,0,1000);
    TH1D* h_CR1electron_TrackDedx_pixel = new TH1D("TrackDedx_pixel_CR1electron","TrackDedx",20,0,20);
    TH1D* h_CR1electron_TrackDedx_strips = new TH1D("TrackDedx_strips_CR1electron","TrackDedx",20,0,20);
    TH1D* h_n_electron = new TH1D("n_electron","n_electron",10,0,10);
    TH1D* h_electronPt = new TH1D("electronPt","electronPt",30,0,300);
    TH1D* h_CR1electronPt = new TH1D("electronPt_CR1electron","electronPt",30,0,300);
    TH1D* h_electronEta = new TH1D("electronEta","electronEta",30,-3,3);
    TH1D* h_electronPhi = new TH1D("electronPhi","electronPhi",30,-3,3);
    //TH1D* h_CR1_TrackMass_pixel = new TH1D("TrackMass_pixel_CR1","Log10(TrackMass_pixel)",50,0,5.5);
    //TH1D* h_CR1_TrackMass_pixel_calib = new TH1D("TrackMass_pixel_CR1_calib","Log10(TrackMass_pixel)",50,0,5.5);
    //TH1D* h_CR1_TrackMass_strips = new TH1D("TrackMass_strips_CR1","Log10(TrackMass_strips)",50,0,5.5);
    //TH1D* h_CR1_TrackMass_strips_calib = new TH1D("TrackMass_strips_CR1_calib","Log10(TrackMass_strips)",50,0,5.5);
    //TH1D* h_CR1_TrackMass_weightedPixelStripsMass = new TH1D("TrackMass_weightedPixelStripsMass_CR1","Log10(TrackMass_weightedPixelStripsMass)",50,0,5.5);
    
    TH1D* h_CR2_MET = new TH1D("MET_CR2","MET",100,0,1000);
    TH1D* h_CR2_MHT = new TH1D("MHT_CR2","MHT",100,0,1000);
    TH1D* h_CR2_HT = new TH1D("HT_CR2","HT",200,0,2000);
    TH1D* h_CR2_MinDeltaPhiMhtJets = new TH1D("dPhiMhtJets_CR2","dPhiMhtJets",100,0,1);
    TH1D* h_CR2_n_jets = new TH1D("n_jets_CR2","n_jets",20,0,20);
    TH1D* h_CR2_n_btags = new TH1D("n_btags_CR2","n_btags",10,0,10);
    TH1D* h_CR2_n_leptons = new TH1D("n_leptons_CR2","n_leptons",10,0,10);
    TH1D* h_CR2_n_DT = new TH1D("n_DT_CR2","n_DT",5,0,5);
    TH1D* h_CR2_n_DT_short = new TH1D("n_DT_short_CR2","n_DT_short",5,0,5);
    TH1D* h_CR2_n_DT_long = new TH1D("n_DT_long_CR2","n_DT_long",5,0,5);
    TH1D* h_CR2_TrackP_pixel = new TH1D("TrackP_pixel_CR2","TrackP",20,0,1000);
    TH1D* h_CR2_TrackPt_pixel = new TH1D("TrackPt_pixel_CR2","TrackPt",20,0,1000);
    TH1D* h_CR2_TrackP_strips = new TH1D("TrackP_strips_CR2","TrackP",20,0,1000);
    TH1D* h_CR2_TrackPt_strips = new TH1D("TrackPt_strips_CR2","TrackPt",20,0,1000);
    TH1D* h_CR2_TrackDedx_pixel = new TH1D("TrackDedx_pixel_CR2","TrackDedx",20,0,20);
    TH1D* h_CR2_TrackDedx_strips = new TH1D("TrackDedx_strips_CR2","TrackDedx",20,0,20);
    TH1D* h_CR2_TrackMass_pixel = new TH1D("TrackMass_pixel_CR2","Log10(TrackMass_pixel)",50,0,5.5);
    TH1D* h_CR2_TrackMass_pixel_calib = new TH1D("TrackMass_pixel_CR2_calib","Log10(TrackMass_pixel)",50,0,5.5);
    TH1D* h_CR2_TrackMass_strips = new TH1D("TrackMass_strips_CR2","Log10(TrackMass_strips)",50,0,5.5);
    TH1D* h_CR2_TrackMass_strips_calib = new TH1D("TrackMass_strips_CR2_calib","Log10(TrackMass_strips)",50,0,5.5);

    // 2D Histograms
    TH2D* h2_TrackP_charginoP_pixel = new TH2D("TrackP_charginoP_pixel","TrackP vs charginoP pixel", 100, 0, 2000, 100, 0, 2000);
    TH2D* h2_MET_charginoPt_pixel = new TH2D("MET_charginoPt_pixel","MET vs charginoPt pixel", 100, 0, 1000, 100, 0, 2000);
    TH2D* h2_MET_TrackPt_pixel = new TH2D("MET_TrackPt_pixel","MET vs TrackPt pixel", 100, 0, 1000, 100, 0, 2000);
    TH2D* h2_METPhi_charginoPhi_pixel = new TH2D("METPhi_charginoPhi_pixel","METPhi vs charginoPhi pixel", 100, 0, 4, 100, 0, 4);
    TH2D* h2_METPhi_TrackPhi_pixel = new TH2D("METPhi_TrackPhi_pixel","METPhi vs TrackPhi pixel", 100, 0, 4, 100, 0, 4);
    TH2D* h2_TrackP_charginoP_strips = new TH2D("TrackP_charginoP_strips","TrackP vs charginoP strips", 100, 0, 2000, 100, 0, 2000);
    TH2D* h2_MET_charginoPt_strips = new TH2D("MET_charginoPt_strips","MET vs charginoPt strips", 100, 0, 1000, 100, 0, 2000);
    TH2D* h2_MET_TrackPt_strips = new TH2D("MET_TrackPt_strips","MET vs TrackPt strips", 100, 0, 1000, 100, 0, 2000);
    TH2D* h2_METPhi_charginoPhi_strips = new TH2D("METPhi_charginoPhi_strips","METPhi vs charginoPhi strips", 100, 0, 4, 100, 0, 4);
    TH2D* h2_METPhi_TrackPhi_strips = new TH2D("METPhi_TrackPhi_strips","METPhi vs TrackPhi strips", 100, 0, 4, 100, 0, 4);
    
    cout << "Total entry : " << fChain->GetEntries() << endl;
    Long64_t nentries = fChain->GetEntries();
    
    // Event loop start
    for (Long64_t ientry=0; ientry<nentries; ++ientry){
    //for (Long64_t ientry=0; ientry<1000; ++ientry){
	if (ientry %100000 ==0) cout << ientry << "th event passing" << endl;
	//cout << ientry << "th event" << endl;

	fChain->GetEntry(ientry);
	
	Int_t    n_DT_short = 0;
    	Int_t    n_DT_long = 0;
    	Int_t    n_DT = 0;
	Int_t	 n_muon = 0;
	Int_t	 n_electron = 0;
    	Double_t charginoDedx;
    	Double_t trackDedxPixel;
    	Double_t trackDedxStrips;
    	//Double_t trackMassPixel;
    	//Double_t trackMassStrips;
    	//Double_t trackMassPixel_calib;
    	//Double_t trackMassStrips_calib;
    	//Double_t trackMass_chargino;
    
	
	//FIXME : Currently 'weight' in skim file is wrong(GenTopWeight)
	if (IsData) weight = 1.0;
	else weight = 1.0 * puWeight * CrossSection / nentries;

	// Event selection start
	if (not passesUniversalSelection) continue; // Nvtx, JetID, various filters
	if (not (n_jets > 0)) continue;
	if (not (MET>280 && MinDeltaPhiMhtJets>0.3)) continue;
	
	// Muon loop start
	for (UInt_t imuon=0; imuon < muons->size(); ++imuon){
	    if (not((*muons_pt)[imuon] > 30)) continue;
	    if (not((*muons_tightID)[imuon])) continue;
	    if (not((*muons_passIso)[imuon])) continue;
	    n_muon++;
	    FillHisto(h_muonPt, (*muons_pt)[imuon],weight);
	    FillHisto(h_muonEta, (*muons_eta)[imuon],weight);
	    FillHisto(h_muonPhi, (*muons_phi)[imuon],weight);
	} // Muon loop end
	FillHisto(h_n_muon, n_muon,weight);
	
	// Electron loop start
	for (UInt_t ielectron=0; ielectron < electrons->size(); ++ielectron){
	    if (not((*electrons_pt)[ielectron] > 30)) continue;
	    if (not((*electrons_tightID)[ielectron])) continue;
	    if (not((*electrons_passIso)[ielectron])) continue;
	    n_electron++;
	    FillHisto(h_electronPt, (*electrons_pt)[ielectron],weight);
	    FillHisto(h_electronEta, (*electrons_eta)[ielectron],weight);
	    FillHisto(h_electronPhi, (*electrons_phi)[ielectron],weight);
	} // Electron loop End
	FillHisto(h_n_electron, n_electron,weight);
	    
	// Veto event if no leptons exist
	//if (n_muon==0 || n_electron==0) continue;
	if (n_muon==1){
	    FillHisto(h_CR1muonPt, (*muons_pt)[0],weight);
	    FillHisto(h_CR1muon_MET, MET, weight);
	    FillHisto(h_CR1muon_MHT, MHT, weight);
	    FillHisto(h_CR1muon_HT, HT, weight);
	    FillHisto(h_CR1muon_n_jets, n_jets, weight);
	}
	if(n_electron==1){
	    FillHisto(h_CR1electronPt, (*electrons_pt)[0],weight);
	    FillHisto(h_CR1electron_MET, MET, weight);
	    FillHisto(h_CR1electron_MHT, MHT, weight);
	    FillHisto(h_CR1electron_HT, HT, weight);
	    FillHisto(h_CR1electron_n_jets, n_jets, weight);
	}

	// SR region
	if (MET>280 && MinDeltaPhiMhtJets>0.3){
	    n_DT = 0;
	    n_DT_short = 0;
	    n_DT_long = 0;
	    trackDedxPixel = 0;
	    trackDedxStrips = 0;
	    //trackMassPixel = 0;
	    //trackMassStrips = 0;
	    //trackMassPixel_calib = 0;
	    //trackMassStrips_calib = 0;
	
	    // track loop start 
	    for (UInt_t itrack=0; itrack < tracks->size(); ++itrack){
	        if (not((*tracks_pt)[itrack] > 30)) continue;
	        //if ((*tracks_is_reco_lepton)[itrack]) continue;
	        if (not((*tracks_passpionveto)[itrack])) continue;
	        if (not((*tracks_passPFCandVeto)[itrack])) continue;
		
		trackDedxPixel = (*tracks_deDxHarmonic2pixel)[itrack];
		trackDedxStrips = (*tracks_deDxHarmonic2strips)[itrack];

		//trackMassPixel = TMath::Sqrt((trackDedxPixel-2.557)*TMath::Power((*tracks_P)[itrack],2)/2.579);
		//trackMassStrips = TMath::Sqrt((trackDedxStrips-2.557)*TMath::Power((*tracks_P)[itrack],2)/2.579);
		//trackMassPixel_calib = TMath::Sqrt((trackDedxPixel-3.01)*TMath::Power((*tracks_P)[itrack],2)/1.74);
		//trackMassStrips_calib = TMath::Sqrt((trackDedxStrips-3.01)*TMath::Power((*tracks_P)[itrack],2)/1.74);
		if (IsSignal) {
		    charginoDedx = 2.579*TMath::Sqrt(1400)/TMath::Sqrt((*tracks_chargino_P)[itrack]) + 2.557;
		    //trackMass_chargino = TMath::Sqrt((charginoDedx-2.557)*TMath::Power((*tracks_chargino_P)[itrack],2)/2.579);
		}

		// Short track selection
	        if ((*tracks_is_pixel_track)[itrack]==1 && ((*tracks_mva_bdt_loose)[itrack]>(*tracks_dxyVtx)[itrack]*(0.5/0.01)-0.3))
	        {
		    n_DT_short++;

	            FillHisto(h_TrackP_pixel,(*tracks_P)[itrack],weight);
	            FillHisto(h_TrackPt_pixel,(*tracks_pt)[itrack],weight);
	            FillHisto(h_TrackDedx_pixel,(*tracks_deDxHarmonic2pixel)[itrack],weight);
	            FillHisto(h_Track_deltaR_with_chargino_pixel,(*tracks_chiCandGenMatchingDR)[itrack],weight);
	            //if (trackDedxPixel>2.557) FillHisto(h_TrackMass_pixel,TMath::Log10(trackMassPixel),weight);
		    //if (trackDedxPixel>3.01) FillHisto(h_TrackMass_pixel_calib,TMath::Log10(trackMassPixel_calib),weight);
		    
		    // Gen-level chargino 
		    if (IsSignal) {
		        FillHisto(h_TrackP_pixel_chargino,(*tracks_chargino_P)[itrack],weight);
	            	FillHisto(h_TrackPt_pixel_chargino,(*tracks_chargino_pt)[itrack],weight);
		    	//FillHisto(h_TrackMass_pixel_charginoMomentum,TMath::Log10(trackMass_chargino),weight);
			FillHisto(h_TrackDedx_pixel_chargino,charginoDedx,weight);
		    }else {
		        FillHisto(h_TrackP_pixel_chargino,(*tracks_P)[itrack],weight);
			FillHisto(h_TrackPt_pixel_chargino,(*tracks_pt)[itrack],weight);
		    	//FillHisto(h_TrackMass_pixel_charginoMomentum,TMath::Log10(trackMassPixel),weight);
			FillHisto(h_TrackDedx_pixel_chargino,(*tracks_deDxHarmonic2pixel)[itrack],weight);
		    }
		    
		    // track matching with gen-chrgino(dR<0.01)
		    if ((*tracks_chiCandGenMatchingDR)[itrack] < 0.01){
		    	FillHisto(h_TrackP_pixel_GenMatch,(*tracks_P)[itrack],weight);
			FillHisto(h_TrackPt_pixel_GenMatch,(*tracks_pt)[itrack],weight);
		    	//FillHisto(h_TrackMass_pixel_GenMatch,TMath::Log10(trackMassPixel),weight);
		    	FillHisto(h2_MET_TrackPt_pixel,MET,(*tracks_P)[itrack],weight);
		    	FillHisto(h2_METPhi_TrackPhi_pixel,METPhi,(*tracks_phi)[itrack],weight);
			if (IsSignal) {
			   FillHisto(h2_TrackP_charginoP_pixel,(*tracks_P)[itrack],(*tracks_chargino_P)[itrack],weight);
		    	   FillHisto(h2_MET_charginoPt_pixel,MET,(*tracks_chargino_P)[itrack],weight);
		    	   FillHisto(h2_METPhi_charginoPhi_pixel,METPhi,(*tracks_chargino_phi)[itrack],weight);
			}
		    }
		    
	        }
		
		// Long track selection
		else if ((*tracks_is_pixel_track)[itrack]==0 && ((*tracks_mva_bdt_loose)[itrack]>(*tracks_dxyVtx)[itrack]*(0.6/0.01)+0.05))
	        {
		    n_DT_long++;

	            FillHisto(h_TrackP_strips,(*tracks_P)[itrack],weight);
	            FillHisto(h_TrackPt_strips,(*tracks_pt)[itrack],weight);
	            FillHisto(h_TrackDedx_strips,(*tracks_deDxHarmonic2strips)[itrack],weight);
	            //if (trackDedxStrips>2.557) FillHisto(h_TrackMass_strips,TMath::Log10(trackMassStrips),weight);
		    //if (trackDedxStrips>3.01) FillHisto(h_TrackMass_strips_calib,TMath::Log10(trackMassStrips_calib),weight);
	            FillHisto(h_Track_deltaR_with_chargino_strips,(*tracks_chiCandGenMatchingDR)[itrack],weight);
		    
		    // Gen-level chargino 
		    if (IsSignal) {
		        FillHisto(h_TrackP_strips_chargino,(*tracks_chargino_P)[itrack],weight);
	            	FillHisto(h_TrackPt_strips_chargino,(*tracks_chargino_pt)[itrack],weight);
		    	//FillHisto(h_TrackMass_strips_charginoMomentum,TMath::Log10(trackMass_chargino),weight);
			FillHisto(h_TrackDedx_strips_chargino,charginoDedx,weight);
		    }else {
		        FillHisto(h_TrackP_strips_chargino,(*tracks_P)[itrack],weight);
			FillHisto(h_TrackPt_strips_chargino,(*tracks_pt)[itrack],weight);
		    	//FillHisto(h_TrackMass_strips_charginoMomentum,TMath::Log10(trackMassStrips),weight);
			FillHisto(h_TrackDedx_strips_chargino,(*tracks_deDxHarmonic2strips)[itrack],weight);
		    }

		    // track matching with gen-chrgino(dR<0.01)
		    if ((*tracks_chiCandGenMatchingDR)[itrack] < 0.01){
		    	FillHisto(h_TrackP_strips_GenMatch,(*tracks_P)[itrack],weight);
			FillHisto(h_TrackPt_strips_GenMatch,(*tracks_pt)[itrack],weight);
		    	//FillHisto(h_TrackMass_strips_GenMatch,TMath::Log10(trackMassStrips),weight);
		    	FillHisto(h2_MET_TrackPt_strips,MET,(*tracks_P)[itrack],weight);
		    	FillHisto(h2_METPhi_TrackPhi_strips,METPhi,(*tracks_phi)[itrack],weight);
			if (IsSignal) {
			   FillHisto(h2_TrackP_charginoP_strips,(*tracks_P)[itrack],(*tracks_chargino_P)[itrack],weight);
		    	   FillHisto(h2_MET_charginoPt_strips,MET,(*tracks_chargino_P)[itrack],weight);
		    	   FillHisto(h2_METPhi_charginoPhi_strips,METPhi,(*tracks_chargino_phi)[itrack],weight);
			}
		    }
	        }
		// no DT region
		else 
		{
	            FillHisto(h_CR_noDT_TrackP,(*tracks_P)[itrack],weight);
	            FillHisto(h_CR_noDT_TrackPt,(*tracks_pt)[itrack],weight);
	            FillHisto(h_CR_noDT_TrackDedx_pixel,(*tracks_deDxHarmonic2pixel)[itrack],weight);
	            FillHisto(h_CR_noDT_TrackDedx_strips,(*tracks_deDxHarmonic2strips)[itrack],weight);
		}
	    } // End of track loop
	   
	    n_DT = n_DT_short + n_DT_long;

	    if (n_DT==0 ){
		FillHisto(h_CR_noDT_MET,MET,weight);
	    	FillHisto(h_CR_noDT_MHT,MHT,weight);
	    	FillHisto(h_CR_noDT_HT,HT,weight);
	    	FillHisto(h_CR_noDT_n_jets,n_jets,weight);
	    	FillHisto(h_CR_noDT_n_btags,n_btags,weight);
	    	FillHisto(h_CR_noDT_n_leptons,n_leptons,weight);
	    	FillHisto(h_CR_noDT_n_DT,n_DT,weight);
	    }
	    else if (n_DT >0)
	    {
		FillHisto(h_MET,MET,weight);
	    	FillHisto(h_MHT,MHT,weight);
	    	FillHisto(h_HT,HT,weight);
	    	FillHisto(h_n_jets,n_jets,weight);
	    	FillHisto(h_n_btags,n_btags,weight);
	    	FillHisto(h_n_leptons,n_leptons,weight);
	    	FillHisto(h_n_DT_short,n_DT_short,weight);
	    	FillHisto(h_n_DT_long,n_DT_long,weight);
	    	FillHisto(h_n_DT,n_DT,weight);
	    }
	    
	} // End of SR region
	
	// CR1 : lepton 
	if (MET>200 && MinDeltaPhiMhtJets>0.3){
	    Int_t n_track = 0;
	    Int_t n_track_short = 0;
	    Int_t n_track_long = 0;
	    Double_t trackDedxPixel = 0;
	    Double_t tracDedxStrips = 0;

	    // track loop start 
	    for (UInt_t itrack=0; itrack < tracks->size(); ++itrack){
	        if (not((*tracks_pt)[itrack] > 30)) continue;
	        //if (not((*tracks_is_reco_lepton)[itrack])) continue; // track is reco lepton

		trackDedxPixel = (*tracks_deDxHarmonic2pixel)[itrack];
		trackDedxStrips = (*tracks_deDxHarmonic2strips)[itrack];
		
		// Track Mass study is held at the moment
		//trackMassPixel = TMath::Sqrt((trackDedxPixel-2.557)*TMath::Power((*tracks_P)[itrack],2)/2.579);
		//trackMassStrips = TMath::Sqrt((trackDedxStrips-2.557)*TMath::Power((*tracks_P)[itrack],2)/2.579);
		//trackMassPixel_calib = TMath::Sqrt((trackDedxPixel-3.01)*TMath::Power((*tracks_P)[itrack],2)/1.74);
		//trackMassStrips_calib = TMath::Sqrt((trackDedxStrips-3.01)*TMath::Power((*tracks_P)[itrack],2)/1.74);

		// Short track selection
	        if ((*tracks_is_pixel_track)[itrack]==1)
	        {
		    n_track_short++;
	            //FillHisto(h_CR1muon_TrackP_pixel,(*tracks_P)[itrack],weight);
	            //FillHisto(h_CR1muon_TrackPt_pixel,(*tracks_pt)[itrack],weight);
	            //FillHisto(h_CR1muon_TrackDedx_pixel,(*tracks_deDxHarmonic2pixel)[itrack],weight);
	            //if (trackDedxPixel>2.557) FillHisto(h_CR1_TrackMass_pixel,TMath::Log10(trackMassPixel),weight);
		    //if (trackDedxPixel>3.01) FillHisto(h_CR1_TrackMass_pixel_calib,TMath::Log10(trackMassPixel_calib),weight);
		    
	        }

		// Long track selection
		else if ((*tracks_is_pixel_track)[itrack]==0)
	        {
		    n_track_long++;
	            //FillHisto(h_CR1_TrackP_strips,(*tracks_P)[itrack],weight);
	            //FillHisto(h_CR1_TrackPt_strips,(*tracks_pt)[itrack],weight);
	            //FillHisto(h_CR1_TrackDedx_strips,(*tracks_deDxHarmonic2strips)[itrack],weight);
	            //if (trackDedxStrips>2.557) FillHisto(h_CR1_TrackMass_strips,TMath::Log10(trackMassStrips),weight);
		    //if (trackDedxStrips>3.01) FillHisto(h_CR1_TrackMass_strips_calib,TMath::Log10(trackMassStrips_calib),weight);
	        }
	    } // End of track loop
	    
	    //n_track = n_track_short + n_track_long;
	    //if (n_track==0 ) continue;
	    
	} // End of CR1

	/*
	// CR2 : Inverted BDT (fake-like track)
	if (MET>200 && MinDeltaPhiMhtJets>0.3){
	    n_DT = 0;
	    n_DT_short = 0;
	    n_DT_long = 0;
	    trackDedxPixel = 0;
	    trackDedxStrips = 0;
	    
	    // track loop start 
	    for (UInt_t itrack=0; itrack < tracks->size(); ++itrack){
	        if (not((*tracks_pt)[itrack] > 30)) continue;
	        if ((*tracks_is_reco_lepton)[itrack]) continue; 

		trackDedxPixel = (*tracks_deDxHarmonic2pixel)[itrack];
		trackDedxStrips = (*tracks_deDxHarmonic2strips)[itrack];

		//trackMassPixel = TMath::Sqrt((trackDedxPixel-2.557)*TMath::Power((*tracks_P)[itrack],2)/2.579);
		//trackMassStrips = TMath::Sqrt((trackDedxStrips-2.557)*TMath::Power((*tracks_P)[itrack],2)/2.579);
		//trackMassPixel_calib = TMath::Sqrt((trackDedxPixel-3.01)*TMath::Power((*tracks_P)[itrack],2)/1.74);
		//trackMassStrips_calib = TMath::Sqrt((trackDedxStrips-3.01)*TMath::Power((*tracks_P)[itrack],2)/1.74);

		// Short track selection with inverted BDT
	        if ((*tracks_mva_bdt_loose)[itrack] < ((*tracks_dxyVtx)[itrack]*(0.5/0.01) - 0.3) && (*tracks_is_pixel_track)[itrack]==1)
	        {
		    n_DT_short++;
	            FillHisto(h_CR2_TrackP_pixel,(*tracks_P)[itrack],weight);
	            FillHisto(h_CR2_TrackPt_pixel,(*tracks_pt)[itrack],weight);
	            FillHisto(h_CR2_TrackDedx_pixel,(*tracks_deDxHarmonic2pixel)[itrack],weight);
	            //if (trackDedxPixel>2.557) FillHisto(h_CR2_TrackMass_pixel,TMath::Log10(trackMassPixel),weight);
		    //if (trackDedxPixel>3.01) FillHisto(h_CR2_TrackMass_pixel_calib,TMath::Log10(trackMassPixel_calib),weight);
		    
	        }

		// Long track selection with inverted BDT
		else if ((*tracks_mva_bdt_loose)[itrack] < ((*tracks_dxyVtx)[itrack]*(0.6/0.01) + 0.05) && (*tracks_is_pixel_track)[itrack]==0)
	        {
		    n_DT_long++;
	            FillHisto(h_CR2_TrackP_strips,(*tracks_P)[itrack],weight);
	            FillHisto(h_CR2_TrackPt_strips,(*tracks_pt)[itrack],weight);
	            FillHisto(h_CR2_TrackDedx_strips,(*tracks_deDxHarmonic2strips)[itrack],weight);
	            //if (trackDedxStrips>2.557) FillHisto(h_CR2_TrackMass_strips,TMath::Log10(trackMassStrips),weight);
		    //if (trackDedxStrips>3.01) FillHisto(h_CR2_TrackMass_strips_calib,TMath::Log10(trackMassStrips_calib),weight);
	        }
	    } // End of track loop
	    
	    n_DT = n_DT_short + n_DT_long;
	    if (n_DT==0 ) continue;
	    
	    FillHisto(h_CR2_MET,MET,weight);
	    FillHisto(h_CR2_MHT,MHT,weight);
	    FillHisto(h_CR2_HT,HT,weight);
	    FillHisto(h_CR2_n_jets,n_jets,weight);
	    FillHisto(h_CR2_n_btags,n_btags,weight);
	    FillHisto(h_CR2_n_leptons,n_leptons,weight);
	    FillHisto(h_CR2_n_DT,n_DT,weight);
	    FillHisto(h_CR2_n_DT_short,n_DT_short,weight);
	    FillHisto(h_CR2_n_DT_long,n_DT_long,weight);
	    
	} // End of CR2
*/	
    } // End of Event loop

    h_MET->Write();
    h_MHT->Write();
    h_HT->Write();
    h_n_jets->Write();
    h_n_btags->Write();
    h_n_leptons->Write();
    h_n_DT_short->Write();
    h_n_DT_long->Write();
    h_n_DT->Write();
    h_TrackP_pixel->Write();
    h_TrackP_pixel_chargino->Write();
    h_TrackP_pixel_GenMatch->Write();
    h_TrackPt_pixel->Write();
    h_TrackPt_pixel_chargino->Write();
    h_TrackPt_pixel_GenMatch->Write();
    h_TrackDedx_pixel->Write();
    h_TrackDedx_pixel_chargino->Write();
    h_TrackMass_pixel->Write();
    h_TrackMass_pixel_calib->Write();
    h_TrackMass_pixel_charginoMomentum->Write();
    h_TrackMass_pixel_GenMatch->Write();
    h_TrackP_strips->Write();
    h_TrackP_strips_chargino->Write();
    h_TrackP_strips_GenMatch->Write();
    h_TrackPt_strips->Write();
    h_TrackPt_strips_chargino->Write();
    h_TrackPt_strips_GenMatch->Write();
    h_TrackDedx_strips->Write();
    h_TrackDedx_strips_chargino->Write();
    h_TrackMass_strips->Write();
    h_TrackMass_strips_calib->Write();
    h_TrackMass_strips_charginoMomentum->Write();
    h_TrackMass_strips_GenMatch->Write();
    h_TrackMass_weightedPixelStripsMass->Write();
    h_Track_deltaR_with_chargino_pixel->Write();
    h_Track_deltaR_with_chargino_strips->Write();

    h_CR_noDT_MET->Write();
    h_CR_noDT_MHT->Write();
    h_CR_noDT_HT->Write();
    h_CR_noDT_n_jets->Write();
    h_CR_noDT_n_btags->Write();
    h_CR_noDT_n_leptons->Write();
    h_CR_noDT_n_DT->Write();
    h_CR_noDT_TrackP->Write();
    h_CR_noDT_TrackPt->Write();
    h_CR_noDT_TrackDedx_pixel->Write();
    h_CR_noDT_TrackDedx_strips->Write();
    
    h_CR1muon_MET->Write();
    h_CR1muon_MHT->Write();
    h_CR1muon_HT->Write();
    h_CR1muon_n_jets->Write();
    h_CR1muon_n_btags->Write();
    h_CR1muon_n_leptons->Write();
    h_CR1muon_TrackP_pixel->Write();
    h_CR1muon_TrackP_strips->Write();
    h_CR1muon_TrackPt_pixel->Write();
    h_CR1muon_TrackPt_strips->Write();
    h_CR1muon_TrackDedx_pixel->Write();
    h_CR1muon_TrackDedx_strips->Write();
    //h_CR1muon_TrackMass_pixel->Write();
    //h_CR1muon_TrackMass_pixel_calib->Write();
    //h_CR1muon_TrackMass_strips->Write();
    //h_CR1muon_TrackMass_strips_calib->Write();
    h_n_muon->Write();
    h_muonPt->Write();
    h_CR1muonPt->Write();
    h_muonEta->Write();
    h_muonPhi->Write();

    h_CR1electron_MET->Write();
    h_CR1electron_MHT->Write();
    h_CR1electron_HT->Write();
    h_CR1electron_n_jets->Write();
    h_CR1electron_n_btags->Write();
    h_CR1electron_n_leptons->Write();
    h_CR1electron_TrackP_pixel->Write();
    h_CR1electron_TrackP_strips->Write();
    h_CR1electron_TrackPt_pixel->Write();
    h_CR1electron_TrackPt_strips->Write();
    h_CR1electron_TrackDedx_pixel->Write();
    h_CR1electron_TrackDedx_strips->Write();
    //h_CR1electron_TrackMass_pixel->Write();
    //h_CR1electron_TrackMass_pixel_calib->Write();
    //h_CR1electron_TrackMass_strips->Write();
    //h_CR1electron_TrackMass_strips_calib->Write();
    h_n_electron->Write();
    h_electronPt->Write();
    h_CR1electronPt->Write();
    h_electronEta->Write();
    h_electronPhi->Write();
    
    h_CR2_MET->Write();
    h_CR2_MHT->Write();
    h_CR2_HT->Write();
    h_CR2_n_jets->Write();
    h_CR2_n_btags->Write();
    h_CR2_n_leptons->Write();
    h_CR2_n_DT->Write();
    h_CR2_n_DT_short->Write();
    h_CR2_n_DT_long->Write();
    h_CR2_TrackP_pixel->Write();
    h_CR2_TrackP_strips->Write();
    h_CR2_TrackPt_pixel->Write();
    h_CR2_TrackPt_strips->Write();
    h_CR2_TrackDedx_pixel->Write();
    h_CR2_TrackDedx_strips->Write();
    h_CR2_TrackMass_pixel->Write();
    h_CR2_TrackMass_pixel_calib->Write();
    h_CR2_TrackMass_strips_calib->Write();
    
    
    h2_TrackP_charginoP_pixel->Write();
    h2_MET_charginoPt_pixel->Write();
    h2_MET_TrackPt_pixel->Write();
    h2_METPhi_charginoPhi_pixel->Write();
    h2_METPhi_TrackPhi_pixel->Write();
    h2_TrackP_charginoP_strips->Write();
    h2_MET_charginoPt_strips->Write();
    h2_MET_TrackPt_strips->Write();
    h2_METPhi_charginoPhi_strips->Write();
    h2_METPhi_TrackPhi_strips->Write();
 
    // Canvas for 2D histogram
    TCanvas *c_trackP_charginoP_pixel = new TCanvas("h2_TrackP_charginoP_pixel","",800,600);
    h2_TrackP_charginoP_pixel->GetXaxis()->SetTitle("Track P");
    h2_TrackP_charginoP_pixel->GetYaxis()->SetTitle("Gen.Chi P");
    h2_TrackP_charginoP_pixel->Draw("COLZ");
    c_trackP_charginoP_pixel->Write();
    
    TCanvas *c_MET_charginoPt_pixel = new TCanvas("h2_MET_charginoPt_pixel","",800,600);
    h2_MET_charginoPt_pixel->GetXaxis()->SetTitle("MET");
    h2_MET_charginoPt_pixel->GetYaxis()->SetTitle("Gen.Chi Pt");
    h2_MET_charginoPt_pixel->Draw("COLZ");
    c_MET_charginoPt_pixel->Write();
    
    TCanvas *c_MET_TrackPt_pixel = new TCanvas("h2_MET_TrackPt_pixel","",800,600);
    h2_MET_TrackPt_pixel->GetXaxis()->SetTitle("MET");
    h2_MET_TrackPt_pixel->GetYaxis()->SetTitle("Track Pt");
    h2_MET_TrackPt_pixel->Draw("COLZ");
    c_MET_TrackPt_pixel->Write();

    TCanvas *c_METPhi_charginoPhi_pixel = new TCanvas("h2_METPhi_charginoPhi_pixel","",800,600);
    h2_METPhi_charginoPhi_pixel->GetXaxis()->SetTitle("METPhi");
    h2_METPhi_charginoPhi_pixel->GetYaxis()->SetTitle("Gen.Chi Phi");
    h2_METPhi_charginoPhi_pixel->Draw("COLZ");
    c_METPhi_charginoPhi_pixel->Write();
    
    TCanvas *c_METPhi_TrackPhi_pixel = new TCanvas("h2_METPhi_TrackPhi_pixel","",800,600);
    h2_METPhi_TrackPhi_pixel->GetXaxis()->SetTitle("METPhi");
    h2_METPhi_TrackPhi_pixel->GetYaxis()->SetTitle("Track Phi");
    h2_METPhi_TrackPhi_pixel->Draw("COLZ");
    c_METPhi_TrackPhi_pixel->Write();
    
    TCanvas *c_trackP_charginoP_strips = new TCanvas("h2_TrackP_charginoP_strips","",800,600);
    h2_TrackP_charginoP_strips->GetXaxis()->SetTitle("Track P");
    h2_TrackP_charginoP_strips->GetYaxis()->SetTitle("Gen.Chi P");
    h2_TrackP_charginoP_strips->Draw("COLZ");
    c_trackP_charginoP_strips->Write();
    
    TCanvas *c_MET_charginoPt_strips = new TCanvas("h2_MET_charginoPt_strips","",800,600);
    h2_MET_charginoPt_strips->GetXaxis()->SetTitle("MET");
    h2_MET_charginoPt_strips->GetYaxis()->SetTitle("Gen.Chi Pt");
    h2_MET_charginoPt_strips->Draw("COLZ");
    c_MET_charginoPt_strips->Write();
    
    TCanvas *c_MET_TrackPt_strips = new TCanvas("h2_MET_TrackPt_strips","",800,600);
    h2_MET_TrackPt_strips->GetXaxis()->SetTitle("MET");
    h2_MET_TrackPt_strips->GetYaxis()->SetTitle("Track Pt");
    h2_MET_TrackPt_strips->Draw("COLZ");
    c_MET_TrackPt_strips->Write();

    TCanvas *c_METPhi_charginoPhi_strips = new TCanvas("h2_METPhi_charginoPhi_strips","",800,600);
    h2_METPhi_charginoPhi_strips->GetXaxis()->SetTitle("METPhi");
    h2_METPhi_charginoPhi_strips->GetYaxis()->SetTitle("Gen.Chi Phi");
    h2_METPhi_charginoPhi_strips->Draw("COLZ");
    c_METPhi_charginoPhi_strips->Write();
    
    TCanvas *c_METPhi_TrackPhi_strips = new TCanvas("h2_METPhi_TrackPhi_strips","",800,600);
    h2_METPhi_TrackPhi_strips->GetXaxis()->SetTitle("METPhi");
    h2_METPhi_TrackPhi_strips->GetYaxis()->SetTitle("Track Phi");
    h2_METPhi_TrackPhi_strips->Draw("COLZ");
    c_METPhi_TrackPhi_strips->Write();

    //fout->Write();
    fout->Close();
}

int main(int argc, char** argv)
{
    return HistoMaker(argv[1], argv[2], argv[3], argv[4], argv[5]);
}
