#!/usr/bin/env python

folder = './output_mediumchunks/'

dict_Run2016_SingleMuon = {
		    'Run2016B':folder+'/Run2016B-SingleMuon.root',
		    'Run2016C':folder+'/Run2016C-SingleMuon.root',
	       	    'Run2016D':folder+'/Run2016D-SingleMuon.root',
               	    'Run2016E':folder+'/Run2016E-SingleMuon.root',
               	    'Run2016F':folder+'/Run2016F-SingleMuon.root',
               	    'Run2016G':folder+'/Run2016G-SingleMuon.root',
               	    'Run2016H':folder+'/Run2016H-SingleMuon.root',
		    }
dict_Run2017_SingleMuon = {
		    'Run2017B':folder+'/Run2017B-SingleMuon.root',
		    'Run2017C':folder+'/Run2017C-SingleMuon.root',
	       	    'Run2017D':folder+'/Run2017D-SingleMuon.root',
               	    'Run2017E':folder+'/Run2017E-SingleMuon.root',
               	    'Run2017F':folder+'/Run2017F-SingleMuon.root',
		    }
dict_Run2018_SingleMuon = {
		    'Run2018A':folder+'/Run2018A-SingleMuon.root',
		    'Run2018B':folder+'/Run2018B-SingleMuon.root',
		    'Run2018C':folder+'/Run2018C-SingleMuon.root',
	       	    'Run2018D':folder+'/Run2018D-SingleMuon.root',
		    }

dict_Summer16 = {
	'WJetsToLNu_TuneCUETP8M1':folder+'/Summer16.WJetsToLNu_TuneCUETP8M1.root',
	'WJetsToLNu_HT-100To200':folder+'/Summer16.WJetsToLNu_HT-100To200.root',
	'WJetsToLNu_HT-200To400':folder+'/Summer16.WJetsToLNu_HT-200To400.root',
	'WJetsToLNu_HT-400To600':folder+'/Summer16.WJetsToLNu_HT-400To600.root',
	'WJetsToLNu_HT-600To800':folder+'/Summer16.WJetsToLNu_HT-600To800.root',
	'WJetsToLNu_HT-800To1200':folder+'/Summer16.WJetsToLNu_HT-800To1200.root',
	'WJetsToLNu_HT-1200To2500':folder+'/Summer16.WJetsToLNu_HT-1200To2500.root',
	'WJetsToLNu_HT-2500ToInf':folder+'/Summer16.WJetsToLNu_HT-2500ToInf.root',
	'DYJetsToLL_M-50_TuneCUETP8M1':folder+'/Summer16.DYJetsToLL_M-50_TuneCUETP8M1.root',
	'DYJetsToLL_M-50_HT-100to200':folder+'/Summer16.DYJetsToLL_M-50_HT-100to200.root',
	'DYJetsToLL_M-50_HT-200to400':folder+'/Summer16.DYJetsToLL_M-50_HT-200to400.root',
	'DYJetsToLL_M-50_HT-400to600':folder+'/Summer16.DYJetsToLL_M-50_HT-400to600.root',
	'DYJetsToLL_M-50_HT-600to800':folder+'/Summer16.DYJetsToLL_M-50_HT-600to800.root',
	'DYJetsToLL_M-50_HT-800to1200':folder+'/Summer16.DYJetsToLL_M-50_HT-800to1200.root',
	'DYJetsToLL_M-50_HT-1200to2500':folder+'/Summer16.DYJetsToLL_M-50_HT-1200to2500.root',
	'DYJetsToLL_M-50_HT-2500toInf':folder+'/Summer16.DYJetsToLL_M-50_HT-2500toInf.root',
	'QCD_HT200to300':folder+'/Summer16.QCD_HT200to300.root',
	'QCD_HT300to500':folder+'/Summer16.QCD_HT300to500.root',
	'QCD_HT500to700':folder+'/Summer16.QCD_HT500to700.root',
	'QCD_HT700to1000':folder+'/Summer16.QCD_HT700to1000.root',
	'QCD_HT1000to1500':folder+'/Summer16.QCD_HT1000to1500.root',
	'QCD_HT1500to2000':folder+'/Summer16.QCD_HT1500to2000.root',
	'QCD_HT2000toInf':folder+'/Summer16.QCD_HT2000toInf.root',
	'TTJets':folder+'/Summer16.TTJets_TuneCUETP8M1.root',
	'ZJetsToNuNu_HT-100To200':folder+'/Summer16.ZJetsToNuNu_HT-100To200.root',
	'ZJetsToNuNu_HT-200To400':folder+'/Summer16.ZJetsToNuNu_HT-200To400.root',
	'ZJetsToNuNu_HT-400To600':folder+'/Summer16.ZJetsToNuNu_HT-400To600.root',
	'ZJetsToNuNu_HT-600To800':folder+'/Summer16.ZJetsToNuNu_HT-600To800.root',
	'ZJetsToNuNu_HT-800To1200':folder+'/Summer16.ZJetsToNuNu_HT-800To1200.root',
	'ZJetsToNuNu_HT-1200To2500':folder+'/Summer16.ZJetsToNuNu_HT-1200To2500.root',
	'ZJetsToNuNu_HT-2500ToInf':folder+'/Summer16.ZJetsToNuNu_HT-2500ToInf.root',
	'WW':folder+'/Summer16.WW_TuneCUETP8M1.root',
	'WZ':folder+'/Summer16.WZ_TuneCUETP8M1.root',
	'ZZ':folder+'/Summer16.ZZ_TuneCUETP8M1.root',
	'WWZ':folder+'/Summer16.WWZ_TuneCUETP8M1.root',
	'WZZ':folder+'/Summer16.WZZ_TuneCUETP8M1.root',
	'ZZZ':folder+'/Summer16.ZZZ_TuneCUETP8M1.root',
	}

