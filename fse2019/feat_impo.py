
'''
Akond Rahman
Feature importance for Solidity Metrics using RF
'''
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

def readDataset(fileParam, dataTypeFlag=True):
  if dataTypeFlag:
    data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1, dtype='float')
  else:
    data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1,  dtype='str')
  return data_set_to_return

def getColumnNames(file_name_param, start, end ):
    ds_   = pd.read_csv(file_name_param)
    temp_ = list(ds_.columns.values)
    temp_ = temp_[start:end]
    return temp_

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP)
    fileToWrite.close()
    return str(os.stat(fileP).st_size)


def getFeatureVector(feature_vec, label_vec):
    list_ = []

    theRndForestModel = RandomForestClassifier()
    theRndForestModel.fit(feature_vec, label_vec)
    feat_imp_vector=theRndForestModel.feature_importances_
    feat_imp_vector=list(feat_imp_vector)

    sorted_feat_imp_vector= [x_ for x_ in feat_imp_vector]
    sorted_feat_imp_vector.sort(reverse=True)
    print sorted_feat_imp_vector, feat_imp_vector

    for feat_imp_val in sorted_feat_imp_vector:
        feat_index = feat_imp_vector.index(feat_imp_val) 
        list_.append(feat_index)
    return list_

def calcFeatureImp(feature_vec, label_vec, feature_names_param, output_file, repeat=10):
    header_str, str2write= '', ''
    for name_ in feature_names_param:
        header_str = header_str + name_ + ','
    theRndForestModel = RandomForestClassifier()
    theRndForestModel.fit(feature_vec, label_vec)
    feat_imp_vector=theRndForestModel.feature_importances_

    for ind_ in xrange(repeat):
        for imp_vec_index in xrange(len(feat_imp_vector)):
            feat_imp_val = round(feat_imp_vector[imp_vec_index], 5)
            str2write = str2write +  str(feat_imp_val) + ','
            print 'Metric:{}, score:{}'.format(feature_names_param[imp_vec_index], feat_imp_val)
            print '-'*25
        str2write = str2write + '\n'
        print '='*50
    str2write = header_str + '\n' + str2write
    output_status= dumpContentIntoFile(str2write, output_file)
    print 'Dumped the RF FEATURE IMPORTANCE file of {} bytes'.format(output_status)


if __name__=='__main__':

   ds_file_name       = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/OST_FULL_DATASET.csv'
   output_file_param  = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/FEAT_IMP_OUT_OST.csv'

#    ds_file_name       = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/WIK_FULL_DATASET.csv'
#    output_file_param  = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/FEAT_IMP_OUT_WIK.csv'

   full_ds=readDataset(ds_file_name)
   full_rows, full_cols = np.shape(full_ds)
   feature_cols = full_cols - 1
   all_features = full_ds[:, 2:feature_cols]
   all_labels  =  full_ds[:, feature_cols]
   defected_file_count     = len([x_ for x_ in all_labels if x_==1.0])
   non_defected_file_count = len([x_ for x_ in all_labels if x_==0.0])
   feature_names = getColumnNames(ds_file_name, 2, feature_cols)
   calcFeatureImp(all_features, all_labels, feature_names, output_file_param)
   print '='*100
