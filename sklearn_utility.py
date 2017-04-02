'''
Sklearn items for prediction model
Akond Rahman
April 02, 2017
'''




from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import precision_score, recall_score
import numpy as np, pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation, svm
from sklearn.linear_model import RandomizedLogisticRegression, LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, mean_absolute_error, accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
import process_metric_utility




def dumpPredPerfValuesToFile(iterations, predPerfVector, fileName):
   str2write=''
   headerStr='AUC,PRECISION,RECALL,'
   for cnt in xrange(iterations):
     auc_   = predPerfVector[0][cnt]
     prec_  = predPerfVector[1][cnt]
     recal  = predPerfVector[2][cnt]
     str2write = str2write + str(auc_) + ',' + str(prec_) + ',' + str(recal) + ',' + '\n'
   str2write = headerStr + '\n' + str2write
   bytes_ = Utility.dumpContentIntoFile(str2write, fileName)
   print "Created {} of {} bytes".format(fileName, bytes_)




def evalClassifier(actualLabels, predictedLabels):
  '''
    the way skelarn treats is the following: first index -> lower index -> 0 -> 'Low'
                                             next index after first  -> next lower index -> 1 -> 'high'
  '''
  target_labels =  ['N', 'Y']
  '''
    peeking into the labels of the dataset
  '''
  #print "Glimpse at  actual:{}, and predicted:{} labels(10th entry in label list)".format(actualLabels[10], predictedLabels[10])
  print classification_report(actualLabels, predictedLabels, target_names=target_labels)
  print">"*25
  '''
  getting the confusion matrix
  '''
  #conf_matr_output = confusion_matrix(actualLabels, predictedLabels)
  print "Confusion matrix start"
  #print conf_matr_output
  conf_matr_output = pd.crosstab(actualLabels, predictedLabels, rownames=['True'], colnames=['Predicted'], margins=True)
  print conf_matr_output
  print "Confusion matrix end"
  # preserve the order first test(real values from dataset), then predcited (from the classifier )
  '''
  the precision score is computed as follows:
  '''
  prec_ = precision_score(actualLabels, predictedLabels, average='binary')
  #print "The precision score is:", prec_
  #print">"*25
  '''
  the recall score is computed as follows:
  '''
  recall_ = recall_score(actualLabels, predictedLabels, average='binary')
  #print">"*25
  '''
    are under the curve values .... reff: http://gim.unmc.edu/dxtests/roc3.htm
    0.80~0.90 -> good, any thing less than 0.70 bad , 0.90~1.00 -> excellent
  '''
  #print predictedLabels
  area_roc_output = roc_auc_score(actualLabels, predictedLabels)
  # preserve the order first test(real values from dataset), then predcited (from the classifier )
  #print "Area under the ROC curve is ", area_roc_output
  #print">"*10
  '''
    mean absolute error (mae) values .... reff: http://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html
    the smaller the better , ideally expect 0.0
  '''
  #mae_output = mean_absolute_error(actualLabels, predictedLabels)
  # preserve the order first test(real values from dataset), then predcited (from the classifier )
  #print "Mean absolute errro output  is ", mae_output
  #print">"*25
  '''
  accuracy_score ... reff: http://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter .... percentage of correct predictions
  ideally 1.0, higher the better
  '''
  #accuracy_score_output = accuracy_score(actualLabels, predictedLabels)
  # preserve the order first test(real values from dataset), then predcited (from the classifier )
  #print "Accuracy output  is ", accuracy_score_output
  #print">"*10
  '''
    this function returns area under the curve , which will be used
    for D.E. and repated measurements
  '''
  return area_roc_output, prec_, recall_


def perform_cross_validation(classiferP, featuresP, labelsP, cross_vali_param, infoP):
  '''
  note: cross_val_predict already uses staritifed k fold :
  reff: http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_predict.html
  '''
  predicted_labels = cross_validation.cross_val_predict(classiferP, featuresP , labelsP, cv=cross_vali_param)
  area_roc_to_ret = evalClassifier(labelsP, predicted_labels)
  return area_roc_to_ret


