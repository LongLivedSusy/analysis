import commands

# init your VOMS proxy, then run script.
# -Viktor

def collect_info(samples, dataformat = "MINIAODSIM", campaign = "RunIISummer16", check_parent_for_AOD = False):

    samples_status = {}
    stats = {"available": 0, "not available": 0}

    for sample in sorted(samples):

        samples_status[sample] = {}

        print sample
        print "************************************"

        if check_parent_for_AOD:

            cmd = 'dasgoclient --query="dataset=/%s/%s/MINIAODSIM"' % (sample, campaign)
            status, text = commands.getstatusoutput(cmd)

            for i_text in text.split():
                if "MINIAODSIM" in i_text:
                    
                    cmd = 'dasgoclient --query="parent dataset=%s"' % (i_text)
                    status, text = commands.getstatusoutput(cmd)
                    break        

            if len(text) == 0:               
                print "Couldn't get parent (AOD) dataset..."

            for i_text in text.split():
                if "AODSIM" in i_text:

                    cmd = 'dasgoclient --query="dataset=%s"' % (i_text)
                    status, text = commands.getstatusoutput(cmd)
                    print text

                    cmd = 'dasgoclient --query="site dataset=%s"' % (i_text)
                    status, text = commands.getstatusoutput(cmd)

        else:

            cmd = 'dasgoclient --query="dataset=/%s/%s/%s"' % (sample, campaign, dataformat)
            status, text = commands.getstatusoutput(cmd)
            print text

            cmd = 'dasgoclient --query="site dataset=/%s/%s/%s"' % (sample, campaign, dataformat)
            status, text = commands.getstatusoutput(cmd)

        print text + "\n"

        samples_status[sample]["dasoutput"] = text

        if "error" in text or "No site records found in PhEDEx" in text:

            samples_status[sample]["available"] = False
            stats["not available"] += 1

        else:

            sites = []

            for i_text in text.split():
                if "MSS" in i_text or "Buffer" in i_text:
                    continue
                if "T1_" in i_text or "T2_" in i_text or "T3_" in i_text:
                    sites.append(i_text)

            if len(sites) > 0:

                samples_status[sample]["available"] = True
                samples_status[sample]["sites"] = " ".join(sites)
                stats["available"] += 1

            else:

                samples_status[sample]["available"] = False

    print "Summary (%s):" % dataformat
    print "%s out of %s samples available" % (stats["available"], len(samples_status))
    
    if stats["not available"] > 0:
        print "Not available or no information:"

    for sample in samples_status:
        if not samples_status[sample]["available"]:
            print "/%s/%s/%s" % (sample, campaign, dataformat)

    return samples_status, stats



if __name__ == "__main__":

    print "@@ Summer16 campaign @@"
    cmssw8_samples = [
                        "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "ZJetsToNuNu_HT-100To200_13TeV-madgraph",
                        "ZJetsToNuNu_HT-200To400_13TeV-madgraph",
                        "ZJetsToNuNu_HT-400To600_13TeV-madgraph",
                        "ZJetsToNuNu_HT-600To800_13TeV-madgraph",
                        "ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
                        "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
                        "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
                        "WW_TuneCUETP8M1_13TeV-pythia8",
                        "ZZ_TuneCUETP8M1_13TeV-pythia8",
                        "WZ_TuneCUETP8M1_13TeV-pythia8",
                        "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
    ]

    collect_info(cmssw8_samples, campaign="RunIISummer*", dataformat = "MINIAODSIM")
    collect_info(cmssw8_samples, campaign="RunIISummer*", dataformat = "AODSIM")


    print "@@ Apr2018 campaign @@"
    cmssw10_samples = [
                       "WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8",
                       "TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",               # other HT-binned TTJets samples missing...
                       "ZJetsToNuNu_HT-100To200_13TeV-madgraph",
                       "ZJetsToNuNu_HT-200To400_13TeV-madgraph",
                       "ZJetsToNuNu_HT-400To600_13TeV-madgraph",
                       "ZJetsToNuNu_HT-600To800_13TeV-madgraph",
                       "ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
                       "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
                       "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
                       "WW_TuneCP5_13TeV-pythia8",
                       "ZZ_TuneCP5_13TeV-pythia8",
                       "WZ_TuneCP5_13TeV-pythia8",
                       "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",
                       "DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8"
                      ]

    #collect_info(cmssw10_samples, campaign="*Apr2018*", dataformat = "MINIAODSIM")
    #collect_info(cmssw10_samples, campaign="*Apr2018*", dataformat = "AODSIM", check_parent_for_AOD = True)
