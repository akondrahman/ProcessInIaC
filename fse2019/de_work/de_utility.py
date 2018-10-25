'''
Akond Rahman
Oct 24, 2018
Utility file for running DE
'''
from sklearn.metrics import classification_report, roc_auc_score, mean_absolute_error, accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import numpy as np, os, math
from sklearn import cross_validation


learnerDict = {'CART': [[0.01, 1.00], [2, 20], [1, 20], [1, 50]],  ###max_features, min_samples_split, min_samples_leaf, max_depth
               'RF'  : [[0.01, 1.00], [2, 50], [2, 20], [1, 20], [10, 150]], ###max_features, max_leaf_nodes, min_samples_split,min_samples_leaf,n_estimators
               'SVM' : [[0.25, 4.00], [0.1, 0.9]],  ### C (Penalty), gamma (aka width of kernel)
               'LOGI' : [[0.1, 1.00]]
               }





def giveMeLimitsOfThisLearner(learnerName):
  return learnerDict[learnerName]



def getDatasetFromCSV(fileParam, dataTypeFlag=True):
  if dataTypeFlag:
        data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1, dtype='float')
  else:
        data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1,  dtype='str')
  return data_set_to_return




def evalClassifier(actualLabels, predictedLabels):
  '''
    the way skelarn treats is the following: first index -> lower index -> 0 -> 'Low'
                                             next index after first  -> next lower index -> 1 -> 'high'
  '''
  target_labels =  ['N', 'Y']

  prec_ = precision_score(actualLabels, predictedLabels, average='binary')
  recall_ = recall_score(actualLabels, predictedLabels, average='binary')
  area_roc_output = roc_auc_score(actualLabels, predictedLabels)
  f_measure_output = f1_score(actualLabels, predictedLabels, average='binary')

  return area_roc_output, prec_, recall_, f_measure_output

def perform_cross_validation(classiferP, featuresP, labelsP, cross_vali_param, infoP):
  predicted_labels = cross_validation.cross_val_predict(classiferP, featuresP , labelsP, cv=cross_vali_param)
  area_roc_to_ret, prec2print, recall2print, fscore2print = evalClassifier(labelsP, predicted_labels)

  return area_roc_to_ret
  # return prec2print
  # return recall2print




def giveTimeStamp():
  import time, datetime
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP )
  fileToWrite.close()
  return str(os.stat(fileP).st_size)

def createLogTransformedFeatures(allFeatureParam):
  log_transformed_feature_dataset_to_ret = []
  dataset_rows = len(allFeatureParam)
  for ind_ in xrange(dataset_rows):
    features_for_this_index = allFeatureParam[ind_, :]
    log_transformed_features_for_index = [math.log1p(x_) for x_ in features_for_this_index]
    log_transformed_feature_dataset_to_ret.append(log_transformed_features_for_index)

  log_transformed_feature_dataset_to_ret = np.array(log_transformed_feature_dataset_to_ret)
  return log_transformed_feature_dataset_to_ret



def createOutputDirectory(dirParam):
  if not os.path.exists(dirParam):
     os.makedirs(dirParam)
  if os.path.exists(dirParam):
     print "Output directory created ..."


def saveResults(list_, file_p):
    str2Dump=''
    for elem_ in list_:
        str2Dump = str2Dump + str(round(elem_, 5)) + ',' + '\n'
    save_status=dumpContentIntoFile(str2Dump, file_p)
    print 'Dumped a file of {} bytes'.format(save_status)
