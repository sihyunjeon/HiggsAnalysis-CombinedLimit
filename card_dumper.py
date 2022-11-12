#!/usr/bin/env python3
import os
import sys
import numpy

from plotter.configs.singlelepton_analysis.systematic_configs import systematic_configs
from plotter.configs.singlelepton_analysis.hist_configs import hist_configs
from plotter.configs.singlelepton_analysis.sample_configs import sample_configs
from plotter.configs.singlelepton_analysis.region_configs import region_configs
from plotter.include.args_parser import args

cwd = os.getcwd()

variables_for_limit = ["masst_recopriboson"]

masses_to_plot = []
masses_to_prepare = []
masses = ["500", "600", "700", "800", "1000", "1200", "1500", "2000"]
for mass in masses:
    masses_to_prepare.append(f"MN__equal__{mass}GeV.txt")
    if mass == "500" or mass == "800" :
        masses_to_plot.append(f"MN__equal__{mass}GeV.txt")

variables = []
for key in list(hist_configs.keys()):
    variables.append(key)

flag_campaign = args.campaign
flag_channel = args.channel
flag_combine = args.combine

rootfiles_path = f"{cwd}/plotter/outputs/yields/{flag_campaign}/"
systematics = {}
systematics_treat = {}
systematics_type = {}
systematics_sample = {}
systematics_campaign = {}
systematics_variation = {}
systematics_special = {}
for syst_source in list(systematic_configs.keys()):
    syst_variation = systematic_configs[syst_source]["variation"]
    syst_type = systematic_configs[syst_source]["type"]
    if syst_variation == "updown" :
        systematics[syst_source] = "1"
        systematics_treat[syst_source] = "shapeN2"
        systematics_type[syst_source] = syst_type
        systematics_variation[syst_source] = syst_variation
    elif syst_variation == "lognormal" :
        systematics[syst_source] = systematic_configs[syst_source][flag_campaign]
        systematics_treat[syst_source] = "lnN"
        systematics_type[syst_source] = syst_type
        systematics_variation[syst_source] = syst_variation
    elif syst_variation == "other":
        syst_name = systematic_configs[syst_source]["name"]
        syst_sample = systematic_configs[syst_source]["sample"]
        systematics_sample[syst_name] = syst_sample
        systematics_type[syst_name] = syst_type
        systematics_variation[syst_name] = syst_variation
        if syst_name == "TopPtReweight":
            systematics[syst_name] = "-"
            systematics_special[syst_name] = "1"
            systematics_treat[syst_name] = "shapeN2"
        elif syst_name == "Scale":
            systematics[syst_name] = "-"
            systematics_special[syst_name] = systematic_configs[syst_source]["value"]
            systematics_treat[syst_name] = "lnN"
        elif syst_name == "PDF":
            systematics[syst_name] = "-"
            systematics_special[syst_name] = systematic_configs[syst_source]["value"]
            systematics_treat[syst_name] = "lnN"

samples = []
for sample_source in sample_configs["background"]:
    if sample_source == "Others": continue
    samples.append(sample_source)
for sample_source in sample_configs["signal"]:
    samples.append(sample_source)

regions = []
for region_source in region_configs[flag_channel]:
    for region_selection in region_configs[flag_channel][region_source]:
        regions.append(f"{region_source}{region_selection}")

def get_process_index(sample):

    if "MN__equal" in sample: return 0
    elif "Top__space__Pair" in sample: return 1
    elif "Single__space__Top" in sample: return 2
    elif "V__plus__Jets" in sample: return 3
    elif "VV__comma__VVV" in sample: return 4
    elif "Others" in sample: return 5
    else:
        sys.exit("unknown process index " + sample)

def dump_cards(variable, region, card_path, rootfile):

    this_rootfile = f"{rootfiles_path}/{rootfile}"

    signals = []
    backgrounds = []
    for sample in samples:
        if not "MN__equal" in sample:
            backgrounds.append(sample)
        else:
            signals.append(sample)

    for signal in signals:
        with open(f"{card_path}/{signal}.txt", "w") as write_file:
            write_file.write("imax 1\n")
            write_file.write("jmax *\n")
            write_file.write("kmax *\n")
            write_file.write("--------------------------------------\n")
            write_file.write(f"shapes * * {rootfiles_path}/{rootfile} $PROCESS;1 $PROCESS_$SYSTEMATIC;1\n")
            write_file.write(f"shapes data_obs * {rootfiles_path}/{rootfile} data;1\n")
            write_file.write("--------------------------------------\n")
            write_file.write(f"bin {region}\n")
            write_file.write("observation -1\n")
            write_file.write("--------------------------------------\n")
            this_bin_line = f"bin {region} "
            this_process_line = f"process {signal} "
            this_index_line = "process 0 "
            this_rate_line = "rate -1 "
            for background in backgrounds:
                this_bin_line = f"{this_bin_line}{region} "
                this_process_line = f"{this_process_line}{background} "
                this_index_line = f"{this_index_line}{get_process_index(background)} "
                this_rate_line = f"{this_rate_line}-1 "
            write_file.write(f"{this_bin_line}\n")
            write_file.write(f"{this_process_line}\n")
            write_file.write(f"{this_index_line}\n")
            write_file.write(f"{this_rate_line}\n")
            write_file.write("--------------------------------------\n")
            for systematic in (systematics.keys()):
                if systematics_type[systematic] == "correlated": this_systematic = systematic
                else: this_systematic = f"{systematic}_{flag_campaign}"
                this_syst_treat = systematics_treat[systematic]
                this_syst_line = f"{this_systematic} {this_syst_treat} "
                try:
                    if "MN__equal" in systematics_sample[systematic]:
                        this_syst_line = f"{this_syst_line}{systematics_special[systematic]} "
                    else:
                        this_syst_line = f"{this_syst_line}{systematics[systematic]} "
                except:
                    this_syst_line = f"{this_syst_line}{systematics[systematic]} "

                for background in backgrounds:
                    if systematics_variation[systematic] == "other":
                        if systematics_sample[systematic] in background:
                            this_syst_value = systematics_special[systematic]
                        else:
                            this_syst_value = systematics[systematic]
                    else:
                        this_syst_value = systematics[systematic]
                    this_syst_line = f"{this_syst_line}{this_syst_value} "
                write_file.write(f"{this_syst_line}\n")
            write_file.write("--------------------------------------\n")
            write_file.write(f"{region} autoMCStats 0 1 1\n")
            if ("ControlRegion" in region):
                if ("DomTT" in region):
                    write_file.write(f"rate_{region}_{flag_campaign} rateParam {region} Top__space__Pair 1\n")
                elif ("DomW" in region):
                    write_file.write(f"rate_{region}_{flag_campaign} rateParam {region} V__plus__Jets 1\n")

