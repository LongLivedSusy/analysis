#!/bin/env python
from ROOT import *
import os
import glob
gROOT.SetBatch(1)

# comments to viktor.kutzner@desy.de
# prepare histograms for combine which contain the prompt and fake background prediction as well as signal and data

# ////////////////configure////////////////////////
combine_path = "/afs/desy.de/user/k/kutznerv/cmssw/CMSSW_10_2_13/src/HiggsAnalysis"
signals_path = "../histograms/signal/"
prompt_bg_file = "../histograms/background/prompt-bg-results.root"
variable = "BinNumberMethod"
# ////////////////configure////////////////////////


datacard_template = """
Date: 2019-08-31 
Description: Disappearing Tracks
---------------------------------------------------------------------------
imax   1  number of channels
jmax   *  number of backgrounds
kmax   *  number of nuisance parameters
---------------------------------------------------------------------------
shapes * * $ROOTFILE $PROCESS $PROCESS_$SYSTEMATIC
---------------------------------------------------------------------------
---------------------------------------------------------------------------
bin            ak
Observation    $OBS
---------------------------------------------------------------------------
bin                               ak     ak     ak     ak      
process                          $LABEL   Electron     Muon     Pion
process                            0             1          2        3
---------------------------------------------------------------------------
rate                             $RATE0           $RATE1       $RATE2       $RATE3
---------------------------------------------------------------------------
lumi_13TeV               lnN    1.027           1.027       1.027   1.027    Luminosity Error
Sys                     shapeN2   1		        -	         -        -       Systematic error 
Sys                     shapeN2   -             1            -        -       Systematic error
Sys                     shapeN2   -             -            1        -       Systematic error
Sys                     shapeN2   -             -            -        1       Systematic error
* autoMCStats 0 1
"""

run_combine = """#!/bin/bash
cd $COMBINEDIR
eval `scramv1 runtime -sh`
cd -
combine -M AsymptoticLimits $DATACARD --name $LABEL --noFitAsimov
"""


def get_integral(histo):

    integral = 0
    for iBin in range(histo.GetNbinsX()):
        value = histo.GetBinContent(iBin)
        width = histo.GetBinWidth(iBin)
        integral += value * width
    return integral


