'''
Akond Rahman
Process extractor from git repositories
April 01, 2017
'''
import os, subprocess, numpy as np
monthDict            = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
                         'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

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
   #print totalCountForChurn
   return totalCountForChurn

def calculateMonthDiffFromTwoDates(early, latest):
    from datetime import datetime
    early_year   = early.split('-')[0]
    latest_year  = latest.split('-')[0]
    early_month  = early.split('-')[-1]
    latest_month = latest.split('-')[-1]
    early_dt     = datetime(int(early_year), int(early_month), 1)
    latest_dt    = datetime(int(latest_year), int(latest_month), 1)

    return (latest_dt.year - early_dt.year)*12 + latest_dt.month - early_dt.month
def getAge(param_file_path, repo_path):
   totalCountForChurn   = 0

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   #print dt_churn_output
   monthList = [dob[0:3] for dob in  dt_churn_output]
   yearist = [dob[-4:] for dob in  dt_churn_output]
   monthAndYeatList = [dob[-4:] + '-' + monthDict[dob[0:3]] for dob in dt_churn_output]
   monthAndYeatList.sort()
   #print monthAndYeatList
   earliesttMonth  = monthAndYeatList[0]
   latesttMonth    = monthAndYeatList[-1]
   age = str(calculateMonthDiffFromTwoDates(earliesttMonth, latesttMonth))
   #print age
   return age



def getUniqueDevCount(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   #print "full path: {}, repo path:{}, theFile:{}".format(param_file_path, repo_path, theFile)
   commitCountCmd    = " git blame "+ theFile +"  | awk '{print $2}' | cut -d'(' -f2 "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   author_count        = len(np.unique(author_count_output))
   #print author_count
   return author_count

def getAvgConsecutiveTimeDiff(month_year_list_param):
    counter = 0
    consecList = []
    len_    = len(month_year_list_param)
    for index_ in xrange(len_):
        first_  = month_year_list_param[index_]
        if((index_+1) < len_):
          second_ = month_year_list_param[index_+1]
          month_diff = calculateMonthDiffFromTwoDates(first_, second_)
          consecList.append(month_diff)
    #print consecList
    avg_month_diff = round(np.mean(consecList), 5)
    return avg_month_diff


def getAverageTimeBetweenEdits(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCommand        = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   #print dt_churn_output
   monthList = [dob[0:3] for dob in  dt_churn_output]
   yearist = [dob[-4:] for dob in  dt_churn_output]
   monthAndYeatList = [dob[-4:] + '-' + monthDict[dob[0:3]] for dob in dt_churn_output]
   monthAndYeatList.sort()
   #print monthAndYeatList
   avgConsecutiveTimeDiff = getAvgConsecutiveTimeDiff(monthAndYeatList)
   #print avgConsecutiveTimeDiff
   return avgConsecutiveTimeDiff

def getAddedChurnMetrics(param_file_path, repo_path):
   totalAddedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = " git log --numstat --oneline " + theFile +  " |  awk '!(NR%2)' | awk '{ print $1 }' "
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   add_churn_output = [int(y_) for y_ in add_churn_output ]
   #print add_churn_output
   totalAddedLinesForChurn = sum(add_churn_output)
   #print totalAddedLinesForChurn
   return totalAddedLinesForChurn




def getDeletedChurnMetrics(param_file_path, repo_path):
   totalDeletedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnDeletedCommand = " git log --numstat --oneline " + theFile + " |  awk '!(NR%2)' | awk '{ print $2 }'"
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   del_churn_output = [int(y_) for y_ in del_churn_output]
   #print del_churn_output
   totalDeletedLinesForChurn = sum(del_churn_output)
   #print totalDeletedLinesForChurn
   return totalDeletedLinesForChurn


def getProcessMetrics(file_path_p, repo_path_p):
    #get commit count
    COMM = getCommitCount(file_path_p, repo_path_p)
    #get age
    AGE  = getAge(file_path_p, repo_path_p)
    #get DEV
    DEV = getUniqueDevCount(file_path_p, repo_path_p)
    #get AVERAGE TIME BETWEEN EDITS
    AVGTIMEOFEDITS = getAverageTimeBetweenEdits(file_path_p, repo_path_p)
    #get total lines added
    ADDTOTALLINES  = getAddedChurnMetrics(file_path_p, repo_path_p)
    # get SLOC
    LOC            = sum(1 for line in open(file_path_p))
    ##Addition Per LOC
    ADDPERLOC      = round(float(ADDTOTALLINES)/float(LOC), 5)
    #get total lines deleted
    DELETETOTALLINES  = getDeletedChurnMetrics(file_path_p, repo_path_p)
    ##Deletion Per LOC
    DELPERLOC      = round(float(DELETETOTALLINES)/float(LOC), 5)

    ### TOTAL LINES CHANGED
    TOT_LOC_CHNG = ADDTOTALLINES + DELETETOTALLINES
    ##Addition Normalized
    ADDNORM      = round(float(ADDTOTALLINES)/float(TOT_LOC_CHNG), 5)
    ##Deletion Normalized
    DELNORM      = round(float(DELETETOTALLINES)/float(TOT_LOC_CHNG), 5)

    ## all process metrics
    all_process_metrics = str(COMM) + ',' + str(AGE) + ',' + str(DEV) + ',' + str(AVGTIMEOFEDITS) + ',' + str(ADDPERLOC) + ','
    all_process_metrics = all_process_metrics +  str(DELPERLOC) + ',' + str(ADDNORM) + ',' + str(DELNORM) + ','
    return all_process_metrics
