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
    ncdy_values = {}
    ccdy_values = {}
    vbf_values = {}

    for this_file in data:
        if "Mu" in this_file: continue
        mass = int(this_file.split("_MN")[1].split("_TuneCP5")[0])
        channel = this_file.split("_TypeIHeavyN")[0]
        categories[channel][mass] = float(open(f"{hist_name}/{this_file}").readlines()[0].strip())
        masses.append(mass)
        total_values[mass] = 0.
        ncdy_values[mass] = 0.
        ccdy_values[mass] = 0.
        vbf_values[mass] = 0.

    masses = sorted(set(masses))
    graphs = {}
    graphs_ratio = {}

    for channel in list(categories.keys()):
        x_values = array.array('d')
        y_values = array.array('d')
        for mass in masses:
            x_values.append(mass)
            y_values.append(categories[channel][mass])
            total_values[mass] = total_values[mass] + categories[channel][mass]
            if channel in ["WtoLNtoLNuHtoLNuBB_VBF", "WtoLNtoLNuZtoLNuBB_VBF", "WtoLNtoLNuZtoLNuQQ_VBF"]:
                vbf_values[mass] = vbf_values[mass] + categories[channel][mass]
            elif channel in ["WtoLNtoLNuHtoLNuBB", "WtoLNtoLNuZtoLNuBB", "WtoLNtoLNuZtoLNuQQ"]:
                ccdy_values[mass] = ccdy_values[mass] + categories[channel][mass]
            elif channel in ["ZtoNuNtoNuLWtoNuLQQ"]:
                ncdy_values[mass] = ncdy_values[mass] + categories[channel][mass]
            else:
                print ("wtf is this")

            if mass == 500 :
                print (mass, channel, total_values[mass],categories[channel][mass])

#        graph = ROOT.TGraph( len(masses), x_values, y_values )
#        graphs[channel] = graph.Clone()

    y_total_values = array.array('d')
    y_ccdy_values = array.array('d')
    y_ncdy_values = array.array('d')
    y_vbf_values = array.array('d')
    y_total_ratios = array.array('d')
    y_ccdy_ratios = array.array('d')
    y_ncdy_ratios = array.array('d')
    y_vbf_ratios = array.array('d')

    for mass in masses:
        y_total_values.append(total_values[mass])
        y_ccdy_values.append(ccdy_values[mass])
        y_ncdy_values.append(ncdy_values[mass])
        y_vbf_values.append(vbf_values[mass])
        y_total_ratios.append(1.0)
        y_ccdy_ratios.append(ccdy_values[mass]/total_values[mass])
        y_ncdy_ratios.append(ncdy_values[mass]/total_values[mass])
        y_vbf_ratios.append(vbf_values[mass]/total_values[mass])

    graphs["total"] = dress_graph("total", masses, x_values, y_total_values)
    graphs["ccdy"] = dress_graph("ccdy", masses, x_values, y_ccdy_values)
    graphs["ncdy"] = dress_graph("ncdy", masses, x_values, y_ncdy_values)
    graphs["vbf"] = dress_graph("vbf", masses, x_values, y_vbf_values)
    graphs_ratio["total"] = dress_graph("total", masses, x_values, y_total_ratios)
    graphs_ratio["ccdy"] = dress_graph("ccdy", masses, x_values, y_ccdy_ratios)
    graphs_ratio["ncdy"] = dress_graph("ncdy", masses, x_values, y_ncdy_ratios)
    graphs_ratio["vbf"] = dress_graph("vbf", masses, x_values, y_vbf_ratios)

    multigraph = ROOT.TMultiGraph()
    i_key = 0
    for key in list(graphs.keys()):
        if key == "total":
            continue
        multigraph.Add(graphs[key])
        i_key = i_key + 1
    multigraph.Add(graphs["total"])

    multigraph_ratio = ROOT.TMultiGraph()
    i_key = 0
    for key in list(graphs_ratio.keys()):
        if key == "total":
            continue
        multigraph_ratio.Add(graphs_ratio[key])
        i_key = i_key + 1


    canvas, canvas_up, canvas_down = get_canvas(hist_name)

    canvas_up.cd()
    multigraph.Draw("AC")
    multigraph.SetMinimum(1.e-8)
    multigraph.SetMaximum(.1)
    multigraph.GetXaxis().SetLabelSize(0)
    multigraph.GetYaxis().SetLabelSize(0.05)
    canvas_up.SetLogy()

    canvas_down.cd()
    multigraph_ratio.Draw("AC")
    multigraph_ratio.SetMinimum(0.)
    multigraph_ratio.SetMaximum(1.)

    multigraph_ratio.GetXaxis().SetLabelSize(0.18)
    multigraph_ratio.GetXaxis().SetTitle("m_{N} [GeV]")
    multigraph_ratio.GetXaxis().SetTitleSize(0.16)
    multigraph_ratio.GetXaxis().SetTitleOffset(1.05)#1.1#1.2
    multigraph_ratio.GetXaxis().SetNdivisions(505)

    multigraph_ratio.GetYaxis().SetRangeUser(0., 1.)
    multigraph_ratio.GetYaxis().SetLabelSize(0.11)
    multigraph_ratio.GetYaxis().SetNdivisions(504)

    canvas_up.cd()
    legend = get_legend(graphs)
    legend.Draw("same")

    canvas.SaveAs(f"outputs/hists/theory/{hist_name}.pdf")

