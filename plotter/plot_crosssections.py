#!/usr/bin/env python3
import ROOT
ROOT.gROOT.SetBatch(True)

import os
import sys
import math
import array
import argparse

from include.args_parser import args

import configs.singlelepton_analysis.root_configs

def draw_histogram(hist_name):

    data = os.listdir(hist_name)

    categories = {}
    for this_file in data:
        if "Mu" in this_file: continue
        channel = this_file.split("_TypeIHeavyN")[0]
        categories[channel] = {}

    masses = []
    total_values = {}
    for this_file in data:
        if "Mu" in this_file: continue
        mass = int(this_file.split("_MN")[1].split("_TuneCP5")[0])
        channel = this_file.split("_TypeIHeavyN")[0]
        categories[channel][mass] = float(open(f"{hist_name}/{this_file}").readlines()[0].strip())
        masses.append(mass)
        total_values[mass] = 0.
    print (categories)
    masses = sorted(set(masses))
    graphs = {}

    for channel in list(categories.keys()):
        x_values = array.array('d')
        y_values = array.array('d')
        for mass in masses:
            x_values.append(mass)
            y_values.append(categories[channel][mass])
            total_values[mass] = total_values[mass] + categories[channel][mass]
            if mass == 500 : print (mass, channel, total_values[mass],categories[channel][mass])
        graph = ROOT.TGraph( len(masses), x_values, y_values )
        graphs[channel] = graph.Clone()

    y_total_values = array.array('d')
    for mass in masses:
         print (mass, total_values[mass])

         y_total_values.append(total_values[mass])

    graphs["total"] = ROOT.TGraph( len(masses), x_values, y_total_values).Clone()
    graphs["total"].SetLineColor(ROOT.kBlack)
    graphs["total"].SetLineWidth(2)
    graphs["total"].SetMarkerColor(ROOT.kBlack)
    graphs["total"].SetMarkerStyle(2)
    graphs["total"].SetMarkerSize(2)

    multigraph = ROOT.TMultiGraph()
    multigraph.Add(graphs["total"])
    i_key = 0
    for key in list(graphs.keys()):
        if key == "total":
            continue
        graphs[key].SetLineColor(hist_configs[i_key]["color"])
        graphs[key].SetLineWidth(2)
        graphs[key].SetMarkerColor(hist_configs[i_key]["color"])
        graphs[key].SetMarkerStyle(hist_configs[i_key]["marker_style"])
        graphs[key].SetMarkerSize(2)
        multigraph.Add(graphs[key])
        i_key = i_key + 1

    canvas, canvas_up, canvas_down = get_canvas(hist_name)
    canvas_up.cd()
    multigraph.Draw("APC")
    canvas_up.SetLogy()
    canvas.SaveAs(f"outputs/hists/theory/{hist_name}.pdf")


def get_legend(hist_backgrounds, hist_data):

    legend = ROOT.TLegend(.75,.60,.85,.85)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)

def dress_histograms(histogram, hist, canvas_up, canvas_down, canvas_pad):

    if (canvas_pad == "up"):
        histogram.SetMinimum(0.1)
        histogram.SetMaximum(histogram.GetMaximum() * 10.)
        canvas_up.SetLogy()

    if (canvas_pad == "down"):
        histogram.GetXaxis().SetTitle(hists[hist]["x_label"])
        histogram.GetXaxis().SetLabelSize(0.14)
        histogram.GetXaxis().SetTitleSize(0.12)
        histogram.GetYaxis().SetRangeUser(0.55, 1.45)
        histogram.GetYaxis().SetLabelSize(0.11)
        histogram.GetYaxis().SetNdivisions(510)

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

    latex_hist = ROOT.TLatex()
    latex_hist.SetNDC()
    latex_hist.SetTextSize(0.03)
    latex_hist.SetTextFont(42)
    latex_hist.SetTextAngle(90)
    latex_hist.DrawLatex(0.065, 0.83, "#sigma/|V_{lN}|^2 [pb]")

    latex_ratio = ROOT.TLatex()
    latex_ratio.SetNDC()
    latex_ratio.SetTextSize(0.03)
    latex_ratio.SetTextFont(42)
    latex_ratio.SetTextAngle(90)
    latex_ratio.DrawLatex(0.065, 0.07, "Ratio")

    return canvas, canvas_up, canvas_down

hist_configs = {
    0 : {
        "marker_style" : 20,
        "color" : ROOT.kRed-4,
    },
    1 : {
        "marker_style" : 25,
        "color" : ROOT.kOrange-3,
    },
    2 : {
        "marker_style" : 22,
        "color" : ROOT.kYellow-3,
    },
    3 : {
        "marker_style" : 32,
        "color" : ROOT.kGreen+1,
    },
    4 : {
        "marker_style" : 24,
        "color" : ROOT.kAzure-3,
    },
    5 : {
        "marker_style" : 21,
        "color" : ROOT.kBlue+2,
    },
    6 : {
        "marker_style" : 26,
        "color" : ROOT.kViolet+1,
    },

}

def main():

    if not os.path.exists(f"outputs/hists/theory/"):
        os.system(f"mkdir -p outputs/hists/theory/")

    draw_histogram("crosssections")


if __name__ == "__main__":

    main()
