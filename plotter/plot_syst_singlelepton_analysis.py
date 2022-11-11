#!/usr/bin/env python3
import ROOT
ROOT.gROOT.SetBatch(True)

import os
import sys
import math
import argparse

from include.args_parser import args

import configs.singlelepton_analysis.root_configs
from configs.singlelepton_analysis.hist_configs import hist_configs  
from configs.singlelepton_analysis.sample_configs import sample_configs
from configs.singlelepton_analysis.region_configs import region_configs
from configs.singlelepton_analysis.systematic_configs import systematic_configs

flag_analyzer = "singlelepton_analysis"
flag_skim = "SkimTree_SingleLepton"

flag_campaign = args.campaign
flag_channel = args.channel
flag_debug = args.debug
flag_write = args.write
flag_no_signal = args.no_signal
flag_no_data = args.no_data

hists = list(hist_configs)
systs = list(systematic_configs)

if not os.path.exists(f"outputs/yields/{flag_campaign}"):
    os.system(f"mkdir -p outputs/yields/{flag_campaign}")

if not os.path.exists(f"outputs/hists/{flag_campaign}"):
    os.system(f"mkdir -p outputs/hists/{flag_campaign}")

def get_systematics(region):

    data_root_files, signal_root_files, background_root_files = check_root_files()

    for hist in hists:

        flag_write = args.write

        hist_null = None

        hist_name = f"{region}_{hist}"
        if flag_write:
            outfile = ROOT.TFile.Open(f"outputs/yields/{flag_campaign}/{hist_name}.root", "RECREATE")
        else:
            outfile = None

        try:
            hist_data = get_added_hist(data_root_files, region, "CENTRAL" , hist_name, "data")["data"]
            hist_null = get_null_hist(get_added_hist(data_root_files, region, "CENTRAL" , hist_name, "data")["data"].Clone())
        except:
            print ("nothing written in data, skipping")
            continue
        canvas, canvas_up, canvas_down = get_canvas(hist_name)

        hist_background_categories = get_added_hist(background_root_files, region, "CENTRAL", hist_name, "background")
        hist_backgrounds = get_histograms(background_root_files, "background", region, hist_name, hist_background_categories, outfile, flag_write, hist_null)

        hist_signal_categories = get_added_hist(signal_root_files, region, "CENTRAL", hist_name, "signal")
        hist_signals = get_histograms(signal_root_files, "signal", region, hist_name, hist_signal_categories, outfile, flag_write, hist_null)

        stack_background = ROOT.THStack()
        hist_ratio_numerator = None
        hist_ratio_denominator = None

        for category in list(hist_backgrounds.keys()):
            hist_background = hist_backgrounds[category]

            if hist_ratio_denominator == None:
                hist_ratio_denominator = hist_background.Clone()
            else:
                hist_ratio_denominator.Add(hist_background)
            stack_background.Add(hist_background.Clone())

        canvas_up.cd()

        if hist_ratio_denominator == None: continue
        stack_background.Draw("hist")
        stack_background.GetXaxis().SetLabelSize(0)
        dress_histograms(stack_background, hist, canvas_up, canvas_down, "up")

        for category in list(hist_signals.keys()):
            hist_signal = hist_signals[category]
            if ("800GeV" in category):
                hist_signal.Draw("samehist")
                hist_signal.GetXaxis().SetLabelSize(0)

        if (True):#hist_configs[hist]["data"]):
            if flag_write:
                outfile.cd()
                hist_data.Write("data")
                hist_data.GetXaxis().SetLabelSize(0)
                ROOT.gROOT.cd()
            hist_data.Draw("samehistP")
            hist_ratio_numerator = hist_data.Clone()

        canvas_down.cd()

        hist_ratio = hist_ratio_numerator.Clone()
        hist_ratio.Divide(hist_ratio_denominator)
        hist_ratio.Draw("histEP")
        dress_histograms(hist_ratio, hist, canvas_up, canvas_down, "down")

        canvas_up.cd()
        legend = get_legend(hist_backgrounds, hist_signals, hist_data)
        legend.Draw("same")

        canvas.SaveAs(f"outputs/hists/{flag_campaign}/{hist_name}.pdf")

        if flag_write:
            outfile.Close()


