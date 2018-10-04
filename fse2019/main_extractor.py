'''
Apri 01, 2017
Extracting process metrics
Akond Rahman
'''
import hg_process_extractor, git_process_extractor, process_metric_utility
MOZFLAG='moz'
WIKIFLAG='wikimedia'
OPENSTACKFLAG='openstack'

def getAllProcessMetricsForSingleFile(full_path_param, repo_path_param, prog_to_file_dict, org_of_file):
  if(MOZFLAG in full_path_param):
     process_metrics         =  hg_process_extractor.getProcessMetrics(full_path_param, repo_path_param, prog_to_file_dict)
     #org_of_file             =  'MOZILLA'
  elif(WIKIFLAG in full_path_param):
      process_metrics         =  git_process_extractor.getProcessMetrics(full_path_param, repo_path_param, prog_to_file_dict)
      #org_of_file             =  'WIKIMEDIA'
  else:
      process_metrics         =  git_process_extractor.getProcessMetrics(full_path_param, repo_path_param, prog_to_file_dict)
      #org_of_file             =  'OPENSTACK'
  print process_metrics
  print "Generated the process metrics ... "
  print "-"*50
  all_metric_as_str_for_file      = org_of_file + ',' + full_path_param + ',' + process_metrics
  return all_metric_as_str_for_file



def getAllProcessMetricForAllFiles(pupp_map_dict_param, datasetFile2Save, prog_to_file_dict, org_name):
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
        all_metric_for_this_file = getAllProcessMetricsForSingleFile(file_, repo_, prog_to_file_dict, org_name)
        str2ret = str2ret + all_metric_for_this_file + defect_status + '\n'
        print "="*75
   dump_stats = process_metric_utility.createDataset(str2ret, datasetFile2Save)
   print "Dumped a file of {} bytes".format(dump_stats)
   return str2ret

'''
testing purpose
'''
test_hg_file  = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/relabs-puppet/manifests/site.pp'
test_git_file = '/Users/akond/PUPP_REPOS/wikimedia-downloads/mariadb/manifests/heartbeat.pp'
git_repo_path = '/Users/akond/PUPP_REPOS/wikimedia-downloads/mariadb'
hg_repo_path  = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/relabs-puppet/'

# getAllProcessMetricsForSingleFile(test_hg_file, hg_repo_path)
# getAllProcessMetricsForSingleFile(test_git_file, git_repo_path)


'''
for dataset geenration
'''

### INPUT
# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.WithoutBadBoys.Final.Categ.csv'
# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'

# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mirantis_Categ_For_DB.csv'
# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Redhat_Categ_For_DB.csv'
# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Cisco_Categ_For_DB.csv'
# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Cern_Categ_For_DB.csv'
# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Bastion_Categ_For_DB.csv'


### OUTPUT
# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_MOZ_FULL_PROCESS_DATASET.csv'
# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_NOBADBOYS_FULL_PROCESS_OPENSTACK_DATASET.csv'
# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_WIKI_FULL_PROCESS_DATASET.csv'

# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_MIRANTIS_FULL_PROCESS_DATASET.csv'
# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_REDHAT_FULL_PROCESS_DATASET.csv'
# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_CISCO_FULL_PROCESS_DATASET.csv'
# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_CERN_FULL_PROCESS_DATASET.csv'
# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_BASTION_FULL_PROCESS_DATASET.csv'

### Multi tasking detection
# org_name = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/'
# org_name = '/Users/akond/PUPP_REPOS/openstack-downloads/'
# org_name = '/Users/akond/PUPP_REPOS/wikimedia-downloads/'

# org_name = '/Users/akond/PUPP_REPOS/mirantis-downloads/'
# ORG   = 'MIRANTIS'
# org_name = '/Users/akond/PUPP_REPOS/redhat-cip-downloads/'
# ORG   = 'REDHAT'
# org_name = '/Users/akond/PUPP_REPOS/cisco-downloads/'
# ORG   = 'CISCO'
# org_name = '/Users/akond/PUPP_REPOS/bastionltd-downloads/'
# ORG   = 'BASTION'


print "Started at:", process_metric_utility.giveTimeStamp()
fullPuppMap   = process_metric_utility.getPuppetFileDetails(theCompleteCategFile)
print "Loaded the defect mapping of files ... "
print "-"*100
'''
programmer to file mapping done, but not used, as no diference in defective and nn defective scripts
'''
if (MOZFLAG in org_name):
    prog_to_file_dict = process_metric_utility.getMercurialProgToFileMapping(org_name)
else:
    prog_to_file_dict = process_metric_utility.getGitProgToFileMapping(org_name)
print 'Done loading all file to programmer mapping ....'
# print prog_to_file_dict
print '-'*100
str_ = getAllProcessMetricForAllFiles(fullPuppMap, datasetFile2Save, prog_to_file_dict, ORG)
print "-"*100
print "We analyzed {} Puppet files".format(len(fullPuppMap))
print "-"*100
print "Ended at:", process_metric_utility.giveTimeStamp()
print "-"*100
