#!/bin/env python
from __future__ import division
import glob
from ROOT import *
from CfgUtils import readSamplesConfig
import treeplotter
import numpy as np
import multiprocessing

def do_plots(path = "./output", config = "../cfg/samples_cmssw8_all.cfg"):

    plot_config = {
        "zmass": {"binw": 2, "xmin": 75, "xmax": 107, "ymin": 1e5, "xlabel": "m_{Z} (GeV)", "logx": False, "logy": True},
                  }
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = "PFCaloMETRatio<5 && lepton_type==11", suffix="_PFCaloMETRatio_ll", ignore_samples="Run201")
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = "PFCaloMETRatio<5 && lepton_type==11", suffix="_PFCaloMETRatio_ee", ignore_samples="Run201")
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = "PFCaloMETRatio<5 && lepton_type==13", suffix="_PFCaloMETRatio_mumu", ignore_samples="Run201")

    plot_config = {
        "n_allvertices": {"binw": 5, "xmin": 0, "xmax": 50, "xlabel": "n_{vertex}", "logx": False, "logy": True},
                  }
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = "PFCaloMETRatio<5 && n_DT>0", suffix="_PFCaloMETRatio_withDT", ignore_samples="Run201")

    plot_config = {
        "HT": {"binw": 25, "xmin": 0, "xmax": 1000, "xlabel": "HT (GeV)", "logx": False, "logy": True},
        "MHT": {"binw": 25, "xmin": 0, "xmax": 1000, "xlabel": "MHT (GeV)", "logx": False, "logy": True},
        "MinDeltaPhiMhtJets": {"binw": 0.1, "xmin": 0, "xmax": 3, "xlabel": "MinDeltaPhiMhtJets", "logx": False, "logy": True},
        "n_jets": {"binw": 1, "xmin": 0, "xmax": 15, "xlabel": "n_{jets}", "logx": False, "logy": True},
                  }
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = "PFCaloMETRatio<5 && MHT>250", suffix="_PFCaloMETRatio_MHT", ignore_samples="Run201")

    plot_config = {
        "HT_cleaned": {"binw": 25, "xmin": 0, "xmax": 1000, "xlabel": "cleaned HT (GeV)", "logx": False, "logy": True},
        "MHT_cleaned": {"binw": 25, "xmin": 0, "xmax": 1000, "xlabel": "cleaned MHT (GeV)", "logx": False, "logy": True},
        "MinDeltaPhiMhtJets_cleaned": {"binw": 0.1, "xmin": 0, "xmax": 3, "xlabel": "cleaned MinDeltaPhiMhtJets", "logx": False, "logy": True},
        "n_jets_cleaned": {"binw": 1, "xmin": 0, "xmax": 15, "xlabel": "cleaned n_{jets}", "logx": False, "logy": True},
                  }
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = "PFCaloMETRatio<5 && MHT_cleaned>250", suffix="_PFCaloMETRatio_MHT", ignore_samples="Run201")

    plot_config = {
        "pass_sr_cleaned": {"binw": 1, "xmin": 0, "xmax": 12, "xlabel": "inclusive control region", "logx": False, "logy": True},
        "zmass": {"binw": 1, "xmin": 70, "xmax": 110, "ymin": 1e5, "xlabel": "m_{Z} (GeV)", "logx": False, "logy": True},
        "n_jets": {"binw": 1, "xmin": 0, "xmax": 15, "xlabel": "n_{jets}", "logx": False, "logy": True},
                  }
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = "PFCaloMETRatio<5", suffix="_PFCaloMETRatio", ignore_samples="Run201")


    plot_config = {
        "MET": {"binw": 25, "xmin": 0, "xmax": 1000, "xlabel": "MET (GeV)", "logx": False, "logy": True},
        "HT": {"binw": 25, "xmin": 0, "xmax": 1000, "xlabel": "HT (GeV)", "logx": False, "logy": True},
        "MHT": {"binw": 25, "xmin": 0, "xmax": 1000, "xlabel": "MHT (GeV)", "logx": False, "logy": True},
        "n_DT": {"binw": 1, "xmin": 0, "xmax": 3, "xlabel": "n_{DT}", "logx": False, "logy": True},
        "n_DT_no_genparticle_in_track_cone": {"binw": 1, "xmin": 0, "xmax": 3, "xlabel": "n_{DT, true}", "logx": False, "logy": True},
        "MinDeltaPhiMhtJets": {"binw": 0.1, "xmin": 0, "xmax": 3, "xlabel": "MinDeltaPhiMhtJets", "logx": False, "logy": True},
        "n_jets": {"binw": 1, "xmin": 0, "xmax": 15, "xlabel": "n_{jets}", "logx": False, "logy": True},
        "n_allvertices": {"binw": 1, "xmin": 0, "xmax": 75, "xlabel": "n_{vertex}", "logx": False, "logy": True},
                  }
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = "pass_sr_cleaned>0 && PFCaloMETRatio<5", suffix="_PFCaloMETRatio_sr", ignore_samples="Run201")


