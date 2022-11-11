#!/usr/bin/env python3
import ROOT
ROOT.gROOT.SetBatch(True)

import os
import sys
import math
import argparse

from include.args_parser import args

import configs.singlelepton_analysis.root_configs
from configs.singlelepton_analysis.sample_configs import sample_configs

flag_analyzer = "singlelepton_analysis"
flag_skim = "SkimTree_SingleLepton"

flag_campaign = args.campaign
flag_channel = "Electron"

def get_systematics(region, hist, case):

    data_root_files, background_root_files = check_root_files()

    hist_name = f"ControlRegion_Electron{region}{hist}"

    hist_data = get_added_hist(data_root_files, region, case, hist_name, "data", case)["data"]

    canvas, canvas_up, canvas_down = get_canvas(hist_name)

    hist_background_categories = get_added_hist(background_root_files, region, case, hist_name, "background", case)
    hist_backgrounds = get_histograms(hist_background_categories)

    stack_background = ROOT.THStack()
    hist_ratio_numerator = None
    hist_ratio_denominator = None

    for category in list(hist_backgrounds.keys()):
        hist_background = hist_backgrounds[category]

        if hist_ratio_denominator == None:
            hist_ratio_denominator = hist_background.Clone()
        else:
            hist_ratio_denominator.Add(hist_background.Clone())
        stack_background.Add(hist_background.Clone())

    canvas_up.cd()

    stack_background.Draw("hist")
    stack_background.GetXaxis().SetLabelSize(0)
    dress_histograms(stack_background, hist, canvas_up, canvas_down, "up")

    hist_data.Draw("samehistP")
    hist_ratio_numerator = hist_data.Clone()

    canvas_down.cd()

    hist_ratio = hist_ratio_numerator.Clone()
    hist_ratio.Divide(hist_ratio_denominator)
    hist_ratio.Draw("histEP")
    dress_histograms(hist_ratio, hist, canvas_up, canvas_down, "down")

    canvas_up.cd()
    legend = get_legend(hist_backgrounds, hist_data)
    legend.Draw("same")

    canvas.SaveAs(f"outputs/hists/check_hem/{flag_campaign}/{case}/{hist_name}.pdf")

def get_null_hist(hist):

    n_bin = hist.GetNbinsX()

    for i_bin in range(1, n_bin):

        hist.SetBinContent(i_bin, 0.0001)

    return hist


def get_histograms(hist_categories):

    histograms = {}
    for category in list(hist_categories.keys()):
        hist_category = hist_categories[category]
        histograms[category] = hist_category.Clone()

    return histograms

def get_legend(hist_backgrounds, hist_data):

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
        histogram.GetXaxis().SetTitle(hists[hist]["x_label"])
        histogram.GetXaxis().SetLabelSize(0.14)
        histogram.GetXaxis().SetTitleSize(0.12)
        histogram.GetYaxis().SetRangeUser(0.35, 1.65)
        histogram.GetYaxis().SetLabelSize(0.11)
        histogram.GetYaxis().SetNdivisions(510)


def get_added_hist(root_files, region, syst_name, hist_name, sample_type, case):

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
                get_root_file_hist = tfile_root_file.Get(f"{case}/{hist_name}").Clone()
            except:
                continue

#            get_root_file_hist.Rebin(hists[hist]["rebin"])

            if sample_type == "data":
                get_root_file_hist.SetMarkerStyle(20)
                get_root_file_hist.SetMarkerSize(1)
                get_root_file_hist.SetMarkerColor(ROOT.kBlack)
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
            root_file_path = f"/data6/Users/shjeon/SKFlatOutput/Run2UltraLegacy_v3/{flag_analyzer}/{flag_campaign}/hem__/DATA/{flag_analyzer}_{flag_skim}_{dataset}_{period}.root"
            if os.path.exists(root_file_path):
                data_root_files["data"].append(root_file_path)
            else:
                print (f"WARNING : {root_file_path} does not exist")

    backgrounds = list(sample_configs["background"])
    background_root_files = {}
    for background in backgrounds:
        processes = sample_configs["background"][background]["process"]

        background_root_files[background] = []

        for process in processes:
            root_file_path = f"/data6/Users/shjeon/SKFlatOutput/Run2UltraLegacy_v3/{flag_analyzer}/{flag_campaign}/hem__/{flag_analyzer}_{flag_skim}_{process}.root"
            if os.path.exists(root_file_path):
                background_root_files[background].append(root_file_path)
            else:
                print (f"WARNING : {root_file_path} does not exist")

    return (data_root_files, background_root_files)

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

def main():

    for case in ["CENTRAL", "WithHEM"]:
        if not os.path.exists(f"outputs/hists/check_hem/{flag_campaign}/{case}"):
            os.system(f"mkdir -p outputs/hists/check_hem/{flag_campaign}/{case}")

        for region in regions:
            for hist in hists:
                get_systematics(region, hist, case)


regions = ["MergedXbbInvMTDPhiSelection", "MergedXqqInvMTDPhiSelection", "MergedDomWSelection", "MergedDomTTSelection", "ResolvedXbbInvMTDPhiSelection", "ResolvedXbqInvMTDPhiSelection", "ResolvedXqqInvMTDPhiSelection", "ResolvedDomWSelection", "ResolvedDomTTSelection"]

hists = {
    "CheckHEM_phi_lepton" : {
        "rebin" : 1,
        "x_label" : "#phi(l)"
    },
    "CheckEta1HEM_phi_lepton" : {
        "rebin" : 1,
        "x_label" : "#phi(l)"
    },
    "CheckEta2HEM_phi_lepton" : {
        "rebin" : 1,
        "x_label" : "#phi(l)"
    },
    "CheckPhi1HEM_phi_lepton" : {
        "rebin" : 1,
        "x_label" : "#phi(l)"
    },
    "CheckPhi2HEM_phi_lepton" : {
        "rebin" : 1,
        "x_label" : "#phi(l)"
    },
    "CheckPhi3HEM_phi_lepton" : {
        "rebin" : 1,
        "x_label" : "#phi(l)"
    },
    "CheckPhi4HEM_phi_lepton" : {
        "rebin" : 1,
        "x_label" : "#phi(l)"
    },
    "CheckHEM_eta_lepton" : {
        "rebin" : 1,
        "x_label" : "#eta(l)"
    },
    "CheckEta1HEM_eta_lepton" : {
        "rebin" : 1,
        "x_label" : "#eta(l)"
    },
    "CheckEta2HEM_eta_lepton" : {
        "rebin" : 1,
        "x_label" : "#eta(l)"
    },
    "CheckPhi1HEM_eta_lepton" : {
        "rebin" : 1,
        "x_label" : "#eta(l)"
    },
    "CheckPhi2HEM_eta_lepton" : {
        "rebin" : 1,
        "x_label" : "#eta(l)"
    },
    "CheckPhi3HEM_eta_lepton" : {
        "rebin" : 1,
        "x_label" : "#eta(l)"
    },
    "CheckPhi4HEM_eta_lepton" : {
        "rebin" : 1,
        "x_label" : "#eta(l)"
    },
}



if __name__ == "__main__":

    main()
