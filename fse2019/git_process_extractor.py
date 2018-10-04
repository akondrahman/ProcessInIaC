'''
Akond Rahman
Process extractor from git repositories
'''

import os, subprocess, numpy as np, operator
from  collections import Counter
from  scipy.stats import entropy


def getCommitCount(param_file_path, repo_path):
   totalCountForChurn   = 1

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   totalCountForChurn = len(dt_churn_output)
   return totalCountForChurn

def getUniqueDevCount(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = " git blame "+ theFile +"  | awk '{print $2}' | cut -d'(' -f2 "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   author_count        = len(np.unique(author_count_output))

   return author_count


def getAddedChurnMetrics(param_file_path, repo_path):
   totalAddedLinesPerCommit = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $1 }' "
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   add_churn_output = [int(y_) for y_ in add_churn_output if y_.isdigit()]

   totalAddedLinesPerCommit = sum(add_churn_output)

   return totalAddedLinesPerCommit




def getDeletedChurnMetrics(param_file_path, repo_path):
   totalDeletedLinesPerCommit = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnDeletedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $2 }' "
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   del_churn_output = [int(y_) for y_ in del_churn_output if y_.isdigit()]

   totalDeletedLinesPerCommit = sum(del_churn_output)
   return totalDeletedLinesPerCommit

def getMinorContribCount(param_file_path, repo_path, sloc):
   minorList = []
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk '{print $2}'  | cut -d'(' -f2"
   command2Run       = cdCommand + blameCommand

   blame_output   = subprocess.check_output(['bash','-c', command2Run])
   blame_output   = blame_output.split('\n')
   blame_output   = [x_ for x_ in blame_output if x_!='']
   author_contrib = dict(Counter(blame_output))

   for author, contribs in author_contrib.items():
      if((float(contribs)/float(sloc)) < 0.05):
        minorList.append(author)
   return len(minorList)



def getHighestContribsPerc(param_file_path, repo_path, sloc):
   owner_contrib = 0 
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk '{print $2}'  | cut -d'(' -f2"
   command2Run       = cdCommand + blameCommand

   blame_output     = subprocess.check_output(['bash','-c', command2Run])
   blame_output     = blame_output.split('\n')
   blame_output     = [x_ for x_ in blame_output if x_!='']
   author_contrib   = dict(Counter(blame_output))

   if (len(author_contrib) > 0):
     highest_author   = max(author_contrib.iteritems(), key=operator.itemgetter(1))[0]
     highest_contr    = author_contrib[highest_author]
   else:
     highest_contr = 0
   if sloc <= 0 :
       sloc += 1
   owner_contrib = (round(float(highest_contr)/float(sloc), 5))
   return owner_contrib

def getDeveloperScatternessOfFile(param_file_path, repo_path, sloc):
   entropy_list      = []
   scatterness = 0 
   tota_mods = 1
   line_cnt  = 0  

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame -n " + theFile + " | awk '{print $2}' "
   command2Run       = cdCommand + blameCommand

   blame_output      = subprocess.check_output(['bash','-c', command2Run])
   blame_output      = blame_output.split('\n')
   blame_output      = [x_ for x_ in blame_output if x_!='']
   line_chng_dict    = dict(Counter(blame_output))

   for k_, v_ in line_chng_dict.iteritems():
       tota_mods = tota_mods + int(v_)

   for lineNo in xrange(sloc):
       line_key  = str(lineNo + 1)
       if (line_key in line_chng_dict):
          line_cnt  = line_chng_dict[line_key]
       else:
          line_cnt  = 0
       
       line_modi_prob  = float(line_cnt) / float(tota_mods) 
       entropy_list.append(line_modi_prob)  

   scatterness  = round(entropy(entropy_list), 5)  

   if((scatterness == float("-inf")) or (scatterness == float("inf"))):
     scatterness = float(0)

   return scatterness



def getProcessMetrics(file_path_p, repo_path_p):
    DEV = getUniqueDevCount(file_path_p, repo_path_p)

    COMM = getCommitCount(file_path_p, repo_path_p)
    ADD_PER_COMMITS = getAddedChurnMetrics(file_path_p, repo_path_p)
    DEL_PER_COMMITS = getDeletedChurnMetrics(file_path_p, repo_path_p)    
    TOT_PER_COMMITS = ADD_PER_COMMITS + DEL_PER_COMMITS

    NOR_ADD_PER_COM = float(ADD_PER_COMMITS) / float(COMM) 
    NOR_DEL_PER_COM = float(DEL_PER_COMMITS) / float(COMM) 
    NOR_TOT_PER_COM = float(TOT_PER_COMMITS) / float(COMM)

    LOC             = sum(1 for line in open(file_path_p))

    MINOR        = getMinorContribCount(file_path_p, repo_path_p, LOC)
    OWNER_LINES  = getHighestContribsPerc(file_path_p, repo_path_p, LOC)
    SCTR         = getDeveloperScatternessOfFile(file_path_p, repo_path_p, LOC)


    all_process_metrics = str(NOR_ADD_PER_COM) + ',' + str(NOR_DEL_PER_COM) + ',' + str(NOR_TOT_PER_COM) + ',' + str(DEV) + ','
    all_process_metrics = all_process_metrics +  str(MINOR) + ',' + str(OWNER_LINES) + ',' + str(SCTR) + ','

    return all_process_metrics