dict_Summer16_FullSimSignal = {
        'Summer16FullSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900':'./output_chargino/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.root',
        }

dict_Summer16_PrivateFastSimSignal = {
	'Summer16FastSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900':folder+'/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.root',
	}

dict_Fall17 = {
	'WJetsToLNu_HT-100To200':folder+'/RunIIFall17MiniAODv2.WJetsToLNu_HT-100To200.root',
	'WJetsToLNu_HT-200To400':folder+'/RunIIFall17MiniAODv2.WJetsToLNu_HT-200To400.root',
	'WJetsToLNu_HT-400To600':folder+'/RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600.root',
	'WJetsToLNu_HT-600To800':folder+'/RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800.root',
	'WJetsToLNu_HT-800To1200':folder+'/RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200.root',
	'WJetsToLNu_HT-1200To2500':folder+'/RunIIFall17MiniAODv2.WJetsToLNu_HT-1200To2500.root',
	'WJetsToLNu_HT-2500ToInf':folder+'/RunIIFall17MiniAODv2.WJetsToLNu_HT-2500ToInf.root',
	'DYJetsToLL_M-50_TuneCUETP8M1':folder+'/RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5.root',
	'DYJetsToLL_M-50_HT-100to200':folder+'/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-100to200.root',
	'DYJetsToLL_M-50_HT-200to400':folder+'/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400.root',
	'DYJetsToLL_M-50_HT-400to600':folder+'/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-400to600.root',
	'DYJetsToLL_M-50_HT-600to800':folder+'/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-600to800.root',
	'DYJetsToLL_M-50_HT-800to1200':folder+'/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-800to1200.root',
	'DYJetsToLL_M-50_HT-1200to2500':folder+'/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-1200to2500.root',
	'DYJetsToLL_M-50_HT-2500toInf':folder+'/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-2500toInf.root',
	'QCD_HT200to300':folder+'/RunIIFall17MiniAODv2.QCD_HT200to300.root',
	'QCD_HT300to500':folder+'/RunIIFall17MiniAODv2.QCD_HT300to500.root',
	'QCD_HT500to700':folder+'/RunIIFall17MiniAODv2.QCD_HT500to700.root',
	'QCD_HT700to1000':folder+'/RunIIFall17MiniAODv2.QCD_HT700to1000.root',
	'QCD_HT1000to1500':folder+'/RunIIFall17MiniAODv2.QCD_HT1000to1500.root',
	'QCD_HT1500to2000':folder+'/RunIIFall17MiniAODv2.QCD_HT1500to2000.root',
	'QCD_HT2000toInf':folder+'/RunIIFall17MiniAODv2.QCD_HT2000toInf.root',
	'TTJets_TuneCP5':folder+'/RunIIFall17MiniAODv2.TTJets_TuneCP5.root',
	'TTJets_HT-600to800':folder+'/RunIIFall17MiniAODv2.TTJets_HT-600to800.root',
	'TTJets_HT-800to1200':folder+'/RunIIFall17MiniAODv2.TTJets_HT-800to1200.root',
	'TTJets_HT-1200to2500':folder+'/RunIIFall17MiniAODv2.TTJets_HT-1200to2500.root',
	'TTJets_HT-2500toInf':folder+'/RunIIFall17MiniAODv2.TTJets_HT-2500toInf.root',
	'WWTo1L1Nu2Q':folder+'/RunIIFall17MiniAODv2.WWTo1L1Nu2Q.root',
	'WZTo1L1Nu2Q':folder+'/RunIIFall17MiniAODv2.WZTo1L1Nu2Q.root',
	'ZZTo2L2Q':folder+'/RunIIFall17MiniAODv2.ZZTo2L2Q.root',
	'ZJetsToNuNu_HT-100To200':folder+'/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200.root',
	'ZJetsToNuNu_HT-200To400':folder+'/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400.root',
	'ZJetsToNuNu_HT-400To600':folder+'/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600.root',
	'ZJetsToNuNu_HT-600To800':folder+'/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-600To800.root',
	'ZJetsToNuNu_HT-800To1200':folder+'/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200.root',
	'ZJetsToNuNu_HT-1200To2500':folder+'/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-1200To2500.root',
	'ZJetsToNuNu_HT-2500ToInf':folder+'/RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf.root',
	}

