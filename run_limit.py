#!/usr/bin/env python3
import os
import sys

masses_to_prepare = []
masses = ["500", "600", "700", "800", "1000", "1200", "1500"]
for mass in masses:
    masses_to_prepare.append(f"MN__equal__{mass}GeV.txt")

cwd = os.getcwd()

def run_limit(mass, card_type):

    path = f"{cwd}/workspace/{card_type}/"
    log_path = f"{cwd}/logs/cards/{card_type}/"
    if not os.path.exists(log_path):
        os.system(f"mkdir -p {log_path}")
    cards = os.listdir(path)

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

    combinecards_electron = f"{combinecards_electron} > {card_type}Electron_{mass}"
    combinecards_muon = f"{combinecards_muon} > {card_type}Muon_{mass}"

    os.chdir(path)

    os.system(combinecards_electron)
    os.system(combinecards_muon)

    os.system(f"combine -M AsymptoticLimits --rMin -5 --run blind -d {card_type}Electron_{mass} --name Electron{mass.replace('.txt', '')} &> {card_type}Electron_{mass.replace('.txt', '.log')}")
    os.system(f"combine -M AsymptoticLimits --rMin -5 --run blind -d {card_type}Muon_{mass} --name Muon{mass.replace('.txt', '')} &> {card_type}Muon_{mass.replace('.txt', '.log')}")
    os.system(f"mv {card_type}*.log {log_path}/")

    os.chdir(cwd)

if __name__ == "__main__":

    for mass in masses_to_prepare:
        for card_type in ["Merged", "Resolved", "Combined"]:
            run_limit(mass, card_type)
