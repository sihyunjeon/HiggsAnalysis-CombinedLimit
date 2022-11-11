import os
import sys
import argparse

parser = argparse.ArgumentParser()

#parser.add_argument('--input', '-i', required=True,
#                    help='path to the input directory')
parser.add_argument('--campaign', default="2017")
parser.add_argument('--channel', default="Muon")
parser.add_argument('--debug', action="store_true", default=False)
parser.add_argument('--write', action="store_true", default=False)
parser.add_argument('--no_data', action="store_true",
                    help='don\'t draw data points in the plots')
parser.add_argument('--no_signal', action="store_true",
                    help='don\'t draw signal points in the plots')
parser.add_argument('--combine', action="store_true", default=False)

args = parser.parse_args()

#if not os.path.exists(args.input): #FIXME
#    sys.exit(f"error : path {args.input} does not exist")
