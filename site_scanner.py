
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

sys.path.append(os.getcwd()+"/resources")
from site_scanner_config import *



hardcoded_config_keys = { "numsites",
                          "datafiledir",
                          "datafilename",
                          "sitefiledir",
                          "sitefilename",
                          "artifactdir",
                          "options",         
                          "win" }       
                  


if __name__=="__main__":
    
    if not os.path.exists("resources/config.json"):
        print("    This program's config file is missing.")
        print("    Try to find it and put it in the resources folder.")
        print("    If you can't...WELP")
        print("    Exiting program.\n")
        time.sleep(1)
        sys.exit()
    
    config_file = open('resources/config.json','r')
    cfg = json.load(config_file)
    config_file.close()
    
    you_screwed_this_up_royally = hardcoded_config_keys ^ set(cfg.keys()) != set()
    
    if you_screwed_this_up_royally:
        print("    This program's config file doesn't have the right set of key/value pairs.")
        print("    How did this happen? How?? HOW??? TELLLLLLL MEEEEEE!!!!")
        print("    (if you changed any key strings in config.json, change them back)")
        print("    Exiting program.\n")
        time.sleep(1)
        sys.exit()
            
    if cfg["datafilename"] not in cfg["datafiledir"]:
        print("    The name of the file that stores the metadata for each site")
        print("    is not in its own file path value in the config file.")
        print("    Rectify this and run the program again.")
        
    choice = "_"
    program_continue = True
    
    while program_continue:
        
        count = 0
        while choice not in cfg["options"] or len(choice) > 1:
            
            count += 1
            if count > 5: break
            
            if platform.system() in cfg["win"]:
                os.system("cls")
            else:
                os.system("clear")
            
            if choice != "_":
                print("\nINVALID CHOICE, PICK AGAIN")
            
            print("\n    Welcome to the Site Scanner.")
            print("    Type the number or indicated letter of your choice and hit enter.\n")
            print("    1. (s)can stored sites for changes")
            print("    2. (c)hange metadata in "+cfg["datafilename"])
            print("    3. (w)rite site data to "+cfg["sitefilename"])
            print("    4. (h)elp with using this program")
            print("    5. (e)xit this program\n")
            print("    choice: ",end="")
            choice = input()
            
        if count > 5:
            print("\n    We're not gonna do this all day.")
            print("    Pick a valid option next time.")
            print("    Exiting program.\n")
            time.sleep(1)
            sys.exit()
        
        program_continue = site_scanner_menu(choice,cfg)
        choice = "_"

    time.sleep(1)
    
