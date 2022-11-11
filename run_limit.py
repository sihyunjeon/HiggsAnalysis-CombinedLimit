#!/usr/bin/env python3
import os
import sys

masses_to_prepare = []
masses = ["500", "600", "700", "800", "1000", "1200", "1500", "2000"]
for mass in masses:
    masses_to_prepare.append(f"MN__equal__{mass}GeV.txt")

cwd = os.getcwd()

path = f"{cwd}/workspace/Combined/"
cards = os.listdir(path)

def run_limit(mass):

    cards_to_run = []

    combinecards_electron = "combineCards.py"
    combinecards_muon = "combineCards.py"


    for card in cards:
        if not mass in card:
            continue
        if not card.endswith(".txt"):
            continue
        if "Combined" in card:
            continue

        if "Electron" in card :
            combinecards_electron = f"{combinecards_electron} {card}"
        if "Muon" in card :
            combinecards_muon = f"{combinecards_muon} {card}"

    combinecards_electron = f"{combinecards_electron} > CombinedElectron_{mass}"
    combinecards_muon = f"{combinecards_muon} > CombinedMuon_{mass}"

    os.chdir(path)

    os.system(combinecards_electron)
    os.system(combinecards_muon)

    os.system(f"combine -M AsymptoticLimits --rMin -5 --run blind -d CombinedElectron_{mass} --name Electron{mass.replace('.txt', '')} &> CombinedElectron_{mass.replace('.txt', '.log')} &")
    os.system(f"combine -M AsymptoticLimits --rMin -5 --run blind -d CombinedMuon_{mass} --name Muon{mass.replace('.txt', '')} &> CombinedMuon_{mass.replace('.txt', '.log')} &")

    os.chdir(cwd)

if __name__ == "__main__":

    for mass in masses_to_prepare:
        run_limit(mass)

