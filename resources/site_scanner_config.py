
try:
    import requests
except:
    print("    You don't have the 'requests' Python library installed.")
    print("    Try \"pip install requests\" (or pip3).")
    print("    Exiting program.")
    sys.exit()
    
try:
    import json
except:
    print("    You don't have access to the 'json' Python library.")
    print("    Try upgrading Python to the latest version.")
    print("    Exiting program.")
    sys.exit()
    
import os
import sys
import datetime
import platform
import time



class data_template:
    def __init__(self):
        self.site = ""
        self.html = ""
        self.hash = ""



def site_scanner_menu(c, config):
    if c in "1sS":
        return site_scanner_scan(config)
    if c in "2cC":
        return site_scanner_change(config)
    if c in "3wW":
        return site_scanner_write(config)
    if c in "4hH":
        return site_scanner_help(config)
    return False



def site_scanner_scan(config):
        
    print("\n    You've chosen to scan "+config["numsites"]+" sites for new html text,")
    print("    and then create full-page artifacts for each site that has changed.")
    print("    *** Continuing on will wipe out current artifacts. ***")
    print("    Continue?\n    (Y)es/(N)o: ",end="")
    scanchoice = input()

    if scanchoice not in ["y","Y","yes","Yes","YES"]:
        print("\n    Ok, we'll stop here and return to the primary prompt.")
        print("    Press 'enter' to continue. . .")
        input()
        time.sleep(1)
        return True
                    
    else:
        print("\n    Wiping out current artifacts...\n")
        time.sleep(1)

        artifacts_directory_list = os.listdir(config["artifactdir"])
        for filename in artifacts_directory_list:
            if ".artifact" in filename:
                os.remove(config["artifactdir"]+filename)
                print("      removed",filename)

        print("\n    Generating scan data...")
        time.sleep(1)

        data_file = open(config["datafiledir"])
        data_file.readline()

        html_fromscan = {}
        for i in range(int(config["numsites"])):
            line_list = data_file.readline().split(',')
            name = line_list[0]
            site = line_list[1]
            req = requests.get(site)
            html_fromscan[name] = data_template()
            html_fromscan[name].site = site
            html_fromscan[name].html = req.text

        data_file.close()

        site_text_file = open(config["sitefiledir"])
        html_onfile = json.load(site_text_file)
        site_text_file.close()

        any_changes = False
                        
        if set(html_fromscan.keys()) ^ set(html_onfile.keys()) != set():
            print("    *******************************************************")
            print("    ***                CRITICAL FAILURE                 ***")
            print("    *** A DIFFERENCE WAS FOUND BETWEEN THE NAMES IN THE ***")
            print("    ***  DATA FILE AND THE NAMES IN THE SITE TEXT FILE. ***")
            print("    ***             PROGRAM CANNOT CONTINUE             ***")
            print("    *******************************************************")
            print("    Exiting program.\n")
            sys.exit()

        print("\n    Creating the artifacts and displaying list of changes...\n")
        time.sleep(1)

        count = 0
        for name in html_fromscan:
            count += 1
            if html_fromscan[name].html != html_onfile[name]:
                if not any_changes:
                    any_changes = True
                print("      SITE "+str(count)+" HAS CHANGED : "+name+", "+html_fromscan[name].site+" ")
                artifact_path = config["artifactdir"]+str(datetime.date.today())+"-"+name+".artifact"
                artifact_file = open(artifact_path,"w")
                artifact_file.write(html_fromscan[name].html)
                artifact_file.close()

        print("\n    You've finished scanning each site for changes in its primary page's html document.")

        if any_changes:
            print("    There were new artifacts created that have text that need to be written to 'sitetext.json'.")
            print("    At this time, you need to change the metadata in "+config["datafilename"]+" either with option 2 or by manual alteration.")
            print("    This should be done prior to or *immediately after* writing new data to "+config["sitefilename"]+" with option 3.")
            
        else:
            print("    There were no changes in the sites scanned at this time.")
            
        print("    Press 'enter' to continue. . .")
        input()
        time.sleep(1)
        return True



def site_scanner_change(config):
    print("\n    Change Metadata Function")
    time.sleep(1)
    return True



def site_scanner_write(config):
    print("\n    You've chosen to retrieve the current artifacts and write new html text to 'sitetext.json'.")
    print("    Are you sure you want to do this right now?")
    print("    (Y)es/(N)o: ",end="")
    writechoice = input()

    if writechoice not in ["y","Y","yes","Yes","YES"]:
        print("\n    Ok, we'll stop here and return to the primary prompt.")
        
    else :    
        print("\n    Loading artifacts and writing to 'sitetext.json'...\n")
        artifacts_list = []
        for thing in os.listdir(config["artifactdir"]):
            if ".artifact" in thing:
                artifacts_list += [thing]

        if len(artifacts_list) > 0:
            site_text_file = open(config["sitefiledir"])
            html_onfile = json.load(site_text_file)
            site_text_file.close()

            for artifact_filename in artifacts_list:
                name = artifact_filename[:len(artifact_filename)-9][11:]
                artifact_file = open(config["artifactdir"]+artifact_filename)
                artifact_text = artifact_file.read()
                artifact_file.close()
                html_onfile[name] = artifact_text

            site_text_file = open(config["sitefiledir"],"w")
            json.dump(html_onfile,site_text_file)
            site_text_file.close()
            print("    The new html text has been written to 'sitetext.json'.")
    
        else:
            print("    No artifacts present! No new data was written!")

    print("    Press 'enter' to continue. . .")
    input()
    time.sleep(1)
    return True
    
    

def site_scanner_help(config):
    print("\n    *************************")
    print("    *** Site Scanner Help ***")
    print("    *************************")
    print("\n    This program allows you to keep track of a list of websites and to scan")
    print("    for changes so that you can manually maintain metadata for each site.")
    print("\n    This program accesses (and modifies, if necessary) 2 files under the")
    print("    resources directory: "+config["datafilename"]+" and "+config["sitefilename"]+".")
    print("\n    The \"scan\" function scans the sites named in "+config["datafilename"]+" for the")
    print("    html produced at each and compares it to what's on file in")
    print("    "+config["sitefilename"]+". All sites for which changes are detected are listed")
    print("    one-by-one so that you can update the metadata in "+config["datafilename"]+",")
    print("    and then artifacts are made for each site. (e.g. \"MySite.artifact\") You")
    print("    then have the opportunity to go to the \"write\" function.")
    print("\n    The \"write\" function accesses the artifacts and writes the data from")
    print("    each to its corresponding entry in "+config["sitefilename"]+" such that when a new")
    print("    scan is done later, the newer data is used for comparison. It's very")
    print("    important that after a scan is performed, the metadata you're looking")
    print("    for and verifying manually is updated in your "+config["datafilename"]+" BEFORE")
    print("    you use the \"write\" function. You can always do another scan later if")
    print("    you don't have time to manually update the *metadata* right away, since")
    print("    the \"scan\" function wipes out old artifacts automatically.\n")
    print("    Press 'enter' to continue. . .",end="")
    input()
    time.sleep(1)
    return True



