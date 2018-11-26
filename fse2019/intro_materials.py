'''
Akond Rahman 
Intro writing analysis 
Nov 25, 2018 
'''
import process_metric_utility
import os 
import subprocess
from collections import Counter
import numpy as np 

def getAddedLines(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = " git log --numstat --oneline " + theFile 
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])

   return add_churn_output


def getHighestContribsPerc(param_file_path, repo_path):
   owner_contrib = 0 
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile 
   command2Run       = cdCommand + blameCommand

   blame_output      = subprocess.check_output(['bash','-c', command2Run])

   return blame_output

def getMinorContribCount(param_file_path, repo_path):
   minorList = []
   devList   = []
   sloc      = sum(1 for line in open(param_file_path))
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk '{print $2}'  | cut -d'(' -f2"
   command2Run       = cdCommand + blameCommand

   blame_output   = subprocess.check_output(['bash','-c', command2Run])
   blame_output   = blame_output.split('\n')
   blame_output   = [x_ for x_ in blame_output if (x_!='' or x_ !='\n')] 
   devList        = np.unique(blame_output)

   author_contrib = dict(Counter(blame_output))

   for author, contribs in author_contrib.items():
      if((float(contribs)/float(sloc)) < 0.05):
        minorList.append(author)
   return len(devList), len(minorList)

def getAllProcessMetricsForSingleFile(full_path_param, repo_path_param):
    out_str_change_size = getAddedLines(full_path_param, repo_path_param)
    print full_path_param
    print '-'*10
    print repo_path_param
    print '-'*10
    # print out_str_change_size
    out_str_dev_names   = getHighestContribsPerc(full_path_param, repo_path_param)
    dev_count, minor_contrib_count = getMinorContribCount(full_path_param, repo_path_param)
    # print out_str_dev_names
    # print '-'*10
    print 'Minor dev count:', minor_contrib_count
    print '-'*10
    print 'All dev count:', dev_count
    print '-'*10    


def getAllProcessMetricForAllFiles(pupp_map_dict_param ):
   for file_, details_ in pupp_map_dict_param.items():
      if ('WTF' not in file_):
        repo_          = details_[1]
        defect_status  = details_[0]       
        if defect_status == '1':
           getAllProcessMetricsForSingleFile(file_, repo_)
           print '='*125


if __name__=='__main__':
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mirantis_Categ_For_DB.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.WithoutBadBoys.Final.Categ.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'

    print "Started at:", process_metric_utility.giveTimeStamp()
    fullPuppMap   = process_metric_utility.getPuppetFileDetails(theCompleteCategFile)

    # DEFECT STATUS 
    getAllProcessMetricForAllFiles(fullPuppMap)   
   