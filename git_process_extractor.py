'''
Akond Rahman
Process extractor from git repositories
April 01, 2017
'''
import os, subprocess, numpy as np



def getCommitCount(param_file_path, repo_path):
   totalCountForChurn = 0

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   totalCountForChurn = len(dt_churn_output)
   print totalCountForChurn
   return totalCountForChurn

def getProcessMetrics(file_path_p, repo_path_p):
    #get commit count
    COMM = getCommitCount(file_path_p, repo_path_p)
