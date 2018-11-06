'''
Akond Rahman 
Nov 05, 2018 
Decision Tree Mining and Printing 
'''
import pandas as pd 
from sklearn  import tree 
import process_metric_utility
import numpy as np 
from subprocess import call

def printDT(x_train, y_train, col_names, png_file_name):
  
  theCARTModel = tree.DecisionTreeClassifier(criterion='gini', max_depth=4, max_leaf_nodes=None, min_samples_leaf=1)
#   theCARTModel = tree.DecisionTreeClassifier(criterion='entropy', max_depth=4, max_leaf_nodes=None, min_samples_leaf=1)
  theCARTModel.fit(x_train, y_train)
  #print dir(theCARTModel.tree_)
  tree.export_graphviz(theCARTModel, out_file='tree.dot', feature_names=col_names)
  call(['dot', '-T', 'png', 'tree.dot', '-o', png_file_name])


def calcFeatureImp(feature_vec, label_vec, feature_names_param, repeat=10):
    header_str, str2write= '', ''
    for name_ in feature_names_param:
        header_str = header_str + name_ + ','
    theCARTModel = tree.DecisionTreeClassifier(criterion='gini', max_depth=4, max_leaf_nodes=None, min_samples_leaf=1)
    theCARTModel.fit(feature_vec, label_vec)
    feat_imp_vector=theCARTModel.feature_importances_

    for ind_ in xrange(repeat):
        for imp_vec_index in xrange(len(feat_imp_vector)):
            feat_imp_val = round(feat_imp_vector[imp_vec_index], 5)
            str2write = str2write +  str(feat_imp_val) + ','
            print 'Metric:{}, score:{}'.format(feature_names_param[imp_vec_index], feat_imp_val)
            print '-'*25
        print '='*50


if __name__=='__main__':
    # dataset_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_MIR_FULL_DATASET.csv' 
    # png_file_ = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/MIR_GINI_TREE.png'

    # dataset_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_MOZ_FULL_DATASET.csv' 
    # png_file_ = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/MOZ_GINI_TREE.png'

    # dataset_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_OST_FULL_DATASET.csv' 
    # png_file_ = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/OST_GINI_TREE.png'

    # dataset_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_WIK_FULL_DATASET.csv' 
    # png_file_ = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/WIK_GINI_TREE.png'

    df_ = pd.read_csv(dataset_file)
    features = list(df_.columns.values)
    exclude_list = ['org', 'file_', 'defect_status']
    features = [x_ for x_ in features if x_ not in exclude_list]
    start_cols =  2

    full_dataset_from_csv = process_metric_utility.getDatasetFromCSV(dataset_file)
    full_rows, full_cols = np.shape(full_dataset_from_csv)

    feature_cols = full_cols - 1  
    all_features = full_dataset_from_csv[:, start_cols:feature_cols]
    dataset_for_labels = process_metric_utility.getDatasetFromCSV(dataset_file)  
    label_cols = full_cols - 1 
    all_labels  =  dataset_for_labels[:, label_cols]

   
    # printDT(all_features, all_labels, features, png_file_)

    calcFeatureImp(all_features, all_labels, features)
    print 'The dataset was:', dataset_file