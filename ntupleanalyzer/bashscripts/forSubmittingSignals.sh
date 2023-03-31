#to create a new round of predictions, first make a new empty directory structure:
cp -r /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/vEmpty /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v18
chmod -R 775 /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v18

#python tools/SubmitJobs_condor.py --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3*/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200*.root" --nfpj 10 --outdir bay_T1qqqqLL
#python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3*/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200*.root" --nfpj 10 --outdir bay_T2btLL
#python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/sbein/CommonSamples/RadiativeMu_2016Fast/ntuple_sidecar/higgsino94x_susyall_mChipm*.root" --nfpj 1 --outdir bay_PureHiggsino


python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3*/RunIIAutumn18FSv3.SMS-T2tb-LLChipm-ctau10to200*.root" --nfpj 10 --outdir bay_T2tbLLAutumn18
python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3*/RunIIAutumn18FSv3.SMS-T2bt-LLChipm-ctau10to200*.root" --nfpj 10 --outdir bay_T2btLLAutumn18
python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3*/RunIIAutumn18FSv3.SMS-T1btbt-LLChipm-ctau10to200*.root" --nfpj 10 --outdir bay_T1btbtLLAutumn18
python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/sbein/CommonSamples/RadiativeMu_2018Fast/ntuple_sidecarv3/higgsino_Autumn18_susyall_*.root" --nfpj 1 --outdir bay_PureHiggsinoAutumn18

python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3*/RunIIFall17FSv3.SMS-T2tb-LLChipm-ctau10to200*.root" --nfpj 10 --outdir bay_T2tbLLFall17
python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3*/RunIIFall17FSv3.SMS-T2bt-LLChipm-ctau10to200*.root" --nfpj 10 --outdir bay_T2btLLFall17
python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3*/RunIIFall17FSv3.SMS-T1btbt-LLChipm-ctau10to200*.root" --nfpj 10 --outdir bay_T1btbtLLFall17
python tools/SubmitJobs_condor.py  --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/sbein/CommonSamples/RadiativeMu_2017Fast/ntuple_sidecarv3/higgsino_Fall17_susyall_*.root" --nfpj 1 --outdir bay_PureHiggsinoFall17
##alternate thingies, like some systematic checks:
python tools/SubmitJobs_condor.py --analyzer tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3*/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200*.root" --nfpj 100 --doprefire True --outdir bay_T1_prefire

#the files will be transfered to the folder from "outdir"; once these finish, they can be merged into place using:
python tools/mergeAndMoveSignals.py "bay_T1btbtLLAutumn18/*.root" /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v18/Signal/T1btbtLLAutumn18/
python tools/mergeAndMoveSignals.py "bay_T2btLLAutumn18/*.root" /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v18/Signal/T2btLLAutumn18/
python tools/mergeAndMoveSignals.py "bay_T2tbLLAutumn18/*.root" /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v18/Signal/T2tbLLAutumn18

python tools/mergeAndMoveSignals.py "bay_T1btbtLLFall17/*.root" /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v18/Signal/T1btbtLLFall17/
python tools/mergeAndMoveSignals.py "bay_T2btLLFall17/*.root" /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v18/Signal/T2btLLFall17/
python tools/mergeAndMoveSignals.py "bay_T2tbLLFall17/*.root" /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v18/Signal/T2tbLLFall17/

