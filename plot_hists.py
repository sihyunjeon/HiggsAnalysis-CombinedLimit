#!/usr/bin/env python3
import ROOT
ROOT.gROOT.SetBatch(True)

import os
import sys
import math
import array
import argparse

from plotter.include.args_parser import args

import plotter.configs.singlelepton_analysis.root_configs
from plotter.configs.singlelepton_analysis.hist_configs import hist_configs  
from plotter.configs.singlelepton_analysis.sample_configs import sample_configs

signal_configs = sample_configs["signal"]

background_configs = sample_configs["background"]
backgrounds = list(background_configs.keys())
ordered_backgrounds = ["VV__comma__VVV", "V__plus__Jets", "Single__space__Top", "Top__space__Pair"]

#if set(backgrounds) != set(ordered_backgrounds):
#    sys.exit("check the background list")
backgrounds = ordered_backgrounds

cwd = os.getcwd()

path_plots = f"{cwd}/plots"
if not os.path.exists(path_plots):
    os.system(f"mkdir -p {path_plots}")

def draw_histogram(campaign, variable):

    masses = ["MN__equal__500GeV"]

    rootfiles = []
    try:
        for rootfile in os.listdir(f"workspace/{campaign}/{variable}/"):
            flag_to_skip = False
            for mass in masses:
                if not mass in rootfile:
                    flag_to_skip = True
            if flag_to_skip:
                continue
            if rootfile.startswith("fitDiagnostics") and rootfile.endswith(".root"):
                rootfiles.append(rootfile)
    except: 
        pass

    for rootfile in rootfiles:
        region = rootfile.replace(".root", "").replace("fitDiagnostics", "").split("_MN__equal__")[0]
        signal = f'MN__equal__{rootfile.replace(".root", "").replace("fitDiagnostics", "").split("_MN__equal__")[1]}'
        openfile = ROOT.TFile(f"workspace/{campaign}/{variable}/{rootfile}")

        hist_background = ROOT.THStack()

        hist_data = openfile.Get(f"shapes_prefit/{region}/data").Clone()
        hist_data = set_histogram(hist_data, variable, region, "data")
        hist_ratio_numerator = hist_data.Clone()
        hist_ratio_denominator = None

        canvas, canvas_up, canvas_down = get_canvas(campaign, variable, region)

        hist_backgrounds = {}
        for background in backgrounds:
            hist = openfile.Get(f"shapes_prefit/{region}/{background}").Clone()
            hist = set_histogram(hist, variable, region, background)
            hist_background.Add(hist)
            hist_backgrounds[background] = hist.Clone()
            if hist_ratio_denominator == None:
                hist_ratio_denominator = hist.Clone()
            else:
                hist_ratio_denominator.Add(hist.Clone())

        hist_signals = {}
        for mass in masses:
            hist  = openfile.Get(f"shapes_prefit/{region}/{mass}").Clone()
            hist = set_histogram(hist, variable, region, mass)
            hist_signals[mass] = hist.Clone()

        canvas_up.cd()
        hist_background.Draw("hist")
        dress_histograms(hist_background, variable, canvas_up, "up")
        for mass in list(hist_signals.keys()):
            hist_signals[mass].Draw("samehist")
        hist_data.Draw("samehistP")
        canvas_down.cd()
        hist_ratio = hist_ratio_numerator.Clone()
        hist_ratio.Divide(hist_ratio_denominator)
        hist_error = hist_ratio.Clone()
        hist_error, hist_line = set_error(hist_error, openfile, variable, region)
        hist_error.Draw("E2")
        hist_line.Draw("samehist")
        hist_ratio.Draw("samehistP0")
        dress_histograms(hist_error, variable, canvas_down, "down")

        canvas_up.cd()
        hist_signal = None
        legend_up = get_legend(hist_backgrounds, hist_data, hist_signals, hist_error)
        legend_up.Draw("same")

        canvas.SaveAs(f"hists/{campaign}_{region}_{variable}.pdf")

