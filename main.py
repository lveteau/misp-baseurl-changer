import os
import sys
import fileinput
import re

def main():

    global auto_install
    auto_install = False

    if len(sys.argv) < 2:
        print("Usage:\n  -- 'python main.py ip' for using your network IP.\n  -- 'python main.py local' change the ip to 'localhost'.\n  -- 'python main.py 192.192.192.192' for using a specific adress.\nAdd '--auto' as a second argument to execute it directly in default location without asking")
        exit()

    if len(sys.argv) > 2:
        if "--auto" in sys.argv[2]:
            auto_install = True

    if "ip" in sys.argv[1]:
        changeURL("http://{}".format(get_ip()))
    elif "local" in sys.argv[1]:
        changeURL("http://localhost")
    else:
        changeURL("http://{}".format(sys.argv[1]))


def get_ip():
    ip_list = os.popen("hostname -I").read().replace("\n", "").split(" ")
    for ip in ip_list:
        if not "127" in ip:
           return ip 

def changeURL(url):
    if auto_install or "y" in raw_input("Do you want to perform this script on the default MISP location ? (/var/www/MISP) [y/N]"):
        default_path = "/var/www/MISP/app/Config/config.php"
        if os.path.exists(default_path):
            perform_sed(default_path, url)
    else:
        user_path = raw_input("Please provide the full absolute path of [MISP FOLDER]/app/Config/config.php (Ctrl C to exit)")
        if os.path.exists(user_path):
            perform_sed(user_path, url)
        else:
            print("File not found, aborting...")
    print("Done")

def perform_sed(path, url):
    for line in fileinput.input(path, inplace = 1): 
        line = line.rstrip()
        if line != "":
            if "baseurl" in line:
                print "    'baseurl' => '{}',".format(url)
            else:
                print line

    os.chmod(path, 0777)
if __name__ == "__main__":
    main()
