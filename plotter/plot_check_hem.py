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

flag_campaign = "2018"
flag_channel = "Electron"

def get_systematics(region, hist):

    root_files = check_root_files()

    hist_name = f"ControlRegion_{flag_channel}{region}{hist}"

    canvas, canvas_up, canvas_down = get_canvas(hist_name)

    hist_background_withhem = get_added_hist(root_files["background"], region, "WithHEM", hist_name, "background")
    hist_background_central = get_added_hist(root_files["background"], region, "CENTRAL", hist_name, "background")
    hist_data_withhem = get_added_hist(root_files["data"], region, "WithHEM", hist_name, "data")
    hist_data_central = get_added_hist(root_files["data"], region, "CENTRAL", hist_name, "data")

    hist_background_withhem.SetLineColor(ROOT.kBlack)
    hist_background_withhem.SetLineWidth(2)
    hist_background_withhem.SetLineStyle(2)

    hist_background_central.SetLineColor(ROOT.kRed)
    hist_background_central.SetLineWidth(2)

    hist_data_withhem.SetLineColor(ROOT.kBlack)
    hist_data_withhem.SetMarkerColor(ROOT.kBlack)
    hist_data_withhem.SetMarkerStyle(24)
    hist_data_withhem.SetMarkerSize(1.2)

    hist_data_central.SetLineColor(ROOT.kRed)
    hist_data_central.SetMarkerColor(ROOT.kRed)
    hist_data_central.SetMarkerStyle(20)
    hist_data_central.SetMarkerSize(1.2)

    canvas_up.cd()

    hist_background_central.Draw("hist")
    dress_histograms(hist_background_central, hist, canvas, canvas_up, canvas_down, "up")
    hist_background_withhem.Draw("samehist")
    hist_data_central.Draw("samehistP")
    hist_data_withhem.Draw("samehistP")

    canvas_down.cd()

    hist_ratio_ref = get_ref_hist(hist_background_withhem)
    hist_ratio_ref.Draw("hist")
    dress_histograms(hist_ratio_ref, hist, canvas, canvas_up, canvas_down, "down")

    hist_ratio1 = hist_data_central.Clone()
    hist_ratio1.Divide(hist_background_central)
    hist_ratio2 = hist_data_withhem.Clone()
    hist_ratio2.Divide(hist_background_withhem)
    hist_ratio1.Draw("sameP")
    hist_ratio2.Draw("sameP")

    canvas_up.cd()

    legend_hists = {
        "Obs. HEM included" : hist_data_withhem,
        "Obs. HEM removed" : hist_data_central,
        "Pre. HEM included" : hist_background_withhem,
        "Pre. HEM removed" : hist_background_central
    }
    legend = get_legend(legend_hists)
    legend.Draw("same")

    canvas.SaveAs(f"outputs/hists/check_hem/{flag_campaign}/{hist_name}.pdf")

def get_ref_hist(hist):

    ref_hist = hist.Clone()

    n_bin = ref_hist.GetNbinsX()

    for i_bin in range(1, n_bin+1):

        ref_hist.SetBinContent(i_bin, 1.0)

    ref_hist.SetMarkerColor(ROOT.kBlack)
    ref_hist.SetLineColor(ROOT.kBlack)
    ref_hist.SetLineWidth(1)

    return ref_hist


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
        if "Obs" in legend_category : legend.AddEntry(legend_hist, legend_category, "p")
        else : legend.AddEntry(legend_hist, legend_category, "l")

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
        histogram.GetYaxis().SetRangeUser(0.1, 1.9)
        histogram.GetYaxis().SetLabelSize(0.18)
        histogram.GetYaxis().SetNdivisions(504)

def get_added_hist(root_files, region, case, hist_name, sample_type):

    added_hists = {}

    hists_to_add = None

    for root_file in root_files:
        try:
            tfile_root_file = ROOT.TFile(root_file)
        except:
            continue

        ROOT.gROOT.cd()
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

    return hists_to_add

def check_root_files():

    root_files = {}
    root_files["background"] = []
    root_files["data"] = []
    for sample in samples["background"]:
        root_file_path = f"/data6/Users/shjeon/SKFlatOutput/Run2UltraLegacy_v3/{flag_analyzer}/{flag_campaign}/hem__/{flag_analyzer}_{flag_skim}_{sample}.root"
        if os.path.exists(root_file_path):
            root_files["background"].append(root_file_path)
        else:
            print (f"WARNING : {root_file_path} does not exist")

    for sample in samples["data"]:

        root_file_path = f"/data6/Users/shjeon/SKFlatOutput/Run2UltraLegacy_v3/{flag_analyzer}/{flag_campaign}/hem__/DATA/{flag_analyzer}_{flag_skim}_{sample}.root"

        if os.path.exists(root_file_path):
            root_files["data"].append(root_file_path)
        else:
            print (f"WARNING : {root_file_path} does not exist")

    return root_files

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

    if not os.path.exists(f"outputs/hists/check_hem/{flag_campaign}/"):
        os.system(f"mkdir -p outputs/hists/check_hem/{flag_campaign}/")

    for region in regions:
        for hist in list(hists.keys()):
            get_systematics(region, hist)

regions = ["MergedDomWSelection", "MergedDomTTSelection", "ResolvedDomWSelection", "ResolvedDomTTSelection"]

hists = {
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

samples = {
    "background" : [
        "WJets_Sherpa", "DYJetsToEE_MiNNLO", "DYJetsToMuMu_MiNNLO", "DYJetsToTauTau_MiNNLO",
        "WWW", "WWZ", "WZZ", "ZZZ", "WW_pythia", "WZ_pythia", "ZZ_pythia", "WplusH_HToBB_WToLNu", "WminusH_HToBB_WToLNu",
        "TTLJ_powheg", "TTLL_powheg", "TTJJ_powheg",
        "SingleTop_sch_Lep", "SingleTop_tW_antitop_NoFullyHad", "SingleTop_tW_top_NoFullyHad", "SingleTop_tch_antitop_Incl", "SingleTop_tch_top_Incl", "ttWToLNu", "ttWToQQ", "ttZToLLNuNu", "ttZToQQ"
        ],
    "data" : [
        "EGamma_A",
        "EGamma_B",
        "EGamma_C",
        "EGamma_D"
    ]
}

#singlelepton_analysis_SkimTree_SingleLepton_EGamma_A.root
#singlelepton_analysis_SkimTree_SingleLepton_EGamma_B.root
#singlelepton_analysis_SkimTree_SingleLepton_EGamma_C.root
#singlelepton_analysis_SkimTree_SingleLepton_EGamma_D.root


if __name__ == "__main__":

    main()