def get_null_hist(hist):

    n_bin = hist.GetNbinsX()

    for i_bin in range(1, n_bin+1):

        hist.SetBinContent(i_bin, 0.000001)

    return hist


def get_histograms(root_files, root_type, region, hist_name, hist_categories, outfile, flag_write, hist_null):

    histograms = {}
    for category in list(hist_categories.keys()):
        hist_category = hist_categories[category]
        histograms[category] = hist_category.Clone()
        this_value = hist_category.GetBinContent(1)
        if flag_write:
            try:
                outfile.cd()
                hist_category.Write(category)
                ROOT.gROOT.cd()
            except:
                outfile.cd()
                hist_null.Write(category)
                ROOT.gROOT.cd()
            for syst in list(systematic_configs.keys()):
                if systematic_configs[syst]["variation"] == "updown" :
                    syst_vars = ["Up", "Down"]
                elif syst == "TopPtReweight":
                    syst_vars = ["Up", "Down"]
                else:
                    continue
                for syst_var in syst_vars:
                    try:
                        ROOT.gROOT.cd()
                        hist_categories_syst = get_added_hist(root_files, region, f"{syst}{syst_var}", hist_name, root_type)
                        hist_category_syst = hist_categories_syst[category]
                        outfile.cd()
                        if systematic_configs[syst]["type"] == "uncorrelated":
                            syst_name = f"{syst}_{flag_campaign}{syst_var}"
                        else:
                            syst_name = f"{syst}{syst_var}"
                        hist_category_syst.Write(f"{category}_{syst_name}")
                        ROOT.gROOT.cd()
                    except:
                        outfile.cd()
                        if systematic_configs[syst]["type"] == "uncorrelated":
                            syst_name = f"{syst}_{flag_campaign}{syst_var}"
                        else:
                            syst_name = f"{syst}{syst_var}"
                        hist_null.Write(f"{category}_{syst_name}")
                        ROOT.gROOT.cd()

    return histograms

def get_legend(hist_backgrounds, hist_signals, hist_data):

    legend = ROOT.TLegend(.75,.60,.85,.85)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)

    for category in list(hist_backgrounds.keys()):
        hist_background = hist_backgrounds[category]
        legend_category = category
        legend_category = legend_category.replace("__plus__", "+")
        legend_category = legend_category.replace("__comma__", ", ")
        legend_category = legend_category.replace("__space__", " ")
        legend.AddEntry(hist_background, legend_category, "f")

    legend.AddEntry(hist_data, "Data", "p")

    return legend

def dress_histograms(histogram, hist, canvas_up, canvas_down, canvas_pad):

    try:
        histogram.GetXaxis().SetRangeUser(hist_configs[hist]["x_min"], hist_configs[hist]["x_max"])
    except:
        pass

    if (canvas_pad == "up"):
        histogram.SetMinimum(0.1)#histogram.GetMinimum() * 0.1)
        histogram.SetMaximum(histogram.GetMaximum() * 1000.0)
        canvas_up.SetLogy()
#        if hist == "bins":
#            histogram.SetMinimum(histogram.GetMinimum() * 0.1)
#            histogram.SetMaximum(histogram.GetMaximum() * 10.0)
#            canvas_up.SetLogy()
#        else:
#            histogram.SetMaximum(histogram.GetMaximum() * 2.0)

    if (canvas_pad == "down"):
        histogram.GetXaxis().SetTitle(hist_configs[hist]["x_label"])
        histogram.GetXaxis().SetLabelSize(0.14)
        histogram.GetXaxis().SetTitleSize(0.12)
        histogram.GetYaxis().SetRangeUser(0.35, 1.65)
        histogram.GetYaxis().SetLabelSize(0.11)
        histogram.GetYaxis().SetNdivisions(510)


