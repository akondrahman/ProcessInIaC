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




def getProcessMetrics(file_path_p, repo_path_p):
    #get commit count
    COMM = getCommitCount(file_path_p, repo_path_p)
