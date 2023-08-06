# Python example script to prepare databases including a directory of
# precalculated densities

import os
from nucdens import access
import glob
import re 

input_dir="/p/scratch/cias-4/le/ncsmdensity/onebody-density-6Li"


comptononedf=access.database(workdir=os.environ["SCRATCH"]+"/densityone")
comptontwodf=access.database(workdir=os.environ["SCRATCH"]+"/densitytwo")

print("First one-body ...")
print(comptononedf.pddf.to_latex())

print("\n\n\n then two-body ...")
print(comptontwodf.pddf.to_latex())
