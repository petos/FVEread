#!/bin/env python3
import os
import glob
import time
import argparse


def parseArgs():
    parser = argparse.ArgumentParser(prog='pyGPIO', description='Set/unset GPIO pins on server.')
    parser.add_argument('--pin', nargs=1, required=True, action='store', help='PIN to work with')
    PIN=parser.parse_args().pin[0]
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
PIN=int(args.pin[0])
                        
base_dir = '/sys/bus/w1/devices/'
while True:
    try:
        device_folder = glob.glob(base_dir + '28*')[0]
        break
    except:
        os.system("FVEGPIO --mode set --value off --type power --pin " + str(PIN))
        time.sleep(65)
        os.system("FVEGPIO --mode set --value on --type power --pin " + str(PIN))
        time.sleep(15)
        pass
device_file = device_folder + '/w1_slave'

print(read_temp())
