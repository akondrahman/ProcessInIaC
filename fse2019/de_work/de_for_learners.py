'''
the core part of the DE runner
Akond Rahman
Oct 24, 2018
'''
import de_utility, numpy as np
from DiffEvolOptimizer import DiffEvolOptimizer
from sklearn import decomposition, svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import RandomizedLogisticRegression, LogisticRegression


pcas_to_explore    = 5 
no_features_to_use = 4  # 4, 4, 3  

'''
FSE 
'''
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/MIR_CHI_DATASET.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/MOZ_CHI_DATASET.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/OST_CHI_DATASET.csv'
dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/WIK_CHI_DATASET.csv'

# dataset_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/JUST_SIZE/MIR.csv'
# dataset_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/JUST_SIZE/MOZ.csv'
# dataset_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/JUST_SIZE/OST.csv'
# dataset_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/JUST_SIZE/WIK.csv'


folds=10
prev_cart_auc   = float(0)
prev_rf_auc     = float(0)
prev_svm_auc    = float(0)
prev_logi_auc   = float(0)

def evaluateCART(paramsForTuning):
  global prev_cart_auc
  # 1. read dataset from file
  full_dataset_from_csv = de_utility.getDatasetFromCSV(dataset_file)
  full_rows, full_cols = np.shape(full_dataset_from_csv)
  ## 2. we will skip the first column, as it has file names
  feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip
  all_features = full_dataset_from_csv[:, 2:feature_cols]
  # 3. get labels
  dataset_for_labels = de_utility.getDatasetFromCSV(dataset_file)  ## unlike phase-1, the labels are '1' and '0', so need to take input as str
  label_cols = full_cols - 1
  all_labels  =  dataset_for_labels[:, label_cols]
  ## 4. do PCA, take all features for PCA
  '''
  lets transform all the features via log transformation
  '''
  log_transformed_features = de_utility.createLogTransformedFeatures(all_features)
  feature_input_for_pca = log_transformed_features
  pcaObj = decomposition.PCA(n_components=pcas_to_explore)
  pcaObj.fit(feature_input_for_pca)
  ## 5. trabsform daatset based on PCA
  pcaObj.n_components=no_features_to_use
  selected_features = pcaObj.fit_transform(feature_input_for_pca)
  ## 6. plugin model parameters
  #print "lol", paramsForTuning[0]
  if((paramsForTuning[0] <= de_utility.learnerDict['CART'][0][0] ) or (paramsForTuning[1] <= de_utility.learnerDict['CART'][1][0]) or (paramsForTuning[2] <= de_utility.learnerDict['CART'][2][0]) or (paramsForTuning[3] <= de_utility.learnerDict['CART'][3][0])):
    cart_area_under_roc = prev_cart_auc
  elif((paramsForTuning[0] > de_utility.learnerDict['CART'][0][1] ) or (paramsForTuning[1] > de_utility.learnerDict['CART'][1][1]) or (paramsForTuning[2] > de_utility.learnerDict['CART'][2][1]) or (paramsForTuning[3] > de_utility.learnerDict['CART'][3][1])):
    cart_area_under_roc = prev_cart_auc
  else:
    theCARTModel = DecisionTreeClassifier(max_features=paramsForTuning[0], min_samples_split=paramsForTuning[1],
                                        min_samples_leaf=paramsForTuning[2], max_depth=paramsForTuning[3]
                                       )
    cart_area_under_roc = de_utility.perform_cross_validation(theCARTModel, selected_features, all_labels, folds, 'CART')
    #print "asi mama:", cart_area_under_roc
    prev_cart_auc = cart_area_under_roc
  #print "current pointer to AUC:", cart_area_under_roc
  return cart_area_under_roc

