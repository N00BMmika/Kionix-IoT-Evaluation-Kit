# The MIT License (MIT)
#
# Copyright 2016 Kionix Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.
import struct
import pylab
import sys
import os
import csv
import argparse
#from lib.util_lib import DELIMITER

""" Tool for plotting kzzz_data_logger.py generated log files"""

def doit(csvfile):
    sensordata=[]
    timestamplist=[]
    if 1:#with open(fname, 'rb') as csvfile:
        
        for t in range(args.skip_lines): csvfile.readline()

        reader = csv.reader(csvfile, delimiter=args.delimiter)
        for a in reader:

            if a==[]: continue # empty line            
            try:
                values = [float(t.replace(',','.')) for t in a if t !='']
            except Exception,e:
                print a, e
                continue

            if args.columns:
                values = [values[t] for t in args.columns]

            if args.timestamps:
                sensordata.append(values[1:])
                timestamplist.append(values[0])
                
            else: 
                sensordata.append(values)
                

        if args.output_file_name:
            outfile = open(args.output_file_name,'w')
            for line in sensordata:
                outfile.write(args.output_delimiter.join([args.output_formatter % round(t*args.output_multiplier) for t in line])+'\n')
        else:

            if timestamplist!=[]: # data with timestamp
                pylab.plot(timestamplist, sensordata, args.tick_mark)
                pylab.xlabel('time')
            else:
                pylab.plot(sensordata, args.tick_mark)
                pylab.xlabel('sample #')
       
            pylab.title(csvfile.name)

            if args.legend:
                pylab.legend(args.legend)

            pylab.grid()
            pylab.show()

if __name__ == '__main__':
    global args
    # todo : improve col separator handling
    parser = argparse.ArgumentParser(
                                     description='Example: %(prog)s log.txt -l gx gy gz -c 9 10 11'
                                     )
    parser.add_argument('-s','--skip_lines',default=0,type=int, help='How many lines skip from beginning of the file.')
    parser.add_argument('-n',action='store_true', help='channel names on 1st row.')
    parser.add_argument('-c','--columns',nargs='*',type=int, help='Which columns to plot (index starts from 0).')
    parser.add_argument('-l','--legend',nargs='*',type=str, help='Names for plot columns.')
    parser.add_argument('-d','--delimiter',type=str, default='\t', help='Column delimiter (default "tab").')
##    parser.add_argument('-o','--output_delimiter',type=str, default=',', help='Column delimiter for output (default ",").')
##    parser.add_argument('-M','--output_formatter',type=str, default='%d', help='Output file data formatter for example %d or %f (default %d).')
    parser.add_argument('-m','--output_multiplier',type=float, default='1.0', help='Output file data multiplier (default 1.0).')
    parser.add_argument('-f','--output_file_name',type=str, default='', help='File to save data (if want to save).')
    parser.add_argument('-x','--tick_mark',type=str, default='', help='Tick mark for data sample for example "x", "o", "x-" etc. default is empty')
    parser.add_argument('-t','--timestamps',action='store_true', help='1st column is timestamps')
    parser.add_argument('fname', type=argparse.FileType('rb'), help='log file name')

    args = parser.parse_args()

    doit(args.fname)
