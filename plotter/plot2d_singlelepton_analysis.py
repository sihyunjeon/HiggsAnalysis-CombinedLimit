#!/usr/bin/env python3
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

import os
import sys
import array
import argparse

from include.args_parser import args

#import configs.singlelepton_analysis.root_configs
from configs.singlelepton_analysis.hist2d_configs import hist_configs  
from configs.singlelepton_analysis.sample_configs import sample_configs
from configs.singlelepton_analysis.region_configs import region_configs

flag_analyzer = "singlelepton_analysis"
flag_skim = "SkimTree_SingleLepton"

flag_campaign = args.campaign
flag_channel = args.channel
flag_debug = args.debug
flag_no_signal = args.no_signal
flag_no_data = args.no_data

def draw_histograms():

    data_root_files, signal_root_files, background_root_files = check_root_files()
    event_selections = check_event_selections()

    hists = list(hist_configs)
    event_preselections = list(event_selections)

    for preselection in event_preselections:
        selections = event_selections[preselection]

        for selection in selections:
            region = f"{preselection}{selection}"

            draw_hist_data = (not flag_no_data) and (region_configs[flag_channel][preselection][selection])
            draw_hist_signal = (not flag_no_signal)

            for hist in hists:

                try:
                    hist_name = f"{region}_{hist}"
                    hist_data = get_added_hist(data_root_files, region, hist_name, "data")["data"]
                    hist_signal_categories = get_added_hist(signal_root_files, region, hist_name, "signal")
                    hist_background_categories = get_added_hist(background_root_files, region, hist_name, "background")
#                hist_background_categories = get_ordered_hist(hist_background_categories)

                    hist_background = None
                    for category in list(hist_background_categories.keys()):
                        hist_background_category = hist_background_categories[category]

                        if hist_background == None:
                            hist_background = hist_background_category
                        else:
                            try:
                                hist_background.Add(hist_background_category)
                            except:
                                continue

                    canvas = ROOT.TCanvas(f"{hist_name}_background", f"{hist_name}_background", 2500, 900)
                    hist_background.Draw("colz")
                    hist_background.GetXaxis().SetRangeUser(hist_configs[hist]["x_min"], hist_configs[hist]["x_max"])
                    hist_background.GetYaxis().SetRangeUser(hist_configs[hist]["y_min"], hist_configs[hist]["y_max"])
                    canvas.SaveAs(f"hists/{hist_name}_background.pdf")

                    for category in list(hist_signal_categories.keys()):
                        hist_signal_category = hist_signal_categories[category]
                        canvas = ROOT.TCanvas(f"hist_signal_{category}", f"hist_signal_{category}", 2500, 900)
                        hist_signal_category.Draw("colz")
                        hist_signal_category.GetXaxis().SetRangeUser(hist_configs[hist]["x_min"], hist_configs[hist]["x_max"])
                        hist_signal_category.GetYaxis().SetRangeUser(hist_configs[hist]["y_min"], hist_configs[hist]["y_max"])
                        canvas.SaveAs(f"hists/{hist_name}_signal_{category}.pdf")
    
                except: pass

def get_added_hist(root_files, region, hist_name, sample_type):

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
            try:
                get_root_file_hist = tfile_root_file.Get(f"CENTRAL/{hist_name}").Clone()
            except:
                continue

            get_root_file_hist.Rebin2D(25, 1)#hist_configs[hist]["x_rebin"])

            if sample_type == "data":
                get_root_file_hist.SetMarkerStyle(20)
                get_root_file_hist.SetMarkerColor(ROOT.kBlack)
            if sample_type == "signal":
                get_root_file_hist.SetLineColor(sample_configs[sample_type][category]["color"])
                get_root_file_hist.SetLineStyle(sample_configs[sample_type][category]["style"])
                get_root_file_hist.SetLineWidth(3)
                signal_cross_section = get_signal_crosssection(root_file)
                get_root_file_hist.Scale(sample_configs[sample_type][category]["scale"] * signal_cross_section)
            if sample_type == "background":
                get_root_file_hist.SetLineColor(ROOT.kBlack)
#                get_root_file_hist.SetLineColor(sample_configs[sample_type][category]["color"])
                get_root_file_hist.SetFillColor(sample_configs[sample_type][category]["color"])

            if hists_to_add == None:
                hists_to_add = get_root_file_hist
            else:
                hists_to_add.Add(get_root_file_hist)

        added_hists[category] = hists_to_add

    return added_hists

def get_signal_crosssection(root_file):

    sample = root_file.split("/")[-1].replace(".root", "").replace(f"{flag_analyzer}_", "")

    with open(f"crosssections/{sample}.txt") as crosssection_file:
        signal_crosssection = float(crosssection_file.read().strip())

    return signal_crosssection

def get_ordered_hist(hist_background_categories):

    hist_background_categories = list(dict(sorted(hist_background_categories.items(), key=lambda item: item[1])))

    return hists_to_stack_ordered

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
            root_file_path = f"samples/{flag_analyzer}/{flag_campaign}/DATA/{flag_analyzer}_{flag_skim}_{dataset}_{period}.root"
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
            root_file_path = f"samples/{flag_analyzer}/{flag_campaign}/{flag_analyzer}_{process}.root"
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
            root_file_path = f"samples/{flag_analyzer}/{flag_campaign}/{flag_analyzer}_{flag_skim}_{process}.root"
            if os.path.exists(root_file_path):
                background_root_files[background].append(root_file_path)
            else:
                print (f"WARNING : {root_file_path} does not exist")

    if (flag_debug):
        print(f"DEBUG : check_root_files:data_root_files = {data_root_files}")
        print(f"DEBUG : check_root_files:signal_root_files = {signal_root_files}")
        print(f"DEBUG : check_root_files:background_root_files = {background_root_files}")

    return (data_root_files, signal_root_files, background_root_files)

def check_event_selections():

    event_selections = {}
    preselections = list(region_configs[flag_channel])
    for preselection in preselections:
        selections = list(region_configs[flag_channel][preselection])
        event_selections[preselection] = []
        for selection in selections:
            event_selections[preselection].append(f"{selection}")

    if (flag_debug):
        print(f"DEBUG : check_event_selections:event_selections = {event_selections}")

    return (event_selections)

def main():

    draw_histograms()

if __name__ == "__main__":

    main()