def evaluateRF(paramsForTuning):
  #reff: http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
  global prev_rf_auc
  # 1. read dataset from file
  full_dataset_from_csv = de_utility.getDatasetFromCSV(dataset_file)
  full_rows, full_cols = np.shape(full_dataset_from_csv)
  ## 2. we will skip the first column, as it has file names
  feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip
  all_features = full_dataset_from_csv[:, 2:feature_cols]
  # 3. get labels
  dataset_for_labels = de_utility.getDatasetFromCSV(dataset_file)  ## unlike phase-1, the labels are '1' and '0', so need to take input as str
  label_cols = full_cols - 1
  all_labels  =  dataset_for_labels[:, label_cols]
  ## 4. do PCA, take all features for PCA
  '''
  lets transform all the features via log transformation
  '''
  log_transformed_features = de_utility.createLogTransformedFeatures(all_features)
  feature_input_for_pca = log_transformed_features
  pcaObj = decomposition.PCA(n_components=pcas_to_explore)
  pcaObj.fit(feature_input_for_pca)
  ## 5. trabsform daatset based on PCA
  pcaObj.n_components=no_features_to_use
  selected_features = pcaObj.fit_transform(feature_input_for_pca)
  ## 6. plugin model parameters
  #print "lol", paramsForTuning[0]
  if((paramsForTuning[0] <= de_utility.learnerDict['RF'][0][0] ) or (paramsForTuning[1] <= de_utility.learnerDict['RF'][1][0]) or (paramsForTuning[2] <= de_utility.learnerDict['RF'][2][0]) or (paramsForTuning[3] <= de_utility.learnerDict['RF'][3][0]) or (paramsForTuning[4] <= de_utility.learnerDict['RF'][4][0])):
    rf_area_under_roc = prev_rf_auc
  elif((paramsForTuning[0] > de_utility.learnerDict['RF'][0][1] ) or (paramsForTuning[1] > de_utility.learnerDict['RF'][1][1]) or (paramsForTuning[2] > de_utility.learnerDict['RF'][2][1]) or (paramsForTuning[3] > de_utility.learnerDict['RF'][3][1])  or (paramsForTuning[4] > de_utility.learnerDict['RF'][4][1])):
    rf_area_under_roc = prev_rf_auc
  else:
    the_RF_Model = RandomForestClassifier(max_features = paramsForTuning[0],    max_leaf_nodes = int(paramsForTuning[1]),
                                          min_samples_split=paramsForTuning[2], min_samples_leaf=paramsForTuning[3],
                                          n_estimators=int(paramsForTuning[4])
                                         )
    rf_area_under_roc = de_utility.perform_cross_validation(the_RF_Model, selected_features, all_labels, folds, 'RF')
    #print "asi mama:", rf_area_under_roc
    prev_rf_auc = rf_area_under_roc
  #print "current pointer to AUC:", rf_area_under_roc
  return rf_area_under_roc

def evaluateSVM(paramsForTuning):
  #reff: http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC
  '''
  need some adjustements for handling string values
  start
  '''
  the_kernels_for_svm = ['linear', 'poly', 'rbf', 'sigmoid']
  '''
  end
  '''
  global prev_svm_auc
  # 1. read dataset from file
  full_dataset_from_csv = de_utility.getDatasetFromCSV(dataset_file)
  full_rows, full_cols = np.shape(full_dataset_from_csv)
  ## 2. we will skip the first column, as it has file names
  feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip
  all_features = full_dataset_from_csv[:, 2:feature_cols]
  # 3. get labels
  dataset_for_labels = de_utility.getDatasetFromCSV(dataset_file)  ## unlike phase-1, the labels are '1' and '0', so need to take input as str
  label_cols = full_cols - 1
  all_labels  =  dataset_for_labels[:, label_cols]
  ## 4. do PCA, take all features for PCA
  '''
  lets transform all the features via log transformation
  '''
  log_transformed_features = de_utility.createLogTransformedFeatures(all_features)
  feature_input_for_pca = log_transformed_features
  pcaObj = decomposition.PCA(n_components=pcas_to_explore)
  pcaObj.fit(feature_input_for_pca)
  ## 5. trabsform daatset based on PCA
  pcaObj.n_components=no_features_to_use
  selected_features = pcaObj.fit_transform(feature_input_for_pca)
  ## 6. plugin model parameters
  #print "lol", paramsForTuning[0]
  if((paramsForTuning[0] <= de_utility.learnerDict['SVM'][0][0] ) or (paramsForTuning[1] <= de_utility.learnerDict['SVM'][1][0]) ):
    svm_area_under_roc = prev_svm_auc
  elif((paramsForTuning[0] > de_utility.learnerDict['SVM'][0][1] ) or (paramsForTuning[1] > de_utility.learnerDict['SVM'][1][1]) ):
    svm_area_under_roc = prev_svm_auc
  else:
    ###selected_kernel = the_kernels_for_svm[int(paramsForTuning[1])]
    ## get the kernel first , then build the model, change the follwoign line: use kernel = 'linear', 'rbf', 'sigmoid'
    the_SVM_Model      = svm.SVC(C = paramsForTuning[0], kernel = 'rbf', gamma = paramsForTuning[1] )
    svm_area_under_roc = de_utility.perform_cross_validation(the_SVM_Model, selected_features, all_labels, folds, 'SVM')
    #print "asi mama:", svm_area_under_roc
    prev_svm_auc = svm_area_under_roc
  #print "current pointer to AUC:", svm_area_under_roc
  return svm_area_under_roc


