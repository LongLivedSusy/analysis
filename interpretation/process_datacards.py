#!/bin/env python
from ROOT import *
import os
import glob
from GridEngineTools import runParallel
gROOT.SetBatch(1)

# comments to viktor.kutzner@desy.de
# prepare histograms and datacards for combine tool. Histograms contain the prompt and fake background prediction as well as signal and data


def zero_out_certain_bins(histo, ignoreBins):
      
    for iBin in range(histo.GetNbinsX()+1):
        if iBin in ignoreBins:
            histo.SetBinContent(iBin, 0)
            histo.SetBinError(iBin, 0)
    return histo
    

def prepare_datacards(variable, combine_path, signals_path, prompt_bg_file, fake_bg_file, out_path, ignoreBins = []):

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
    bin                               ak     ak     ak     ak     ak
    process                          $LABEL   Electron     Muon     Pion     Fake
    process                            0             1          2        3        4
    ---------------------------------------------------------------------------
    rate                             $RATE0           $RATE1       $RATE2       $RATE3       $RATE4
    ---------------------------------------------------------------------------
    lumi_13TeV               lnN    1.027           1.027       1.027    1.027    1.027    Luminosity Error
    Sys                     shapeN2   1		        -	         -         -         -       Systematic error 
    Sys                     shapeN2   -             1            -         -         -       Systematic error
    Sys                     shapeN2   -             -            1         -         -       Systematic error
    Sys                     shapeN2   -             -            -         1         -       Systematic error
    Sys                     shapeN2   -             -            -         -         1       Systematic error
    * autoMCStats 0 1
    """

    run_combine = """#!/bin/bash
    cd $COMBINEDIR
    eval `scramv1 runtime -sh`
    cd -
    combine -M AsymptoticLimits $DATACARD --name $LABEL --noFitAsimov
    """

    os.system("mkdir -p %s" % out_path)
    os.system("rm %s/*root" % out_path)

    for i_signal_point, signal_point in enumerate(glob.glob(signals_path + "/*root")):

        #if i_signal_point>0: break

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
        h_signal = zero_out_certain_bins(h_signal, ignoreBins)
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
        h_electronbg = zero_out_certain_bins(h_electronbg, ignoreBins)
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
        h_muonbg = zero_out_certain_bins(h_muonbg, ignoreBins)
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
        h_pionbg = zero_out_certain_bins(h_pionbg, ignoreBins)
        h_pionbg.SetName("Pion")
        fin.Close()

        h_pionbg_up = h_signal.Clone()
        h_pionbg_up.SetDirectory(0)
        h_pionbg_up.SetName("Pion_SysUp")
        h_pionbg_down = h_signal.Clone()
        h_pionbg_down.SetDirectory(0)
        h_pionbg_down.SetName("Pion_SysDown")

        fin = TFile(fake_bg_file, "read")
        h_fakebg = fin.Get("hFkBaseline_%s" % variable)
        h_fakebg.SetDirectory(0)
        h_fakebg = zero_out_certain_bins(h_fakebg, ignoreBins)
        h_fakebg.SetName("Fake")
        fin.Close()

        h_fakebg_up = h_signal.Clone()
        h_fakebg_up.SetDirectory(0)
        h_fakebg_up.SetName("Fake_SysUp")
        h_fakebg_down = h_signal.Clone()
        h_fakebg_down.SetDirectory(0)
        h_fakebg_down.SetName("Fake_SysDown")

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
        fout = TFile("%s/%s" % (out_path, output_file_name), "recreate")
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
        h_fakebg.Write()
        h_fakebg_up.Write()
        h_fakebg_down.Write()
        h_obs.Write()
        h_obs_up.Write()
        h_obs_down.Write
        fout.Close()

        print "Writing datacard..."
        datacard = datacard_template
        datacard = datacard.replace("$OBS", str(h_obs.Integral()) )
        datacard = datacard.replace("$RATE0", str(h_signal.Integral()) )
        datacard = datacard.replace("$RATE1", str(h_electronbg.Integral()) )
        datacard = datacard.replace("$RATE2", str(h_muonbg.Integral()) )
        datacard = datacard.replace("$RATE3", str(h_pionbg.Integral()) )
        datacard = datacard.replace("$RATE4", str(h_fakebg.Integral()) )
        datacard = datacard.replace("$LABEL", "Signalg%s_chi%s" % (gluino_mass, lsp_mass) )
        datacard = datacard.replace("$ROOTFILE", output_file_name )

        datacard_file = "%s/%s" % (out_path, output_file_name.replace(".root", ".txt"))
        with open(datacard_file, "w") as datacard_fout:
            datacard_fout.write(datacard)

        print "Computing limit..."

        script_name = output_file_name.replace(".root", ".sh")

        shell_script = run_combine
        shell_script = shell_script.replace("$COMBINEDIR", combine_path)
        shell_script = shell_script.replace("$DATACARD", datacard_file.split("/")[-1])
        shell_script = shell_script.replace("$LABEL", "Signalg%s_chi%s" % (gluino_mass, lsp_mass))
        with open("%s/%s" % (out_path, script_name), "w") as shell_fout:
            shell_fout.write(shell_script)

        print "Point ok"


def run_limit_calculation(out_path):
    
    files = glob.glob(out_path + "/*.sh")
    commands = []
    
    for i_script_name, script_name in enumerate(files):
        script_name = script_name.split("/")[-1]
        cmd = "cd %s; chmod +x %s; ./%s" % (out_path, script_name, script_name)
        commands.append(cmd)
                    
    runParallel(commands, "grid", condorDir=out_path, confirm=False, babysit=False)
        

if __name__ == "__main__":

    combine_cmssw_path = "/afs/desy.de/user/k/kutznerv/cmssw/CMSSW_10_2_13/src/HiggsAnalysis"
    signals_path =       "../histograms/Piano/v2/Signal/T1qqqqLL"
    prompt_bg_file =     "../histograms/Piano/v2/Background/prompt-bg-results.root"
    fake_bg_file =       "../histograms/Piano/v2/Background/fake-bg-results.root"
    variable =           "BinNumberMethod"

    out_paths = {
                     "allbins": [],
                     "noleptons": range(49, 80+1) + range(85, 88+1),
                     "onlyleptons": range(0, 48+1) + range(81, 84+1),
                }

    for out_path in out_paths:

        signal = signals_path.split("/")[-1]

        prepare_datacards(variable, combine_cmssw_path, signals_path, prompt_bg_file, fake_bg_file, signal + "_" + out_path, ignoreBins = out_paths[out_path])
        print "Running combine for all points..."
        run_limit_calculation(signal + "_" + out_path)


