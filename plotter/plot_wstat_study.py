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

flag_analyzer = "singlelepton_analysis"
flag_skim = "SkimTree_SingleLepton"

flag_campaign = args.campaign

def get_systematics(hist):

    signal_root_files = check_root_files()

    selections = ["MatchingMerged", "MatchingResolved"]

    hist_signals = {}

    for selection in selections:

        hist_name = f"{selection}_{hist}"

        canvas, canvas_up, canvas_down = get_canvas(hist_name)

        hist_signals[selection] = get_histograms(get_added_hist(signal_root_files, selection, "Study_Signal", hist_name))


    canvas_up.cd()

    for selection in selections:
        for signal in list(signals.keys()):
            try:
                hist_signals[selection][signal].SetLineColor(signals[signal]["color"])
                hist_signals[selection][signal].Draw("samehist")
                dress_histograms(hist_signals[selection][signal], hist, canvas, canvas_up, canvas_down, "up")
            except:
                continue

    canvas_down.cd()

    hist_ratio_ref = get_ref_hist(hist_signals["MatchingMerged"][signal].Clone())
    hist_ratio_ref.SetLineStyle(2)
    hist_ratio_ref.Draw("hist")
    dress_histograms(hist_ratio_ref, hist, canvas, canvas_up, canvas_down, "down")

    canvas_up.cd()

    legend = get_legend(hist_signals)

    legend.Draw("same")
    canvas.SaveAs(f"outputs/hists/signal_study/{flag_campaign}/{hist}.pdf")


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

def get_legend(hist_signals):

    legend = ROOT.TLegend(.2,.68,.88,.88)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.032)
    legend.SetNColumns(2)

    for category in list(hist_signals.keys()):
        for mass in list(hist_signals[category].keys()):
            try:
                hist_signal = hist_signals[category][mass]
                legend_category = f"{mass} : {category}".replace("Matching", "").replace("Matched", "")
                legend_category = legend_category.replace("__plus__", "+")
                legend_category = legend_category.replace("__comma__", ", ")
                legend_category = legend_category.replace("__space__", " ")
                legend_category = legend_category.replace("MN__equal__", "m_{N} = ")
                legend_category = legend_category.replace("GeV", " GeV")

                legend.AddEntry(hist_signal, legend_category, "l")
            except:
                continue
    return legend

def dress_histograms(histogram, hist, canvas, canvas_up, canvas_down, canvas_pad):

    if (canvas_pad == "up"):
        histogram.SetMinimum(0.)#histogram.GetMinimum() * 0.1)
        histogram.SetMaximum(histogram.GetMaximum() * 1.5)
        histogram.GetXaxis().SetLabelSize(0)
        histogram.GetYaxis().SetLabelSize(0.06)#0.1#0.18
        if "deltar" in hist:
            histogram.SetMinimum(0.1)
            histogram.SetMaximum(histogram.GetMaximum() * 100)
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

def get_added_hist(root_files, region, case, hist_name):

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

            signal_cross_section = get_signal_crosssection(root_file)
            get_root_file_hist.Scale(signal_cross_section)
            get_root_file_hist.Rebin(hists[hist]["rebin"])
            get_root_file_hist.SetLineWidth(2)
            if "Resolved" in region: get_root_file_hist.SetLineStyle(2)
            get_root_file_hist.GetXaxis().SetRangeUser(hists[hist]["x_min"], hists[hist]["x_max"])

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

    signal_root_files = {}
    for signal in list(signals.keys()):
        processes = signals[signal]["process"]

        signal_root_files[signal] = []

        for process in processes:
            root_file_path = f"/data6/Users/shjeon/SKFlatOutput/Run2UltraLegacy_v3/{flag_analyzer}/{flag_campaign}/signal__/{flag_analyzer}_{process}.root"
            if os.path.exists(root_file_path):
                signal_root_files[signal].append(root_file_path)
            else:
                print (f"WARNING : {root_file_path} does not exist")

    return signal_root_files

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

    if not os.path.exists(f"outputs/hists/signal_study/{flag_campaign}/"):
        os.system(f"mkdir -p outputs/hists/signal_study/{flag_campaign}/")

    for hist in list(hists.keys()):
        get_systematics(hist)

signals = {

    "MN__equal__500GeV" : {
        "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN500_TuneCP5_13TeV-amcatnlo-pythia8"],
        "style" : 1,
        "scale" : 1.,
        "color" : ROOT.kRed
    },
    "MN__equal__700GeV" : {
        "process" : ["WtoLNtoLNuHtoLNuBB_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-Mu_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuHtoLNuBB_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuBB_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "WtoLNtoLNuZtoLNuQQ_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8", "ZtoNuNtoNuLWtoNuLQQ_TypeIHeavyN-El_MN700_TuneCP5_13TeV-amcatnlo-pythia8"],
        "style" : 1,
        "scale" : 1.,
        "color" : ROOT.kBlue
    },
}

hists = {

}

backgrounds = {
    "Sherpa" : {
        "sample" : "WJets_Sherpa",
        "color" : ROOT.kRed
    },
    "aMCatNLO" : {
        "sample" : "WJets_amcatnlo",
        "color" : ROOT.kBlue
    },
    "MadGraph" : {
        "sample" : "WJets_MG",
        "color" : ROOT.kGreen
    }
}

#[shjeon@tamsa1 SKFlatAnalyzer]$ ls /data6/Users/shjeon/SKFlatOutput//Run2UltraLegacy_v3/singlelepton_analysis/2016preVFP/wstat__
#singlelepton_analysis_SkimTree_SingleLepton_WJets_MG.root  singlelepton_analysis_SkimTree_SingleLepton_WJets_amcatnlo.root


def get_signal_crosssection(root_file):

    sample = root_file.split("/")[-1].replace(".root", "").replace(f"{flag_analyzer}_", "")

    with open(f"crosssections/{sample}.txt") as crosssection_file:
        signal_crosssection = float(crosssection_file.read().strip())

    if flag_campaign == "2016preVFP":
        signal_crosssection = signal_crosssection * 19517.523849863
    if flag_campaign == "2016postVFP":
        signal_crosssection = signal_crosssection * 16812.151722482
    if flag_campaign == "2017":
        signal_crosssection = signal_crosssection * 41477.877400009
    if flag_campaign == "2018":
        signal_crosssection = signal_crosssection * 59827.879502925

    return signal_crosssection


if __name__ == "__main__":

    main()
