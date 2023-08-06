import pandas as pd 
import os
import hashlib
import  paramiko 
from scp import SCPClient
import shutil
import requests
import gzip
import datetime
import re 
import numpy as np
import h5py 
import hdf5plugin 
import fortranformat as ff 
import f90nml


class database:
    """This class defines an object that accesses density files stored online and index in pandas table."""
    
    def  __init__(self,webbase="https://just-object.fz-juelich.de:8080/v1/AUTH_1715b19bd3304fb4bb04f4beccea0cf2/densitystore/",pddf_hdf="densities_table.h5",workdir=""):
        """Initializes the object that gives read and write access to density files
           - webbase url of online storage for files
             in most cases, files will be already uploaded. Uploading is possible using methods defined below. 
           - pddf_hdf filename of pandas data frame containing the local index of the files.
             The table is generated if not available and written density files are added. 
           - workdir working directory for density table and density file downloads    
        """

        # add "/" to filename if required
        if webbase[-1]!="/":
           webbase=webbase+"/"
        if workdir!="":   
          if workdir[-1]!="/":
            workdir=workdir+"/"
                       
        # keep input in object 
        self.pddf_hdf=pddf_hdf
        self.webbase=webbase
        self.workdir=workdir

        if workdir!="" and (not os.path.exists(workdir)):
           os.mkdir(workdir) 

           
        
        # check whether data frame file is available online 
        url = webbase+pddf_hdf
        r=requests.get(url, stream=True)
        try:
          r.raise_for_status()
          table_online=True
        except requests.HTTPError:
          table_online=False

        print("table_online:",table_online)

        # check whether table is locally available

        table_local=os.path.exists(workdir+pddf_hdf)

        print("table_local:",table_local)

        # use local file if available 
        # download table if online available
        # or generate empty one if neither online nor offline available

        if table_online and not table_local:
           self._download_file_(url,workdir)    
           print("Table file is downloaded: ",url)
           table_local=True 

        
        # if file could not be downloaded and is not available
        # create an empty table otherwise load  table

        if table_local:
          self.pddf=pd.read_hdf(workdir+pddf_hdf, "/densityfiles") 
          print("Read in file: ",workdir+pddf_hdf)
          # and if it came from online sources, set local flags to false
          if table_online:
            self.pddf["localavail"]=False
            self.pddf["localonly"]=False
        else:
          self.pddf=pd.DataFrame()
          savedf=self.pddf.copy(deep=True)
          savedf["localavail"]=False
          savedf["localonly"]=False
          savedf.to_hdf(self.workdir+self.pddf_hdf, key='densityfiles', mode='w')
          print("Generated empty table ...")

        
