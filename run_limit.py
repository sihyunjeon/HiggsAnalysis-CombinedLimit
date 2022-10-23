#!/usr/bin/env python3
import os

cards = os.listdir("cards")

for card in cards:
    os.system(f"combine -M AsymptoticLimits --rMin -5 --run blind -d cards/{card} > {card}.log")
#    print (f"combine -M AsymptoticLimits --rMin -5 --run blind")# -d {card}")

