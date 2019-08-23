#include <iostream>
#include <math.h>
#include <stdlib.h>
#include <fstream>
#include <iomanip>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include <algorithm>


double totLumi = 35.9;
TString inFileDir="rootFiles";
TFile* fBkg      = TFile::Open(inFileDir+"/allNminus1event25Nov.root");

//signal
TFile *fSig10       = TFile::Open(inFileDir+"/Scale_NmOneHists_event_g1800_chi1400_27_200970_10.root");
TFile *fSig30       = TFile::Open(inFileDir+"/Scale_NmOneHists_event_g1800_chi1400_27_200970_30.root");
TFile *fSig50       = TFile::Open(inFileDir+"/Scale_NmOneHists_event_g1800_chi1400_27_200970_50.root");
TFile *fSig100      = TFile::Open(inFileDir+"/Scale_NmOneHists_event_g1800_chi1400_27_200970_100.root");

//get normalised uncertainity
double getSysUnc(TH1F *hCentral, TH1F* hUp, TH1F* hDown){
  return 1 + max(fabs(hUp->Integral() - hCentral->Integral()), fabs(hCentral->Integral() - hDown->Integral()))/hCentral->Integral();
}

//get statistical uncertainity
double getStatUnc(TH1F* hCentral, double sError = 0.0){
  double  norm = hCentral->IntegralAndError(1, hCentral->GetNbinsX(), sError);
  double statUnc = (norm > 0) ? 1 + (fabs(sError)/norm) : 1.00;
  return statUnc;
}
//----------------------------------------//
//function to make data card for each mass
//----------------------------------------//
void makeOneDataCard(int mass=1400, TString label="mass1400"){
  cout<<" ======> mass point: "<<mass<<endl;
  //Bkg
  double sf_Bkg = 1;
  TH1F* hBkg = (TH1F*)fBkg->Get("BkginclusiveMET_all");

  //Data
  double sf_data = 1; 
  //TH1F* hData = fData->Get("DatainclusiveMET_all");

  //Signal
  double sf_sig = 1;
  TH1F* hSig10  =(TH1F*)fSig10->Get("SiginclusiveMET_all");
  TH1F* hSig30  =(TH1F*)fSig30->Get("SiginclusiveMET_all");
  TH1F* hSig50  =(TH1F*)fSig50->Get("SiginclusiveMET_all");
  TH1F* hSig100 =(TH1F*)fSig100->Get("SiginclusiveMET_all");
  TH1F* hSig = (TH1F*)hSig10->Clone("hSig");
  hSig->Reset();
  hSig->Add(hSig10);
  hSig->Add(hSig30);
  hSig->Add(hSig50);
  hSig->Add(hSig100);

  //open input template data card
  ifstream in;
  char* c = new char[1000];
  in.open("templateDataCard.log");
  //create output data card for 13 TeV
  string outDataCard = "datacard_13TeV_dissAppTrack_M%d.txt";
  ofstream out(Form(outDataCard.c_str(), mass));
  out.precision(8);

  out.precision(8);
  time_t secs=time(0);
  tm *t=localtime(&secs);
  while (in.good()){
    in.getline(c,1000,'\n');
    if (in.good()){
      string line(c);
      if(line.find("Date")!=string::npos){
        string day = string(Form("%d",t->tm_mday));
        string month = string(Form("%d",t->tm_mon+1));
        string year = string(Form("%d",t->tm_year+1900));
        line.replace( line.find("XXX") , 3 , day+"/"+month+"/"+year);
        out << line << endl;
      }
      else if(line.find("Description")!=string::npos){
        line.replace( line.find("YYY") , 3 , string(Form("%d", mass)) );
        line.replace( line.find("ZZZ") , 3 , string(Form("%f", totLumi)) );
        out << line << endl;
      }
      else if(line.find("Observation")!=string::npos){
        line.replace( line.find("XXX") , 3 , string(Form("%.0f", 0.0)));
        //line.replace( line.find("XXX") , 3 , string(Form("%.0f", hData->Integral())));
        out << line << endl;
      }
      else if(line.find("process")!=string::npos && line.find("Sig")!=string::npos){
        line.replace( line.find("YYY") , 3 , string(Form("%d", mass)) );
        out << line << endl;
      }
      else if(line.find("rate")!=string::npos){
        string rate = "rate               ";
        string space = "            ";
        out << rate ;
        out << space << hSig->Integral()
            << space << hBkg->Integral()
            << endl;
      }
      else if(line.find("CMS_stat_Sig")!=string::npos){
        line.replace( line.find("XXXX") , 4 , string(Form("%.2f", getStatUnc(hSig,  0))));
        out << line << endl;
      }
      else if(line.find("CMS_stat_Bkg")!=string::npos){
        line.replace( line.find("XXXX") , 4 , string(Form("%.2f", getStatUnc(hBkg,  0))));
        out << line << endl;
      }
     else if(line.find("CMS_scale_j")!=string::npos){
        float JESUnc_sig = 1.00;
        //float JESUnc_sig = (hSig->Integral() > 0) ? getSysUnc(hSig, hSig_JESUp, hSig_JESDown) : 1.00;
        line.replace( line.find("SSSS") , 4 , string(Form("%.3f", JESUnc_sig)) );

        float JESUnc_Bkg = 1.00;
        //float JESUnc_Bkg = (hBkg->Integral() > 0) ? getSysUnc(hBkg, hBkg_JESUp, hBkg_JESDown) : 1.00;
        line.replace( line.find("BBBB") , 4 , string(Form("%.3f", JESUnc_Bkg)) );
        out << line << endl;
      }
     else if(line.find("CMS_res_j")!=string::npos){
        float JERUnc_hSig = 1.00;
        //float JERUnc_hSig = (hSig->Integral() > 0) ? getSysUnc(hSig, hSig_JERUp, hSig_JERDown) : 1.00;
        line.replace( line.find("SSSS") , 4 , string(Form("%.3f", JERUnc_hSig)) );

        float JERUnc_Bkg = 1.00;
        //float JERUnc_Bkg = (hBkg->Integral() > 0) ? getSysUnc(hBkg, hBkg_JERUp, hBkg_JERDown) : 1.00;
        line.replace( line.find("BBBB") , 4 , string(Form("%.3f", JERUnc_Bkg)) );
        out << line << endl;
      }
      else{ //default without changes
        out << line << endl;
      }
    }
  }
  out.close();
  in.close();
}

//----------------------------------------//
//make data card for all masses
//----------------------------------------//
void makeDisAppTrackDataCard(){
  makeOneDataCard(1400,  "sig1400");
  //makeOneDataCard(1400,  "sig1400");
  //makeOneDataCard(1400,  "sig1400");
}

