'''
Akond Rahman
Sep 24, 2017
Get time series data for process metrics
'''
import process_metric_utility, hg_process_extractor, git_process_extractor
import shutil, os
import subprocess

def getYearWiseRepos():
   dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'
   repo_dir     = '/Users/akond/PUPP_REPOS/wikimedia-downloads/'
   the0000Time  = '2005'

   dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.Final.Categ.csv'
   repo_dir     = '/Users/akond/PUPP_REPOS/openstack-downloads/'
   the0000Time  = '2005'

   dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
   repo_dir     = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/'
   the0000Time  = '2005'

   '''
   line 27-57 is for getting year wise data
   it is semi automated .... sometimes need to do git stash / hg revrt by manually going into directories
   '''
   repo_file    =  repo_dir + 'eligible_repos.csv'
   all_repos = process_metric_utility.getAllRepos(repo_file)
   all_time_vals, file_per_time_dict, file_defect_dict, repo_dict = process_metric_utility.getAllYearsFromDataset(dataset_file)
   for repo_ in all_repos:
       for time_ in all_time_vals:
           try:
              dir2copy = repo_dir + repo_
              dest_dir = dir2copy + '-' + time_ + '/'
              if((os.path.exists(dest_dir))==False):
                  shutil.copytree(dir2copy, dest_dir)
              '''
              also do git reset
              '''
              if time_=='0000':
                     time_ = the0000Time
              #git checkout `git rev-list -1 --before="$DATE" master`
              cdCommand            = "cd " + dest_dir + " ; "
              if 'mozilla' in dest_dir:
                  date2reset='Dec ' + time_
                  commitCommand        = "hg update -d '"+ date2reset +"'"
              else:
                  date2reset='Dec 15 ' + time_
                  commitCommand        = "git checkout `git rev-list -1 --before='"+ date2reset +"' master`"
              command2Run          = cdCommand + commitCommand
              #print command2Run
              subprocess.check_output(['bash','-c', command2Run])
              print '='*50

           except shutil.Error as e_:
              print 'Directory not copied. Error:', e_


if __name__=='__main__':
   '''
   to get year wise repos un comment the following line , for metric extraction it is commented 
   '''
   #getYearWiseRepos()


   '''
   get metrics for each dataset:
   '''

   # categ_file_  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
   # org_name     = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/'
   # org_for_name = 'MOZILLA'
   # bad_boys_    = [' ']

   # categ_file_  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.Final.Categ.csv'
   # org_name     = '/Users/akond/PUPP_REPOS/openstack-downloads/'
   # org_for_name = 'OPENSTACK'
   # bad_boys_    = ['/Users/akond/PUPP_REPOS/openstack-downloads/puppet-neutron/examples/neutron.pp',
   #                 '/Users/akond/PUPP_REPOS/openstack-downloads/puppet-nova/manifests/quota.pp',
   #                 '/Users/akond/PUPP_REPOS/openstack-downloads/puppet-swift/manifests/storage/filter/recon.pp',
   #                 '/Users/akond/PUPP_REPOS/openstack-downloads/puppet-nova/manifests/params.pp',
   #                 '/Users/akond/PUPP_REPOS/openstack-downloads/fuel-library/deployment/puppet/osnailyfacter/manifests/install_ssh_keys.pp'
   #                 ]

   # categ_file_  = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'
   # org_name     = '/Users/akond/PUPP_REPOS/wikimedia-downloads/'
   # org_for_name = 'WIKIMEDIA'
   # bad_boys_    = [' ']


   if ('mozilla' in org_name):
       prog_to_file_dict_ = process_metric_utility.getMercurialProgToFileMapping(org_name)
   else:
       prog_to_file_dict_ = process_metric_utility.getGitProgToFileMapping(org_name)
   repo_file_dict = process_metric_utility.getRepoToFileMapping(categ_file_)

   years_list = process_metric_utility.getAllYearsFromCategFile(categ_file_)
   for year_info in years_list:
       if year_info !='0000':
          str2write_year = ''
          # get defect data based on year, file name: a dictionary of files with defect staus
          defect_of_files = process_metric_utility.getDefectData(year_info, categ_file_)
          #print defect_of_files
          for repo_, file_list in repo_file_dict.iteritems():
             if repo_.endswith('/'):
               repo_ = repo_[:-1]
             time_str = '-' + year_info + '/'
             time_repo_ = repo_ + time_str
             all_pp_files=process_metric_utility.getRecursivelyPPFilles(time_repo_)
             for time_pp_file in all_pp_files:
               pp_file = time_pp_file.replace(time_str, '/')
               #print time_pp_file, pp_file
               # check if the file is already in the origina dataset, and has defect information
               if ((pp_file in file_list) and (pp_file in defect_of_files)):
                 if(pp_file not in bad_boys_):
                    #print time_pp_file, time_repo_
                    if 'mozilla' in pp_file:
                      time_process_metrics = hg_process_extractor.getProcessMetrics(time_pp_file, time_repo_, prog_to_file_dict_)
                    else:
                      time_process_metrics = git_process_extractor.getProcessMetrics(time_pp_file, time_repo_, prog_to_file_dict_)
                    defect_of_file=defect_of_files[pp_file]
                    print 'File:{},Year:{},Defect?:{}'.format(time_pp_file, year_info, defect_of_file)
                    print 'Metrics:', time_process_metrics
                    ### writing time
                    str2write_year = str2write_year + time_repo_ + ',' + pp_file + ',' + time_process_metrics + defect_of_file + '\n'
                    print '-'*50
                 else:
                    print 'FOUND A BAD BOY !!!--->',time_pp_file


          folder2write = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/' + org_for_name + '/' + year_info + '/'
          if (os.path.exists(folder2write)==False):
                os.makedirs(folder2write)
          file2write  = folder2write + 'TIME_PROCESSMETRIC_DATASET.csv'
          header_str = 'TIME_REPO,ORIG_FILE,COMM,AGE,DEV,ADDPERLOC,DELPERLOC,SUMCHNG,TOTCHNGPERLOC,AVGCHNG,MINOR,SCTR,MT_PP,MT_NON_PP,defect_status'
          str2write_year = header_str + '\n' + str2write_year
          dump_status = process_metric_utility.dumpContentIntoFile(str2write_year, file2write)
          print 'Dumped time-wise-process-dataset of size(bytes):', dump_status
          print '='*100