def get_filenames(tree_folder, configuration_file):

    samples = readSamplesConfig(configuration_file)

    for file_name in glob.glob(tree_folder + "/*.root"):

        for sample in samples:

            sample_name = sample.replace("_RA2AnalysisTree", "")

            if "filenames" not in samples[sample]:
                samples[sample]["filenames"] = []
            if sample_name in file_name:
                samples[sample]["filenames"].append(file_name)
                break

    for sample in samples.keys():
        if sample != "global" and len(samples[sample]["filenames"]) == 0:
            #print "No files found for sample, ignoring:", sample
            del samples[sample]

    return samples


def get_weighted_count(variable, cutstring, path="./output_tautrack", config="../cfg/samples_cmssw8_all.cfg"):

    samples = get_filenames(path, config)

    histograms = {}

    weighted_counts = {"total": 0}

    for sample in samples.keys():
     
        if sample == "global": continue
        if len(samples[sample]["filenames"]) == 0: continue            

        contents = treeplotter.get_histogram_from_file(samples[sample]["filenames"], "Events", variable, cutstring=cutstring)
        count = contents[0].GetEntries()
        nev = contents[1]
        xsec = samples[sample]["xsec"]
        lumi = samples["global"]["lumi"]
        weighted_count = count * lumi * xsec / nev
        weighted_counts[sample] = weighted_count
        if samples[sample]["type"] == "b":
            weighted_counts["total"] += weighted_count

    return weighted_counts


