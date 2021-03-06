'''
Akond Rahman
April 01, 2017
utility file for process metric
'''
from collections import Counter
import os, csv, numpy as np, time, datetime
import os, subprocess, numpy as np, operator
from  collections import Counter
from scipy.stats import entropy
import math
import pandas as pd

def getPuppetFileDetails(theCompleteCategFile):
    dictOfAllFiles={}
    dict2Ret={}
    with open(theCompleteCategFile, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
        repo_of_file       = row_[1]
        categ_of_file      = row_[3]
        full_path_of_file  = row_[4]
        if full_path_of_file not in dictOfAllFiles:
            dictOfAllFiles[full_path_of_file] = [[ categ_of_file ], repo_of_file]
        else:
            dictOfAllFiles[full_path_of_file][0] = dictOfAllFiles[full_path_of_file][0] + [ categ_of_file ]
    for k_, v_ in dictOfAllFiles.items():
       uniq = np.unique(v_[0])
       if ((len(uniq)==1) and (uniq[0]=='N')):
         dict2Ret[k_] = ('0', v_[1])
       else:
         dict2Ret[k_] = ('1', v_[1])
    return dict2Ret




def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP )
  fileToWrite.close()
  return str(os.stat(fileP).st_size)
def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def createDataset(str2Dump, datasetNameParam):
   headerOfFile0='org,file_,'
   #headerOfFile1='COMM,AGE,DEV,AVGTIMEOFEDITS,ADDPERLOC,'
   headerOfFile1='COMM,AGE,DEV,ADDPERLOC,'
   #headerOfFile2='DELPERLOC,ADDNORM,DELNORM,AVGCHNG,MINOR,OWN,SCTR,'
   headerOfFile2='DELPERLOC,SUMCHNG,TOTCHNGPERLOC,AVGCHNG,MINOR,SCTR,'
   #headerOfFile3='COMM_SIZE,MT_PP, MT_NON_PP,'
   headerOfFile3='MT_PP,MT_NON_PP,'
   headerOfFile4='defect_status'

   headerStr = headerOfFile0 + headerOfFile1 + headerOfFile2  +  headerOfFile3 + headerOfFile4

   str2Write = headerStr + '\n' + str2Dump
   return dumpContentIntoFile(str2Write, datasetNameParam)
def getDatasetFromCSV(fileParam, dataTypeFlag=True):
  if dataTypeFlag:
    data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1, dtype='float')
  else:
        data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1,  dtype='str')
  return data_set_to_return

'''
for opnestack bad boys
'''
def getScatterFromBadBoyFile(fileName, sloc):
   blame_output =[]
   '''
   output list
   '''
   lineNoProb        = []
   lineNoCnt         = []
   '''
   '''
   lineNoProb = []
   with open(theCompleteCategFile, 'rU') as file_:
      reader_ = csv.reader(file_)
      for row_ in reader_:
          blame_output.append(row_[0])
   line_chng_dict    = dict(Counter(blame_output))
   #print line_chng_dict
   for lineNo in xrange(sloc):
       line_key  = str(lineNo + 1)
       if (line_key in line_chng_dict):
          line_cnt  = line_chng_dict[line_key]
       else:
          line_cnt  = 0
       line_prob = float(line_cnt)/float(sloc)
       lineNoProb.append(line_prob) ### Version 1
       lineNoCnt.append(line_cnt)   ### Version 2
   #print "len:{}, list:{}, loc:{}".format(len(lineNoProb), lineNoProb, sloc)
   scatterness_prob = round(entropy(lineNoProb), 5)  ##Version 1
   scatterness_cnt  = round(entropy(lineNoCnt), 5)  ##Version 2
   '''
   handling -inf, inf
   '''
   if((scatterness_cnt == float("-inf")) or (scatterness_cnt == float("inf"))):
     scatterness_cnt = float(0)
   return scatterness_cnt
