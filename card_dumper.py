#!/usr/bin/env python3
import os
import sys
import uproot
import numpy

from configs.singlelepton_analysis.systematic_configs import systematic_configs

cwd = os.getcwd()

try:
    campaigns = [sys.argv[1]]
except:
    campaigns = ["2016preVFP", "2016postVFP", "2017", "2018"]
try:
    variables = [sys.argv[2]]
except:
    variables = ["n_events_weighted", "masst_recopriboson"]

rootfiles_path = ""
cards_path = ""
workspace_path = ""


def check_root_files(variable, campaign):

    global rootfiles_path
    global cards_path
    global workspace_path

    rootfiles = []

    for rootfile in os.listdir(rootfiles_path):

        if (variable in rootfile):

            if not rootfile.endswith(".root"):
                continue

            if (("SignalRegion" in rootfile) or ("ControlRegion" in rootfile)) and ("Selection" in rootfile) :
                print (f"Including {rootfile}")
                rootfiles.append(rootfile)
            else:
                print (f"Skipping {rootfile}")
                continue

    return rootfiles

def write_data_card(rootfile, variable, campaign):

    global rootfiles_path
    global cards_path
    global workspace_path

    file_name = rootfile.replace(".root", "")
    data_cards = {}

    with uproot.open(f"{rootfiles_path}/{rootfile}") as this_rootfile:

        fake_keys = this_rootfile.keys()
        keys = []
        for fake_key in fake_keys:
            store_key = True
            for syst in list(systematic_configs.keys()):
                if syst in fake_key:
                    store_key = False
                    break
            if store_key:
                keys.append(fake_key)

        signal_names = []
        background_names = []
        for key in keys:
            if key.startswith("data"):
                continue

            if key.startswith("MN"):
                signal_names.append(key.replace(';1',''))
            else:
                background_names.append(key.replace(';1',''))

        if not os.path.exists(f"{cards_path}/{variable}"):
            os.system(f"mkdir -p {cards_path}/{variable}")

        for signal_name in signal_names:
            card_path = f"{cards_path}/{variable}/{signal_name}_{file_name}.txt"
            card_write = open(card_path, "w")
            card_write.write("imax 1\n")
            card_write.write("jmax *\n")
            card_write.write("kmax *\n")
            card_write.write("--------------------------------------\n")
            card_write.write(f"shapes * * {rootfiles_path}/{rootfile} $PROCESS;1 $PROCESS_$SYSTEMATIC;1\n")
            card_write.write(f"shapes data_obs * {rootfiles_path}/{rootfile} data;1\n")
            card_write.write("--------------------------------------\n")
            card_write.write(f"bin {file_name}\n")
            card_write.write("observation -1\n")
            card_write.write("--------------------------------------\n")
            card_write.write(f"bin {file_name} ")
            for background_name in background_names:
                card_write.write(f"{file_name} ")
            card_write.write("\n")
            card_write.write(f"process {signal_name} ")
            for background_name in background_names:
                card_write.write(f"{background_name} ")
            card_write.write("\n")
            card_write.write("process 0 ")
            syst_shape_sig = "1 "
            syst_shape_all = "1 "
            for i_process in range(len(background_names)):
                card_write.write(f"{i_process+1} ")
                syst_shape_sig = f"{syst_shape_sig}- "
                syst_shape_all = f"{syst_shape_all}1 "

            card_write.write("\n")
            card_write.write("rate -1 ")
            for i_process in range(len(background_names)):
                card_write.write("-1 ")
            card_write.write("\n")
            card_write.write("--------------------------------------\n")

            for syst in list(systematic_configs.keys()):
                if systematic_configs[syst]["type"] == "shapeyear":
                    card_write.write(f"{syst}_{campaign} shapeN2 {syst_shape_all}\n")
                elif systematic_configs[syst]["type"] == "shape":
                    card_write.write(f"{syst} shapeN2 {syst_shape_all}\n")
                elif systematic_configs[syst]["type"] == "off":
                    continue
                elif systematic_configs[syst]["type"] == "other":
                    syst_type = systematic_configs[syst][campaign].split("__")[0]
                    syst_value = systematic_configs[syst][campaign].split("__")[1] 
                    card_write.write(f"{syst} {syst_type} {syst_value} ")
                    for i_process in range(len(background_names)):
                        card_write.write(f"{syst_value} ")
                    card_write.write("\n")

                else:
                    print (f"Warning : unknown systematic type = {systematic_configs[syst]['type']}")
                    continue
            card_write.write("--------------------------------------\n")
            card_write.write(f"{file_name} autoMCStats 0 1 1\n")
            if "Resolved" in file_name:
                card_write.write(f"rate_ResolvedDomTT_{campaign} rateParam {file_name} Top__space__Pair 1\n")
                card_write.write(f"rate_ResolvedDomW_{campaign} rateParam {file_name} V__plus__Jets 1\n")
            if "Merged" in file_name:
                card_write.write(f"rate_MergedDomTT_{campaign} rateParam {file_name} Top__space__Pair 1\n")
                card_write.write(f"rate_MergedDomW_{campaign} rateParam {file_name} V__plus__Jets 1\n")

            card_write.close()