# adapted from https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    def _download_file_(self,url,workdir):
        """Auxiliary routine to download a file given by url to the workdir"""
       
        local_filename = workdir+url.split('/')[-1]
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
         r.raise_for_status()
         with open(local_filename, 'wb') as f:
           for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
        return local_filename


    def add_file(self,filename=None,**labels):
        """This routine adds a file to the data base locally
           filename - absolute path to local file
           labels should be given according to standard set (see in _prep_label_).
           returns hashname of the file
        """

        # prepare dictionary specifying the case wanted
        # also does some basic checks of consistency 
        specs=self._prep_label_(**labels)

        # prepare unique file name for internal use

        uniquefilename,hashname=self._unique_filename_(specs)
        
        # check for file in existing data base
        # combine spects to a df selection

        try:
          select=(self.pddf["kind"]==specs["kind"])
          for key, value in specs.items():
            select &= (self.pddf[key]==value) 
          if len(self.pddf.loc[select]) > 0:
             densitypresent=True
          else:   
             densitypresent=False
        except:
          # assume empty frame   
          densitypresent=False

        if densitypresent:  
          raise ValueError("Density is already present!")
      
        # now check whether the hash is already used
        # and prepare flag to mark files that are only local
        
        specs["hashname"]=hashname
        specs["uniquefilename"]=uniquefilename
        specs["localonly"]=True
        specs["localavail"]=True
        specs["addtime"]=pd.to_datetime('now')
        specs["moditime"]=pd.to_datetime(datetime.datetime.fromtimestamp(os.path.getmtime(filename)))
        
        try:
          select=(self.pddf["hashname"]==specs["hashname"])
          if len(self.pddf.loc[select]) > 0:
             densitypresent=True
          else:   
             densitypresent=False
        except:
          # assume empty frame   
          densitypresent=False
          
        if densitypresent:  
          raise ValueError("hashname is already present! This is an issue ... ")

        # now add file to database
        # first copy to working directory
        shutil.copy(filename,self.workdir+hashname)
        # then add row to data base
        self.pddf=self.pddf.append(specs,ignore_index=True)
        # and save table to disc 
        savedf=self.pddf.copy(deep=True)
        savedf.to_hdf(self.workdir+self.pddf_hdf, key='densityfiles', mode='w')

        # returns hashed name of the file
        return hashname 

    def _prep_label_(self,**labels):
            """This method augments the labels by a standard set of labels given as
               shown in source code. Some basic checks of the file labels are performed. 
            """
            standard_labels={'Z':0,'N':0,"E[MeV]":0.0,
              'NP12A':0, 'NP12B':0, 'NP12':0, 'P12A':0, 'P12B':0,'P12C':0,
              'NP34A':0, 'NP34B':0, 'NP34':0, 'P34A':0, 'P34B':0,'P34C':0,
              'NP3A':0, 'NP3B':0, 'NP3':0, 'P3A':0, 'P3B':0, 'P3C':0,
              'NQ4A':0, 'NQ4B':0, 'NQ4':0, 'Q4A':0, 'Q4B':0, 'Q4C':0,
              'NQA':0, 'NQB':0, 'NQ':0, 'QA':0, 'QB':0, 'QC':0,
              'NPTA':0, 'NPTB':0,'NPT':0, 'PTA':0, 'PTB':0, 'PTC':0,
              'NEA':0, 'NEB':0, 'NE':0, 'EA':0, 'EB':0, 'EC':0,
              'NX':0,
              'taumax':0, 'lsummax':0,'lmax':0, 'j12max':0, 'l3max':0,'l4max':0,'lammax':0,'MTtot':0, 'Jtot':0,
              'MODENN':'none', 'orderNN':'none','LambdaNN':0.0, 'potnr':0, 'empotnr':0,
              'lam3NF':0.0, 'c1':0.0, 'c3':0.0, 'c4':0.0, 'cd':0.0, 'ce':0.0,
              'cE1':0.0, 'cE2':0.0, 'cE3':0.0, 'cE4':0.0, 'cE5':0.0, 'cE6':0.0, 'cE7':0.0, 'cE8':0.0, 'cE9':0.0, 'cE10':0.0,
              'tnforder':'no3nf','j12max3nf':0,'j3max3nf':0,
              'relcalc':0,
              'nnsrg':0, 'tnfsrg':0, 'lambdaSRGNN':0.0,'lambdaSRG3N':0.0, 'potbareNN':0, 'potbareNNTNF':0, 'ostatSRGNN':0, 'ostatSRGTNF':0,
              'cutnumSRGNN':0.0, 'cutnumSRGTNF':0.0,'omega':0.0, 'theta':0.0,
              'j12maxdens':0, 'taumaxdens':0, 'lmaxdens':0, 'nphitilde':0, 'nxtilde':0, }
        
            out_label={**standard_labels,**labels}

            # remove entries for uniquefilename,localonly,localavail,addtime,moditime
            try:
              del out_label['uniquefilename']
            except:
              pass  
            try:
              del out_label['localonly']
            except:
              pass  
            try:
              del out_label['localavail']
            except:
              pass  
            try:
              del out_label['addtime']
            except:
              pass  
            try:
              del out_label['moditime']
            except:
              pass  

            try:
              out_label["MTtot"]=out_label["mt4"] 
            except:
              pass  
            try:
              out_label["Jtot"]=out_label["j4"]  
            except:
              pass  
          # remove out_label to shorten dataset, keep energy 
            try:
              del out_label["H1[MeV]"]
            except:
              pass  
            try:
              del out_label["H2[MeV]"]
            except:
              pass  
            try:
              del out_label["ECSB[MeV]"]
            except:
              pass  
            try:
              del out_label["T[MeV]"]
            except:
              pass  
            try:
              del out_label["VNN1[MeV]"]
            except:
              pass  
            try:
              del out_label["VNN2[MeV]"]
            except:
              pass  
            try:
              del out_label["V3N[MeV]"]
            except:
              pass  
            try:
              del out_label["CSB[keV]"]
            except:
              pass  
            try:
              del out_label["NORM31"]
            except:
              pass  
            try:
              del out_label["NORM22"]
            except:
              pass  
            try:
              del out_label["P(S)[%]"]
            except:
              pass  
            try:
              del out_label["P(P)[%]"]
            except:
              pass  
            try:
              del out_label["P(D)[%]"]
            except:
              pass  
            try:
              del out_label["P(p)[%]"]
            except:
              pass  
            try:
              del out_label["P(n)[%]"]
            except:
              pass  
            try:
              del out_label["P(pp)[%]"]
            except:
              pass  
            try:
              del out_label["P(np)[%]"]
            except:
              pass  
            try:
              del out_label["P(nn)[%]"]
            except:
              pass  
            try:
              del out_label["r(p)[fm]"]
            except:
              pass  
            try:
              del out_label["r(n)[fm]"]
            except:
              pass  
            try:
              del out_label["r(NN)[fm]"]
            except:
              pass  
            try:
              del out_label["ETA"]
            except:
              pass  
            try:
              del out_label["DEV"]
            except:
              pass  
            try:
              del out_label["mt4"]
            except:
              pass  
            try:
              del out_label["j4"]   
            except:
              pass  
          
       
            # check the grid point numbers to find sums, if necessary 
            if out_label['NP12A']+out_label['NP12B']!=0:
               out_label['NP12']=out_label['NP12A']+out_label['NP12B']   
            if out_label['NP3A']+out_label['NP3B']!=0:
               out_label['NP3']=out_label['NP3A']+out_label['NP3B']   
            if out_label['NQ4A']+out_label['NQ4B']!=0:
               out_label['NQ4']=out_label['NQ4A']+out_label['NQ4B']   
            if out_label['NQA']+out_label['NQB']!=0:
               out_label['NQ']=out_label['NQA']+out_label['NQB']   
            if out_label['NP34A']+out_label['NP34B']!=0:
               out_label['NP34']=out_label['NP34A']+out_label['NP34B']   
            if out_label['NPTA']+out_label['NPTB']!=0:
               out_label['NPT']=out_label['NPTA']+out_label['NPTB']         
            if out_label['NEA']+out_label['NEB']!=0:
               out_label['NE']=out_label['NEA']+out_label['NEB']         

            # make all str lower characters 
            for key in out_label.keys():    
              if type(out_label[key])==type('test'):
                 out_label[key]=out_label[key].lower()

            if not (out_label["MODENN"] in ["av18","chsms","cdbonn","ibm189","chsfr"]):
               raise(ValueError("'MODENN' not defined"))
            if not (out_label["tnforder"] in ["no3nf","n2lo"]):
               raise(ValueError("'tnforder' not defined"))
            if (out_label["N"] != int(out_label["N"])) or (out_label["N"] < 1) :
               raise(ValueError("'N' not defined"))
            if (out_label["Z"] != int(out_label["Z"])) or (out_label["Z"] < 1) :
               raise(ValueError("'Z' not defined"))
            if (out_label["Jtot"] != int(out_label["Jtot"])) or (out_label["Jtot"] < 0) :
               raise(ValueError("'Jtot' not defined"))
            if  out_label["MTtot"] != int(out_label["MTtot"]) :
               raise(ValueError("'MTtot' not defined"))
           
            return out_label        

    def _unique_filename_(self,specs):
        """prepares a unique file name and its hash value"""

        uniquefilename="comp-dens-{kind}-Z={Z}-N={N}-mt={MTtot}-J={Jtot}-{MODENN}-{orderNN}-cut={LambdaNN}".format(**specs)

        if specs["tnforder"] != "no3nf": 
          uniquefilename+="-tnf={tnforder}-tnfcut={lam3NF}-c1={c1}-c3={c3}-c4={c4}-cd={cd}-ce={ce}".format(**specs)
          if specs["cE1"] != 0.0:  
            uniquefilename+="-cE1={cE1}".format(**specs)
          if specs["cE2"] != 0.0:  
            uniquefilename+="-cE2={cE2}".format(**specs)
          if specs["cE3"] != 0.0:  
            uniquefilename+="-cE3={cE3}".format(**specs)
          if specs["cE4"] != 0.0:  
            uniquefilename+="-cE4={cE4}".format(**specs)
          if specs["cE5"] != 0.0:  
            uniquefilename+="-cE5={cE5}".format(**specs)
          if specs["cE6"] != 0.0:  
            uniquefilename+="-cE6={cE6}".format(**specs)
          if specs["cE7"] != 0.0:  
            uniquefilename+="-cE7={cE7}".format(**specs)
          if specs["cE8"] != 0.0:  
            uniquefilename+="-cE8={cE8}".format(**specs)
          if specs["cE9"] != 0.0:  
            uniquefilename+="-cE9={cE9}".format(**specs)
          if specs["cE10"] != 0.0:  
            uniquefilename+="-cE10={cE10}".format(**specs)
        if specs["nnsrg"] != 'none':
          uniquefilename+="-srgNN={lambdaSRGNN}-{potbareNN}-{ostatSRGNN}-{cutnumSRGNN}-{empotsrg}".format(**specs)
        if specs["tnfsrg"] != 'False':
          uniquefilename+="-srg3N={lambdaSRG3N}-{potbareNNTNF}-{ostatSRGTNF}-{cutnumSRGTNF}".format(**specs)
          
        if specs["NP12A"]+specs["NP12B"]!=0:   
          uniquefilename+="-np12a={NP12A}-np12b={NP12B}".format(**specs)
        elif  specs["NP12"]!=0:
          uniquefilename+="-np12={NP12}".format(**specs)
          
        if specs["NP3A"]+specs["NP3B"]!=0:   
          uniquefilename+="-np3a={NP3A}-np3b={NP3B}".format(**specs)
        elif  specs["NP3"]!=0:
          uniquefilename+="-np3={NP3}".format(**specs)
          
        if specs["NQ4A"]+specs["NQ4B"]!=0:   
          uniquefilename+="-nq4a={NQ4A}-nq4b={NQ4B}".format(**specs)
        elif  specs["NQ4"]!=0:
          uniquefilename+="-nq4={NQ4}".format(**specs)
            
        if specs["NQA"]+specs["NQB"]!=0:   
          uniquefilename+="-nqa={NQA}-nqb={NQB}".format(**specs)
        elif  specs["NQ"]!=0:
          uniquefilename+="-nq={NQ}".format(**specs)
          
        if specs["NPTA"]+specs["NPTB"]!=0:   
          uniquefilename+="-npta={NPTA}-nptb={NPTB}".format(**specs)
        elif  specs["NPT"]!=0:
          uniquefilename+="-npt={NPT}".format(**specs)
            
        if specs["NEA"]+specs["NEB"]!=0:   
          uniquefilename+="-nea={NEA}-neb={NEB}".format(**specs)
        elif  specs["NE"]!=0:
          uniquefilename+="-ne={NE}".format(**specs)
        if  specs["NX"]!=0:
          uniquefilename+="-nx={NX}".format(**specs)
          
            
        uniquefilename+="-jmx={j12max}-lmx={lmax}-lsum={lsummax}-Tmx={taumax}".format(**specs)
        # now add the additional parameters of density
        uniquefilename+="-nxt={nxtilde}-nph={nphitilde}".format(**specs)
        uniquefilename+="-j12mxd={j12maxdens}-lmxd={lmaxdens}-taumxd={taumaxdens}".format(**specs)
        try:
          uniquefilename+="-lsmxd={lsummaxdens}".format(**specs)
        except:
          pass
        uniquefilename+="-om={omega}-th={theta}".format(**specs)
        
        hashname=hashlib.sha256(str.encode(str(specs))).hexdigest()
    
        return uniquefilename,hashname        
        
    def get_file(self,**labels):
        """Labels should be given according to standard set (see in _prep_label_).
           On exit the local filename (hashname) and a unique filename are returned.
           If not available locally, the file is downloaded.
           If not available remote, a ValueError is raised. 
        """

        # prepare dictionary specifying the case wanted
        specs=labels
        # look for case in database         
        try:
          select=(self.pddf["kind"]==specs["kind"])
          for key, value in specs.items():
            try:  # do not test for columns that are undefined 
              usevalue=not np.isnan(value)
            except:
              usevalue=True    
            if usevalue:    
              select &= (self.pddf[key]==value)                
          if len(self.pddf.loc[select]) > 0:
             densitypresent=True
          else:   
             densitypresent=False
        except:
          # assume empty frame   
          densitypresent=False

        # if not present, raise an error
        if not densitypresent:  
            raise ValueError("Density is not present in this database!")
        
        # check for unique file
        nhits=len(self.pddf.loc[select])
        if nhits!=1:
            print("Found several hits:")
            print(self.pddf.loc[select].to_markdown())
            raise ValueError("Wave function not unique: {0:d} hits found!".format(nhits))
        
        # then get filenames ...
        hashname=self.pddf.loc[select]["hashname"].item()
        uniquefilename=self.pddf.loc[select]["uniquefilename"].item()
        # and keep the complete labels for later use 
        self.lastaccess=self.pddf.loc[select].to_dict(orient='records')[0]
                
        # if the density is present check whether it is locally available
        if not bool(self.pddf.loc[select]["localavail"].item()):
            index=int(self.pddf.index[select].tolist()[0])
            # and download the gzipped version if not available locally
            url=self.webbase+hashname+".gz"
            print("url: ",url)
            print("workdir: ",self.workdir)
            self._download_file_(url,self.workdir)
            # and ungzip the downloaded file 
            with gzip.open(self.workdir+hashname+".gz", 'rb') as f_in:
               with open(self.workdir+hashname, 'wb') as f_out:
                  shutil.copyfileobj(f_in, f_out)
            self.pddf.at[index,"localavail"]=True
            os.remove(self.workdir+hashname+".gz")
            
            # now the unzipped version should be available 
            
        return self.workdir+hashname,uniquefilename 

    def cleanup(self):
        """removes all local files from working directory except a possibly available table file"""

        try:
          select=(self.pddf["localavail"]==True)
          if len(self.pddf.loc[select]) > 0:
             densitypresent=True
          else:   
             densitypresent=False
        except:
          # assume empty frame   
          densitypresent=False

        # if some local files are present 
        if densitypresent:  
          for index,row in self.pddf[select].iterrows():
              # remove the file
              os.remove(self.workdir+row["hashname"])
              # and mark accordingly in table 
              self.pddf.at[index,"localavail"]=False
              self.pddf.at[index,"localonly"]=False

    def upload(self,host,user,keyfile,remotedir):
        """gzips and moves all new files to remote server.
           Leaves the local copies unchanged.
           Also saves table and uploads the file.
           host -- hostname of remote server
           user -- username on remote server
           keyfile -- full filename of the ssh key 
           remotedir -- directory on that server
        """

        # first select all new files in database
        try:
          select=(self.pddf["localonly"]==True)
          if len(self.pddf.loc[select]) > 0:
             densitypresent=True
          else:   
             densitypresent=False
        except:
          # assume empty frame   
          densitypresent=False

        # if some new local files are present 
        if densitypresent:  
          for index,row in self.pddf[select].iterrows():
              # first generate a gzipped version of the file
              hashname=row["hashname"]
              with open(self.workdir+hashname, 'rb') as f_in:
                with gzip.open(self.workdir+hashname+".gz", 'wb') as f_out:
                  shutil.copyfileobj(f_in, f_out)

              # now upload the new gzipped file
              self._upload_file_(host,user,keyfile,remotedir,self.workdir+hashname+".gz")
              # remove gzipped file 
              os.remove(self.workdir+row["hashname"]+".gz")              
              # and mark accordingly in table 
              self.pddf.at[index,"localonly"]=False

        # the write table to disk
        savedf=self.pddf.copy(deep=True)
        savedf["localonly"]=False
        savedf["localavail"]=False
        savedf.to_hdf(self.workdir+self.pddf_hdf, key='densityfiles', mode='w')
        # and upload table file
        self._upload_file_(host,user,keyfile,remotedir,self.workdir+self.pddf_hdf)


    def _upload_file_(self,host,user,keyfile,remotedir,localfile):
        """Establishes ssh connection and uploads a single binary file.
           host -- hostname of the remote server
           user -- username on remote server
           remotedir -- directory on remote server
           localfile -- full filename including path on local computer
        """
        
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user,key_filename=keyfile)

        
        with SCPClient(ssh.get_transport()) as scp:
           scp.put(localfile, remotedir)
        
    def remove_file(self,index):
        """This routine removes a file from the data base locally.
           The file is idenfied by the index within the table.
           
        """

        # check whether file is downloaded and get hashname
        hashname=self.pddf.iloc[2]['hashname']
        # try to remove file 
        # first copy to working directory
        try:
          os.remove(self.workdir+hashname)
        except:
          pass
        # drop row from table
        self.pddf=self.pddf.drop(self.pddf.index[[index]])
        self.pddf.reset_index(drop=True, inplace=True)
        # and save table to disc 
        savedf=self.pddf.copy(deep=True)
        savedf.to_hdf(self.workdir+self.pddf_hdf, key='densityfiles', mode='w')
        
    def merge(self,old):
       """Merges two databases for density files
       old -- other database including the density files and table

       Both databases need to be completely disjunct which is checked according to the
       hashnames of the files.
       """

       # first merge the tables to a preliminary

       mergedf=pd.concat([self.pddf,old.pddf])

       duplicates=mergedf.duplicated(subset=['hashname'])

       if duplicates.any():
         raise(ValueError("Tables are not completely disjunct in terms of filenames!"))

       # now files seem to be disjunct, therefore I add all old files to the new dictory, I keep all other info
       # including the timestamps by using finally the merged table from above

       for index,row in old.pddf.iterrows():
           rowdict=dict(row)       
           hashname,uniquefilename=old.get_file(**rowdict)
           shutil.copy(hashname,self.workdir)
           
           
       # if all files are copied, the two tables can be merged again (includes downloaded file tags)
       # before old files from old table are marked as new
       previoustab=old.pddf.copy(deep=True)
       previoustab["localonly"]=True
       self.pddf=pd.concat([self.pddf,previoustab])
       # reset index so that all rows get a unique numbering
       self.pddf=self.pddf.reset_index(drop=True)

       savedf=self.pddf.copy(deep=True)
       savedf.to_hdf(self.workdir+self.pddf_hdf, key='densityfiles', mode='w')

    def prep_upload(self,tmpdir):
        """gzips and moves all new files to a temporary directory.
           Leaves the local copies unchanged.
           Also saves table and copies this file to temp directory.
           tmpdir -- directory for temporarily storing new files
           This method is meant as a preparation to upload new files to
           remote database. 
        """

        # add "/" to filename if required
        if tmpdir!="":   
          if tmpdir[-1]!="/":
            tmpdir=tmpdir+"/"
                       

            # first select all new files in database
        try:
          select=(self.pddf["localonly"]==True)
          if len(self.pddf.loc[select]) > 0:
             denspresent=True
          else:   
             denspresent=False
        except:
          # assume empty frame   
          denspresent=False

        # if some new local files are present 
        if denspresent:  
          for index,row in self.pddf[select].iterrows():
              # first generate a gzipped version of the file
              hashname=row["hashname"]
              with open(self.workdir+hashname, 'rb') as f_in:
                with gzip.open(self.workdir+hashname+".gz", 'wb') as f_out:
                  shutil.copyfileobj(f_in, f_out)

              # now upload the new gzipped file
              shutil.copy(self.workdir+hashname+".gz",tmpdir)
              # remove gzipped file 
              os.remove(self.workdir+row["hashname"]+".gz")              
              # and mark accordingly in table 
              self.pddf.at[index,"localonly"]=False

        # the write table to disk
        savedf=self.pddf.copy(deep=True)
        savedf["localonly"]=False
        savedf["localavail"]=False
        savedf.to_hdf(self.workdir+self.pddf_hdf, key='densityfiles', mode='w')
        # and copy table file
        shutil.copy(self.workdir+self.pddf_hdf,tmpdir)
       