def get_added_hist(root_files, region, syst_name, hist_name, sample_type):

    hist = hist_name.replace(f"{region}_", "")

    categories = list(root_files.keys())
    added_hists = {}

    for category in categories:

        hists_to_add = None

        for root_file in root_files[category]:
            try:
                tfile_root_file = ROOT.TFile(root_file)
            except:
                continue

            ROOT.gROOT.cd()
            if syst_name != "CENTRAL": 
                tdir_name = f"SYST_{syst_name}"
            else:
                tdir_name = "CENTRAL"

            try:
                get_root_file_hist = tfile_root_file.Get(f"{tdir_name}/{hist_name}").Clone()
            except:
                continue

            try:
                get_root_file_hist.Rebin(hist_configs[hist]["rebin"])
            except:
                pass

            if sample_type == "data":
                get_root_file_hist.SetMarkerStyle(20)
                get_root_file_hist.SetMarkerSize(1)
                get_root_file_hist.SetMarkerColor(ROOT.kBlack)
            if sample_type == "signal":
                get_root_file_hist.SetMarkerColor(sample_configs[sample_type][category]["color"])
                get_root_file_hist.SetLineColor(sample_configs[sample_type][category]["color"])
                get_root_file_hist.SetLineStyle(sample_configs[sample_type][category]["style"])
                get_root_file_hist.SetLineWidth(3)
                signal_cross_section = get_signal_crosssection(root_file)
                get_root_file_hist.Scale(sample_configs[sample_type][category]["scale"] * signal_cross_section)
            if sample_type == "background":
                get_root_file_hist.SetLineColor(ROOT.kBlack)
                get_root_file_hist.SetFillColor(sample_configs[sample_type][category]["color"])
            if hists_to_add == None:
                if get_root_file_hist == None:
                    pass
                else:
                    hists_to_add = get_root_file_hist.Clone()
            else:
                if get_root_file_hist == None:
                    pass
                else:
                    hists_to_add.Add(get_root_file_hist.Clone())

        try:
            added_hists[category] = hists_to_add.Clone()
        except:
            pass

    return added_hists

def get_signal_crosssection(root_file):

    sample = root_file.split("/")[-1].replace(".root", "").replace(f"{flag_analyzer}_", "")

    with open(f"crosssections/{sample}.txt") as crosssection_file:
        signal_crosssection = float(crosssection_file.read().strip())

    return signal_crosssection

def check_root_files():

    datasets = list(sample_configs["data"][flag_channel])
    data_root_files = {}
    data_root_files["data"] = []
    for dataset in datasets:
        try:
            periods = sample_configs["data"][flag_channel][dataset][flag_campaign]
        except:
            continue

        for period in periods:
            root_file_path = f"/data6/Users/shjeon/SKFlatOutput/Run2UltraLegacy_v3/{flag_analyzer}/{flag_campaign}/syst__/DATA/{flag_analyzer}_{flag_skim}_{dataset}_{period}.root"
            if os.path.exists(root_file_path):
                data_root_files["data"].append(root_file_path)
            else:
                print (f"WARNING : {root_file_path} does not exist")

    signals = list(sample_configs["signal"])
    signal_root_files = {}
    for signal in signals:
        processes = sample_configs["signal"][signal]["process"]

        signal_root_files[signal] = []

        for process in processes:
            root_file_path = f"/data6/Users/shjeon/SKFlatOutput/Run2UltraLegacy_v3/{flag_analyzer}/{flag_campaign}/syst__/{flag_analyzer}_{process}.root"
            if os.path.exists(root_file_path):
                signal_root_files[signal].append(root_file_path)
            else:
                print (f"WARNING : {root_file_path} does not exist")

    backgrounds = list(sample_configs["background"])
    background_root_files = {}
    for background in backgrounds:
        processes = sample_configs["background"][background]["process"]

        background_root_files[background] = []

        for process in processes:
            root_file_path = f"/data6/Users/shjeon/SKFlatOutput/Run2UltraLegacy_v3/{flag_analyzer}/{flag_campaign}/syst__/{flag_analyzer}_{flag_skim}_{process}.root"
            if os.path.exists(root_file_path):
                background_root_files[background].append(root_file_path)
            else:
                print (f"WARNING : {root_file_path} does not exist")

    if (flag_debug):
        print(f"DEBUG : check_root_files:data_root_files = {data_root_files}")
        print(f"DEBUG : check_root_files:signal_root_files = {signal_root_files}")
        print(f"DEBUG : check_root_files:background_root_files = {background_root_files}")

    return (data_root_files, signal_root_files, background_root_files)

