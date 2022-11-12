import os
import sys

campaigns = os.listdir("workspace")
for campaign in campaigns:
    if campaign in ["Combined", "Merged", "Resolved"]: continue
    variables = os.listdir("workspace/" + campaign)
    for variable in variables:

        checkfiles = os.listdir("workspace/" + campaign + "/" + variable + "/")
        for checkfile in checkfiles:
            if not (checkfile.startswith("higgs") and checkfile.endswith(".root")):
                continue
            rerun_zombie = False
            if not os.path.exists("workspace/" + campaign + "/" + variable + "/" + checkfile):
                rerun_zombie = True
            else:
                size = os.path.getsize("workspace/" + campaign + "/" + variable + "/" + checkfile)
                if size < 6000:
                    rerun_zombie = True
            if rerun_zombie:
                copyfile = campaign + "_" + variable + "_" + checkfile.replace("higgsCombine", "").replace(".FitDiagnostics.mH125.root", ".sh")
#                print (copyfile)
                os.system("cp tmp/" + copyfile + " ./tmp_submit.sh")
                os.system("source ./tmp_submit.sh")
                os.system("rm tmp_submit.sh")
