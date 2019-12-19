import collections
import re

def convert_cut_string(cut, increment_variable = "i", input_variables = False):

    # this function converts ROOT cutstrings into python eval statements.
    # if you give the variable values in a input_variables dictionary, the statement is evaluated to a boolean

    output = cut
    variables = re.findall(r'\w+', cut)
    for variable in list(set(variables)):

        try:
            float(variable)
        except:

            if not input_variables:
                output = output.replace(variable, "event." + variable + "[" + increment_variable + "]")
            else:
                output = output.replace(variable, str(input_variables[variable]))

    output = output.replace("&&", " and ").replace("||", " or ")

    if output.split()[0] == "and":
        output = " ".join(output.split()[1:])

    if not input_variables:
        return output
    else:
        return eval(output)


tags = collections.OrderedDict()
    
#good_track = " && tracks_is_reco_lepton==0 && tracks_passPFCandVeto==1 && tracks_passpionveto==1 && tracks_passmask!=0 "
good_track = " && tracks_is_reco_lepton==0 && tracks_passPFCandVeto==1 "
base_cuts = " && passesUniversalSelection==1 " + good_track

#tags["tight_short"] = {
#                            "base_cuts": "passesUniversalSelection==1",
#                            "SR": good_track + " && tracks_is_pixel_track==1 && tracks_mva_bdt>0.1 ",
#                            "CR": " ",
#                          }
#tags["tight_long"] = {
#                            "base_cuts": "passesUniversalSelection==1",
#                            "SR": good_track + " && tracks_is_pixel_track==0 && tracks_mva_bdt>0.25 ",
#                            "CR": " ",
#                          }
#tags["loose1_short"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>0 && tracks_dxyVtx<=0.01",
#                            "CR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>0 && tracks_dxyVtx>0.01",
#                          }
#tags["loose1_long"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>0 && tracks_dxyVtx<=0.01",
#                            "CR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>0 && tracks_dxyVtx>0.01",
#                          }
#tags["loose2_short"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>0 && tracks_dxyVtx<=0.01",
#                            "CR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>0 && tracks_dxyVtx>0.02 && tracks_dxyVtx<0.1",
#                          }
#tags["loose2_long"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>0 && tracks_dxyVtx<=0.01",
#                            "CR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>0 && tracks_dxyVtx>0.02 && tracks_dxyVtx<0.1",
#                          }
#tags["loose3_short"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>tracks_dxyVtx*0.5/0.01",
#                            "CR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose<tracks_dxyVtx*0.5/0.01",
#                          }
#tags["loose3_long"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>tracks_dxyVtx*0.5/0.01",
#                            "CR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose<tracks_dxyVtx*0.5/0.01",
#                          }
#tags["loose4_short"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.7/0.01) - 0.1)",
#                            "CR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.7/0.01) - 0.1)",
#                          }
#tags["loose4_long"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.7/0.01) + 0.15)",
#                            "CR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.7/0.01) + 0.15)",
#                          }
#tags["loose3_short"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>tracks_dxyVtx*0.5/0.01",
#                            "CR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose<tracks_dxyVtx*0.5/0.01",
#                          }
#tags["loose3_long"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>tracks_dxyVtx*0.5/0.01",
#                            "CR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose<tracks_dxyVtx*0.5/0.01",
#                          }
#tags["loose4_short"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.7/0.01) - 0.1)",
#                            "CR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.7/0.01) - 0.1)",
#                          }
#tags["loose4_long"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.7/0.01) + 0.15)",
#                            "CR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.7/0.01) + 0.15)",
#                          }
#tags["loose5_short"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.5/0.01) - 0.3)",
#                            "CR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.5/0.01) - 0.3)",
#                          }
#tags["loose5_long"] = {
#                            "base_cuts": "passesUniversalSelection==1" + good_track,
#                            "SR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.6/0.01) + 0.05)",
#                            "CR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.6/0.01) + 0.05)",
#                          }
#tags["loose6_short"] = {
#                            "base_cuts": base_cuts,
#                            "SR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.65/0.01) - 0.25)",
#                            "CR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.65/0.01) - 0.25)",
#                       }
#tags["loose6_long"] = {
#                            "base_cuts": base_cuts,
#                            "SR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.7/0.01) + 0.05)",
#                            "CR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.7/0.01) + 0.05)",
#                       }
#tags["loose7_short"] = {
#                            "base_cuts": base_cuts,
#                            "SR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.65/0.01) - 0.25)",
#                            "CR": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.65/0.01) - 0.5)",
#                       }
#tags["loose7_long"] = {
#                            "base_cuts": base_cuts,
#                            "SR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.7/0.01) + 0.05)",
#                            "CR": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.7/0.01) - 0.5)",
#                       }
tags["loose8"] = {
                   "SR_short": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.65/0.01) - 0.25) && tracks_trkRelIso<0.01",
                   "CR_short": " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_dxyVtx>0.02",
                   "SR_long": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.7/0.01) + 0.05) && tracks_trkRelIso<0.01",
                   "CR_long": " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.7/0.01) - 0.5) && tracks_dxyVtx>0.02",
                 }


if __name__ == "__main__":

    print "Test"
    input_variables = {"tracks_is_pixel_track": 1, "tracks_mva_bdt_loose": 0.5, "tracks_dxyVtx": 0.001, "tracks_trkRelIso": 11110.00001}
    print convert_cut_string(tags["loose8"]["SR_short"], increment_variable = "i", input_variables = input_variables)

