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
from configs.singlelepton_analysis.hist_configs import hist_configs

flag_analyzer = "singlelepton_analysis"
flag_skim = "SkimTree_SingleLepton"

flag_campaign = args.campaign
flag_channel = args.channel

def get_systematics(region, hist):

    background_root_files = check_root_files()

    hist_name = f"ControlRegion_{flag_channel}{region}_{hist}"

    canvas, canvas_up, canvas_down = get_canvas(hist_name)

    hist_background_weighted = get_histograms(get_added_hist(background_root_files, region, "CENTRAL", hist_name, "background"))
    hist_background_unweighted = get_histograms(get_added_hist(background_root_files, region, "WithoutTopPtRwgt", hist_name, "background"))

    hist_stacked_weighted = None
    hist_stacked_unweighted = None

    for category in list(hist_background_weighted.keys()):
        hist_to_stack = hist_background_weighted[category]
        if hist_stacked_weighted == None:
            hist_stacked_weighted = hist_to_stack.Clone()
        else:
            hist_stacked_weighted.Add(hist_to_stack.Clone())

    for category in list(hist_background_unweighted.keys()):
        hist_to_stack = hist_background_unweighted[category]
        if hist_stacked_unweighted == None:
            hist_stacked_unweighted = hist_to_stack.Clone()
        else:
            hist_stacked_unweighted.Add(hist_to_stack.Clone())

    canvas_up.cd()

    hist_stacked_weighted.SetLineColor(ROOT.kRed)
    hist_stacked_weighted.SetLineWidth(2)
    hist_stacked_weighted.Draw("hist")
    dress_histograms(hist_stacked_weighted, hist, canvas, canvas_up, canvas_down, "up")

    hist_stacked_unweighted.SetLineColor(ROOT.kBlack)
    hist_stacked_unweighted.SetLineWidth(2)
    hist_stacked_unweighted.SetLineStyle(2)
    hist_stacked_unweighted.Draw("samehist")
    dress_histograms(hist_stacked_unweighted, hist, canvas, canvas_up, canvas_down, "up")

    canvas_down.cd()

    hist_ratio_ref = get_ref_hist(hist_stacked_unweighted)
    hist_ratio_ref.Draw("hist")

    hist_ratio = hist_stacked_weighted.Clone()
    hist_ratio.Divide(hist_stacked_unweighted)
    hist_ratio.SetMarkerColor(ROOT.kRed)
    hist_ratio.SetMarkerStyle(20)
    hist_ratio.SetMarkerSize(1.2)
    hist_ratio.Draw("sameP")

    dress_histograms(hist_ratio_ref, hist, canvas, canvas_up, canvas_down, "down")

    canvas_up.cd()
    legend_hists = {
        "Weighted" : hist_stacked_weighted,
        "Unweighted" : hist_stacked_unweighted
    }
    legend = get_legend(legend_hists)
    legend.Draw("same")

    canvas.SaveAs(f"outputs/hists/check_toppt/{flag_campaign}/{hist_name}.pdf")

def get_ref_hist(hist):

    ref_hist = hist.Clone()

    n_bin = ref_hist.GetNbinsX()

    for i_bin in range(1, n_bin+1):

        ref_hist.SetBinContent(i_bin, 1.0)

    ref_hist.SetMarkerColor(ROOT.kBlack)
    ref_hist.SetLineColor(ROOT.kBlack)
    ref_hist.SetLineWidth(1)

    return ref_hist


def get_histograms(hist_categories):

    histograms = {}
    for category in list(hist_categories.keys()):
        hist_category = hist_categories[category]
        histograms[category] = hist_category.Clone()

    return histograms

def get_legend(legend_hists):

    legend = ROOT.TLegend(.3,.62,.88,.88)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    legend.SetNColumns(2)

    for category in list(legend_hists.keys()):
        legend_hist = legend_hists[category]
        legend_category = category
        legend_category = legend_category.replace("__plus__", "+")
        legend_category = legend_category.replace("__comma__", ", ")
        legend_category = legend_category.replace("__space__", " ")
        legend.AddEntry(legend_hist, legend_category, "l")

    return legend