'''
list missing files
'''
def listMissingFiles(dataset_1, dataset_2):
    static_datset =[]
    process_dataset = []
    str_ = ''
    with open(dataset_1, 'rU') as file_:
          reader_ = csv.reader(file_)
          next(reader_, None)
          for row_ in reader_:
              static_datset.append(row_[1])
    print len(static_datset)
    print(len(np.unique(static_datset)))
    print(Counter(static_datset))
    with open(dataset_2, 'rU') as file_2:
          reader2_ = csv.reader(file_2)
          next(reader2_, None)
          for row_2 in reader2_:
              process_dataset.append(row_2[1])
    missing_files = [x for x in static_datset if x not in process_dataset]
    for file_name in missing_files:
        str_ = str_ + file_name + ',' + '\n'
    dumpContentIntoFile(str_, '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/DoAgainOpenstack.csv')




def createOutputDirectory(dirParam):
  if not os.path.exists(dirParam):
     os.makedirs(dirParam)
  if os.path.exists(dirParam):
     print "Output directory created ..."

def getMercurialProgrammerList(file_with_rel_path, repo_path):
   prog_output = []
   if (('student' not in file_with_rel_path) and ('.csv' not in file_with_rel_path) and ('.txt' not in file_with_rel_path) and ('EXTRA_AST' not in file_with_rel_path)):
      cdCommand         = "cd " + repo_path + " ; "
      commitCountCmd    = "hg churn --diffstat  " + file_with_rel_path + " | awk '{print $1}'  "
      command2Run = cdCommand + commitCountCmd
      _output = subprocess.check_output(['bash','-c', command2Run])
      prog_output = _output.split('\n')
      prog_output = [x_ for x_ in prog_output if x_!='']
   return prog_output

def getRepoList(org_name_p):
    repoList2Ret = []
    the_eligible_file = org_name_p + 'eligible_repos.csv'
    with open(the_eligible_file, 'rU') as file_:
         reader_ = csv.reader(file_)
         for row_ in reader_:
             repoList2Ret.append( org_name_p + row_[0] + '/')
    return repoList2Ret

def getMercurialProgToFileMapping(org_name_p):
   dict2ret = {}
   repo_list = getRepoList(org_name_p)
   for repo_path_param in repo_list:
       cdCommand         = "cd " + repo_path_param + " ; "
       progToFileCommand = "hg status --all | cut -d' ' -f2 "
       command2Run = cdCommand + progToFileCommand

       all_file_in_repo_output = subprocess.check_output(['bash','-c', command2Run])
       all_file_in_repo_output = all_file_in_repo_output.split('\n')
       all_file_in_repo_output = [x_ for x_ in all_file_in_repo_output if x_!='']
       for file_ in all_file_in_repo_output:
           prog_list = getMercurialProgrammerList(file_, repo_path_param)
           for programmer_ in prog_list:
               if programmer_ not in dict2ret:
                  dict2ret[programmer_] =  [file_]
               else:
                  dict2ret[programmer_] = dict2ret[programmer_] + [file_]
   return dict2ret

def getGitProgrammerList(file_with_rel_path, repo_path):
   prog_output = []
   #print file_with_rel_path, repo_path
   if (('student' not in file_with_rel_path) and ('.csv' not in file_with_rel_path) and ('.txt' not in file_with_rel_path) and ('EXTRA_AST' not in file_with_rel_path)):
      cdCommand         = "cd " + repo_path + " ; "
      commitCountCmd    = " git blame "+ file_with_rel_path +"  | awk '{print $2}' | cut -d'(' -f2 "
      command2Run = cdCommand + commitCountCmd
      _output = subprocess.check_output(['bash','-c', command2Run])
      prog_output = _output.split('\n')
      prog_output = [x_ for x_ in prog_output if x_!='']
   return prog_output





