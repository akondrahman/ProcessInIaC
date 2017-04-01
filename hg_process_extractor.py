'''
extract process metrics from hg repositories
April 01, 2017
Akond Rahman
'''
import os, subprocess, numpy as np



def getCommitCount(param_file_path, repo_path):
   totalCommitCount = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   #print "full path: {}, repo path:{}, theFile:{}".format(param_file_path, repo_path, theFile)
   commitCountCmd    = "hg log  " +  theFile +  " | grep -c '^changeset' "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])

   commit_count_output = commit_count_output.split('\n')
   commit_count_output = [x_ for x_ in commit_count_output if x_!='']
   commit_count_output = [int(y_) for y_ in commit_count_output if (y_.isdigit())==True]
   commit_count_output = str(commit_count_output[0])
   return commit_count_output




def calculateMonthDiffFromTwoDates(early, latest):
    from datetime import datetime
    early_year   = early.split('-')[0]
    latest_year  = latest.split('-')[0]
    early_month  = early.split('-')[1]
    latest_month = latest.split('-')[1]
    early_day    = early.split('-')[-1]
    latest_day   = latest.split('-')[-1]

    early_dt     = datetime(int(early_year), int(early_month), int(early_day))
    latest_dt    = datetime(int(latest_year), int(latest_month), int(latest_day))

    return (latest_dt.year - early_dt.year)*12 + latest_dt.month - early_dt.month
def getAge(param_file_path, repo_path):
   totalCountForChurn   = 0
   monthDict            = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
                           'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = " hg churn --dateformat '%Y-%m-%d' " +  theFile +    " | awk '{print $1 }' "
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   monthAndYeatList = [x_ for x_ in dt_churn_output if x_!='']
   #print monthAndYeatList
   monthAndYeatList.sort()
   print monthAndYeatList
   earliesttMonth  = monthAndYeatList[0]
   latesttMonth    = monthAndYeatList[-1]
   age = str(calculateMonthDiffFromTwoDates(earliesttMonth, latesttMonth))
   print age
   return age



def getProcessMetrics(file_path_p, repo_path_p):
    #get commit count
    COMM = getCommitCount(file_path_p, repo_path_p)
    #get AGE
    AGE = getAge(file_path_p, repo_path_p)