def get_regions():

    regions = {}
    selections = list(region_configs[flag_channel])

    for selection in selections:
        for event_selection in region_configs[flag_channel][selection]:
            region = f"{selection}{event_selection}"
            regions[region] = region_configs[flag_channel][selection][event_selection]

    return regions

def get_canvas(hist_name):

    canvas = ROOT.TCanvas(hist_name, hist_name, 800, 800)
    canvas.SetFillColor(0)
    canvas.SetFrameFillStyle(0)

    canvas_up = None
    canvas_down = None

    canvas.Divide(1,2)
    canvas_up = ROOT.TPad(f"{hist_name}_canvas_up", "", 0.0, 0.25, 1.0, 1.0)
    canvas_up.SetFillColor(0)
    canvas_up.SetFrameFillStyle(0)
    canvas_up.Draw()
    canvas_up.SetTopMargin( 0.07 );
    canvas_up.SetBottomMargin( 0.025 );
    canvas_up.SetLeftMargin( 0.15 );
    canvas_up.SetRightMargin( 0.032 );

    canvas_down = ROOT.TPad(f"{hist_name}_canvas_down", "", 0.0, 0.0, 1.0, 0.25)
    canvas_down.SetFillColor(0)
    canvas_down.SetFrameFillStyle(0)
    canvas_down.Draw()
    canvas_down.SetTopMargin( 0.035 );
    canvas_down.SetBottomMargin( 0.4 );
    canvas_down.SetLeftMargin( 0.15 );
    canvas_down.SetRightMargin( 0.032 );

    latex_cms = ROOT.TLatex()
    latex_cms.SetNDC()
    latex_cms.SetTextSize(0.035)
    latex_cms.DrawLatex(0.15, 0.96, "#font[62]{CMS} #font[42]{#it{#scale[0.8]{Preliminary}}}")

    latex_lumi = ROOT.TLatex()
    latex_lumi.SetNDC()
    latex_lumi.SetTextSize(0.035)
    latex_lumi.SetTextFont(42)
    if flag_campaign == "2016preVFP":
        latex_lumi.DrawLatex(0.73, 0.96, "19.5 fb^{-1} (13 TeV)")
    if flag_campaign == "2016postVFP":
        latex_lumi.DrawLatex(0.73, 0.96, "16.8 fb^{-1} (13 TeV)")
    if flag_campaign == "2017":
        latex_lumi.DrawLatex(0.73, 0.96, "41.5 fb^{-1} (13 TeV)")
    if flag_campaign == "2018":
        latex_lumi.DrawLatex(0.73, 0.96, "59.8 fb^{-1} (13 TeV)")

    latex_hist = ROOT.TLatex()
    latex_hist.SetNDC()
    latex_hist.SetTextSize(0.027)
    latex_hist.SetTextFont(42)
    latex_hist.SetTextAngle(90)
    latex_hist.DrawLatex(0.065, 0.83, "Events/Bin")

    latex_ratio = ROOT.TLatex()
    latex_ratio.SetNDC()
    latex_ratio.SetTextSize(0.027)
    latex_ratio.SetTextFont(42)
    latex_ratio.SetTextAngle(90)
    latex_ratio.DrawLatex(0.065, 0.07, "Data/Prediction")

    return canvas, canvas_up, canvas_down