def evaluateLOGI(paramsForTuning):
  #reff: http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
  '''
  need some adjustements for handling string values
  start
  '''
  the_penalty_for_logi = ['l1', 'l2']
  '''
  end
  '''
  global prev_logi_auc
  # 1. read dataset from file
  full_dataset_from_csv = de_utility.getDatasetFromCSV(dataset_file)
  full_rows, full_cols = np.shape(full_dataset_from_csv)
  ## 2. we will skip the first column, as it has file names
  feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip
  all_features = full_dataset_from_csv[:, 2:feature_cols]
  # 3. get labels
  dataset_for_labels = de_utility.getDatasetFromCSV(dataset_file)  ## unlike phase-1, the labels are '1' and '0', so need to take input as str
  label_cols = full_cols - 1
  all_labels  =  dataset_for_labels[:, label_cols]
  ## 4. do PCA, take all features for PCA
  '''
  lets transform all the features via log transformation
  '''
  log_transformed_features = de_utility.createLogTransformedFeatures(all_features)
  feature_input_for_pca = log_transformed_features
  pcaObj = decomposition.PCA(n_components=pcas_to_explore)
  pcaObj.fit(feature_input_for_pca)
  ## 5. trabsform daatset based on PCA
  pcaObj.n_components=no_features_to_use
  selected_features = pcaObj.fit_transform(feature_input_for_pca)
  ## 6. plugin model parameters
  #print "lol", paramsForTuning[0]
  if( (paramsForTuning[0] <= de_utility.learnerDict['LOGI'][0][0] ) ):
    logi_area_under_roc = prev_logi_auc
  elif( (paramsForTuning[0] > de_utility.learnerDict['LOGI'][0][1] ) ):
    logi_area_under_roc = prev_logi_auc
  else:
    the_LOGI_Model      = LogisticRegression( C = paramsForTuning[0], penalty = 'l2' )
    logi_area_under_roc = de_utility.perform_cross_validation(the_LOGI_Model, selected_features, all_labels, folds, 'LOGI')
    #print "asi mama:", logi_area_under_roc
    prev_logi_auc = logi_area_under_roc
  #print "current pointer to AUC:", logi_area_under_roc
  return logi_area_under_roc


def giveMeFuncNameOfThisLearner(learnerNameP):
   if learnerNameP=='CART':
    func2ret = evaluateCART
   elif learnerNameP=='RF':
    func2ret = evaluateRF
   elif learnerNameP=='SVM':
    func2ret = evaluateSVM
   elif learnerNameP=='LOGI':
    func2ret = evaluateLOGI
   return func2ret


def evaluateLearners(learnerName):
    '''
    Two things are variable: the paramters to be tuned, and the function of the lewarner
    '''
    limits_of_params   = de_utility.giveMeLimitsOfThisLearner(learnerName)
    print "Loaded required parameter limits of:", learnerName
    fn_name_of_learner = giveMeFuncNameOfThisLearner(learnerName)
    print "Loaded required obj. func of:", learnerName
    '''
    '''
    #ngen, npop = 100, 10   # npop fpr 10~30 gives good results , ngen for 30~70 givess good results
    ngen, npop = 50, 10
    my_f, my_c = 0.5, 0.5
    print "Params of DE->(gen:{}, pop:{}, f:{}, c:{})".format(ngen, npop, my_f, my_c)
    print "Dataset:", dataset_file
    print "="*100
    ndim = len(limits_of_params)
    #print limits_of_params
    pop = np.zeros([ngen, npop, ndim])
    loc = np.zeros([ngen, ndim])
    de = DiffEvolOptimizer(fn_name_of_learner, limits_of_params, npop, F=my_f, C=my_c, maximize=True)
    for i, res in enumerate(de(ngen)):
      pop[i,:,:] = de.population.copy()
      loc[i,:] = de.location.copy()
    print "Learner: {}, solution:{}, optimized prediction performance:{}".format(learnerName, de.location, abs(de.value))
    print "="*100
    return abs(de.value)
