'''
MAIN TIME PREDICTION
AKOND RAHMAN
SEP 25, 2017
'''
from sklearn import decomposition
import numpy as np , pandas as pd, os
from itertools import combinations
import process_metric_utility
import time_sklearn_modeling

def constructCombos(ds_param):
        ds_lists, output_list  = [], []
        for dir_ in os.listdir(ds_param):
            if (dir_!='.DS_Store'):
               dir2look = ds_param + dir_ + '/'
               #file2look = dir2look + 'TIME_PROCESSMETRIC_DATASET.csv'
               file2look = dir2look + 'BFS_TIME_PROCESSMETRIC_DATASET.csv'
               if(os.path.exists(file2look)):
                  ds_lists.append(file2look)
        ds_lists =  list(combinations(ds_lists, 2))
        for combo in ds_lists:
            train_file, test_file = combo
            train_path, test_path = os.path.dirname(train_file), os.path.dirname(test_file)
            train_year_value, test_year_value =  int(train_path.split('/')[-1]), int(test_path.split('/')[-1])
            #print train_year_value, test_year_value
            if((test_year_value > train_year_value) and ((test_year_value - train_year_value)==1)):
                output_list.append(combo)
        return output_list

def constructHeuristics(ds_param):
    train_file, test_file = ds_param + 'FIRST_HALF.csv', ds_param + 'SECOND_HALF.csv'
    return [(train_file, test_file)]

def getPCAInsights(pcaParamObj, no_of_pca_comp_to_see):
    print '+'*25
    print 'PCA metric importance zone  ...'
    print '+'*25
    for comp_index in xrange(no_of_pca_comp_to_see):
        all_metric_value_in_one_component =  np.abs(pcaParamObj.components_[comp_index])
        non_zero_metric_cnt = len([x_ for x_ in all_metric_value_in_one_component if x_ > 0])
        print 'Number of non-zero metrics:{}, of {}'.format(non_zero_metric_cnt, len(all_metric_value_in_one_component))
        print '$'*15
        sorted_all_metric_index_in_one_component = all_metric_value_in_one_component.argsort()[::-1]
        for met_index in sorted_all_metric_index_in_one_component:
            print 'Metric index:{}, metric score:{}'.format(met_index, all_metric_value_in_one_component[met_index])
            print '~'*10
        # top_components_index = sorted_all_metric_value_in_one_component[:how_many_metrics]
        # print top_components_index
        print '$'*15
    print "+"*25

def performPCA(feature_matrix_p):
   '''
   PCA ZONE
   '''
   feature_input_for_pca = feature_matrix_p
   pca_comp = 10 ###  must be less than or equal to no of features
   pcaObj = decomposition.PCA(n_components=pca_comp)
   pcaObj.fit(feature_input_for_pca)
   # variance of features
   variance_of_features = pcaObj.explained_variance_
   # how much variance is explained each component
   variance_ratio_of_features = pcaObj.explained_variance_ratio_
   print "Explained varaince ratio"
   for index_ in xrange(len(variance_ratio_of_features)):
       print "Principal component#{}, explained variance:{}".format(index_+1, variance_ratio_of_features[index_])
   print "-"*50
   # see how much explained variance is covered by the number of compoenents , and set the number
   no_features_to_use = 7 #using one PCA you get lesser accuracy, so we'll use 10, always check how much variance is explained
   print "Of all the features, we will use:", no_features_to_use
   print "-"*50
   pcaObj.n_components=no_features_to_use
   selected_features = pcaObj.fit_transform(feature_matrix_p)
   print "Selected feature dataset size:", np.shape(selected_features)
   print "-"*50
   getPCAInsights(pcaObj, no_features_to_use)
   print "-"*50
   return selected_features

if __name__=='__main__':
   PCA = True

   # ds_dir   = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MOZILLA/"
   # folder_to_save = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/MOZILLA_BFS_TIME_PRED_RES/"
   # folder_to_save = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/MOZILLA_TIME_PRED_RES/"
   # folder_to_save = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/MOZILLA_HEURISTIC_TIME_PRED_RES/"

   # ds_dir   = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OPENSTACK/"
   # folder_to_save = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/OPENSTACK_BFS_TIME_PRED_RES/"
   # folder_to_save = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/OPENSTACK_TIME_PRED_RES/"
   # folder_to_save = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/OPENSTACK_HEURISTIC_TIME_PRED_RES/"

   # ds_dir   = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/WIKIMEDIA/"
   # folder_to_save = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/WIKIMEDIA_BFS_TIME_PRED_RES/"
   # folder_to_save = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/WIKIMEDIA_TIME_PRED_RES/"
   # folder_to_save = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/WIKIMEDIA_HEURISTIC_TIME_PRED_RES/"

   # train_test_combos = constructCombos(ds_dir)
   train_test_combos = constructHeuristics(ds_dir)

   #print train_test_combos
   for index_ in xrange(len(train_test_combos)):
       train_file, test_file = train_test_combos[index_]
       #print train_file, test_file
       '''
       training dataset zone
       '''
       train_log_features, train_labels = process_metric_utility.getFeaturesAndLabels(train_file)
       '''
       test dataset zone
       '''
       test_log_features, test_labels = process_metric_utility.getFeaturesAndLabels(test_file)
       if PCA:
          train_log_features = performPCA(train_log_features)
          test_log_features  = performPCA(test_log_features)
       '''
       do prediction: 10 times iteration
       '''
       folder2write = folder_to_save +  str(index_) + '/'
       if((os.path.exists(folder2write))==False):
           os.makedirs(folder2write)
       time_sklearn_modeling.performIterativeModeling(train_log_features, test_log_features, train_labels, test_labels, folder2write, 10)
       print '='*100