def getGitProgToFileMapping(org_name_p):
   dict2ret = {}
   repo_list = getRepoList(org_name_p)
   #print repo_list
   for repo_path_param in repo_list:
       #print repo_path_param
       cdCommand         = "cd " + repo_path_param + " ; "
       progToFileCommand = "git ls-files "
       command2Run = cdCommand + progToFileCommand

       all_file_in_repo_output = subprocess.check_output(['bash','-c', command2Run])
       all_file_in_repo_output = all_file_in_repo_output.split('\n')
       all_file_in_repo_output = [x_ for x_ in all_file_in_repo_output if x_!='']
       #print all_file_in_repo_output
       for file_ in all_file_in_repo_output:
           prog_list = getGitProgrammerList(file_, repo_path_param)
           for programmer_ in prog_list:
               if programmer_ not in dict2ret:
                  dict2ret[programmer_] =  [file_]
               else:
                  dict2ret[programmer_] = dict2ret[programmer_] + [file_]
   return dict2ret


def createLogTransformedFeatures(allFeatureParam):
  log_transformed_feature_dataset_to_ret = []
  dataset_rows = len(allFeatureParam)
  print "-"*50
  print "Dataset rows:",dataset_rows
  print "-"*50
  for ind_ in xrange(dataset_rows):
    features_for_this_index = allFeatureParam[ind_, :]
    ## do the log tranform on the extracted index
    ## the following code handles the issue for zero values
    log_transformed_features_for_index = [math.log1p(x_) for x_ in features_for_this_index]
    log_transformed_feature_dataset_to_ret.append(log_transformed_features_for_index)
  ## convert to numpy  array
  log_transformed_feature_dataset_to_ret = np.array(log_transformed_feature_dataset_to_ret)
  return log_transformed_feature_dataset_to_ret
'''
YEAR WISE DATA EXTRACTION
'''
def getYear(single_date):
    dt2ret = single_date.split('-')[0]
    return dt2ret

def getTimeInfo(id_param, repo_param):
    dict2see = {}
    if repo_param.endswith('/'):
       repo_param = repo_param
    else:
       repo_param = repo_param + '/'
    file2read = repo_param + 'fullThrottle_msg_file_map.csv'
    with open(file2read, 'rU') as f:
         reader_ = csv.reader(f)
         for row in reader_:
             id_       = row[0]
             ts_    = row[2]
             dict2see[id_] = ts_
    return dict2see[id_param]



def getYearFileCount(df_param):
    _df = pd.DataFrame(df_param, columns=['ID', 'REPO', 'FILE', 'TIME', 'DEFECTSTATUS'])
    _df['YEAR']  = _df['TIME'].apply(getYear)
    _df         = _df.sort(['YEAR'])
    _df_year_cnt = _df.groupby(['YEAR'])[['FILE']].count()

    y_list         = _df_year_cnt.index.get_level_values('YEAR').tolist()
    y_c_list       = _df_year_cnt['FILE'].tolist()
    return y_list, y_c_list



def getAllYearsFromDataset(categ_file_param):
       str2write = ''
       df_list = []
       '''
       dicionary to hold files for each year
       '''
       year_file_dict, defect_file_dict, repo_file_dict = {}, {}, {}
       with open(categ_file_param, 'rU') as f:
         reader_ = csv.reader(f)
         next(reader_, None)
         for row in reader_:
             id_       = row[0]
             repo_     = row[1]
             categ_    = row[3]
             if categ_=='N':
                 defect_status = '0'
             else:
                 defect_status = '1'
             filepath_ = row[4]
             time_ = getTimeInfo(id_, repo_)
             time2write = time_.split(' ')[0]
             df_list.append((id_, repo_, filepath_, time2write, defect_status))
             '''
             dictionary year
             '''
             y2write = getYear(time2write)
             if y2write not in year_file_dict:
                 year_file_dict[y2write] = [filepath_]
             else:
                 year_file_dict[y2write] = year_file_dict[y2write] + [filepath_]
             '''
             dictionary files
             '''
             if filepath_ not in defect_file_dict:
                 defect_file_dict[filepath_] = defect_status
             '''
             dictionary repos
             '''
             if filepath_ not in repo_file_dict:
                 repo_file_dict[filepath_] = repo_
       # get all years, and files in the year for the dataset
       y_list, y_c_list = getYearFileCount(df_list)
       return y_list, year_file_dict, defect_file_dict, repo_file_dict

