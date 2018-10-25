'''
main script to call DE for parameter tuning
Akond Rahman
Oct 24, 2018
'''
import de_for_learners, de_utility, time
import numpy as np
date_for_dir   = time.strftime("%Y-%m-%d")
no_of_iterations  =  10

dir_              = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/DE_FSE2019/'
'''
create output directory
'''
de_utility.createOutputDirectory(dir_)
str2Dump=""
cart_holder, lr_holder, rf_holder, svm_holder =[], [], [], []
for cnt in xrange(no_of_iterations):
    perf_cart, perf_lr, perf_rf, perf_svm = 0, 0, 0, 0
    print "Iteration #", cnt
    print "*"*100
    print "Started at:", de_utility.giveTimeStamp()
    print "*"*100

    #1. run DE for tuning CART
    perf_cart = de_for_learners.evaluateLearners('CART')
    cart_holder.append(perf_cart)

    # ###2. run DE for tuning Logistic Regression
    perf_lr = de_for_learners.evaluateLearners('LOGI')
    lr_holder.append(perf_lr)

    # # 3. run DE for tuning RF
    perf_rf =  de_for_learners.evaluateLearners('RF')
    rf_holder.append(perf_rf)

    ###4. run DE for tuning SVM
    perf_svm = de_for_learners.evaluateLearners('SVM')
    svm_holder.append(perf_svm)



    print "Ended at:", de_utility.giveTimeStamp()
    print "*"*100

de_utility.saveResults(cart_holder, dir_  + '_CART_'  + '.csv')
de_utility.saveResults(lr_holder,   dir_  + '_LOGI_'  + '.csv')
de_utility.saveResults(rf_holder,   dir_  + '_RAFO_'  + '.csv')
de_utility.saveResults(svm_holder,  dir_  + '_SUVM_'  + '.csv')
print "CART:::MEDIAN:::", np.median(cart_holder)
print "LORI:::MEDIAN:::", np.median(lr_holder)
print "RAFO:::MEDIAN:::", np.median(rf_holder)
print "SUVM:::MEDIAN:::", np.median(svm_holder)
print "*"*100