def dress_histograms(histogram, hist, canvas, canvas_up, canvas_down, canvas_pad):

    if (canvas_pad == "up"):
        histogram.SetMinimum(0.1)#histogram.GetMinimum() * 0.1)
        histogram.SetMaximum(histogram.GetMaximum() * 10000.0)
        histogram.GetXaxis().SetLabelSize(0)
        histogram.GetYaxis().SetLabelSize(0.06)#0.1#0.18
        canvas_up.SetLogy()

    if (canvas_pad == "down"):
        histogram.GetXaxis().SetTitle(hists[hist]["x_label"])
        histogram.GetXaxis().SetLabelSize(0.18)
        histogram.GetXaxis().SetTitleSize(0.16)
        histogram.GetXaxis().SetTitleOffset(1.05)#1.1#1.2
        histogram.GetXaxis().SetNdivisions(505)
        histogram.GetYaxis().SetRangeUser(0.7, 1.3)
        histogram.GetYaxis().SetLabelSize(0.18)
        histogram.GetYaxis().SetNdivisions(504)

def get_added_hist(root_files, region, case, hist_name, sample_type):

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
            print (f"{case}/{hist_name}")
            try:
                get_root_file_hist = tfile_root_file.Get(f"{case}/{hist_name}").Clone()
            except:
                continue

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

    backgrounds = list(sample_configs["background"])
    background_root_files = {}
    for background in backgrounds:
        processes = sample_configs["background"][background]["process"]

        background_root_files[background] = []

        for process in processes:
            root_file_path = f"/data6/Users/shjeon/SKFlatOutput/Run2UltraLegacy_v3/{flag_analyzer}/{flag_campaign}/toppt__/{flag_analyzer}_{flag_skim}_{process}.root"
            if os.path.exists(root_file_path):
                background_root_files[background].append(root_file_path)
            else:
                print (f"WARNING : {root_file_path} does not exist")

    return background_root_files

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
    latex_hist.SetTextSize(0.042)
    latex_hist.SetTextFont(42)
    latex_hist.SetTextAngle(90)
    latex_hist.DrawLatex(0.065, 0.76, "Events/Bin")

    latex_ratio = ROOT.TLatex()
    latex_ratio.SetNDC()
    latex_ratio.SetTextSize(0.042)
    latex_ratio.SetTextFont(42)
    latex_ratio.SetTextAngle(90)
    latex_ratio.DrawLatex(0.065, 0.12, "Ratio")

    return canvas, canvas_up, canvas_down

def main():

    if not os.path.exists(f"outputs/hists/check_toppt/{flag_campaign}/"):
        os.system(f"mkdir -p outputs/hists/check_toppt/{flag_campaign}/")

    for region in regions:
        for hist in list(hist_configs.keys()):
            get_systematics(region, hist)

regions = ["MergedDomWSelection", "MergedDomTTSelection", "ResolvedDomWSelection", "ResolvedDomTTSelection"]

hists = {
    "dphi_leptonmet" : {
        "x_label" : "#Delta#phi(l,E^{miss}_{T})",
    },
    "mass_recosecboson" : {
        "x_label" : "m(X^{reco}) [GeV]",
    },
    "masst_recopriboson" : {
        "x_label" : "m_{T}(l,E^{miss}_{T},J) [GeV]",
    },
    "masst_leptonmet" : {
        "x_label" : "m_{T}(l,E^{miss}_{T}) [GeV]",
    },
    "met" : {
        "x_label" : "E^{miss}_{T} [GeV]",
    },
    "n_jet" : {
        "x_label" : "Number of jets",
    },
    "n_bjet" : {
        "x_label" : "Number of b-jets",
    },
    "pt_lepton" : {
        "x_label" : "p_{T}(l) [GeV]",
    },
}



if __name__ == "__main__":

    main()
