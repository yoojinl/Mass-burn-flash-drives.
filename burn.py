#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os, sys, time, re, commands
import multiprocessing
import curses
from optparse import OptionParser

TIMEOUT = 3
UPDATE_SCREEN = 1

class State:
    FREE = 0
    START = 1
    DONE = 2

def parse_arguments():
    parser = OptionParser("sudo python burn.py -f device_list.txt -i file.img")
    parser.add_option("-f", "--file", dest="devices_file_name",
                      help="file with devices list, separated by new line symbol, example: sda sdb sdc.", metavar="FILE")

    parser.add_option("-i", "--img", dest="img_file_name",
                      help="*.img file to burn to the flash device.", metavar="FILE")

    (options, args) = parser.parse_args()

    if(not (options.devices_file_name and options.img_file_name)):
        parser.error("Incorrect number of arguments, use argument --help for more information.")

    return options.devices_file_name, options.img_file_name

def burn(dev_name, img_name, states):
    while(True):
        if not is_connect(dev_name):
            time.sleep(TIMEOUT)
            continue

        states[dev_name] = State.START
        
        respond = commands.getoutput("find /dev/ -maxdepth 1 | grep %s | xargs sudo umount" % dev_name)
        respond = commands.getoutput("sudo dd if=%s of=/dev/%s bs=1M" % (img_name, dev_name))

        states[dev_name] = State.DONE

        # wait for disconnect
        while(is_connect(dev_name)):
            time.sleep(TIMEOUT)

        states[dev_name] = State.FREE


def is_connect(dev_name):
    respond = commands.getoutput("ls /dev/%s" % dev_name)

    if respond == ("/dev/%s" % dev_name):
        return True
    return False

def get_dev_list(file_name):
    dev_list = open(file_name, 'r')
    dev_list = dev_list.readlines()
    dev_list_without_new_line = []
    for line in dev_list:
        dev_list_without_new_line.append(line.rstrip())
    return dev_list_without_new_line

def get_state_list(dev_list):
    manager = multiprocessing.Manager()
    states = manager.dict()

    for dev in dev_list:
        states[dev] = State.FREE
    return states

def make_frame(states):
    states_dict = dict(states)
    frame = "Burn runing.\n"
    frame += "F - insert flash drive.\n"
    frame += "R - now burnt.\n"
    frame += "D - burn finished, disconnect flash drive.\n\n"
    frame += "Press 'q' for exit.\n\n"
    frame += "dev   state\n"
    frame += "-----------\n"
    for dev, state in states_dict.items():
        state_format = ''
        if state == State.FREE: state_format = 'F'
        elif state == State.START: state_format = 'R'
        elif state == State.DONE: state_format = 'D'
        
        row_list = [str(dev), str(state_format)]
        row_format = ''

        for row in row_list:
            row_format += '{0:{width}}'.format(row, width=8)
        row_format += "\n"
        
        frame += row_format

    return frame

if __name__ == '__main__':
    dev_file_name, img_file_name = parse_arguments()

    dev_list = get_dev_list(dev_file_name)
    states = get_state_list(dev_list)

    pool = multiprocessing.Pool(len(dev_list))
    for dev in dev_list:
        pool.apply_async(burn, (dev, img_file_name, states))

    pool.close()

    import curses
    stdscr = curses.initscr()
    stdscr.nodelay(True)

    while(True):
        frame = make_frame(states)
        stdscr.addstr(0, 0, frame)
        stdscr.refresh()
        
        time.sleep(UPDATE_SCREEN)
        press_key = stdscr.getch()
        if press_key == ord('q'):
            pool.terminate()
            curses.endwin()
            sys.exit(os.EX_OK)
