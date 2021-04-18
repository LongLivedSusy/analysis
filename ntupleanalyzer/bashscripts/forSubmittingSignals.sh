#to create a new round of predictions, first make a new empty directory structure:
cp -r /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/vEmpty /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v8


python tools/SubmitJobs_condor.py --analyzer tools/TheAnalyzer_systematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200*.root" --nfpj 50 --outdir bay_T1
python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzer_systematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200*.root" --nfpj 50 --outdir bay_T2tt
python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzer_systematics.py --fnamekeyword "/nfs/dust/cms/user/beinsam/CommonSamples/MC_BSM/CompressedHiggsino/RadiativeMu_2016Fast/ntuple_sidecar/higgsino94x_susyall_mChipm*.root" --nfpj 1 --outdir bay_PurHiggsino


#the files will be transfered to the folder from "outdir"; once these finish, they can be merged into place using:
python tools/mergeAndMoveSignals.py "bay_T1/*.root" /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v7/Signal/T1qqqqLL/
python tools/mergeAndMoveSignals.py "bay_T2tt/*.root" /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v7/Signal/T2btLL/
python tools/mergeAndMoveSignals.py "bay_PureHiggsino/*.root" /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v7/Signal/PureHiggsino

