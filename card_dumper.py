#!/usr/bin/env python3
import os
import sys
import uproot
import numpy

from configs.singlelepton_analysis.systematic_configs import systematic_configs

campaign = sys.argv[1]

if not campaign in ["2016preVFP", "2016postVFP", "2017", "2018"]:
    sys.exit(f'{campaign} not in ["2016preVFP", "2016postVFP", "2017", "2018"]')

rootfiles_path = f"{os.getcwd()}/outputs/yields/{campaign}"
cards_path = f"{os.getcwd()}/outputs/cards/{campaign}"
if not os.path.exists(cards_path):
    os.system(f"mkdir -p {cards_path}")

rootfiles = []

for rootfile in os.listdir(rootfiles_path):

    if not rootfile.endswith(".root"):
        continue

    if ("SignalRegion" in rootfile) or (("ControlRegion" in rootfile) and ("Selection" in rootfile)):
        print (f"Including {rootfile}")
        rootfiles.append(rootfile)
    else:
        print (f"Skipping {rootfile}")
        continue


def write_data_card(rootfile):

    file_name = rootfile.replace("_masst_recopriboson.root", "")

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


        for signal_name in signal_names:
            card_path = f"{cards_path}/{signal_name}_{file_name}.txt"
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
            card_write.write(f"{file_name} autoMCStats 0 0 1\n")
            if "Resolved" in file_name:
                card_write.write(f"rate_ResolvedDomTT_{campaign} rateParam {file_name} Top__space__Pair 1\n")
                card_write.write(f"rate_ResolvedDomW_{campaign} rateParam {file_name} V__plus__Jets 1\n")
            if "Merged" in file_name:
                card_write.write(f"rate_MergedDomTT_{campaign} rateParam {file_name} Top__space__Pair\n")
                card_write.write(f"rate_MergedDomW_{campaign} rateParam {file_name} V__plus__Jets\n")

            card_write.close()

for rootfile in rootfiles:
    write_data_card(rootfile)


