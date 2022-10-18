#!/bin/env python3
import os
import glob
import time
import argparse


def parseArgs():
    parser = argparse.ArgumentParser(prog='FVEgetTemp.py', description='Get temperature from sensor with --ID ID.')
    parser.add_argument('--ID', nargs=1, required=False, action='store', help='ID in /sys/bus/w1/devices/. There is 28- prefix, value means behind the 28-prefix')
    return parser.parse_args()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
  lines = read_temp_raw()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw()
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = round(float(temp_string) / 1000.0,1)
    return temp_c


args = parseArgs()
ID=None
if args.ID is not None:
    ID=str(args.ID[0])
                        
base_dir = '/sys/bus/w1/devices/'
if ID is not None:
    device_folder = glob.glob(base_dir + '28-' + ID)[0]
else:
    device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

print(read_temp())