def dress_graph(signal_type, masses, x_values, y_values):

    graph = ROOT.TGraph( len(masses), x_values, y_values )

    graph.SetLineColor(signals[signal_type]["color"])
    graph.SetLineWidth(3)
#    graph.SetLineStyle(signals[signal_type]["line_style"])
    graph.SetMarkerColor(signals[signal_type]["color"])
    graph.SetMarkerStyle(signals[signal_type]["marker_style"])
    graph.SetMarkerSize(2)

    return graph

def get_legend(graphs):

    legend = ROOT.TLegend(.2,.1,.7,.4)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
#    legend.SetTextColor(signals[key]["color"])
#    legend.SetNColumns(2)

    for key in list(graphs.keys()):
        legend_graph = graphs[key]
        legend_key = signals[key]["legend"]
        legend.AddEntry(legend_graph, legend_key, "l")

    return legend

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
    latex_hist.SetTextSize(0.04)
    latex_hist.SetTextFont(42)
    latex_hist.SetTextAngle(90)
    latex_hist.DrawLatex(0.05, 0.42, "#sigma(pp #rightarrow #mu#nuq#bar{q} or #mu#nub#bar{b})/|V_{#muN}|^{2} [pb]")

    latex_ratio = ROOT.TLatex()
    latex_ratio.SetNDC()
    latex_ratio.SetTextSize(0.042)
    latex_ratio.SetTextFont(42)
    latex_ratio.SetTextAngle(90)
    latex_ratio.DrawLatex(0.05, 0.12, "Ratio")

    return canvas, canvas_up, canvas_down

signals = {
    "total" : {
        "marker_style" : 20,
        "line_style" : 1,
        "color" : ROOT.kBlack,
        "legend" : "Total"
    },
    "ccdy" : {
        "marker_style" : 21,
        "line_style" : 3,
        "color" : ROOT.kRed-4,
        "legend" : "Charged Current DY"
    },
    "ncdy" : {
        "marker_style" : 22,
        "line_style" : 6,
        "color" : ROOT.kBlue-4,
        "legend" : "Neutral Current DY"
    },
    "vbf" : {
        "marker_style" : 23,
        "line_style" : 9,
        "color" : ROOT.kSpring-8,
        "legend" : "#gamma Induced VBF"
    },

}

def main():

    if not os.path.exists(f"outputs/hists/theory/"):
        os.system(f"mkdir -p outputs/hists/theory/")

    draw_histogram("crosssections")


if __name__ == "__main__":

    main()