class densfile2b:
    """This class defines an object that allows to read a 2-body density file into numpy arrays
       and to compress a file."""
    def  __init__(self,filen_in,printlevel=0):
        """This opens a 2b density file for reading and reads all info an prints simple statistics.
           optional parameter printlevel controls amout of printout: 0 = none, 1 = limited, 2 = extensive 
        
           After using this method, the kinematics and data are properties of the objects
              - maxrhoindex: number of non-zero channel combinations 
              - num2Nchan: number of channels alpha = 0,num2Nchan 
              - qn2Nchan[alpha,0:6] - quantum numbers of channel alpha:  l,s,j,t,mt,mj,2xMJ
              - rhoindx[alpha,alpha]: gives index for channel combination used as rhoarray index  
        
              - meshtype usually 'TRNS'
              - mesh uses parameters for number of grid points p12n1,p12n2,p12ntot
                and interval boundaries p12a,p12b,p12c.
                The grid and weights are in arrays p12p,p12w. 
              - rhoarray[rindx-1,ip12p,ip12] contains the density data
                   rindx is the channel index from rhoindx
                   ip12p and ip12 (0:p12ntot-1) the indices of outgoing and incoming relative momentum
        
           The kinematics are defined by
              - omval: omega in fm-1 
              - qval: momentum transfer in fm-1 
              - thetaqval: angle for momentum transfer 
              - thetaval: angle for outgoing photon (incoming in z-direction)      
        """
        # read in density and calculate correlation radius and norm for checking
        # for conversions
        hbarc=197.327

        # open file 
        # assume that file only contains one density 
        # read this density and auxiliary fields 
        filein=h5py.File(filen_in, 'r')

        # first read bookkeeping 
        self.maxrhoindex=filein['maxrhoindex'][()]
        self.num2Nchan=filein['num2Nchan'][()]
        self.qn2Nchan=filein['qn2Nchan'][()]
        self.rhoindx=filein['rhoindx'][()]
        
        if printlevel>0:
          print('Number of channels and couplings:   {0:d}  {1:d}\n'.format(self.num2Nchan,self.maxrhoindex))
        if printlevel>1:  
          print('Channels:\n')
          print("{0:>5s} {1:>3s} {2:>3s} {3:>3s} {4:>3s} {5:>3s} {6:>3s}  {7:>3s}".format(
          "alpha","l","s","j","t","mt","mj","2.MJ"))
          for alpha in range(self.num2Nchan):
            print("{0:5d} {1:3d} {2:3d} {3:3d} {4:3d} {5:3d} {6:3d}  {7:3d}".format(alpha,
                   self.qn2Nchan[alpha,0],self.qn2Nchan[alpha,1],self.qn2Nchan[alpha,2],
                   self.qn2Nchan[alpha,3],self.qn2Nchan[alpha,4],self.qn2Nchan[alpha,5],
                   self.qn2Nchan[alpha,6]))



        # now read and print mesh parameters 
        self.meshtype=''.join(list(map(lambda x: x.decode('utf-8'), filein['meshtype'][()]))).strip()
        self.p12n1=filein['p12n1'][()]
        self.p12n2=filein['p12n2'][()]
        self.p12ntot=filein['p12ntot'][()]

        self.p12a=filein['p12p1'][()]
        self.p12b=filein['p12p2'][()]
        self.p12c=filein['p12p3'][()]

        self.p12p=filein['p12p'][()]
        self.p12w=filein['p12w'][()]

        if printlevel>0:
          print("MESHTYPE: {0:s}".format(self.meshtype))
          print("NP12:     {0:d} {1:d}  {2:d} ".format(self.p12n1,self.p12n2,self.p12ntot))
          print("P12:      {0:15.6e}  {1:15.6e}  {2:15.6e} \n ".format(self.p12a,self.p12b,self.p12c))
        if printlevel>1:
          print("Grid points: \n")
          for ip in range(self.p12ntot):
            print("P12MESH:   {0:15.6e} {1:15.6e}".format(self.p12p[ip],self.p12w[ip]))


        for rhogroup in filein.keys():
          if 'RHO' in rhogroup: 
              resexpr=re.search(r"RHO\_om\=(.*)\_th\=(.*)",rhogroup)
              om=float(resexpr.group(1))
              th=float(resexpr.group(2))
              group=filein[rhogroup]
              self.rhoarray=group["RHO"][()]
              self.omval=group["omval"][()]
              self.qval=group["qval"][()]
              self.thetaqval=group["thetaqval"][()]
              self.thetaval=group["thetaval"][()]
              if printlevel>0:
                print("OMEGA   = {0:15.6e}  {1:15.6e}".format(om*hbarc,self.omval*hbarc))
                print("THETA   = {0:15.6e}  {1:15.6e}".format(th*180.0/np.pi,self.thetaval*180.0/np.pi))
                print("q,theta = {0:15.6e}  {1:15.6e}".format(self.qval*hbarc,self.thetaqval*180.0/np.pi))
    
        # integrate to get normalization or ff 
        
        ffsum1=0.0
        ffsum2=0.0
        for alpha in range(self.num2Nchan):
            rindx=self.rhoindx[alpha,alpha]
            if self.qn2Nchan[alpha,6]==-1:
                ffsum1+=np.einsum("ii,i,i->",self.rhoarray[rindx-1,:,:],self.p12p**2,self.p12w)
            else:    
                ffsum2+=np.einsum("ii,i,i->",self.rhoarray[rindx-1,:,:],self.p12p**2,self.p12w)

        if printlevel>0:
          print("     {0:>15s} {1:>15s}    {2:>15s}  {3:>15s}".format("qval[fm-1]","qval[MeV]","ffsum1","ffsum2"))
          print("FF:  {0:15.6e} {1:15.6e}    {2:15.6e}  {3:15.6e}".format(self.qval,self.qval*hbarc,ffsum1,ffsum2))


        filein.close()
        if printlevel>0:
          print("File size read:  {0:d}".format(os.path.getsize(filen_in)))
        

    def compress(self,filen_out,tolerance,printlevel=0):
        """This method write the current data in compressed form to the new file file_out using
           ZFP compression with accuracy tolerance. Optional parameter printlevel controls printout."""
    
        fileout=h5py.File(filen_out, 'w')
        
        # write all entries from self object
        # first bookkeeping to root
        dsetout=fileout.create_dataset("maxrhoindex",self.maxrhoindex.shape,dtype="i4") 
        dsetout[()]=self.maxrhoindex
        
        dsetout=fileout.create_dataset("num2Nchan",self.num2Nchan.shape,dtype="i4") 
        dsetout[()]=self.num2Nchan
        
        dsetout=fileout.create_dataset("qn2Nchan",self.qn2Nchan.shape,dtype="i4") 
        dsetout[()]=self.qn2Nchan
        
        dsetout=fileout.create_dataset("rhoindx",self.rhoindx.shape,dtype="i4") 
        dsetout[()]=self.rhoindx

        # then grid points to root
        meshname=list(self.meshtype)
        dsetout=fileout.create_dataset("meshtype",(len(meshname),),dtype="|S1") 
        dsetout[()]=meshname
        
        dsetout=fileout.create_dataset("p12n1",self.p12n1.shape,dtype="i4") 
        dsetout[()]=self.p12n1
        dsetout=fileout.create_dataset("p12n2",self.p12n2.shape,dtype="i4") 
        dsetout[()]=self.p12n2
        dsetout=fileout.create_dataset("p12ntot",self.p12ntot.shape,dtype="i4") 
        dsetout[()]=self.p12ntot

        dsetout=fileout.create_dataset("p12p1",self.p12a.shape,dtype="f8") 
        dsetout[()]=self.p12a
        dsetout=fileout.create_dataset("p12p2",self.p12b.shape,dtype="f8") 
        dsetout[()]=self.p12b
        dsetout=fileout.create_dataset("p12p3",self.p12c.shape,dtype="f8") 
        dsetout[()]=self.p12c
        

        dsetout=fileout.create_dataset("p12p",self.p12p.shape,dtype="f8") 
        dsetout[()]=self.p12p
        dsetout=fileout.create_dataset("p12w",self.p12w.shape,dtype="f8") 
        dsetout[()]=self.p12w

        # finally add group date for RHO density
        lineformat = ff.FortranRecordWriter('("RHO_om=",SP,E13.6,"_th=",E13.6)')
        groupname=lineformat.write([self.omval,self.thetaval])
        groupout=fileout.create_group(groupname)
        
        dsetout=groupout.create_dataset("RHO",self.rhoarray.shape,dtype="f4", **hdf5plugin.Zfp(accuracy=tolerance)) 
        dsetout[()]=self.rhoarray

        dsetout=groupout.create_dataset("omval",self.omval.shape,dtype="f8") 
        dsetout[()]=self.omval
        dsetout=groupout.create_dataset("qval",self.qval.shape,dtype="f8") 
        dsetout[()]=self.qval
        dsetout=groupout.create_dataset("thetaqval",self.thetaqval.shape,dtype="f8") 
        dsetout[()]=self.thetaqval
        dsetout=groupout.create_dataset("thetaval",self.thetaval.shape,dtype="f8") 
        dsetout[()]=self.thetaval        
        fileout.close()
        if printlevel>0:
          print("File size written:  {0:d}".format(os.path.getsize(filen_out)))

    
