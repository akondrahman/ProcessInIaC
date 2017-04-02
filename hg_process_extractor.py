'''
extract process metrics from hg repositories
April 01, 2017
Akond Rahman
'''
import os, subprocess, numpy as np, operator
monthDict            = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
                           'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
from collections import Counter
from  scipy.stats import entropy




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


   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = " hg churn --dateformat '%Y-%m-%d' " +  theFile +    " | awk '{print $1 }' "
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   monthAndYeatList = [x_ for x_ in dt_churn_output if x_!='']
   #print monthAndYeatList
   monthAndYeatList.sort()
   #print monthAndYeatList
   earliesttMonth  = monthAndYeatList[0]
   latesttMonth    = monthAndYeatList[-1]
   age = calculateMonthDiffFromTwoDates(earliesttMonth, latesttMonth)
   #print age
   return age
def getUniqueDevCount(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   #print "full path: {}, repo path:{}, theFile:{}".format(param_file_path, repo_path, theFile)
   commitCountCmd    = "hg churn --diffstat  " + theFile + " | awk '{print $1}'  "
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
   commitCommand        = " hg churn --dateformat '%Y-%m-%d' " +  theFile +    " | awk '{print $1 }' "
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   monthAndYeatList = [x_ for x_ in dt_churn_output if x_!='']
   monthAndYeatList.sort()
   #print monthAndYeatList
   avgConsecutiveTimeDiff = getAvgConsecutiveTimeDiff(monthAndYeatList)
   #print avgConsecutiveTimeDiff
   return avgConsecutiveTimeDiff
def getAddedChurnMetrics(param_file_path, repo_path):
   totalAddedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = "hg churn --diffstat " + theFile + " | awk '{print $2}' | cut -d'/' -f1 | cut -d'+' -f2 | sed -e  's/ /,/g'"
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   add_churn_output = [int(y_) for y_ in add_churn_output if (y_.isdigit())==True]
   #print add_churn_output
   totalAddedLinesForChurn = sum(add_churn_output)
   #print totalAddedLinesForChurn
   return totalAddedLinesForChurn




def getDeletedChurnMetrics(param_file_path, repo_path):
   totalDeletedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnDeletedCommand = " hg churn --diffstat " + theFile + " | awk '{print $2}' | cut -d'/' -f2 | cut -d'-' -f2 | sed -e  's/ /,/g'"
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   del_churn_output = [int(y_) for y_ in del_churn_output]
   #print del_churn_output
   totalDeletedLinesForChurn = sum(del_churn_output)
   #print totalDeletedLinesForChurn
   return totalDeletedLinesForChurn




def getAverageChangedLines(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnDeletedCommand = " hg churn --diffstat " + theFile + " | awk '{print $2}' | cut -d'/' -f2 | cut -d'-' -f2 | sed -e  's/ /,/g'"
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   del_churn_output = [int(y_) for y_ in del_churn_output]
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = "hg churn --diffstat " + theFile + " | awk '{print $2}' | cut -d'/' -f1 | cut -d'+' -f2 | sed -e  's/ /,/g'"
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   add_churn_output = [int(y_) for y_ in add_churn_output if (y_.isdigit())==True]

   chanegHolder     = add_churn_output + del_churn_output
   #print chanegHolder
   avgChangeLOC     = np.mean(chanegHolder)
   #print avgChangeLOC
   return avgChangeLOC
def getMinorContribCount(param_file_path, repo_path, sloc):
   minorList = []
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " hg annotate -u " + theFile + " | cut -d':' -f1 "
   command2Run       = cdCommand + blameCommand

   blame_output   = subprocess.check_output(['bash','-c', command2Run])
   blame_output   = blame_output.split('\n')
   blame_output   = [x_ for x_ in blame_output if x_!='']
   author_contrib = dict(Counter(blame_output))
   #print author_contrib
   for author, contribs in author_contrib.items():
      if((float(contribs)/float(sloc)) < 0.05):
          minorList.append(author)
   return len(minorList)




def getHighestContribsPerc(param_file_path, repo_path, sloc):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " hg annotate -u " + theFile + " | cut -d':' -f1 "
   command2Run       = cdCommand + blameCommand

   blame_output     = subprocess.check_output(['bash','-c', command2Run])
   blame_output     = blame_output.split('\n')
   blame_output     = [x_ for x_ in blame_output if x_!='']
   author_contrib   = dict(Counter(blame_output))
   highest_author   = max(author_contrib.iteritems(), key=operator.itemgetter(1))[0]
   highest_contr    = author_contrib[highest_author]
   #print "LOC:{}, A:{}, C:{}, dict:{}".format(sloc, highest_author, highest_contr, author_contrib)
   return (round(float(highest_contr)/float(sloc), 5))*100

def getDeveloperScatternessOfFile(param_file_path, repo_path, sloc):
   '''
   output list
   '''
   lineNoProb        = []
   lineNoCnt         = []
   '''
   '''
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " hg annotate -uln   " + theFile + "  | cut -d':' -f2 "
   command2Run       = cdCommand + blameCommand
   blame_output      = subprocess.check_output(['bash','-c', command2Run])
   blame_output      = blame_output.split('\n')
   blame_output      = [x_ for x_ in blame_output if x_!='']
   line_chng_dict    = dict(Counter(blame_output))
   #print line_chng_dict
   for lineNo in xrange(sloc):
       line_key  = str(lineNo + 1)
       if (line_key in line_chng_dict):
          line_cnt  = line_chng_dict[line_key]
       else:
          line_cnt  = 0
       line_prob = round(float(line_cnt)/float(sloc), 4)
       lineNoProb.append(line_prob) ### Version 1
       lineNoCnt.append(line_cnt)   ### Version 2
   #print "len:{}, list:{}, loc:{}".format(len(lineNoProb), lineNoProb, sloc)
   scatterness_prob = entropy(lineNoProb)  ##Version 1
   scatterness_cnt  = entropy(lineNoCnt)  ##Version 2
   print "list:{} ...\n prob->entropy:{}".format(lineNoProb, scatterness_prob)
   print "list:{} ... len():{} ...\n count->entropy:{} ...sloc:{}".format(lineNoCnt, len(lineNoCnt), scatterness_cnt, sloc)
   return scatterness_prob, scatterness_cnt

def getProcessMetrics(file_path_p, repo_path_p):
    #get commit count
    COMM = getCommitCount(file_path_p, repo_path_p)
    #get AGE
    AGE = getAge(file_path_p, repo_path_p)
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
    ### AVG CHANGED LINES PER COMMIT
    AVGCHNG      = getAverageChangedLines(file_path_p, repo_path_p)

    ### GET MINOR CONTRIBUTOR COUNT
    MINOR        = getMinorContribCount(file_path_p, repo_path_p, LOC)
    ### GET HIGHEST CONTRIBUTOR's Authored lines
    OWN          = getHighestContribsPerc(file_path_p, repo_path_p, LOC)
    ### GET Scatterness of a file
    SCTR         = getDeveloperScatternessOfFile(file_path_p, repo_path_p, LOC)

    ## all process metrics
    all_process_metrics = str(COMM) + ',' + str(AGE) + ',' + str(DEV) + ',' + str(AVGTIMEOFEDITS) + ',' + str(ADDPERLOC) + ','
    all_process_metrics = all_process_metrics +  str(DELPERLOC) + ',' + str(ADDNORM) + ',' + str(DELNORM) + ','
    all_process_metrics = all_process_metrics + str(AVGCHNG) + ',' + str(MINOR) + ',' + str(OWN) + ',' + str(SCTR) + ','
    return all_process_metrics
