'''
get summary stats from datasets
Akond Rahman
Nov 05, 2018
'''
from scipy import stats
import pandas as pd
import numpy as np
import cliffsDelta


mirantis_file  ="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_MIR_FULL_DATASET.csv"
mozilla_file   ="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_MOZ_FULL_DATASET.csv"
openstack_file ="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_OST_FULL_DATASET.csv"
wikimedia_file ="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_WIK_FULL_DATASET.csv"




def giveTimeStamp():
  import time, datetime
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

dataset_files = [mirantis_file, mozilla_file, openstack_file, wikimedia_file]

print "Started at:", giveTimeStamp()
for dataset_file in dataset_files:
    name = dataset_file.split('/')[-1]
    print "Dataset:", name
    df2read = pd.read_csv(dataset_file)
    #print df2read.head()

    features = df2read.columns
    dropcols = ['repo_', 'file_', 'defect_status', 'org', 'REPO', 'COMMITID', 'FILE', 'ADD_PER_COM_PER_LOC', 'DEL_PER_COM_PER_LOC', 'TOT_PER_COM_PER_LOC']
    features2see = [x_ for x_ in features if x_ not in dropcols]
    for feature_ in features2see:
           #print feature_
           '''
           all data summary
           '''
           data_for_feature = df2read[feature_]
           median_, mean_, total_ = np.median(data_for_feature), np.mean(data_for_feature), sum(data_for_feature)
           print "Feature:{}, [ALL DATA] median:{}, mean:{}, sum:{}".format(feature_, median_, mean_, total_  )
           print '='*50
           defective_vals_for_feature     = df2read[df2read['defect_status']==1][feature_]
           non_defective_vals_for_feature = df2read[df2read['defect_status']==0][feature_]
           '''
           summary time
           '''
           print 'THE FEATURE IS:', feature_
           print '='*25
           #print "Defective values stats: \n", defective_vals_for_feature.describe()
           print "Defective values [MEDIAN]:{}, [MEAN]:{}".format(np.median(list(defective_vals_for_feature)), np.mean(list(defective_vals_for_feature)))
           #print "Non defective values stats: \n", non_defective_vals_for_feature.describe()
           print "Non Defective values [MEDIAN]:{}, [MEAN]:{}".format(np.median(list(non_defective_vals_for_feature)), np.mean(list(non_defective_vals_for_feature)))
           
           if feature_=='OWNER_LINES':
              TS, p = stats.mannwhitneyu(list(non_defective_vals_for_feature), list(defective_vals_for_feature), alternative='greater')
           else:
              TS, p = stats.mannwhitneyu(list(defective_vals_for_feature), list(non_defective_vals_for_feature), alternative='greater')

           cliffs_delta = cliffsDelta.cliffsDelta(list(defective_vals_for_feature), list(non_defective_vals_for_feature))
           print 'Feature:{}, pee value:{}, cliffs:{}'.format(feature_, p, cliffs_delta)
           print '='*50
    print '*'*100
print "Ended at:", giveTimeStamp()
