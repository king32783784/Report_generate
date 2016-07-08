#/usr/bin/env python
# coding: utf-8
'''
    Name: Test report automatically generate tool
    Function: Automatically generate performance test results xls format report
              with Python and XlsxWriter
    Author: peng.li@i-soft.com.cn
    Date :20160701
'''
import os
import sys
from optparse import OptionParser

if __name__== "__main__":
    parser = OptionParser()
    parser.add_option("-o", "--osname", dest="processosname",
                      help="Enter the name of the comparison system like \
                            isoft deepin")
    parser.add_option("-t", "--type", dest="filetype",
                      help="Enter the type of the result file, such as xls html")
    parser.add_option("-i", "--items", dest="processitems",
                      help="Enter the items of comparison, like cpu io")
    (options, args) = parser.parse_args()
    reciveargs = {}
    reciveargs['osnames'] = options.processosname.split()
    reciveargs['type'] = options.filetype.split()
    reciveargs['items'] = options.processitems.split()
    print reciveargs