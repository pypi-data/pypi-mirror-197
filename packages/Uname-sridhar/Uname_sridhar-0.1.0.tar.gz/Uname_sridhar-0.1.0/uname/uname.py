#! /usr/bin/python
import os
import sys
import optparse 
def main():
    parser = optparse.OptionParser(usage="%prog [option]",version="%prog 1.0")
    parser.add_option( "-a", "--all" ,action="store_true",dest="uname",
                    help="print the details about our machine")
    parser.add_option("-s","--kernel-name",action="store_true",dest="sys_name",
                    help="print the details about our OPerating system Kernal name and its details")
    parser.add_option("-r","--kernel-release",action="store_true",dest="release",
                    help="print the kernel release")
    parser.add_option("-n","--nodename",action="store_true",dest="nodename",
                    help="print the kernel release")
    parser.add_option("-p","--processor",action="store_true",dest="processor",
                    help="print the processor type (non-portable)")
    parser.add_option("-v","--kernel-version",action="store_true",dest="version",
                    help="print the kernel version")
    parser.add_option("-m","--machine",action="store_true",dest="machine",
                    help="print the machine hardware name")

    parser.add_option("-i","--hardware-platform",dest="identifies",action="store_true",
                    help="print the hardware platform (non-portable)")
    parser.add_option("-o","--operating-system",dest="operating-system",action="store_true",
                    help="print the operating system")

    (options, args) = parser.parse_args()
    try:
        if options.ensure_value('uname',False)==True:
            return os.system("uname -a")
        if options.ensure_value('operating-system',False)==True:
            return os.system("uname -o")
        if options.ensure_value('sys_name',False):
            return os.system("uname -s")
        if options.ensure_value('release',False)==True:
            return os.system("uname -r")
        if options.ensure_value('machine',False)==True:
            return os.system("uname -m")
        if options.ensure_value('node_name',False)==True:
            return os.system("uname -a")
        if options.ensure_value('identifies',False):
            return os.system("uname -i") 
        if options.ensure_value('version',False):
            return os.system("uname -v") 
        if options.ensure_value('processor',False):
            return os.system("uname -p")
        if options.ensure_value('nodename',False):
            return os.system("uname -n")  
    except:
        print("Error Occured")

if __name__ == "__main__":
    main()
