#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os, sys, time, re, commands
import multiprocessing
from optparse import OptionParser

TIMEOUT = 3

def parse_arguments():
    parser = OptionParser("python burn.py -f device_list.txt -i file.img")
    parser.add_option("-f", "--file", dest="devices_list",
                      help="file with devices list, separated by new line symbol, example: sda sdb sdc.", metavar="FILE")

    parser.add_option("-i", "--img", dest="img_file",
                      help="*.img file to burn to the flash device.", metavar="FILE")

    (options, args) = parser.parse_args()

    if(not (options.devices_list and options.img_file)):
        parser.error("Incorrect number of arguments, use argument --help for more information.")

    return options

def burn(dev_name, iso_name):
    while(True):
        if not is_connect(dev_name):
            time.sleep(TIMEOUT)
            continue

        print bcolors.START + "Dev %s - start burn." % dev_name + bcolors.ENDC
        
        respond = commands.getoutput("find /dev/ -maxdepth 1 | grep %s | xargs sudo umount" % dev_name)
        respond = commands.getoutput("sudo dd if=%s of=/dev/%s bs=1M" % (iso_name, dev_name))

        rate = re.search('([0-9]+) c', respond).group(0)
        
        print bcolors.OKGREEN + "Dev %s - done %s." % (dev_name, rate) + bcolors.ENDC
        print bcolors.OKGREEN + "Please disconnect usb device - %s."  % dev_name + bcolors.ENDC

        # wait for disconnect
        while(is_connect(dev_name)):
            time.sleep(TIMEOUT)
            
        print bcolors.WARNING + "Please connect next usb device - %s."  % dev_name + bcolors.ENDC

def is_connect(dev_name):
    respond = commands.getoutput("ls /dev/%s" % dev_name)

    if respond == ("/dev/%s" % dev_name):
        return True
    return False

if __name__ == '__main__':
    args = parse_arguments()
    iso_name = args.img_file
    dev_list_file = args.devices_list

    dev_list = open(dev_list_file, 'r')
    dev_list = dev_list.readlines()
    dev_list_without_new_line = []
    for line in dev_list:
        dev_list_without_new_line.append(line.rstrip())
    dev_list = dev_list_without_new_line

    print "\n\n"
    print 'Divices for burn: ' + ' '.join(dev_list)

    pool = multiprocessing.Pool(len(dev_list))
    
    for dev in dev_list:
        pool.apply_async(burn, (dev, iso_name))

    pool.close()
    pool.join()
    