def performCART(featureParam, labelParam, foldParam, infoP):
  theCARTModel = DecisionTreeClassifier()
  '''
  with optimized parameters
  first mozilla, then wikimedia
  '''
  ###theCARTModel = DecisionTreeClassifier(max_features=0.55, min_samples_split=7.08, min_samples_leaf=19.25, max_depth=17.32)
  ###theCARTModel = DecisionTreeClassifier(max_features=0.55, min_samples_split=19.37, min_samples_leaf=6.80, max_depth=22.10)

  cart_area_under_roc = perform_cross_validation(theCARTModel, featureParam, labelParam, foldParam, infoP)
  print "For {}, area under ROC is: {}".format(infoP, cart_area_under_roc[0])
  return cart_area_under_roc





def performKNN(featureParam, labelParam, foldParam, infoP):
  theKNNModel = KNeighborsClassifier()
  '''
  with optimized parameters
  '''
  knn_area_under_roc = perform_cross_validation(theKNNModel, featureParam, labelParam, foldParam, infoP)
  print "For {}, area under ROC is: {}".format(infoP, knn_area_under_roc[0])
  return knn_area_under_roc





def performRF(featureParam, labelParam, foldParam, infoP):
  theRndForestModel = RandomForestClassifier()
  '''
  with optimized parameters
  first mozilla then wiki
  '''
  #theRndForestModel = RandomForestClassifier(max_features = int(1.65),    max_leaf_nodes = int(44.10),
  #                                          min_samples_split=16.44, min_samples_leaf=8.35,
  #                                          n_estimators=int(17.85))

  # theRndForestModel = RandomForestClassifier(max_features = 1,    max_leaf_nodes = int(3.75),
  #                                         min_samples_split=14.55, min_samples_leaf=12.78,
  #                                         n_estimators=int(97.58))
  rf_area_under_roc = perform_cross_validation(theRndForestModel, featureParam, labelParam, foldParam, infoP)
  print "For {} area under ROC is: {}".format(infoP, rf_area_under_roc[0])
  return rf_area_under_roc

def performSVC(featureParam, labelParam, foldParam, infoP):
  theSVMModel = svm.SVC(kernel='rbf').fit(featureParam, labelParam)
  '''
  with optimized parameters
  first mozilla then wiki
  '''
  #theSVMModel = svm.SVC(C = 0.59, kernel = 'rbf', gamma = 0.12).fit(featureParam, labelParam)
  ###theSVMModel = svm.SVC(C = 0.38, kernel = 'rbf', gamma = 0.50).fit(featureParam, labelParam)
  svc_area_under_roc = perform_cross_validation(theSVMModel, featureParam, labelParam, foldParam, infoP)
  print "For {} area under ROC is: {}".format(infoP, svc_area_under_roc[0])
  return svc_area_under_roc


def performLogiReg(featureParam, labelParam, foldParam, infoP):
  theLogisticModel = LogisticRegression()
  '''
  with optimized parameters
  first is mozilla then wiki
  '''
  ###theLogisticModel = LogisticRegression( C = 0.60, penalty = 'l1' )
  ###theLogisticModel = LogisticRegression( C = 0.11, penalty = 'l1' )
  theLogisticModel.fit(featureParam, labelParam)
  logireg_area_under_roc = perform_cross_validation(theLogisticModel, featureParam, labelParam, foldParam, infoP)
  print "For {} area under ROC is: {}".format(infoP, logireg_area_under_roc[0])
  return logireg_area_under_roc



def performNaiveBayes(featureParam, labelParam, foldParam, infoP):
  theNBModel = GaussianNB()
  #theNBModel = MultinomialNB()
  #theNBModel = BernoulliNB()
  '''
  with optimized parameters
  first is mozilla then wiki
  '''
  theNBModel.fit(featureParam, labelParam)
  gnb_area_under_roc = perform_cross_validation(theNBModel, featureParam, labelParam, foldParam, infoP)
  print "For {} area under ROC is: {}".format(infoP, gnb_area_under_roc[0])
  return gnb_area_under_roc



