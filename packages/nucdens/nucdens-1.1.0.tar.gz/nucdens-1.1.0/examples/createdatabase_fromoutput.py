# this script creates from the files in a directory a databased of wave function files
# files are compressed when added, all files of the input directory need to be proper
# wave functions, files are added to the online database 

from nucdens import access
import os
import glob
import re
import fileextract as fe
import re

tolerance=1e-8
uploaddir=os.environ["SCRATCH"]+"/densdbupload"
workdir=os.environ["SCRATCH"]+"/densdbtest/"
inputdir=os.environ["HOME"]+"/data/compton-density-3he-3h-chsfr/000003/"

# create database, download one if existent
densdb=access.database(workdir=workdir)

filelist=glob.glob(inputdir+'0*submit/work/comp*out')

for file_in in filelist:
  # get the run number
  print("Working on file: ",file_in) 
  labels=fe.getComptonDensity(file_in)
  dens2bfile=labels["rho2bname"] # .replace("/p/scratch/cjikp03",os.environ["SCRATCH"])
  dens1bfile=labels["rho1bname"] # .replace("/p/scratch/cjikp03",os.environ["SCRATCH"])
  del labels["rho1bname"]
  del labels["rho2bname"]
  del labels["WAVEIN"]
  
  # now first add the 2body density
  labels["kind"]="two"
  print("Read file: ",dens2bfile)
  densin=access.densfile2b(dens2bfile,printlevel=1)
  # augment by info from output file 
  hashnamewf=densdb.add_file(filename=dens2bfile,**labels)  
  # compress file using the hashname 
  densin.compress(workdir+hashnamewf,tolerance,printlevel=1)
  # read in again to check basic properties 
  densin=access.densfile2b(workdir+hashnamewf,printlevel=1)
    
  # then add the 1body density 
  labels["kind"]="one"
  print("Read file: ",dens1bfile)
  densin=access.densfile1b(dens1bfile,printlevel=1)
  # augment by info from output file 
  hashnamewf=densdb.add_file(filename=dens1bfile,**labels)  
  
#print complete list of files
print(densdb.pddf)

# now create upload ready version 
densdb.prep_upload(uploaddir)