def plot_fakerate_binned(variable, xmin, xmax, binw, file_name, data, xlabel, cutstring, extra_text, ratioplot, decorrelate_events):

    #def fakerate_binned(variable, xmin, xmax, binw, cutstring = "", sample_label = "total"):
    #    if sample_label == "total": return ( [5,15,25,35,45], [0.5,0.1,0.2,0.4,0.04], [0.4,0.2,0.1,0.35,0.04] )
    #    else: return ( [5,15,25,35,45], [0.05,0.01,0.02,0.04,0.04], [0.04,0.02,0.01,0.035,0.04] )
    #def fakerate_binnedX(variable, xmin, xmax, binw, cutstring = "", sample_label = "total"):

    yaxis_limits = [1, 0]

    def fakerate_binned(variable, xmin, xmax, binw, cutstring = "", sample_label = "total", is_data = False):

        xvals = []
        yvals_fakerate = []
        yvals_fakerateGen = []

        if len(cutstring) > 0:
            cutstring = cutstring + " && "

        for min_variable, max_variable in zip(np.arange(xmin, xmax, binw), np.arange(xmin+binw, xmax+binw, binw)):

            base_cuts = cutstring + "%s>=%s && %s<%s" % (variable, min_variable, variable, max_variable)

            if decorrelate_events and not is_data:
                nom = get_weighted_count("n_DT", base_cuts + " && EvtNumEven==0 && n_DT>0")[sample_label]
                denom = get_weighted_count("n_DT", base_cuts + " && EvtNumEven==0")[sample_label]
                nomGen = get_weighted_count("n_DT_no_genparticle_in_track_cone", base_cuts + " && EvtNumEven==1 && n_DT>0 && gen_track_cone_taucorrected==-1000")[sample_label]
                denomGen = get_weighted_count("n_DT", base_cuts + " && EvtNumEven==1")[sample_label]
            else:        
                nom = get_weighted_count("n_DT", base_cuts + " && n_DT>0")[sample_label]
                denom = get_weighted_count("n_DT", base_cuts)[sample_label]
                if not is_data:
                    nomGen = get_weighted_count("n_DT", base_cuts + " && n_DT>0 && gen_track_cone_taucorrected==-1000")[sample_label]
                else:
                    nomGen = nom
                denomGen = denom

            if denom > 0:
                fakerate = nom / denom
            else:
                fakerate = 0.0

            if denomGen > 0:
                fakerateGen = nomGen / denomGen
            else:
                fakerateGen = 0.0

            xvals.append(min_variable)
            yvals_fakerate.append(fakerate)
            yvals_fakerateGen.append(fakerateGen)

            if min(fakerate, fakerateGen) < yaxis_limits[0] and min(fakerate, fakerateGen) != 0:
                yaxis_limits[0] = min(fakerate, fakerateGen)
            if max(fakerate, fakerateGen) > yaxis_limits[1]:
                yaxis_limits[1] = max(fakerate, fakerateGen)

            print sample_label, variable, min_variable, "-->", max_variable, "FR =", fakerate, "FR (gen) =", fakerateGen

        return xvals, yvals_fakerate, yvals_fakerateGen

    xvals, yvals, yvals_gen = fakerate_binned(variable, xmin, xmax, binw, cutstring = cutstring, sample_label = "total")
    if data:
        xvals, yvals_data, yvals_data_ignore = fakerate_binned(variable, xmin, xmax, binw, cutstring = cutstring, sample_label = "Run2016C-03Feb2017-v1.Single_RA2AnalysisTree", is_data=True)

    canvas = TCanvas("fakerate", "fakerate", 800, 800)
    l = canvas.GetLeftMargin()
    t = canvas.GetTopMargin()
    r = canvas.GetRightMargin()
    b = canvas.GetBottomMargin()
    canvas.SetTopMargin(0.4*t)
    canvas.SetBottomMargin(1.2*b)
    canvas.SetLeftMargin(1.5*l)
    canvas.SetRightMargin(0.3*r)
    canvas.cd()
    if not ratioplot:       
        canvas.SetLogy()


    if ratioplot:
        # init padding and go to top pad:
        pad1 = TPad("pad1", "pad1", 0, 0.2, 1, 1.0)
        pad1.SetRightMargin(0.05)
        pad1.SetLogy(True)
        pad2 = TPad("pad2", "pad2", 0.0, 0.025, 1.0, 0.27)
        pad2.SetBottomMargin(0.4)
        pad2.SetRightMargin(0.05)
        pad1.Draw()
        pad2.Draw()
        pad1.cd()
        pad1.SetLogy()

    gr = {}

    gr[variable] = TH1F("fakes", "fakes", int(xmax/binw), xmin, xmax)
    gr[variable+"Gen"] = TH1F("fakesGen", "fakesGen", int(xmax/binw), xmin, xmax)
    if data: gr[variable+"Data"] = TH1F("fakesData", "fakesData", int(xmax/binw), xmin, xmax)
    legend = TLegend(0.55, 0.85, 0.98, 0.98)
    legend.SetTextSize(0.03)

    for i in range(len(xvals)):
        gr[variable].Fill(xvals[i], abs(yvals[i]))
        gr[variable+"Gen"].Fill(xvals[i], abs(yvals_gen[i]))
        if data: gr[variable+"Data"].Fill(xvals[i], abs(yvals_data[i]))
    if ratioplot:
        gr[variable].SetTitle(";;fake rate")
    else:
        if xlabel:
            gr[variable].SetTitle(";%s;fake rate" % xlabel)
        else:
            gr[variable].SetTitle(";%s;fake rate" % variable)

    print "Using ranges:", yaxis_limits
    gr[variable].GetYaxis().SetRangeUser(yaxis_limits[0]/10.0, yaxis_limits[1]*10.0)

    gr[variable].Draw("hist")
    gr[variable+"Gen"].Draw("same hist")
    if data: gr[variable+"Data"].Draw("same hist")

    if ratioplot:
        gr[variable].GetXaxis().SetLabelSize(0)
        gr[variable].GetYaxis().SetTitleOffset(1.0)

    legend.AddEntry(gr[variable], "fake rate (MC)")
    legend.AddEntry(gr[variable+"Gen"], "fake rate (MC + GenInfo)")
    if data: legend.AddEntry(gr[variable+"Data"], "fake rate (Run 2016C)")
    legend.Draw()

    #gr[variable].SetMarkerStyle(5)
    gr[variable].SetLineColor(kGreen)
    gr[variable].SetLineWidth(2)
    #gr[variable+"Gen"].SetMarkerStyle(20)
    gr[variable+"Gen"].SetLineColor(kRed)
    gr[variable+"Gen"].SetLineStyle(2)
    #gr[variable+"Gen"].SetMarkerColor(kRed)
    gr[variable+"Gen"].SetLineWidth(2)
    
    if data: 
        #gr[variable+"Data"].SetMarkerStyle(20)
        #gr[variable+"Data"].SetMarkerColor(kBlack)
        gr[variable+"Data"].SetLineColor(kBlack)
        gr[variable+"Data"].SetLineWidth(2)

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.05)
    latex.SetTextAlign(11)
    #latex.DrawLatex(0.15, 0.85, "event selection:")
    #latex.DrawLatex(0.15, 0.80, extra_text)

    # bottom pad:
    if ratioplot:
        pad2.cd()

        ratio = gr[variable].Clone()
        ratio.Divide(gr[variable+"Gen"])
        ratio.SetLineColor(kBlack)
        ratio.SetMarkerStyle(20)
        ratio.Draw("hist p")

        if xlabel:
            ratio.SetTitle(";%s;ratio" % xlabel)
        else:
            ratio.SetTitle(";%s;ratio" % variable)
        ratio.GetXaxis().SetTitleSize(0.12)
        ratio.GetYaxis().SetTitleSize(0.12)
        ratio.GetYaxis().SetTitleOffset(0.35)
        ratio.GetYaxis().SetRangeUser(0.5,1.5)
        ratio.GetYaxis().SetNdivisions(4)
        ratio.GetXaxis().SetLabelSize(0.12)
        ratio.GetYaxis().SetLabelSize(0.12)
        pad2.SetGridx(True)
        pad2.SetGridy(True)

    canvas.SaveAs(file_name)
    canvas.SaveAs(file_name.replace(".pdf", ".root"))