def performModeling(features, labels, foldsParam):
  #r_, c_ = np.shape(features)
  ### lets do CART (decision tree)
  performCART(features, labels, foldsParam, "CART")
  print "="*100
  # ### lets do knn (nearest neighbor)
  # performKNN(features, labels, foldsParam, "KNN")
  # print "="*100
  ### lets do RF (ensemble method: random forest)
  performRF(features, labels, foldsParam, "RF")
  print "="*100
  ### lets do SVC (support vector: support-vector classification)
  performSVC(features, labels, foldsParam, "SVC")
  print "="*100
  ### lets do Logistic regession
  performLogiReg(features, labels, foldsParam, "LogiRegr")
  print "="*100
  ### lets do naive bayes
  performNaiveBayes(features, labels, foldsParam, "Naive-Bayes")
  print "="*100
def performIterativeModeling(featureParam, labelParam, foldParam, iterationP):
  cart_prec_holder, cart_recall_holder, holder_cart = [], [], []
  # knn_prec_holder,  knn_recall_holder,  holder_knn  = [], [], []
  rf_prec_holder,   rf_recall_holder,   holder_rf   = [], [], []
  svc_prec_holder,  svc_recall_holder,  holder_svc  = [], [], []
  logi_prec_holder, logi_recall_holder, holder_logi = [], [], []
  nb_prec_holder,   nb_recall_holder,   holder_nb   = [], [], []
  for ind_ in xrange(iterationP):
    ## iterative modeling for CART
    cart_area_roc      = performCART(featureParam, labelParam, foldParam, "CART")[0]
    cart_prec_         = performCART(featureParam, labelParam, foldParam, "CART")[1]
    cart_recall_       = performCART(featureParam, labelParam, foldParam, "CART")[2]
    holder_cart.append(cart_area_roc)
    cart_prec_holder.append(cart_prec_)
    cart_recall_holder.append(cart_recall_)
    cart_area_roc = float(0)
    cart_prec_    = float(0)
    cart_recall_  = float(0)


    ## iterative modeling for RF
    rf_area_roc = performRF(featureParam, labelParam, foldParam, "Rand. Forest")[0]
    rf_prec_    = performRF(featureParam, labelParam, foldParam, "Rand. Forest")[1]
    rf_recall_  = performRF(featureParam, labelParam, foldParam, "Rand. Forest")[2]
    holder_rf.append(rf_area_roc)
    rf_prec_holder.append(rf_prec_)
    rf_recall_holder.append(rf_recall_)
    rf_area_roc = float(0)
    rf_prec_    = float(0)
    rf_recall_  = float(0)

    ## iterative modeling for SVC
    svc_area_roc = performSVC(featureParam, labelParam, foldParam, "Supp. Vector Classi.")[0]
    svc_prec_    = performSVC(featureParam, labelParam, foldParam, "Supp. Vector Classi.")[1]
    svc_recall_  = performSVC(featureParam, labelParam, foldParam, "Supp. Vector Classi.")[2]
    holder_svc.append(svc_area_roc)
    svc_prec_holder.append(svc_prec_)
    svc_recall_holder.append(svc_recall_)
    svc_area_roc = float(0)
    svc_prec_    = float(0)
    svc_recall_  = float(0)

    ## iterative modeling for logistic regression
    logi_reg_area_roc = performLogiReg(featureParam, labelParam, foldParam, "Logi. Regression Classi.")[0]
    logi_reg_preci_   = performLogiReg(featureParam, labelParam, foldParam, "Logi. Regression Classi.")[1]
    logi_reg_recall   = performLogiReg(featureParam, labelParam, foldParam, "Logi. Regression Classi.")[2]
    holder_logi.append(logi_reg_area_roc)
    logi_prec_holder.append(logi_reg_preci_)
    logi_recall_holder.append(logi_reg_recall)
    logi_reg_area_roc = float(0)
    logi_reg_preci_   = float(0)
    logi_reg_recall   = float(0)

    ## iterative modeling for naiev bayes
    nb_area_roc = performNaiveBayes(featureParam, labelParam, foldParam, "Naive Bayes")[0]
    nb_preci_   = performNaiveBayes(featureParam, labelParam, foldParam, "Naive Bayes")[1]
    nb_recall   = performNaiveBayes(featureParam, labelParam, foldParam, "Naive Bayes")[2]
    holder_nb.append(nb_area_roc)
    nb_prec_holder.append(nb_preci_)
    nb_recall_holder.append(nb_recall)
    nb_area_roc = float(0)
    nb_preci_   = float(0)
    nb_recall   = float(0)

  print "-"*50
  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(holder_cart),
                                                                          np.median(holder_cart), max(holder_cart),
                                                                          min(holder_cart))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(cart_prec_holder),
                                                                          np.median(cart_prec_holder), max(cart_prec_holder),
                                                                          min(cart_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(cart_recall_holder),
                                                                          np.median(cart_recall_holder), max(cart_recall_holder),
                                                                          min(cart_recall_holder))
  print "*"*25
  cart_all_pred_perf_values = (holder_cart, cart_prec_holder, cart_recall_holder)
  dumpPredPerfValuesToFile(iterationP, cart_all_pred_perf_values, '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/PRED_PERF_CART.csv')
  print "-"*50

  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(holder_rf),
                                                                          np.median(holder_rf), max(holder_rf),
                                                                          min(holder_rf))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(rf_prec_holder),
                                                                          np.median(rf_prec_holder), max(rf_prec_holder),
                                                                          min(rf_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(rf_recall_holder),
                                                                          np.median(rf_recall_holder), max(rf_recall_holder),
                                                                          min(rf_recall_holder))
  print "*"*25
  rf_all_pred_perf_values = (holder_rf, rf_prec_holder, rf_recall_holder)
  dumpPredPerfValuesToFile(iterationP, rf_all_pred_perf_values, '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/PRED_PERF_RF.csv')
  print "-"*50

  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class.", np.mean(holder_svc),
                                                                          np.median(holder_svc), max(holder_svc),
                                                                          min(holder_svc))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class.", np.mean(svc_prec_holder),
                                                                            np.median(svc_prec_holder), max(svc_prec_holder),
                                                                            min(svc_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class.", np.mean(svc_recall_holder),
                                                                            np.median(svc_recall_holder), max(svc_recall_holder),
                                                                            min(svc_recall_holder))
  print "*"*25
  svc_all_pred_perf_values = (holder_svc, svc_prec_holder, svc_recall_holder)
  dumpPredPerfValuesToFile(iterationP, svc_all_pred_perf_values, '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/PRED_PERF_SVC.csv')
  print "-"*50

  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(holder_logi),
                                                                          np.median(holder_logi), max(holder_logi),
                                                                          min(holder_logi))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(logi_prec_holder),
                                                                            np.median(logi_prec_holder), max(logi_prec_holder),
                                                                            min(logi_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(logi_recall_holder),
                                                                            np.median(logi_recall_holder), max(logi_recall_holder),
                                                                            min(logi_recall_holder))
  print "*"*25
  nb_all_pred_perf_values = (holder_logi, logi_prec_holder, logi_recall_holder)
  dumpPredPerfValuesToFile(iterationP, logireg_all_pred_perf_values, '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/PRED_PERF_LOGIREG.csv')
  print "-"*50

  '''
  added later: March 14, 2017: 12:01 AM
  '''
  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Naive Bayes", np.mean(holder_nb),
                                                                          np.median(holder_nb), max(holder_nb),
                                                                          min(holder_nb))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Naive Bayes", np.mean(nb_prec_holder),
                                                                            np.median(nb_prec_holder), max(nb_prec_holder),
                                                                            min(nb_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Naive Bayes", np.mean(nb_recall_holder),
                                                                            np.median(nb_recall_holder), max(nb_recall_holder),
                                                                            min(nb_recall_holder))
  print "*"*25
  nb_all_pred_perf_values = (holder_nb, nb_prec_holder, nb_recall_holder)
  dumpPredPerfValuesToFile(iterationP, nb_all_pred_perf_values, '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/PRED_PERF_NB.csv')
  print "-"*50
