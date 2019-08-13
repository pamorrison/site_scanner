
try:
    import requests
except:
    print("You don't have the 'requests' Python library installed.")
    print("Try \"pip install requests\".")
    print("Exiting program.")
    exit()
    
try:
    import json
except:
    print("You don't have access to the 'json' Python library.")
    print("Try upgrading Python to the latest version.")
    print("Exiting program.")
    exit()
    
import os
import sys
import datetime
import platform
import time

class data_template:
    def __init__(self):
        self.site = ""
        self.html = ""
        
if __name__=="__main__":
        
    config = num_sites_to_scan = data_location = site_text_location = artifacts_location = None
    yes_choices = ["y","Y","yes","Yes","YES"]
    scan_choices = ["scan","Scan","SCAN"]
    write_choices = ["write","Write","WRITE"]
    win_choices = ["win32","Windows"]
    
    if platform.system() in win_choices:
        os.system("cls")
    else:
        os.system("clear")
    
    print("\n  Choose 'scan' or 'write': ",end="")
    choice = input()
    
    while choice not in scan_choices and choice not in write_choices:
        print("\n  Invalid choice.")
        print("  Choose 'scan' or 'write': ",end="")
        choice = input()
    
    if choice in scan_choices:
        
        config_file = open('resources/config.json','r')
        config = json.load(config_file)
        config_file.close()
        
        num_sites_to_scan = int(config['first # sites'])
        data_location = str(config['data dir'])
        site_text_location = str(config['site text dir'])
        artifacts_location = str(config['artifacts dir'])
        
        print("\n  You've chosen to scan",num_sites_to_scan,"sites for new html text,")
        print("  and then create full-page artifacts for each site that has changed.")
        print("  *** Continuing on will wipe out current artifacts. ***")
        print("  Continue? (y/n): ",end="")
        choice2 = input()
        
        if choice2 not in yes_choices:
            print("  Exiting program.\n")
            exit()
        
        print("\n  Wiping out current artifacts...")
        time.sleep(1)

        artifacts_directory_list = os.listdir(artifacts_location)
        for filename in artifacts_directory_list:
            if ".artifact" in filename:
                os.remove(artifacts_location+filename)
                print("  removed",filename)
        
        print("\n  Generating scan data...")
        time.sleep(1)
        
        data_file = open(data_location)
        data_file.readline()

        html_fromscan = {}
        for i in range(num_sites_to_scan):
            line_list = data_file.readline().split(',')
            name = line_list[0]
            site = line_list[1]
            req = requests.get(site)
            html_fromscan[name] = data_template()
            html_fromscan[name].site = site
            html_fromscan[name].html = req.text

        data_file.close()
        
        site_text_file = open(site_text_location)
        html_onfile = json.load(site_text_file)
        site_text_file.close()
        
        any_changes = False
        
        if "".join(html_fromscan.keys()) != "".join(html_onfile.keys()):
            print("  *** CRITICAL FAILURE")
            print("  *** A DIFFERENCE WAS FOUND BETWEEN THE HACKATHON NAMES IN THE DATA FILE")
            print("  *** AND THE HACKATHON NAMES IN THE SITE TEXT FILE")
            print("  *** PROGRAM CANNOT CONTINUE")
            print("  Exiting program.\n")
            exit()
        
        print("\n  Creating list of changes...")
        time.sleep(1)
        
        count = 0
        for name in html_fromscan:
            count += 1
            if html_fromscan[name].html != html_onfile[name]:
                if not any_changes:
                    any_changes = True
                print("    Site "+str(count)+": CHANGED - "+name+", "+html_fromscan[name].site+" \n")
                artifact_path = artifacts_location+str(datetime.date.today())+"-"+name+".artifact"
                artifact_file = open(artifact_path,"w")
                artifact_file.write(html_fromscan[name].html)
                artifact_file.close()
        
        print("\n  You've finished scanning each site for changes in its primary page's html document,")
        
        if any_changes:
            print("  and there were new artifacts created that have text that need to be written to 'sitetext.json'.")
            print("  At this time, you need to change the 'source of truth' a.k.a the 'hackathons.csv' document.")
            print("  This should be done prior to or *immediately after* writing new data to 'sitetext.json'.")
            print("  Would you like to write the new data to 'sitetext.json' right now?")
            print("  Yes/No: ",end="")
            choice3 = input()
            if choice3 in yes_choices:
                choice = "write"
        else:
            print("  but there were no changes in the sites scanned.")
            print("  Exiting program.\n")
            exit()
    
    if choice != "write":
        print("\n  You've chosen not to write the new data to 'sitetext.json' at this time.")
        print("  Remember to run this program again and choose the 'write' option write this data ASAP,")
        print("  once the manual checks on each changed website have been performed.")
        print("  Exiting program.\n")
        exit()
    
    else:
                
        if config == None:
            config_file = open('resources/config.json','r')
            config = json.load(config_file)
            config_file.close()
        
            site_text_location = str(config['site text dir'])
            artifacts_location = str(config['artifacts dir'])
    
        print("\n  You've chosen to retrieve the current artifacts and write new html text to 'sitetext.json'.")
        print("  Are you sure you want to do this right now?")
        print("  Yes/No: ",end="")
        choice4 = input()
        
        if choice4 not in yes_choices:
            print("\n  Ok, we'll stop here.")
            print("  Exiting program.\n")
            exit()
        print("\n  Loading artifacts and writing to 'sitetext.json'...")
        
        artifacts_list = os.listdir(artifacts_location)
        
        if len(artifacts_list) > 0:
            site_text_file = open(site_text_location)
            html_onfile = json.load(site_text_file)
            site_text_file.close()
        
            for artifact_filename in artifacts_list:
                name = artifact_filename[:len(artifact_filename)-9][11:]
                artifact_file = open(artifacts_location+artifact_filename)
                artifact_text = artifact_file.read()
                artifact_file.close()
                html_onfile[name] = artifact_text
        
            site_text_file = open(site_text_location,"w")
            json.dump(html_onfile,site_text_file)
            site_text_file.close()
            print("  The new html text has been written to 'sitetext.json'.")
            
        else:
            print("  No artifacts present!")
        
        print("  Exiting progarm.\n")

 
















