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
"calculate average ODR of log file and find smalles and biggest timedelta"


def validate(fname, skiplines, colsep, deltatime_in_log, multiplier):
    starttime = -1
    endtime = 0
    samples = 0
    deltamax = 0
    deltamaxind = 0
    deltaminind = 0
    prevtime = 0
    
    deltamin = 9999999
    delta = 0
    deltasum=0
    with open(fname,'r') as infile:
        for line in infile:
            samples +=1
            if samples < skiplines:
                continue
            if line[0] in ['*','#']:
                continue
            
            linedata =  line.split(colsep)
            if deltatime_in_log:
                timestamp = (float(linedata[0]) * multiplier) + prevtime
            else:
                timestamp = float(linedata[0]) * multiplier
            
            if starttime == -1:
                starttime = timestamp
            else:
                delta = timestamp-prevtime
                deltamax = max(deltamax, delta)
                if deltamax == delta:
                    deltamaxind = samples

                deltamin = min(deltamin, delta)
                deltasum += delta

                if deltamin == delta:
                    deltaminind = samples
                
            prevtime = timestamp

    print 'start time %0.5f (s)' % starttime
    print 'stop time  %0.5f (s)' % prevtime
    print 'duration   %0.5f (s)' % (prevtime - starttime)
    print 'samples    %d' % samples
    
    print 'max delta  %.5f (ms) / %d (Hz) at sample %d' % (deltamax * 1000, 1. / deltamax, deltamaxind)
    if deltamin:
        print 'min delta  %.5f (ms) / %d (Hz) at sample %d' % (deltamin * 1000, 1. / deltamin, deltaminind)
    else:        
        print 'min delta  %.5f (ms) at sample %d' % (deltamin * 1000, deltaminind)

    print 'avg delta  %.5f (ms)' % ((deltasum / samples) * 1000)

    print 'ODR avg    %.2f (Hz)' % (samples / float(prevtime-starttime))
    


import argparse as __argparse
_argparser = __argparse.ArgumentParser(description='Example: %(prog)s -s')
_argparser.add_argument('-c','--colsep',default='\t',type=str)
_argparser.add_argument('-s','--skiprows',default = 0, type=int )
_argparser.add_argument('-d','--deltatime_in_log',action='store_true')
_argparser.add_argument('-t','--timestamp_multiplier',type=float, default=1.0)
_argparser.add_argument('fname', type=str, help='log file name')

args = _argparser.parse_args()
validate(args.fname, args.skiprows, args.colsep, args.deltatime_in_log, args.timestamp_multiplier)