def merge_histograms(variable, signals_path, prompt_bg_file):

    os.system("rm ../histograms/combined/*root")

    for signal_point in glob.glob(signals_path + "/*root"):

        try:
            gluino_mass = int( signal_point.split("Glu")[-1].split("_Chi1ne")[0] )
            lsp_mass = int( signal_point.split("_Chi1ne")[-1].split("_Chi")[0].replace(".root", "") )
        except:
            gluino_mass = int( signal_point.split("Glu")[-1].split("_Chi1pm")[0] )
            lsp_mass = int( signal_point.split("_Chi1pm")[-1].split("_Chi")[0].replace(".root", "") )

        print "Merging histograms..."
        print "Processing", signal_point, gluino_mass, lsp_mass

        fin = TFile(signal_point, "read")
        h_signal = fin.Get("hBaseline_%s" % variable.replace("Method", "Truth"))
        h_signal.SetDirectory(0)
        h_signal.SetName("Signalg%s_chi%s" % (gluino_mass, lsp_mass) )
        fin.Close()

        h_signal_up = h_signal.Clone()
        h_signal_up.SetDirectory(0)
        h_signal_up.SetName("Signalg%s_chi%s_SysUp" % (gluino_mass, lsp_mass) )
        h_signal_down = h_signal.Clone()
        h_signal_down.SetDirectory(0)
        h_signal_down.SetName("Signalg%s_chi%s_SysDown" % (gluino_mass, lsp_mass) )

        fin = TFile(prompt_bg_file, "read")
        h_electronbg = fin.Get("hElBaseline_%s" % variable)
        h_electronbg.SetDirectory(0)
        h_electronbg.SetName("Electron")
        fin.Close()

        h_electronbg_up = h_signal.Clone()
        h_electronbg_up.SetDirectory(0)
        h_electronbg_up.SetName("Electron_SysUp")
        h_electronbg_down = h_signal.Clone()
        h_electronbg_down.SetDirectory(0)
        h_electronbg_down.SetName("Electron_SysDown")
        
        fin = TFile(prompt_bg_file, "read")
        h_muonbg = fin.Get("hMuBaseline_%s" % variable)
        h_muonbg.SetDirectory(0)
        h_muonbg.SetName("Muon")
        fin.Close()

        h_muonbg_up = h_signal.Clone()
        h_muonbg_up.SetDirectory(0)
        h_muonbg_up.SetName("Muon_SysUp")
        h_muonbg_down = h_signal.Clone()
        h_muonbg_down.SetDirectory(0)
        h_muonbg_down.SetName("Muon_SysDown")

        fin = TFile(prompt_bg_file, "read")
        h_pionbg = fin.Get("hPiBaseline_%s" % variable)
        h_pionbg.SetDirectory(0)
        h_pionbg.SetName("Pion")
        fin.Close()

        h_pionbg_up = h_signal.Clone()
        h_pionbg_up.SetDirectory(0)
        h_pionbg_up.SetName("Pion_SysUp")
        h_pionbg_down = h_signal.Clone()
        h_pionbg_down.SetDirectory(0)
        h_pionbg_down.SetName("Pion_SysDown")

        # write some bogus data:
        h_obs = h_signal.Clone()
        h_obs.SetDirectory(0)
        h_obs.SetName("data_obs")
        h_obs_up = h_signal.Clone()
        h_obs_up.SetDirectory(0)
        h_obs_up.SetName("data_obs_SysUp")
        h_obs_down = h_signal.Clone()
        h_obs_down.SetDirectory(0)
        h_obs_down.SetName("data_obs_SysDown")

        output_file_name = signal_point.split("/")[-1]
        fout = TFile("../histograms/combined/%s" % output_file_name, "recreate")
        h_signal.Write()
        h_signal_up.Write()
        h_signal_down.Write()
        h_electronbg.Write()
        h_electronbg_up.Write()
        h_electronbg_down.Write()
        h_muonbg.Write()
        h_muonbg_up.Write()
        h_muonbg_down.Write()
        h_pionbg.Write()
        h_pionbg_up.Write()
        h_pionbg_down.Write()
        h_obs.Write()
        h_obs_up.Write()
        h_obs_down.Write
        fout.Close()

        print "Writing datacard..."
        datacard = datacard_template
        datacard = datacard.replace("$OBS", str(get_integral(h_obs)) )
        datacard = datacard.replace("$RATE0", str(get_integral(h_signal)) )
        datacard = datacard.replace("$RATE1", str(get_integral(h_electronbg)) )
        datacard = datacard.replace("$RATE2", str(get_integral(h_muonbg)) )
        datacard = datacard.replace("$RATE3", str(get_integral(h_pionbg)) )
        datacard = datacard.replace("$LABEL", "Signalg%s_chi%s" % (gluino_mass, lsp_mass) )
        datacard = datacard.replace("$ROOTFILE", output_file_name )

        datacard_file = "../histograms/combined/%s" % output_file_name.replace(".root", ".txt")
        with open(datacard_file, "w") as datacard_fout:
            datacard_fout.write(datacard)

        print "Computing limit..."

        shell_script = run_combine
        shell_script = shell_script.replace("$COMBINEDIR", combine_path)
        shell_script = shell_script.replace("$DATACARD", datacard_file.split("/")[-1])
        shell_script = shell_script.replace("$LABEL", "Signalg%s_chi%s" % (gluino_mass, lsp_mass))
        with open("../histograms/combined/run_combine.sh", "w") as shell_fout:
            shell_fout.write(shell_script)

        os.system("cd ../histograms/combined/; chmod +x run_combine.sh; ./run_combine.sh")

        break

merge_histograms(variable, signals_path, prompt_bg_file)



