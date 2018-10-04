'''
Apri 01, 2017
Extracting process metrics
Akond Rahman
'''
import hg_process_extractor
import git_process_extractor 
import process_metric_utility

MOZFLAG='moz'
WIKIFLAG='wikimedia'
OPENSTACKFLAG='openstack'

def getAllProcessMetricsForSingleFile(full_path_param, repo_path_param, org_of_file):
  if(MOZFLAG in full_path_param):
     process_metrics         =  hg_process_extractor.getProcessMetrics(full_path_param, repo_path_param)
  elif(WIKIFLAG in full_path_param):
      process_metrics         =  git_process_extractor.getProcessMetrics(full_path_param, repo_path_param)
  else:
      process_metrics         =  git_process_extractor.getProcessMetrics(full_path_param, repo_path_param)
  print process_metrics
  print "Generated the process metrics ... "
  print "-"*50
  all_metric_as_str_for_file      = org_of_file + ',' + full_path_param + ',' + process_metrics
  return all_metric_as_str_for_file



def getAllProcessMetricForAllFiles(pupp_map_dict_param, datasetFile2Save, org_name):
   str2ret=''
   fileCount = 0
   '''
   LOAD the file to programmer dicts first
   '''
   #moz_prog_to_file_dist = process_metric_utility.getMercurialProgToFileMapping(repo_)
   for file_, details_ in pupp_map_dict_param.items():
     if (file_!= 'WTF'):
        fileCount = fileCount + 1
        repo_                    = details_[1]
        defect_status            = details_[0]
        print "Analyzing ... \nfile#{}\ndefect status:{}\nfile:{}\nrepo:{}".format(fileCount, defect_status, file_, repo_)
        all_metric_for_this_file = getAllProcessMetricsForSingleFile(file_, repo_, org_name)
        str2ret = str2ret + all_metric_for_this_file + defect_status + '\n'
        print "="*75
   dump_stats = process_metric_utility.createDataset(str2ret, datasetFile2Save)
   print "Dumped a file of {} bytes".format(dump_stats)
   return str2ret

'''
for dataset generation 
'''

### INPUT

init_dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/MIR_FUL_PRO.csv'
ORG = 'MIRANTIS'

# init_dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/MOZ_FUL_PRO.csv'
# init_dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/OST_FUL_PRO.csv'
# init_dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/WIK_FUL_PRO.csv'


### OUTPUT

datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/MIR_CHANGE_DATASET.csv'




print "Started at:", process_metric_utility.giveTimeStamp()
fullPuppMap   = process_metric_utility.getPuppetFileDetails(init_dataset_file)
print "Loaded the defect mapping of files ... "
print "-"*100


str_ = getAllProcessMetricForAllFiles(fullPuppMap, datasetFile2Save, ORG)
print "-"*100
print "We analyzed {} Puppet files".format(len(fullPuppMap))
print "-"*100
print "Ended at:", process_metric_utility.giveTimeStamp()
print "-"*100
