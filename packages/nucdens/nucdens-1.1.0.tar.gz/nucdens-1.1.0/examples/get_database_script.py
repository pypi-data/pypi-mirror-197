# Python example script to prepare databases including a directory of
# precalculated densities

import os
from nucdens import access 


comptondf=access.database(workdir=os.environ["HOME"]+"/work/denstest")

# now cycle through all data
damagedfile=[]
for index,row in comptondf.pddf.iterrows():
    densid=dict(row)
    hashname,uniquename=comptondf.get_file(**densid)
    if densid["kind"]=="two":
      # and compress if two body density 
      density2b=access.densfile2b(hashname,printlevel=1)
      density2b.compress(hashname,1e-6,printlevel=1)
    else:  
      # otherwise just read        
      try:
        density1b=access.densfile1b(hashname,printlevel=1)
      except:
        damagedfile=[index]+damagedfile

for index in damagedfile:
  print("Remove file ",index)
  comptondf.remove_file(index)  