def get_signal_systematics():

    data_root_files, signal_root_files, background_root_files = check_root_files()

    den_central_hists = get_added_hist(signal_root_files, "NONE", "Signal", f"DEN_NoCut_Nominal", "signal")
    num_central_resolved_hists = get_added_hist(signal_root_files, "NONE", "Signal", f"NUM_{flag_channel}Resolved_Nominal", "signal")
    num_central_merged_hists = get_added_hist(signal_root_files, "NONE", "Signal", f"NUM_{flag_channel}Merged_Nominal", "signal")

    keys = list(den_central_hists.keys())

    acceptance_central_resolved = {}
    acceptance_central_merged = {}
    systematics_error_resolved = {}
    systematics_error_merged = {}
    systematics_scale_resolved = {}
    systematics_scale_merged = {}
    for key in keys:
        acceptance_central_resolved[key] = (num_central_resolved_hists[key].GetBinContent(1))/(den_central_hists[key].GetBinContent(1))
        acceptance_central_merged[key] = (num_central_merged_hists[key].GetBinContent(1))/(den_central_hists[key].GetBinContent(1))
        systematics_error_resolved[key] = 0.
        systematics_error_merged[key] = 0.
        systematics_scale_resolved[key] = 0.
        systematics_scale_merged[key] = 0.

    for i in range(0, 100):
        den_error_hists = get_added_hist(signal_root_files, "NONE", "Signal", f"DEN_NoCut_Error{i}", "signal")
        num_error_resolved_hists = get_added_hist(signal_root_files, "NONE", "Signal", f"NUM_{flag_channel}Resolved_Error{i}", "signal")
        num_error_merged_hists = get_added_hist(signal_root_files, "NONE", "Signal", f"NUM_{flag_channel}Merged_Error{i}", "signal")
        acceptance_error_resolved = {}
        acceptance_error_merged = {}
        for key in keys:
            acceptance_error_resolved[key] = (num_error_resolved_hists[key].GetBinContent(1))/(den_error_hists[key].GetBinContent(1))
            systematics_error_resolved[key] += (acceptance_error_resolved[key] - acceptance_central_resolved[key]) * (acceptance_error_resolved[key] - acceptance_central_resolved[key])
            acceptance_error_merged[key] = (num_error_merged_hists[key].GetBinContent(1))/(den_error_hists[key].GetBinContent(1))
            systematics_error_merged[key] += (acceptance_error_merged[key] - acceptance_central_merged[key]) * (acceptance_error_merged[key] - acceptance_central_merged[key])

    for i in range(0, 9):
        den_scale_hists = get_added_hist(signal_root_files, "NONE", "Signal", f"DEN_NoCut_Scale{i}", "signal")
        num_scale_resolved_hists = get_added_hist(signal_root_files, "NONE", "Signal", f"NUM_{flag_channel}Resolved_Scale{i}", "signal")
        num_scale_merged_hists = get_added_hist(signal_root_files, "NONE", "Signal", f"NUM_{flag_channel}Merged_Scale{i}", "signal")
        acceptance_scale_resolved = {}
        acceptance_scale_merged = {}
        for key in keys:
            acceptance_scale_resolved[key] = (num_scale_resolved_hists[key].GetBinContent(1))/(den_scale_hists[key].GetBinContent(1))
            systematics_scale_resolved[key] += (acceptance_scale_resolved[key] - acceptance_central_resolved[key]) * (acceptance_scale_resolved[key] - acceptance_central_resolved[key])
            acceptance_scale_merged[key] = (num_scale_merged_hists[key].GetBinContent(1))/(den_scale_hists[key].GetBinContent(1))
            systematics_scale_merged[key] += (acceptance_scale_merged[key] - acceptance_central_merged[key]) * (acceptance_scale_merged[key] - acceptance_central_merged[key])

    for key in keys:
        systematics_error_resolved[key] = math.sqrt(systematics_error_resolved[key])
        systematics_scale_resolved[key] = math.sqrt(systematics_scale_resolved[key])
        systematics_error_merged[key] = math.sqrt(systematics_error_merged[key])
        systematics_scale_merged[key] = math.sqrt(systematics_scale_merged[key])

        print ("resolved ============")
        print (key, systematics_error_resolved[key], systematics_scale_resolved[key])
        print ("merged ============")
        print (key, systematics_error_merged[key], systematics_scale_merged[key])

def main():

    regions = get_regions()
    for region in regions:
        get_systematics(region)

#    get_signal_systematics()


if __name__ == "__main__":

    main()
