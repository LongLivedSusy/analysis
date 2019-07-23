#include <iostream>
#include <string>
#include <fstream>
#include "TApplication.h"
#include "TH1D.h"
#include "TFile.h"
#include "TMath.h"
#include "TChain.h"
#include <vector>
#include "TLorentzVector.h"
#include "TBranch.h"
#include "TSystem.h"

using namespace std;

int HistoMaker(const char* inputfile, const char* outdir, const char* outputfile)
{
    cout << "Running HistoMaker" << endl;
    cout << "Input file list : " << inputfile << endl;
    cout << "Output Directory : " << outdir << endl;
    cout << "Output file : " << outputfile << endl;
    TChain *fChain = new TChain("Events");
    ifstream input(inputfile);
    string line;
    if (input.is_open()){
        while(getline(input,line)){
            cout << line << endl;
            fChain->Add(line.c_str());
        }
    }
    else return 0;
    input.close();

    fChain->SetBranchStatus("*",0);  // disable all branches
    fChain->SetBranchStatus("MET",1);  // activate branchname
    fChain->SetBranchStatus("MHT",1);  // activate branchname
    fChain->SetBranchStatus("HT",1);  // activate branchname
    fChain->SetBranchStatus("MinDeltaPhiMhtJets",1);  // activate branchname
    fChain->SetBranchStatus("CrossSection",1);  // activate branchname
    fChain->SetBranchStatus("puWeight",1);  // activate branchname
    fChain->SetBranchStatus("n_jets",1);  // activate branchname
    fChain->SetBranchStatus("n_btags",1);  // activate branchname
    fChain->SetBranchStatus("n_leptons",1);  // activate branchname
    fChain->SetBranchStatus("passesUniversalSelection",1);  // activate branchname
    fChain->SetBranchStatus("tracks",1);  // activate branchname
    fChain->SetBranchStatus("tracks_is_pixel_track",1);  // activate branchname
    fChain->SetBranchStatus("tracks_nValidPixelHits",1);  // activate branchname
    fChain->SetBranchStatus("tracks_nValidTrackerHits",1);  // activate branchname
    fChain->SetBranchStatus("tracks_is_baseline_track",1);  // activate branchname
    fChain->SetBranchStatus("tracks_pt",1);  // activate branchname
    fChain->SetBranchStatus("tracks_deDxHarmonic2pixel",1);  // activate branchname
    fChain->SetBranchStatus("tracks_deDxHarmonic2strips",1);  // activate branchname
    fChain->SetBranchStatus("tracks_deDxHarmonic2weighted",1);  // activate branchname
    fChain->SetBranchStatus("tracks_massfromdeDxPixel",1);  // activate branchname
    fChain->SetBranchStatus("tracks_massfromdeDxStrips",1);  // activate branchname
    fChain->SetBranchStatus("tracks_massfromdeDx_weightedDeDx",1);  // activate branchname
    fChain->SetBranchStatus("tracks_massfromdeDx_weightedPixelStripsMass",1);  // activate branchname
    fChain->SetBranchStatus("tracks_mva_bdt",1);  // activate branchname
    fChain->SetBranchStatus("tracks_mva_bdt_loose",1);  // activate branchname

    // Declaration of leaf types
    Float_t         MET;
    Float_t         MHT;
    Float_t         HT;
    Float_t         MinDeltaPhiMhtJets;
    Float_t         PFCaloMETRatio;
    Float_t         dilepton_invmass;
    Float_t         dilepton_pt1;
    Float_t         dilepton_pt2;
    Float_t         madHT;
    Float_t         CrossSection;
    Float_t         puWeight;
    Float_t         NumInteractions;
    Float_t         MHT_cleaned;
    Float_t         HT_cleaned;
    Float_t         MinDeltaPhiMhtJets_cleaned;
    Int_t           n_jets;
    Int_t           n_btags;
    Int_t           n_leptons;
    Int_t           n_allvertices;
    Int_t           n_NVtx;
    Int_t           EvtNumEven;
    Int_t           dilepton_CR;
    Int_t           qcd_CR;
    Int_t           qcd_sideband_CR;
    Int_t           dilepton_leptontype;
    Int_t           passesUniversalSelection;
    Int_t           n_genLeptons;
    Int_t           n_genElectrons;
    Int_t           n_genMuons;
    Int_t           n_genTaus;
    Int_t           n_jets_cleaned;
    Int_t           n_btags_cleaned;
    vector<int>     *region;
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
    //vector<int>     *tracks_nValidPixelHits;
    //vector<int>     *tracks_nValidTrackerHits;
    vector<int>     *tracks_fake;
    vector<int>     *tracks_prompt_electron;
    vector<int>     *tracks_prompt_muon;
    vector<int>     *tracks_prompt_tau;
    vector<int>     *tracks_prompt_tau_widecone;
    vector<int>     *tracks_prompt_tau_leadtrk;
    vector<int>     *tracks_passpionveto;
    vector<int>     *tracks_is_baseline_track;
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
    vector<double>  *tracks_pt;
    vector<double>  *tracks_P;
    vector<double>  *tracks_eta;
    vector<double>  *tracks_phi;
    vector<double>  *tracks_trkMiniRelIso;
    vector<double>  *tracks_trackJetIso;
    vector<double>  *tracks_ptError;
    vector<double>  *tracks_neutralPtSum;
    vector<double>  *tracks_neutralWithoutGammaPtSum;
    vector<double>  *tracks_minDrLepton;
    vector<double>  *tracks_matchedCaloEnergyJets;
    vector<double>  *tracks_deDxHarmonic2pixel;
    vector<double>  *tracks_deDxHarmonic2strips;
    vector<double>  *tracks_deDxHarmonic2weighted;
    vector<double>  *tracks_massfromdeDxPixel;
    vector<double>  *tracks_massfromdeDxStrips;
    vector<double>  *tracks_massfromdeDx_weightedDeDx;
    vector<double>  *tracks_massfromdeDx_weightedPixelStripsMass;
    vector<double>  *tracks_chi2perNdof;
    vector<double>  *tracks_chargedPtSum;
    vector<double>  *tracks_chiCandGenMatchingDR;
    vector<double>  *tracks_LabXYcm;
    vector<double>  *tracks_mva_bdt;
    vector<double>  *tracks_mva_bdt_loose;

    // List of branches
    TBranch        *b_MET;   //!
    TBranch        *b_MHT;   //!
    TBranch        *b_HT;   //!
    TBranch        *b_MinDeltaPhiMhtJets;   //!
    TBranch        *b_PFCaloMETRatio;   //!
    TBranch        *b_dilepton_invmass;   //!
    TBranch        *b_dilepton_pt1;   //!
    TBranch        *b_dilepton_pt2;   //!
    TBranch        *b_madHT;   //!
    TBranch        *b_CrossSection;   //!
    TBranch        *b_puWeight;   //!
    TBranch        *b_NumInteractions;   //!
    TBranch        *b_MHT_cleaned;   //!
    TBranch        *b_HT_cleaned;   //!
    TBranch        *b_MinDeltaPhiMhtJets_cleaned;   //!
    TBranch        *b_n_jets;   //!
    TBranch        *b_n_btags;   //!
    TBranch        *b_n_leptons;   //!
    TBranch        *b_n_allvertices;   //!
    TBranch        *b_n_NVtx;   //!
    TBranch        *b_EvtNumEven;   //!
    TBranch        *b_dilepton_CR;   //!
    TBranch        *b_qcd_CR;   //!
    TBranch        *b_qcd_sideband_CR;   //!
    TBranch        *b_dilepton_leptontype;   //!
    TBranch        *b_passesUniversalSelection;   //!
    TBranch        *b_n_genLeptons;   //!
    TBranch        *b_n_genElectrons;   //!
    TBranch        *b_n_genMuons;   //!
    TBranch        *b_n_genTaus;   //!
    TBranch        *b_n_jets_cleaned;   //!
    TBranch        *b_n_btags_cleaned;   //!
    TBranch        *b_region;   //!
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
    //TBranch        *b_tracks_nValidPixelHits;   //!
    //TBranch        *b_tracks_nValidTrackerHits;   //!
    TBranch        *b_tracks_fake;   //!
    TBranch        *b_tracks_prompt_electron;   //!
    TBranch        *b_tracks_prompt_muon;   //!
    TBranch        *b_tracks_prompt_tau;   //!
    TBranch        *b_tracks_prompt_tau_widecone;   //!
    TBranch        *b_tracks_prompt_tau_leadtrk;   //!
    TBranch        *b_tracks_passpionveto;   //!
    TBranch        *b_tracks_is_baseline_track;   //!
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
    TBranch        *b_tracks_pt;   //!
    TBranch        *b_tracks_P;   //!
    TBranch        *b_tracks_eta;   //!
    TBranch        *b_tracks_phi;   //!
    TBranch        *b_tracks_trkMiniRelIso;   //!
    TBranch        *b_tracks_trackJetIso;   //!
    TBranch        *b_tracks_ptError;   //!
    TBranch        *b_tracks_neutralPtSum;   //!
    TBranch        *b_tracks_neutralWithoutGammaPtSum;   //!
    TBranch        *b_tracks_minDrLepton;   //!
    TBranch        *b_tracks_matchedCaloEnergyJets;   //!
    TBranch        *b_tracks_deDxHarmonic2pixel;   //!
    TBranch        *b_tracks_deDxHarmonic2strips;   //!
    TBranch        *b_tracks_deDxHarmonic2weighted;   //!
    TBranch        *b_tracks_massfromdeDxPixel;   //!
    TBranch        *b_tracks_massfromdeDxStrips;   //!
    TBranch        *b_tracks_massfromdeDx_weightedDeDx;   //!
    TBranch        *b_tracks_massfromdeDx_weightedPixelStripsMass;   //!
    TBranch        *b_tracks_chi2perNdof;   //!
    TBranch        *b_tracks_chargedPtSum;   //!
    TBranch        *b_tracks_chiCandGenMatchingDR;   //!
    TBranch        *b_tracks_LabXYcm;   //!
    TBranch        *b_tracks_mva_bdt;   //!
    TBranch        *b_tracks_mva_bdt_loose;   //!

    cout << "Initialize variables at HistMaker" << endl;
    // Set object pointer
    region = 0;
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
    //tracks_nValidPixelHits = 0;
    //tracks_nValidTrackerHits = 0;
    tracks_fake = 0;
    tracks_prompt_electron = 0;
    tracks_prompt_muon = 0;
    tracks_prompt_tau = 0;
    tracks_prompt_tau_widecone = 0;
    tracks_prompt_tau_leadtrk = 0;
    tracks_passpionveto = 0;
    tracks_is_baseline_track = 0;
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
    tracks_pt = 0;
    tracks_P = 0;
    tracks_eta = 0;
    tracks_phi = 0;
    tracks_trkMiniRelIso = 0;
    tracks_trackJetIso = 0;
    tracks_ptError = 0;
    tracks_neutralPtSum = 0;
    tracks_neutralWithoutGammaPtSum = 0;
    tracks_minDrLepton = 0;
    tracks_matchedCaloEnergyJets = 0;
    tracks_deDxHarmonic2pixel = 0;
    tracks_deDxHarmonic2strips = 0;
    tracks_deDxHarmonic2weighted = 0;
    tracks_massfromdeDxPixel = 0;
    tracks_massfromdeDxStrips = 0;
    tracks_massfromdeDx_weightedDeDx = 0;
    tracks_massfromdeDx_weightedPixelStripsMass = 0;
    tracks_chi2perNdof = 0;
    tracks_chargedPtSum = 0;
    tracks_chiCandGenMatchingDR = 0;
    tracks_LabXYcm = 0;
    tracks_mva_bdt = 0;
    tracks_mva_bdt_loose = 0;
    
    // Set branch addresses and branch pointers
    fChain->SetMakeClass(1);

    fChain->SetBranchAddress("MET", &MET, &b_MET);
    fChain->SetBranchAddress("MHT", &MHT, &b_MHT);
    fChain->SetBranchAddress("HT", &HT, &b_HT);
    fChain->SetBranchAddress("MinDeltaPhiMhtJets", &MinDeltaPhiMhtJets, &b_MinDeltaPhiMhtJets);
    fChain->SetBranchAddress("PFCaloMETRatio", &PFCaloMETRatio, &b_PFCaloMETRatio);
    fChain->SetBranchAddress("dilepton_invmass", &dilepton_invmass, &b_dilepton_invmass);
    fChain->SetBranchAddress("dilepton_pt1", &dilepton_pt1, &b_dilepton_pt1);
    fChain->SetBranchAddress("dilepton_pt2", &dilepton_pt2, &b_dilepton_pt2);
    fChain->SetBranchAddress("madHT", &madHT, &b_madHT);
    fChain->SetBranchAddress("CrossSection", &CrossSection, &b_CrossSection);
    fChain->SetBranchAddress("puWeight", &puWeight, &b_puWeight);
    fChain->SetBranchAddress("NumInteractions", &NumInteractions, &b_NumInteractions);
    fChain->SetBranchAddress("MHT_cleaned", &MHT_cleaned, &b_MHT_cleaned);
    fChain->SetBranchAddress("HT_cleaned", &HT_cleaned, &b_HT_cleaned);
    fChain->SetBranchAddress("MinDeltaPhiMhtJets_cleaned", &MinDeltaPhiMhtJets_cleaned, &b_MinDeltaPhiMhtJets_cleaned);
    fChain->SetBranchAddress("n_jets", &n_jets, &b_n_jets);
    fChain->SetBranchAddress("n_btags", &n_btags, &b_n_btags);
    fChain->SetBranchAddress("n_leptons", &n_leptons, &b_n_leptons);
    fChain->SetBranchAddress("n_allvertices", &n_allvertices, &b_n_allvertices);
    fChain->SetBranchAddress("n_NVtx", &n_NVtx, &b_n_NVtx);
    fChain->SetBranchAddress("EvtNumEven", &EvtNumEven, &b_EvtNumEven);
    fChain->SetBranchAddress("dilepton_CR", &dilepton_CR, &b_dilepton_CR);
    fChain->SetBranchAddress("qcd_CR", &qcd_CR, &b_qcd_CR);
    fChain->SetBranchAddress("qcd_sideband_CR", &qcd_sideband_CR, &b_qcd_sideband_CR);
    fChain->SetBranchAddress("dilepton_leptontype", &dilepton_leptontype, &b_dilepton_leptontype);
    fChain->SetBranchAddress("passesUniversalSelection", &passesUniversalSelection, &b_passesUniversalSelection);
    fChain->SetBranchAddress("n_genLeptons", &n_genLeptons, &b_n_genLeptons);
    fChain->SetBranchAddress("n_genElectrons", &n_genElectrons, &b_n_genElectrons);
    fChain->SetBranchAddress("n_genMuons", &n_genMuons, &b_n_genMuons);
    fChain->SetBranchAddress("n_genTaus", &n_genTaus, &b_n_genTaus);
    fChain->SetBranchAddress("n_jets_cleaned", &n_jets_cleaned, &b_n_jets_cleaned);
    fChain->SetBranchAddress("n_btags_cleaned", &n_btags_cleaned, &b_n_btags_cleaned);
    fChain->SetBranchAddress("region", &region, &b_region);
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
//     fChain->SetBranchAddress("tracks_nValidPixelHits", &tracks_nValidPixelHits, &b_tracks_nValidPixelHits);
//     fChain->SetBranchAddress("tracks_nValidTrackerHits", &tracks_nValidTrackerHits, &b_tracks_nValidTrackerHits);
    fChain->SetBranchAddress("tracks_fake", &tracks_fake, &b_tracks_fake);
    fChain->SetBranchAddress("tracks_prompt_electron", &tracks_prompt_electron, &b_tracks_prompt_electron);
    fChain->SetBranchAddress("tracks_prompt_muon", &tracks_prompt_muon, &b_tracks_prompt_muon);
    fChain->SetBranchAddress("tracks_prompt_tau", &tracks_prompt_tau, &b_tracks_prompt_tau);
    fChain->SetBranchAddress("tracks_prompt_tau_widecone", &tracks_prompt_tau_widecone, &b_tracks_prompt_tau_widecone);
    fChain->SetBranchAddress("tracks_prompt_tau_leadtrk", &tracks_prompt_tau_leadtrk, &b_tracks_prompt_tau_leadtrk);
    fChain->SetBranchAddress("tracks_passpionveto", &tracks_passpionveto, &b_tracks_passpionveto);
    fChain->SetBranchAddress("tracks_is_baseline_track", &tracks_is_baseline_track, &b_tracks_is_baseline_track);
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
    fChain->SetBranchAddress("tracks_pt", &tracks_pt, &b_tracks_pt);
    fChain->SetBranchAddress("tracks_P", &tracks_P, &b_tracks_P);
    fChain->SetBranchAddress("tracks_eta", &tracks_eta, &b_tracks_eta);
    fChain->SetBranchAddress("tracks_phi", &tracks_phi, &b_tracks_phi);
    fChain->SetBranchAddress("tracks_trkMiniRelIso", &tracks_trkMiniRelIso, &b_tracks_trkMiniRelIso);
    fChain->SetBranchAddress("tracks_trackJetIso", &tracks_trackJetIso, &b_tracks_trackJetIso);
    fChain->SetBranchAddress("tracks_ptError", &tracks_ptError, &b_tracks_ptError);
    fChain->SetBranchAddress("tracks_neutralPtSum", &tracks_neutralPtSum, &b_tracks_neutralPtSum);
    fChain->SetBranchAddress("tracks_neutralWithoutGammaPtSum", &tracks_neutralWithoutGammaPtSum, &b_tracks_neutralWithoutGammaPtSum);
    fChain->SetBranchAddress("tracks_minDrLepton", &tracks_minDrLepton, &b_tracks_minDrLepton);
    fChain->SetBranchAddress("tracks_matchedCaloEnergyJets", &tracks_matchedCaloEnergyJets, &b_tracks_matchedCaloEnergyJets);
    fChain->SetBranchAddress("tracks_deDxHarmonic2pixel", &tracks_deDxHarmonic2pixel, &b_tracks_deDxHarmonic2pixel);
    fChain->SetBranchAddress("tracks_deDxHarmonic2strips", &tracks_deDxHarmonic2strips, &b_tracks_deDxHarmonic2strips);
    fChain->SetBranchAddress("tracks_deDxHarmonic2weighted", &tracks_deDxHarmonic2weighted, &b_tracks_deDxHarmonic2weighted);
    fChain->SetBranchAddress("tracks_massfromdeDxPixel", &tracks_massfromdeDxPixel, &b_tracks_massfromdeDxPixel);
    fChain->SetBranchAddress("tracks_massfromdeDxStrips", &tracks_massfromdeDxStrips, &b_tracks_massfromdeDxStrips);
    fChain->SetBranchAddress("tracks_massfromdeDx_weightedDeDx", &tracks_massfromdeDx_weightedDeDx, &b_tracks_massfromdeDx_weightedDeDx);
    fChain->SetBranchAddress("tracks_massfromdeDx_weightedPixelStripsMass", &tracks_massfromdeDx_weightedPixelStripsMass, &b_tracks_massfromdeDx_weightedPixelStripsMass);
    fChain->SetBranchAddress("tracks_chi2perNdof", &tracks_chi2perNdof, &b_tracks_chi2perNdof);
    fChain->SetBranchAddress("tracks_chargedPtSum", &tracks_chargedPtSum, &b_tracks_chargedPtSum);
    fChain->SetBranchAddress("tracks_chiCandGenMatchingDR", &tracks_chiCandGenMatchingDR, &b_tracks_chiCandGenMatchingDR);
    fChain->SetBranchAddress("tracks_LabXYcm", &tracks_LabXYcm, &b_tracks_LabXYcm);
    fChain->SetBranchAddress("tracks_mva_bdt", &tracks_mva_bdt, &b_tracks_mva_bdt);
    fChain->SetBranchAddress("tracks_mva_bdt_loose", &tracks_mva_bdt_loose, &b_tracks_mva_bdt_loose);
   
    // Histogram
    TH1::SetDefaultSumw2();
    TH1D* h_MET = new TH1D("MET","MET",100,0,1000);
    TH1D* h_MHT = new TH1D("MHT","MHT",100,0,1000);
    TH1D* h_HT = new TH1D("HT","HT",200,0,2000);
    TH1D* h_MinDeltaPhiMhtJets = new TH1D("dPhiMhtJets","dPhiMhtJets",100,0,1);
    TH1D* h_n_jets = new TH1D("n_jets","n_jets",20,0,20);
    TH1D* h_n_btags = new TH1D("n_btags","n_btags",10,0,10);
    TH1D* h_n_leptons = new TH1D("n_leptons","n_leptons",10,0,10);
    TH1D* h_n_DT = new TH1D("n_DT","n_DT",5,0,5);
    TH1D* h_TrackMass_short = new TH1D("TrackMass_short","Log10(TrackMass_short)",50,0,5.5);
    TH1D* h_TrackMass_long_strips = new TH1D("TrackMass_long_strips","Log10(TrackMass_long_strips)",50,0,5.5);
    TH1D* h_TrackMass_long_weightedPixelStripsMass = new TH1D("TrackMass_long_weightedPixelStripsMass","Log10(TrackMass_long_weightedPixelStripsMass)",50,0,5.5);

    cout << "Total entry : " << fChain->GetEntries() << endl;
    Long64_t nentries = fChain->GetEntries();
    Long64_t weight = 1;
    
    // Event loop start
    for (Long64_t ientry=0; ientry<nentries; ++ientry){
	if (ientry %10000 ==0) cout << ientry << "th event passing" << endl;

	fChain->GetEntry(ientry);
	weight = CrossSection * puWeight;
	
	// Event selection start
	if (passesUniversalSelection==0) continue;
	if (HT < 100) continue;
	if (MHT < 180) continue;
	if (n_jets == 0) continue;
	if (n_leptons != 0) continue;
	
	// track loop start 
	for (UInt_t itrack=0; itrack < tracks->size(); ++itrack){
	    if ((*tracks_pt)[itrack] < 30) continue;
	    if ((*tracks_mva_bdt)[itrack]>0.1 && (*tracks_is_pixel_track)[itrack]==1)
	    {
	        h_TrackMass_short->Fill(TMath::Log10((*tracks_massfromdeDxPixel)[itrack]),weight);
	    }
	    if ((*tracks_mva_bdt)[itrack]>0.25 && (*tracks_is_pixel_track)[itrack]==0)
	    {
	        h_TrackMass_long_strips->Fill(TMath::Log10((*tracks_massfromdeDxStrips)[itrack]),weight);
	        h_TrackMass_long_weightedPixelStripsMass->Fill(TMath::Log10((*tracks_massfromdeDx_weightedPixelStripsMass)[itrack]),weight);
	    }
	}
	
	h_MET->Fill(MET,weight);
	h_MHT->Fill(MHT,weight);
	h_HT->Fill(HT,weight);
	h_n_jets->Fill(n_jets,weight);
	h_n_btags->Fill(n_btags,weight);
	h_n_leptons->Fill(n_leptons,weight);
    }
    
    // Normalize 
    h_MET->Scale(1./nentries);
    h_MHT->Scale(1./nentries);
    h_HT->Scale(1./nentries);
    h_n_jets->Scale(1./nentries);
    h_n_btags->Scale(1./nentries);
    h_n_leptons->Scale(1./nentries);
    h_TrackMass_short->Scale(1./nentries);
    h_TrackMass_long_strips->Scale(1./nentries);
    h_TrackMass_long_weightedPixelStripsMass->Scale(1./nentries);

    
    // Save root file
    TFile* fout = new TFile(Form("./%s/%s",outdir,outputfile),"recreate");
    h_MET->Write();
    h_MHT->Write();
    h_HT->Write();
    h_n_jets->Write();
    h_n_btags->Write();
    h_n_leptons->Write();
    h_TrackMass_short->Write();
    h_TrackMass_long_strips->Write();
    h_TrackMass_long_weightedPixelStripsMass->Write();
    fout->Close();
}

int main(int argc, char** argv)
{
    return HistoMaker(argv[1], argv[2], argv[3]);
}
