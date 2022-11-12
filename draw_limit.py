#!/usr/bin/env python3

import os
import sys
import array
import argparse
import ROOT
import plotter.configs.singlelepton_analysis.root_configs

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--output", dest="output", default="limit")
parser.add_argument("-c", "--channel", dest="channel", default="Muon")
parser.add_argument("-r", "--region", dest="region", default="Combined")

channel = parser.parse_args().channel
region = parser.parse_args().region
output = f"limit_{channel}_{region}"

masses = [500, 600, 700, 800, 1000, 1200, 1500]

#workspace/Combined/CombinedElectron_MN__equal__1000GeV.log

def get_expected_limits():

    limits = {}

    for mass in masses:

        logfile = f"Combined{channel}_MN__equal__{mass}GeV.log"

        limits[mass] = {}

        for region in ["Combined", "Merged", "Resolved"]:
            logfile = f"{region}{channel}_MN__equal__{mass}GeV.log"
            limits[mass][region] = {}
            with open(f"logs/cards/{region}/{logfile}") as read_lines:
                lines = read_lines.readlines()
                for line in reversed(lines):
                    line = line.strip()
                    if " 50.0%" in line: limits[mass][region]["50.0%"] = float(line.split(" < ")[1])
                    if region == "Combined":
                        if " 2.5%" in line: limits[mass][region]["2.5%"] = float(line.split(" < ")[1])
                        if " 16.0%" in line: limits[mass][region]["16.0%"] = float(line.split(" < ")[1])
                        if " 84.0%" in line: limits[mass][region]["84.0%"] = float(line.split(" < ")[1])
                        if " 97.5%" in line: limits[mass][region]["97.5%"] = float(line.split(" < ")[1])

    return limits

def draw_limits(limits):

    x_grids = array.array('d')
    y_grids_exp_2sig_up = array.array('d')
    y_grids_exp_1sig_up = array.array('d')
    y_grids_exp = array.array('d')
    y_grids_exp_1sig_down = array.array('d')
    y_grids_exp_2sig_down = array.array('d')
    y_grids_exp_merged = array.array('d')
    y_grids_exp_resolved = array.array('d')

    for mass in masses:
        x_grids.append(mass)
        y_grids_exp_2sig_up.append(limits[mass]["Combined"]["97.5%"] - limits[mass]["Combined"]["50.0%"])
        y_grids_exp_1sig_up.append(limits[mass]["Combined"]["84.0%"] - limits[mass]["Combined"]["50.0%"])
        y_grids_exp.append(limits[mass]["Combined"]["50.0%"])
        y_grids_exp_1sig_down.append(limits[mass]["Combined"]["50.0%"] - limits[mass]["Combined"]["16.0%"])
        y_grids_exp_2sig_down.append(limits[mass]["Combined"]["50.0%"] - limits[mass]["Combined"]["2.5%"])
        y_grids_exp_merged.append(limits[mass]["Merged"]["50.0%"])
        y_grids_exp_resolved.append(limits[mass]["Resolved"]["50.0%"])

    graph_exp_merged = ROOT.TGraphAsymmErrors(len(masses), x_grids, y_grids_exp_merged, 0, 0, 0, 0)
    graph_exp_merged.SetLineColor(ROOT.kAzure+1)
    graph_exp_merged.SetLineWidth(5)
    graph_exp_merged.SetLineStyle(2)

    graph_exp_resolved = ROOT.TGraphAsymmErrors(len(masses), x_grids, y_grids_exp_resolved, 0, 0, 0, 0)
    graph_exp_resolved.SetLineColor(ROOT.kPink-9)
    graph_exp_resolved.SetLineWidth(5)
    graph_exp_resolved.SetLineStyle(2)

    graph_exp = ROOT.TGraphAsymmErrors(len(masses), x_grids, y_grids_exp, 0, 0, 0, 0)
    graph_exp.SetLineColor(ROOT.kBlack)
    graph_exp.SetLineWidth(5)
    graph_exp.SetLineStyle(2)

    graph_exp_1sig = ROOT.TGraphAsymmErrors(len(masses), x_grids, y_grids_exp, 0, 0, y_grids_exp_1sig_down, y_grids_exp_1sig_up)
    graph_exp_1sig.SetLineColor(ROOT.kGreen+1)
    graph_exp_1sig.SetFillColor(ROOT.kGreen+1)
    graph_exp_1sig.SetMarkerColor(ROOT.kGreen+1)

    graph_exp_2sig = ROOT.TGraphAsymmErrors(len(masses), x_grids, y_grids_exp, 0, 0, y_grids_exp_2sig_down, y_grids_exp_2sig_up)
    graph_exp_2sig.SetLineColor(ROOT.kOrange)
    graph_exp_2sig.SetFillColor(ROOT.kOrange)
    graph_exp_2sig.SetMarkerColor(ROOT.kOrange)

    canvas = ROOT.TCanvas()
    hist_dummy = ROOT.TH1D("hist_dummy", "hist_dummy", 2500, 0., 2500.)
    hist_dummy.SetTitle("")
    hist_dummy.Draw("hist")
    hist_dummy.GetXaxis().SetTitle("m_{N} [GeV]")
    if channel == "Muon":
        hist_dummy.GetYaxis().SetTitle("|V_{#muN}|^{2}")
    elif channel == "Electron":
        hist_dummy.GetYaxis().SetTitle("|V_{eN}|^{2}")
    hist_dummy.GetYaxis().SetTitleSize(0.055)
    hist_dummy.GetXaxis().SetRangeUser(500., 1250.)
    hist_dummy.GetYaxis().SetRangeUser(0.08, 1.0)

    graph_exp_2sig.Draw("3same")
    graph_exp_1sig.Draw("3same")
    graph_exp.Draw("lsame")
    graph_exp_merged.Draw("lsame")
    graph_exp_resolved.Draw("lsame")
    hist_dummy.Draw("axissame")

    legend = ROOT.TLegend(0.55, 0.2, 0.9, 0.40)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.AddEntry(graph_exp, "Expected limit", "l")
    legend.AddEntry(graph_exp_1sig, "68% expected limit", "f")
    legend.AddEntry(graph_exp_2sig, "95% expected limit", "f")

    latex_cms = ROOT.TLatex()
    latex_cms.SetNDC()
    latex_cms.SetTextSize(0.035)
    latex_cms.DrawLatex(0.16, 0.96, "#font[62]{CMS} #font[42]{#it{#scale[0.8]{Preliminary}}}")

    latex_lumi = ROOT.TLatex()
    latex_lumi.SetNDC()
    latex_lumi.SetTextSize(0.035)
    latex_lumi.SetTextFont(42)
    latex_lumi.DrawLatex(0.73, 0.96, "138 fb^{-1} (13 TeV)")

    legend.Draw("same")

#    canvas.SetLogx()
    canvas.SetLogy()
    canvas.SaveAs(f"{output}.pdf")

def main():

    limits = get_expected_limits()
    draw_limits(limits)

if __name__ == "__main__":

    main()