def set_error(hist_error, openfile, variable, region):

    hist_error_mc = openfile.Get(f"shapes_prefit/{region}/total_background").Clone()
    hist_error_data = openfile.Get(f"shapes_prefit/{region}/data").Clone()

    try:
        x_bins = hist_configs[variable]["x_bins"]["Combined"]
    except:
        if "Merged" in region:
            x_bins = hist_configs[variable]["x_bins"]["Merged"]
        elif "Resolved" in region:
            x_bins = hist_configs[variable]["x_bins"]["Resolved"]

    x_bins = array.array("f", x_bins)

    new_hist_error_mc = ROOT.TH1D(f"{region}_{variable}_error_mc", f"{region}_{variable}_error_mc", int(len(x_bins)-1), x_bins)
    new_hist_error_data = ROOT.TH1D(f"{region}_{variable}_error_data", f"{region}_{variable}_error_data", int(len(x_bins)-1), x_bins)

    bins_to_ignore = 1
    if (int(len(x_bins)-1) != hist_error_data.GetN()):
        if (int(len(x_bins)-2) != hist_error_data.GetN()):
            bins_to_ignore = 2
        else:
            sys.exit(f"error with number of bins : {variable}")
    for i in range(0, int(len(x_bins)-bins_to_ignore)):
        try:
            new_hist_error_data.SetBinContent(i+1, hist_error_data.GetErrorY(i)/hist_error_data.GetPointY(i))
        except:
            new_hist_error_data.SetBinContent(i+1, 0.)

    if (int(len(x_bins)-1) != hist_error_mc.GetNbinsX()):
        if (int(len(x_bins)-2) != hist_error_mc.GetNbinsX()):
            bins_to_ignore = 2
        else:
            sys.exit(f"error with number of bins : {variable}")
    for i in range(0, int(len(x_bins)-bins_to_ignore)):
        try:
            new_hist_error_mc.SetBinContent(i+1, hist_error_mc.GetBinError(i+1)/hist_error_mc.GetBinContent(i+1))
        except:
            new_hist_error_mc.SetBinContent(i+1, 0.)

    new_hist_error = ROOT.TH1D(f"{region}_{variable}_error", f"{region}_{variable}_error", int(len(x_bins)-1), x_bins)
    for i in range(1, int(len(x_bins))):
        bin_error = math.sqrt(new_hist_error_data.GetBinContent(i)*new_hist_error_data.GetBinContent(i) + new_hist_error_mc.GetBinContent(i)*new_hist_error_mc.GetBinContent(i)) * hist_error.GetBinContent(i)
        new_hist_error.SetBinContent(i, 1.0)
        new_hist_error.SetBinError(i, bin_error)

    hist_line = new_hist_error.Clone()

    new_hist_error.SetFillColor(ROOT.kYellow-7)
    new_hist_error.SetLineColor(ROOT.kYellow-7)
    new_hist_error.SetFillStyle(3144)
    new_hist_error.SetMarkerSize(0)

    hist_line.SetMarkerSize(0)
    hist_line.SetLineColor(ROOT.kBlack)
    hist_line.SetLineWidth(2)
    hist_line.SetLineStyle(3)

    return new_hist_error, hist_line

def set_histogram(hist, variable, region, process):

    try:
        x_bins = hist_configs[variable]["x_bins"]["Combined"]
    except:
        if "Merged" in region:
            x_bins = hist_configs[variable]["x_bins"]["Merged"]
        elif "Resolved" in region:
            x_bins = hist_configs[variable]["x_bins"]["Resolved"]
        else:
            sys.exit("unknown x_bins definition")

    x_bins = array.array("f", x_bins)

    new_hist = ROOT.TH1D(f"{region}_{variable}_{process}", f"{region}_{variable}_{process}", int(len(x_bins)-1), x_bins)

    if process == "data":
        new_hist.SetMarkerStyle(20)
        new_hist.SetMarkerSize(1.2)
        new_hist.SetMarkerColor(ROOT.kBlack)
    elif "MN__equal__" in process: #signal
        new_hist.SetMarkerColor(signal_configs[process]["color"])
        new_hist.SetLineColor(signal_configs[process]["color"])
        new_hist.SetLineWidth(3)
        new_hist.SetLineStyle(8)
    else: #background
        new_hist.SetFillColor(background_configs[process]["color"]) 
        new_hist.SetLineColor(background_configs[process]["color"])

    bins_to_ignore = 1
    if process == "data": 
        if (int(len(x_bins)-1) != hist.GetN()):
            if (int(len(x_bins)-2) != hist.GetN()):
                bins_to_ignore = 2
            else:
                sys.exit(f"error with number of bins : {process} {variable}")
        for i in range(0, int(len(x_bins)-bins_to_ignore)):
            new_hist.SetBinContent(i+1, hist.GetPointY(i))
    else:
        if (int(len(x_bins)-1) != hist.GetNbinsX()):
            if (int(len(x_bins)-2) != hist.GetNbinsX()):
                bins_to_ignore = 2
            else:
                sys.exit(f"error with number of bins : {process} {variable}")
        for i in range(0, int(len(x_bins)-bins_to_ignore)):
            new_hist.SetBinContent(i+1, hist.GetBinContent(i+1))

    return new_hist

