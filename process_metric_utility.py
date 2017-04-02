'''
Akond Rahman
April 01, 2017
utility file for process metric
'''
import os, csv, numpy as np, time, datetime
theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/New.Final.Categ.csv'


def getPuppetFileDetails():
    dictOfAllFiles={}
    dict2Ret={}
    with open(theCompleteCategFile, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
        repo_of_file       = row_[1]
        categ_of_file      = row_[3]
        full_path_of_file  = row_[4]
        if full_path_of_file not in dictOfAllFiles:
            dictOfAllFiles[full_path_of_file] = [[ categ_of_file ], repo_of_file]
        else:
            dictOfAllFiles[full_path_of_file][0] = dictOfAllFiles[full_path_of_file][0] + [ categ_of_file ]
    for k_, v_ in dictOfAllFiles.items():
       uniq = np.unique(v_[0])
       if ((len(uniq)==1) and (uniq[0]=='N')):
         dict2Ret[k_] = ('0', v_[1])
       else:
         dict2Ret[k_] = ('1', v_[1])
    return dict2Ret




def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w');
  fileToWrite.write(strP );
  fileToWrite.close()
  return str(os.stat(fileP).st_size)
def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def createDataset(str2Dump, datasetNameParam):
   headerOfFile0='org,file_,'
   headerOfFile1='COMM,AGE,DEV,AVGTIMEOFEDITS,ADDPERLOC,'
   headerOfFile2='DELPERLOC,ADDNORM,DELNORM,AVGCHNG,MINOR,OWN,SCTR,'
   headerOfFile3='defect_status'

   headerStr = headerOfFile0 + headerOfFile1 + headerOfFile2 + headerOfFile3

   str2Write = headerStr + '\n' + str2Dump
   return dumpContentIntoFile(str2Write, datasetNameParam)
def getDatasetFromCSV(fileParam, dataTypeFlag=True):
  if dataTypeFlag:
    data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1, dtype='float')
  else:
        data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1,  dtype='str')
  return data_set_to_return
