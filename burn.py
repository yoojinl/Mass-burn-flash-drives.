#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os, sys, time, re, commands
import multiprocessing

TIMEOUT = 3

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

class bcolors:
    START = '\033[95m'
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

if __name__ == '__main__':
    iso_name = sys.argv[1]
    dev_list_file = sys.argv[2]

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
    
