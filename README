# Mass burn flash drives.

You need burn ~200 flash drives?
This is script can help you.

# How?

## 1. Disable automount flash drives in your system.

In gnome you can do so:

    $ gconf-editor

    And uncheck the next parameters:
    /apps/nautilus/preferences/media_automount
    /apps/nautilus/preferences/media_automount_open

## 2. Make a device list.

Example:

    $ cat dev.txt
    sdb
    sdc
    sdd
    sde
    sdf
    sdg
    sdh
    sdi
    sdj

## 3. Run script.

    sudo python burn.py -f dev.txt -i file.img

After launch, displays next text:

    Burn runing.
    F - insert flash drive.
    R - now burnt.
    D - burn finished, disconnect flash drive.
    
    Press 'q' for exit.
    
    dev   state
    -----------
    sdb     F
    sdc     F
    sdd     F
    sde     F
    sdf     F
    sdg     F
    sdh     F
    sdi     F
    sdj     F

## Help.
    $ python burn.py --help
    Usage: sudo python burn.py -f device_list.txt -i file.img
    
    Options:
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  file with devices list, separated by new line symbol,
                            example: sda sdb sdc.
      -i FILE, --img=FILE   *.img file to burn to the flash device.
