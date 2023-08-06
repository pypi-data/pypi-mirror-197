#! /usr/bin/python
import os
import sys
import optparse 
def main():
    try:
        if((sys.argv[1]=="-a")or (sys.argv[1]=="--all")):
            return os.system("uname -a")
        if((sys.argv[1]=="-s")or (sys.argv[1]=="--kernel-name")):
            return os.system("uname -s")
        if((sys.argv[1]=="-r")or (sys.argv[1]=="--kernel-release")):
            return os.system("uname -r")
        if((sys.argv[1]=="-n")or (sys.argv[1]=="--nodename")):
            return os.system("uname -n")
        if((sys.argv[1]=="-p")or (sys.argv[1]=="--processor")):
            return os.system("uname -p")
        if((sys.argv[1]=="-v")or (sys.argv[1]=="--kernel-version")):
            return os.system("uname -v")
        if((sys.argv[1]=="-m")or (sys.argv[1]=="--machine")):
            return os.system("uname -m")
        if((sys.argv[1]=="-i")or (sys.argv[1]=="--hardware-platform")):
            return os.system("uname -i")
        if((sys.argv[1]=="-o")or (sys.argv[1]=="--operating-system")):
            return os.system("uname -o")
        if((sys.argv[1]=="-h")or (sys.argv[1]=="--help")):
            print(f"{sys.argv[0]} <option>")
            print(f"{sys.argv[0]} shows the details about our Machine")
    except NameError as name_error:
        print(name_error)

if __name__ == "__main__":
    main()
