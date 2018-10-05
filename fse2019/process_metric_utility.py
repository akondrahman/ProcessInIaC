'''
Akond Rahman
April 01, 2017
utility file for process metric
'''
from collections import Counter
import os, csv, numpy as np, time, datetime
import os, subprocess, numpy as np, operator
from  collections import Counter
from scipy.stats import entropy
import math
import pandas as pd

def getPuppetFileDetails(theCompleteCategFile):
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
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP )
  fileToWrite.close()
  return str(os.stat(fileP).st_size)
def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret


def createDataset(str2Dump, datasetNameParam):
   headerOfFile0='org,file_,'
   headerOfFile1='ADD_PER_COM,DEL_PER_COM,TOT_PER_COM,ADD_PER_COM_PER_LOC,DEL_PER_COM_PER_LOC,TOT_PER_COM_PER_LOC,DEVS,'
   headerOfFile2='MINORS,OWNER_LINES,SCATERNESS,DEV_MET,COLA_MET,'
   headerOfFile3='defect_status'

   headerStr = headerOfFile0 + headerOfFile1 + headerOfFile2  +  headerOfFile3 

   str2Write = headerStr + '\n' + str2Dump
   return dumpContentIntoFile(str2Write, datasetNameParam)
def getDatasetFromCSV(fileParam, dataTypeFlag=True):
  if dataTypeFlag:
    data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1, dtype='float')
  else:
        data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1,  dtype='str')
  return data_set_to_return

def createOutputDirectory(dirParam):
  if not os.path.exists(dirParam):
     os.makedirs(dirParam)
  if os.path.exists(dirParam):
     print "Output directory is there already ..."

def getMercurialProgrammerList(file_with_rel_path, repo_path):
   prog_output = []
   if (('student' not in file_with_rel_path) and ('.csv' not in file_with_rel_path) and ('.txt' not in file_with_rel_path) and ('EXTRA_AST' not in file_with_rel_path)):
      cdCommand         = "cd " + repo_path + " ; "
      commitCountCmd    = "hg churn --diffstat  " + file_with_rel_path + " | awk '{print $1}'  "
      command2Run = cdCommand + commitCountCmd
      _output = subprocess.check_output(['bash','-c', command2Run])
      prog_output = _output.split('\n')
      prog_output = [x_ for x_ in prog_output if x_!='']
   return prog_output

def getRepoList(org_name_p):
    repoList2Ret = []
    the_eligible_file = org_name_p + 'eligible_repos.csv'
    with open(the_eligible_file, 'rU') as file_:
         reader_ = csv.reader(file_)
         for row_ in reader_:
             repoList2Ret.append( org_name_p + row_[0] + '/')
    return repoList2Ret

def getMercurialProgToFileMapping(org_name_p):
   dict2ret = {}
   repo_list = getRepoList(org_name_p)
   for repo_path_param in repo_list:
       cdCommand         = "cd " + repo_path_param + " ; "
       progToFileCommand = "hg status --all | cut -d' ' -f2 "
       command2Run = cdCommand + progToFileCommand

       all_file_in_repo_output = subprocess.check_output(['bash','-c', command2Run])
       all_file_in_repo_output = all_file_in_repo_output.split('\n')
       all_file_in_repo_output = [x_ for x_ in all_file_in_repo_output if x_!='']
       for file_ in all_file_in_repo_output:
           prog_list = getMercurialProgrammerList(file_, repo_path_param)
           for programmer_ in prog_list:
               if programmer_ not in dict2ret:
                  dict2ret[programmer_] =  [file_]
               else:
                  dict2ret[programmer_] = dict2ret[programmer_] + [file_]
   return dict2ret

def getGitProgrammerList(file_with_rel_path, repo_path):
   prog_output = []
   #print file_with_rel_path, repo_path
   if (('student' not in file_with_rel_path) and ('.csv' not in file_with_rel_path) and ('.txt' not in file_with_rel_path) and ('EXTRA_AST' not in file_with_rel_path)):
      cdCommand         = "cd " + repo_path + " ; "
      commitCountCmd    = " git blame "+ file_with_rel_path +"  | awk '{print $2}' | cut -d'(' -f2 "
      command2Run = cdCommand + commitCountCmd
      _output = subprocess.check_output(['bash','-c', command2Run])
      prog_output = _output.split('\n')
      prog_output = [x_ for x_ in prog_output if x_!='']
   return prog_output





def getGitProgToFileMapping(org_name_p):
   dict2ret = {}
   repo_list = getRepoList(org_name_p)
   #print repo_list
   for repo_path_param in repo_list:
       #print repo_path_param
       cdCommand         = "cd " + repo_path_param + " ; "
       progToFileCommand = "git ls-files "
       command2Run = cdCommand + progToFileCommand

       all_file_in_repo_output = subprocess.check_output(['bash','-c', command2Run])
       all_file_in_repo_output = all_file_in_repo_output.split('\n')
       all_file_in_repo_output = [x_ for x_ in all_file_in_repo_output if x_!='']
       #print all_file_in_repo_output
       for file_ in all_file_in_repo_output:
           prog_list = getGitProgrammerList(file_, repo_path_param)
           for programmer_ in prog_list:
               if programmer_ not in dict2ret:
                  dict2ret[programmer_] =  [file_]
               else:
                  dict2ret[programmer_] = dict2ret[programmer_] + [file_]
   return dict2ret


def createLogTransformedFeatures(allFeatureParam):
  log_transformed_feature_dataset_to_ret = []
  dataset_rows = len(allFeatureParam)
  print "-"*50
  print "Dataset rows:",dataset_rows
  print "-"*50
  for ind_ in xrange(dataset_rows):
    features_for_this_index = allFeatureParam[ind_, :]
    log_transformed_features_for_index = [math.log1p(x_) for x_ in features_for_this_index]
    log_transformed_feature_dataset_to_ret.append(log_transformed_features_for_index)
  log_transformed_feature_dataset_to_ret = np.array(log_transformed_feature_dataset_to_ret)
  return log_transformed_feature_dataset_to_ret

def getMeenelyDetails(meenely_file):
    dict_ = {}
    with open(meenely_file, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
        dev_met_of_file = row_[10]
        col_met_of_file = row_[11]
        
        path_of_file    = row_[1]

        if path_of_file not in dict_:
            dict_[path_of_file] = (dev_met_of_file, col_met_of_file)
    
    return dict_