def merge_data_card(variable, campaign):

    global rootfiles_path
    global cards_path
    global workspace_path

    cards = os.listdir(f"{cards_path}/{variable}/")

    combineCards = "combineCards.py "
  
    channels = ["Electron", "Muon"]

    for channel in channels:
        mass_points = []

        if not os.path.exists(f"{workspace_path}/{variable}/{channel}"):
            os.system(f"mkdir -p {workspace_path}/{variable}/{channel}")

        for card in cards:
            if channel in card:
                os.system(f"mv {cards_path}/{variable}/{card} {workspace_path}/{variable}/{channel}/")
                mass_point = f'{card.split("GeV_")[0]}GeV'

                mass_points.append(mass_point)

        mass_points = set(mass_points)
        for mass_point in mass_points:
            sandbox_path = f"{workspace_path}/{variable}/{channel}/{mass_point}/"
            if not os.path.exists(sandbox_path):
                os.system(f"mkdir -p {sandbox_path}")
            os.chdir(f"{workspace_path}/{variable}/{channel}")
            os.system(f"mv *{mass_point}*{channel}*txt {mass_point}/")

            cards_to_combine = os.listdir(sandbox_path)
            signal_cards = []
            control_cards = []

            for card in sorted(cards_to_combine):
                if "Signal" in card:
                    signal_cards.append(card)
                elif "Control" in card:
                    control_cards.append(card)

            combineCards = "combineCards.py"
            combineCardsMerged = "combineCards.py"
            combineCardsResolved = "combineCards.py"
            for i in range(len(signal_cards)):
                combineCards = f"{combineCards} SIGNAL{i}={signal_cards[i]} "
                if "Merged" in signal_cards[i]:
                    combineCardsMerged = f"{combineCardsMerged} SIGNAL{i}={signal_cards[i]} "
                elif "Resolved" in signal_cards[i]:
                    combineCardsResolved = f"{combineCardsMerged} SIGNAL{i}={signal_cards[i]} "
            for i in range(len(control_cards)):
                combineCards = f"{combineCards} CONTROL{i}={control_cards[i]} "
                if "Merged" in control_cards[i]:
                    combineCardsMerged = f"{combineCardsMerged} CONTROL{i}={control_cards[i]} "
                elif "Resolved" in control_cards[i]:
                    combineCardsResolved = f"{combineCardsMerged} CONTROL{i}={control_cards[i]} "

            os.chdir(f"{workspace_path}/{variable}/{channel}/{mass_point}/")
            os.system(f"{combineCards}  > {mass_point}__{channel}__CombinedFinal.txt")
            os.system(f"{combineCardsMerged}  > {mass_point}__{channel}__MergedFinal.txt")
            os.system(f"{combineCardsResolved}  > {mass_point}__{channel}__ResolvedFinal.txt")

            migrated_cards = os.listdir("./")
            for card in migrated_cards:
                if not "Final" in card:
                    os.system(f"rm {card}")

            os.chdir(sandbox_path)

    os.chdir(cwd)

def write_wrapper():

    global workspace_path

    os.chdir(cwd)

    campaigns = os.listdir("workspace/")
    dict_cards = {}
    keys = {}
    keys["campaign"] = []
    keys["channel"] = []
    keys["mass"] = []
    observable = "masst_recopriboson"
    for campaign in campaigns:
        channels = os.listdir(f"workspace/{campaign}/{observable}/")
        keys["campaign"].append(campaign)
        for channel in channels:
            masses = os.listdir(f"workspace/{campaign}/{observable}/{channel}/")
            keys["channel"].append(channel)
            for mass in masses:
                this_card = f"workspace/{campaign}/{observable}/{channel}/{mass}/{mass}__{channel}__CombinedFinal.txt"
                keys["mass"].append(mass)
#                os.system(f"cp {this_card} tmp_{campaign}_this_card.txt")
#                os.system("combine -M AsymptoticLimits -d tmp_{campaign}_this_card.txt --run blind > logs/{mass}__{channel}__Combined.log")

    for mass in list(keys["mass"]):
        for channel in list(keys["channel"]):
            combineCards = "combineCards.py "
            for campaign in list(keys["campaign"]):
                this_card = f"workspace/{campaign}/{observable}/{channel}/{mass}/{mass}__{channel}__CombinedFinal.txt"
                os.system(f"cp {this_card} tmp_{campaign}_{mass}__{channel}__CombinedFinal.txt")
                combineCards = f"{combineCards} tmp_{campaign}_{mass}__{channel}__CombinedFinal.txt "
            combineCards = f"{combineCards} > {mass}__{channel}__CombinedFinal.txt"
            os.system(combineCards)
            os.system("rm tmp_*__CombinedFinal.txt")

def main():

    global rootfiles_path
    global cards_path
    global workspace_path

    for campaign in campaigns:

        rootfiles_path = f"{cwd}/outputs/yields/{campaign}"
        cards_path = f"{cwd}/outputs/cards/{campaign}"
        workspace_path = f"{cwd}/workspace/{campaign}"

        if not os.path.exists(cards_path):
            os.system(f"mkdir -p {cards_path}")
            os.system(f"mkdir -p {workspace_path}")

        for variable in variables:

            rootfiles = check_root_files(variable, campaign)
            print (" ------------------------------------------------ ")
            print (f" Writing datacard for {campaign} : {variable} ")
            print (" ------------------------------------------------ ")

            for rootfile in rootfiles:

                write_data_card(rootfile, variable, campaign)

            merge_data_card(variable, campaign)

    write_wrapper()

if __name__ == "__main__":

    main()