def run_combine_for_plot(mass, variable, workspace_path):

    cards_to_convert = os.listdir(workspace_path)
    
    os.chdir(workspace_path)
    
    for card_to_convert in cards_to_convert:
        if not mass in card_to_convert:
            continue
        text2workspace = f"text2workspace.py {card_to_convert} -m 125 -o {card_to_convert.replace('.txt', '.root')}"
        combine = f"combine -M FitDiagnostics {card_to_convert.replace('.txt', '.root')} -m 125 --rMin -5 --rMax 5 --saveShapes --saveWithUncertainties --name {card_to_convert.replace('.txt', '')} > {card_to_convert.replace('.txt', '.log')}"
        os.system(text2workspace)
        sleep_count = 0
        while (not os.path.exists(card_to_convert.replace('.txt', '.root'))):
            sleep_count = sleep_count + 1
            os.system("sleep 2")
            if (sleep_count > 5):
                print(f"sleep count exceeded, issues with {card_to_convert.replace('.txt', '.root')}")
                break
        os.system(combine)

        fix_zombie = f"{cwd}/tmp/{flag_campaign}_{variable}_{card_to_convert.replace('.txt', '.sh')}"
        with open (fix_zombie, "w") as write_zombie:
            write_zombie.write(f"cd {workspace_path}\n")
            write_zombie.write(f"{text2workspace}\n")
            write_zombie.write(f"{combine}\n")
            write_zombie.write(f"cd {cwd}\n")

    os.chdir(cwd)

def combine_cards_for_limit(mass, variable, workspace_path, cards_to_merge, card_type):

    os.chdir(workspace_path)

    combinecards = "combineCards.py"
    for card in cards_to_merge:
        if "Selection" not in card:
            continue
        if card_type == "Combined":
            combinecards = f"{combinecards} {card}"
        elif card_type in card:
            combinecards = f"{combinecards} {card}"
        else:
            continue
    combinecards = f"{combinecards} > {flag_channel}_{flag_campaign}_{variable}_{mass}"
    os.system(combinecards)
    os.system(f"cp {flag_channel}_{flag_campaign}_{variable}_{mass} {cwd}/workspace/{card_type}/")
    
    os.chdir(cwd)

def main():

    cards_path = f"{cwd}/cards/{flag_campaign}/"
    workspaces_path = f"{cwd}/workspace/{flag_campaign}/"
    os.system("mkdir -p workspace/Combined/")
    os.system("mkdir -p workspace/Merged/")
    os.system("mkdir -p workspace/Resolved/")
    os.system("mkdir -p tmp")
    rootfiles = os.listdir(rootfiles_path)

    if not flag_combine:
        for variable in variables:
            for region in regions:
                card_path = f"{cards_path}/{variable}/{region}/"
                if not os.path.exists(card_path):
                    os.system(f"mkdir -p {card_path}")

                for rootfile in rootfiles:
                    if (variable in rootfile) and (region in rootfile):
                        dump_cards(variable, region, card_path, rootfile)

        for variable in variables:
            workspace_path = f"{workspaces_path}/{variable}/"
            if not os.path.exists(workspace_path):
                os.system(f"mkdir -p {workspace_path}")
            for mass in masses_to_prepare:
                for region in regions:
                    card_file_from = f"{cards_path}/{variable}/{region}/{mass}"
                    if os.path.exists(card_file_from):
                        card_file_to = f"{workspace_path}/{region}_{mass}"
                        os.system(f"cp {card_file_from} {card_file_to}")

        for variable in variables:
            workspace_path = f"{workspaces_path}/{variable}/"
            for mass in masses_to_plot:
                run_combine_for_plot(mass, variable, workspace_path)

    else:
        for variable in variables_for_limit:
            workspace_path = f"{workspaces_path}/{variable}/"
            cards_in_workspace = os.listdir(workspace_path)
            for mass in masses_to_prepare:
                cards_to_merge = []
                for card_in_workspace in cards_in_workspace:
                    if not flag_channel in card_in_workspace:
                        continue
                    if mass in card_in_workspace:
                        cards_to_merge.append(card_in_workspace)
                combine_cards_for_limit(mass, variable, workspace_path, cards_to_merge, "Combined")
                combine_cards_for_limit(mass, variable, workspace_path, cards_to_merge, "Merged")
                combine_cards_for_limit(mass, variable, workspace_path, cards_to_merge, "Resolved")


if __name__ == "__main__":

    main()