class densfile1b:
    """This class defines an object that allows to read a 1-body density file into numpy arrays"""
    def  __init__(self,filen_in,printlevel=0):
        """This opens a 1b density file for reading and reads all info an prints simple statistics.
        
           After using this method, the kinematics and data are properties of the objects
              - maxrhoindex: number of non-zero channel combinations 
              - num2Nchan: number of channels alpha = 0,num2Nchan 
              - qn2Nchan[alpha,0:6] - quantum numbers of channel alpha:  l,s,j,t,mt,mj,2xMJ
              - rhoindx[alpha,alpha]: gives index for channel combination used as rhoarray index  
        
              - meshtype usually 'TRNS'
              - mesh uses parameters for number of grid points p12n1,p12n2,p12ntot
                and interval boundaries p12a,p12b,p12c.
                The grid and weights are in arrays p12p,p12w. 
              - rhoarray[rindx-1,ip12p,ip12] contains the density data
                   rindx is the channel index from rhoindx
                   ip12p and ip12 (0:p12ntot-1) the indices of outgoing and incoming relative momentum
        
           The kinematics are defined by
              - omval: omega in fm-1 
              - qval: momentum transfer in fm-1 
              - thetaqval: angle for momentum transfer 
              - thetaval: angle for outgoing photon (incoming in z-direction)      
        """
        
        # read in density and calculate correlation radius and norm for checking
        # for conversions
        hbarc=197.327

        # first read the namelist part containing the bookkeeping
        nml = f90nml.read(filen_in)
        self.maxrho1bindex=nml['book1ndim']['maxrho1bindex']
        rho1bindxlist=nml['book1ndata']['rho1bindx']
        self.rho1bindx=np.array(rho1bindxlist).reshape(self.maxrho1bindex,8)

        # print bookkeeping
        if printlevel>0:
          print("maxrho1bindex = {0:d}".format(self.maxrho1bindex))
        if printlevel>1:
          print("{0:>5s}  {1:>4s}  {2:>4s}  {3:>4s}  {4:>4s}  {5:>4s}  {6:>4s}  {7:>4s}  {8:>4s}".format(
                 "chan","2.ms","2.mt","2.M","2.msp","2.mtp","2.Mp","k","K"))
          for i in range(self.maxrho1bindex):
            print("{0:5d}  {1:4d}  {2:4d}  {3:4d}  {4:4d}  {5:4d}  {6:4d}  {7:4d}  {8:>4d}".format(i,
                   self.rho1bindx[i,0],self.rho1bindx[i,1],self.rho1bindx[i,2],
                   self.rho1bindx[i,3],self.rho1bindx[i,4],
                   self.rho1bindx[i,5],self.rho1bindx[i,6],self.rho1bindx[i,7]))
        # now read data part of same file 
        filein=open(filen_in,"r")

        indxflag=False
        getline=False
        self.rho1b=np.empty((self.maxrho1bindex),dtype=np.double)
        lastlinecount=self.maxrho1bindex//6+1
        lastlinedata=self.maxrho1bindex%6
        
        for line in filein:
          if getline:
            data=line.split()
            if count==0:
              self.omval=float(data[0])
              self.thetaval=float(data[1])
              self.qval=float(data[2])
              self.thetaqval=float(data[3])              
            elif count==lastlinecount:
              for col in range(lastlinedata):
                self.rho1b[(count-1)*6+col]=data[col]
            else:
              self.rho1b[(count-1)*6]=data[0]
              self.rho1b[(count-1)*6+1]=data[1]
              self.rho1b[(count-1)*6+2]=data[2]
              self.rho1b[(count-1)*6+3]=data[3]
              self.rho1b[(count-1)*6+4]=data[4]
              self.rho1b[(count-1)*6+5]=data[5]
            count+=1  
          if "RHO1BINDX" in line:
            indxflag=True
          if "/" in line and indxflag:
            getline=True
            count=0    
        filein.close()

        # print basic normalization for testing 

        sump=0.0
        sumn=0.0
        sum=0.0
        for rindx in range(self.maxrho1bindex):
          # define quantum numbers
          ms=self.rho1bindx[rindx,0]
          mt=self.rho1bindx[rindx,1]
          bm=self.rho1bindx[rindx,2]
          msp=self.rho1bindx[rindx,3]
          mtp=self.rho1bindx[rindx,4]
          bmp=self.rho1bindx[rindx,5]
          k=self.rho1bindx[rindx,6]
          bk=self.rho1bindx[rindx,7]
            
          if bk==0 and k==0 and ms==msp and mt==mtp and bm==bmp:
            if mt==1:  #  proton 
                sump=sump+self.rho1b[rindx]
            if mt==-1:  #  neutron 
                sumn=sumn+self.rho1b[rindx]
            sum=sum+self.rho1b[rindx]
        if printlevel>0:
          print("FF1B:   {0:15.6e} {1:15.6e} {2:15.6e} {3:15.6e}".format(self.qval,sumn,sump,sum) )  
          print("omega  =   {0:15.6e} ".format(self.omval*hbarc) )  
          print("q      =   {0:15.6e} ".format(self.qval*hbarc) )  
          print("theta  =   {0:15.6e} ".format(self.thetaval*180.0/np.pi) )  
          print("thetaq =   {0:15.6e} ".format(self.thetaqval*180.0/np.pi) )  
 
