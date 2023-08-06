# Python example script to prepare databases including a directory of
# precalculated densities

import os
from nucdens import access
import glob
import re 

input_dir="/p/scratch/cias-4/le/ncsmdensity/onebody-density-6Li"


comptondf=access.database(workdir=os.environ["SCRATCH"]+"/densityone")


file_list=glob.glob(input_dir+"/*.dat")
specs={}
specs["kind"]="one"
specs["srg"]="3body"              

specs["lsummax"]=0
specs["lmax"]=6
specs["j12max"]=5
specs["MTtot"]=0 # twice MT
specs["np12a"]=0 # np12 is not relevant in one-body case
specs["np12b"]=0

specs["c1"]=-1.23
specs["c3"]=-4.65
specs["c4"]=3.28
specs["cd"]=0.89180
specs["ce"]=-0.38595

for file_name in file_list:
    print(file_name)
    result=re.search(r"onebody-density-(.*?)-J=(.*?)-T=(.*?)-NN=(.*?)-ostat=(.*?)-cutnnum=(.*?)-3N=(.*?)-Ntotmax=(.*?)-omegaHO=(.*?)-lambda=(.*?)-omega=(.*?)-theta=(.*?).dat",file_name)

    
    if result.group(1)=="6Li":
        specs["N"]=3
        specs["Z"]=3
        
    specs["Jtot"]=2*int(result.group(2))  # store twice angular momentum and isospin 
    specs["Tmax"]=2*int(result.group(3))

    if result.group(4)=="N4LOSMS+":
        specs["nninter"]="sms"
        specs["order"]="N4LO+"
        if int(result.group(5))!=5:
            raise(ValueError("inconsistent ostat ?"))


    cutnum=int(result.group(6))
    specs["cutoff"]=[400,450,500,550][cutnum-1]

    if result.group(7)=="N2LO450":
        specs["tnf"]="n2lo"
        specs["tnfcut"]=450
    else:
       raise ValueError("consistent tnf") 
                  
    specs["Nmax"]=int(result.group(8))                
    specs["OmegaHO"]=float(result.group(9))

    specs["srgval"]=float(result.group(10))              
                   
    specs["omega"]=float(result.group(11))
    specs["theta"]=float(result.group(12))            


    


    comptondf.add_file(filename=file_name,**specs)

print(comptondf.pddf.to_latex())


print("Then merge with previous database ... ")
    

compton2bodydf=access.database(workdir=os.environ["SCRATCH"]+"/densitytwo")

comptondf.merge(compton2bodydf)
print(comptondf.pddf.to_latex())