'''
TIME DATASET SPLITTING EXTRACT ZONE
'''

def getAllRepos(file_name):
       all_repos = []
       with open(file_name, 'rU') as f:
         reader_ = csv.reader(f)
         for row in reader_:
             all_repos.append(row[0])
       return all_repos

'''
TIME METRIC EXTRACT ZONE
'''
def getRepoToFileMapping(categ_output_file):
    repo_file_dict={}
    with open(categ_output_file, 'rU') as f:
      reader_ = csv.reader(f)
      next(reader_, None)
      for row in reader_:
          repo_     = row[1]
          filepath_ = row[4]
          if repo_ not in repo_file_dict:
             repo_file_dict[repo_] = filepath_
          else:
             repo_file_dict[repo_] = repo_file_dict[repo_] + filepath_
    return repo_file_dict


def getRecursivelyPPFilles(repo_path):
        all_files = []
        for root, subFolders, _files in os.walk(repo_path):
            for file_ in _files:
                if ('.pp' in file_):
                   the_pp_file = os.path.join(root, file_)
                   if('EXTRA_AST' not in the_pp_file):
                     all_files.append(the_pp_file)
        return all_files


def getDefectData(year_param, categ_file_param):
       defect_file_dict, output_dict = {}, {}
       with open(categ_file_param, 'rU') as f:
         reader_ = csv.reader(f)
         next(reader_, None)
         for row in reader_:
             id_       = row[0]
             file_     = row[4]
             repo_     = row[1]
             categ_    = row[3]
             time_ = getTimeInfo(id_, repo_)
             y2check = time_.split(' ')[0]
             y2check = y2check.split('-')[0]
             #print y2check, year_param
             if (y2check==year_param):
                 if file_ not in defect_file_dict:
                    defect_file_dict[file_] = [categ_]
                 else:
                    defect_file_dict[file_] =  defect_file_dict[file_] + [categ_]
       for file_, categs in defect_file_dict.iteritems():
           categs_ = np.unique(categs)
           if((categs_[0]=='N') and (len(categs_)==1)):
               defect_satus = '0'
           else:
               defect_satus = '1'
           output_dict[file_] = defect_satus
       return output_dict
def getAllYearsFromCategFile(categ_file_param):
       df_list = []
       with open(categ_file_param, 'rU') as f:
         reader_ = csv.reader(f)
         next(reader_, None)
         for row in reader_:
             id_       = row[0]
             repo_     = row[1]
             filepath_ = row[4]
             categ_    = row[3]
             if categ_=='N':
                 defect_status = '1'
             else:
                 defect_status = '0'
             time_ = getTimeInfo(id_, repo_)
             time2write = time_.split(' ')[0]

             df_list.append((id_, repo_, filepath_, time2write, defect_status))

       # get all years, and files in the year for the dataset
       y_list, y_c_list = getYearFileCount(df_list)
       return y_list
'''
PREDICTION TIME SPLITTING
'''

def getFeaturesAndLabels(file_name_param):
       training_dataset = getDatasetFromCSV(file_name_param)
       full_rows, full_cols = np.shape(training_dataset)
       feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip
       training_features = training_dataset[:, 2:feature_cols]
       '''
       lets transform all the features via log transformation
       '''
       log_transformed_train_features = createLogTransformedFeatures(training_features)
       '''
       get labels
       '''
       dataset_for_labels = getDatasetFromCSV(file_name_param)
       label_cols = full_cols - 1
       all_labels  =  dataset_for_labels[:, label_cols]
       defected_file_count     = len([x_ for x_ in all_labels if x_==1.0])
       non_defected_file_count = len([x_ for x_ in all_labels if x_==0.0])
       print "No of. defects={}, non-defects={}".format(defected_file_count, non_defected_file_count)
       print "-"*50
       return log_transformed_train_features, all_labels