def get_legend(hist_backgrounds, hist_data, hist_signals, hist_error):

    legend_up = ROOT.TLegend(.3,.62,.88,.88)
    legend_up.SetBorderSize(0)
    legend_up.SetFillColor(0)
    legend_up.SetFillStyle(0)
    legend_up.SetTextFont(42)
    legend_up.SetTextSize(0.04)
    legend_up.SetNColumns(2)

    for background in reversed(backgrounds):
        hist_background = hist_backgrounds[background]
        legend_background = background
        legend_background = legend_background.replace("__plus__", "+")
        legend_background = legend_background.replace("__comma__", ", ")
        legend_background = legend_background.replace("__space__", " ")
        legend_up.AddEntry(hist_background, legend_background, "f")

    legend_up.AddEntry(hist_data, "Data", "p")

    for signal in reversed(list(hist_signals.keys())):
        hist_signal = hist_signals[signal]
        legend_signal = signal
        legend_signal = legend_signal.replace("MN__equal__", "m_{N} = ")
        legend_signal = legend_signal.replace("GeV", " GeV")
        legend_up.AddEntry(hist_signal, legend_signal, "l")

    legend_up.AddEntry(hist_error, "Total Uncertainty", "f")

    return legend_up

def dress_histograms(histogram, variable, canvas, canvas_pad):

    if (canvas_pad == "up"):
        histogram.SetMinimum(0.1)#histogram.GetMinimum() * 0.1)
        histogram.SetMaximum(histogram.GetMaximum() * 10000.0)
        histogram.GetXaxis().SetLabelSize(0)
        histogram.GetYaxis().SetLabelSize(0.06)#0.1#0.18
        canvas.SetLogy()

    if (canvas_pad == "down"):
        histogram.GetXaxis().SetTitle(hist_configs[variable]["x_label"])
        histogram.GetXaxis().SetLabelSize(0.18)
        histogram.GetXaxis().SetTitleSize(0.16)
        histogram.GetXaxis().SetTitleOffset(1.05)#1.1#1.2
        histogram.GetXaxis().SetNdivisions(505)
        histogram.GetYaxis().SetRangeUser(0.1, 1.9)
        histogram.GetYaxis().SetLabelSize(0.18)
        histogram.GetYaxis().SetNdivisions(504)


def get_canvas(campaign, variable, selection):

    hist_name = f"{campaign}_{variable}_{selection}"

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
    if campaign == "2016preVFP":
        latex_lumi.DrawLatex(0.73, 0.96, "19.5 fb^{-1} (13 TeV)")
    if campaign == "2016postVFP":
        latex_lumi.DrawLatex(0.73, 0.96, "16.8 fb^{-1} (13 TeV)")
    if campaign == "2017":
        latex_lumi.DrawLatex(0.73, 0.96, "41.5 fb^{-1} (13 TeV)")
    if campaign == "2018":
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
    latex_ratio.DrawLatex(0.065, 0.082, "Obs./Pred.")

    return canvas, canvas_up, canvas_down

def main():

    campaigns = os.listdir("workspace")
    for campaign in campaigns:
        variables = os.listdir(f"workspace/{campaign}")
        for variable in variables:
            draw_histogram(campaign, variable)

if __name__ == "__main__":

    main()