def multi_wrapper(args):

    if args[0] == "plot_fakerate_binned":
        plot_fakerate_binned(args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10], args[11])

    if args[0] == "do_plots":
        do_plots()

if __name__ == "__main__":

    pool = multiprocessing.Pool(int(multiprocessing.cpu_count()*0.55))
    parameters = []

    #do_plots()
    #plot_fakerate_binned("HT_cleaned", 0, 1500, 100, "fakerate_HT.pdf", extra_text="m_{inv}(Z#rightarrow ll)=91 #pm 10 GeV, p_{T}(l)>30 GeV, PFCaloMETRatio<5", cutstring="PFCaloMETRatio<5")
    #plot_fakerate_binned("MHT_cleaned", 0, 1100, 100, "fakerate_MHT.pdf", extra_text="m_{inv}(Z#rightarrow ll)=91 #pm 10 GeV, p_{T}(l)>30 GeV, PFCaloMETRatio<5", cutstring="PFCaloMETRatio<5")
    #plot_fakerate_binned("n_jets_cleaned", 0, 11, 1, "fakerate_njets.pdf", extra_text="m_{inv}(Z#rightarrow ll)=91 #pm 10 GeV, p_{T}(l)>30 GeV, PFCaloMETRatio<5", cutstring="PFCaloMETRatio<5")
    #plot_fakerate_binned("MinDeltaPhiMhtJets_cleaned", 0, 3, 0.2, "fakerate_MinDeltaPhiMhtJets.pdf", extra_text="m_{inv}(Z#rightarrow ll)=91 #pm 10 GeV, p_{T}(l)>30 GeV, PFCaloMETRatio<5", cutstring="PFCaloMETRatio<5")
    #plot_fakerate_binned("n_allvertices", 0, 50, 5, "fakerate_allvertices.pdf", extra_text="m_{inv}(Z#rightarrow ll)=91 #pm 10 GeV, p_{T}(l)>30 GeV, PFCaloMETRatio<5", cutstring="PFCaloMETRatio<5")
   
    #parameters.append(["do_plots"])
    parameters.append(["plot_fakerate_binned", "n_allvertices", 5, 40, 5, "fakerate_allvertices_ll.pdf", True, "number of vertices", "PFCaloMETRatio<5", "", False, True])
    parameters.append(["plot_fakerate_binned", "n_allvertices", 0, 40, 5, "fakerate_allvertices_ee.pdf", True, "number of vertices", "PFCaloMETRatio<5 && lepton_type==11", "", False, True])
    parameters.append(["plot_fakerate_binned", "n_allvertices", 0, 40, 5, "fakerate_allvertices_mumu.pdf", True, "number of vertices", "PFCaloMETRatio<5 && lepton_type==13", "", False, True])
    parameters.append(["plot_fakerate_binned", "HT_cleaned", 0, 800, 100, "fakerate_HT.pdf", True, "cleaned H_{T}", "PFCaloMETRatio<5", "", False, True])
    parameters.append(["plot_fakerate_binned", "MHT_cleaned", 0, 1100, 100, "fakerate_MHT.pdf", True, "cleaned missing H_{T}", "PFCaloMETRatio<5", "", False, True])
    parameters.append(["plot_fakerate_binned", "n_jets_cleaned", 0, 6, 1, "fakerate_njets.pdf", True, "cleaned n_{jets}", "PFCaloMETRatio<5", "", False, True])
    parameters.append(["plot_fakerate_binned", "MinDeltaPhiMhtJets_cleaned", 0, 3, 0.2, "fakerate_MinDeltaPhiMhtJets.pdf", True, "cleaned min #Delta #phi (MH_{T}, jets)", "PFCaloMETRatio<5", "", False, True])
    parameters.append(["plot_fakerate_binned", "pass_sr_cleaned", 0, 11, 1, "pass_sr_cleaned.pdf", False, "inclusive signal region", "PFCaloMETRatio<5", "", False, True])
    
    pool.map(multi_wrapper, parameters)     

    # alt:

    #print "Events with DT:"
    #plot_config = {"n_DT": {"binw": 1, "xmin": 0, "xmax": 3, "xlabel": "n_{DT}", "logx": False, "logy": True}}
    #treeplotter.loop_over_files("./output", "../cfg/samples_cmssw8_all.cfg", plot_config, tree_folder_name="Events", cutstring = "pass_sr_cleaned>0 && PFCaloMETRatio<5", suffix="_sr", debug=True)

    #plot_config = {"n_allvertices": {"binw": 1, "xmin": 0, "xmax": 50, "xlabel": "n_{vertex}", "logx": False, "logy": True}}
    #treeplotter.loop_over_files("./output", "../cfg/samples_cmssw8_all.cfg", plot_config, tree_folder_name="Events", cutstring = "pass_sr_cleaned>0 && PFCaloMETRatio<5", suffix="_test", debug=True, ignore_samples="Run201")

    #plot_fakerate_binned("pass_sr_cleaned", 0, 4, 1, "datasr.root", extra_text="m_{inv}(Z#rightarrow ll)=91 #pm 10 GeV, p_{T}(l)>30 GeV, PFCaloMETRatio<5", cutstring="PFCaloMETRatio<5")
    #plot_fakerate_binned("n_allvertices", 0, 50, 5, "n_allvertices_data.pdf", extra_text="m_{inv}(Z#rightarrow ll)=91 #pm 10 GeV, p_{T}(l)>30 GeV, PFCaloMETRatio<5", cutstring="PFCaloMETRatio<5")
    #plot_fakerate_binned("n_allvertices", 0, 10, 5, "test.pdf", xlabel="number of vertices", extra_text="m_{inv}(Z#rightarrow ll)=91 #pm 10 GeV, p_{T}(l)>30 GeV, PFCaloMETRatio<5", cutstring="PFCaloMETRatio<5", data=True)

    plot_config = {
        "n_DT":                                 {"binw": 1, "xmin": 0, "xmax": 3, "xlabel": "n_{DT}", "logx": False, "logy": True},
                  }
    treeplotter.loop_over_files("./output_tautrack", "../cfg/samples_cmssw8_all.cfg", plot_config, folder="plots_tautrack", tree_folder_name="Events", cutstring="PFCaloMETRatio<5", suffix="", ignore_samples="Run201")
    
    plot_config = {
        "n_DT_no_genparticle_in_track_cone":    {"binw": 1, "xmin": 0, "xmax": 3, "xlabel": "n_{DT}", "logx": False, "logy": True},
                  }
    treeplotter.loop_over_files("./output_tautrack", "../cfg/samples_cmssw8_all.cfg", plot_config, folder="plots_tautrack", tree_folder_name="Events", cutstring="PFCaloMETRatio<5 && gen_track_cone_genstatus==1 && gen_track_cone_taucorrected>-1000", suffix="", ignore_samples="Run201")
        
    plot_config = {
        "gen_track_cone_pdgid":                 {"binw": 1, "xmin": -50, "xmax": 50, "xlabel": "generator particle PDG ID", "logx": False, "logy": True},
        "gen_track_cone_parent":                {"binw": 1, "xmin": -50, "xmax": 50, "xlabel": "generator particle PDG ID", "logx": False, "logy": True},
        "gen_track_cone_taucorrected":          {"binw": 1, "xmin": -50, "xmax": 50, "xlabel": "generator particle PDG ID", "logx": False, "logy": True},
        "gen_track_cone_genstatus":             {"binw": 1, "xmin": -50, "xmax": 50, "xlabel": "generator particle PDG ID", "logx": False, "logy": True},
                  }
    treeplotter.loop_over_files("./output_tautrack", "../cfg/samples_cmssw8_all.cfg", plot_config, folder="plots_tautrack", tree_folder_name="Events", cutstring="PFCaloMETRatio<5 && n_DT>0", suffix="_dt", ignore_samples="Run201")
    
