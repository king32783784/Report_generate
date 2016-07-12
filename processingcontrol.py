# coding: utf-8
import sys
from datasorting import ResultSorting
from mkxls import *
reload(sys)
sys.setdefaultencoding('utf8')
sheet_speccpu_data = [
    [
        ["spec2000， bigger is better", "spec2000"],
        ["ITEM", "SPECint2000", "SPECfp2000", "SPECint_rate2000",\
        "SPECfp_rate2000"],
        ],
]

sheet_syscpu_data = [
    [
        ["execution time, less is better", "sysbench"],
        ["ITEM", "10000", "20000", "30000"],
    ],
]

sheet_sysmem_data = [
    [
        ["Operations performed ops/sec", "sysbench"],
        ["ITEM", "4threads", "8threads"],
    ],
    [
        ["Transferred  MB/sec", "sysbench"],
        ["ITEM", "4threads", "8threads"],
    ],
]

sheet_lmbench_data =[
    [
        ["Processor, Processes - times in microseconds - smaller is better", \
        "Processor"],
        ["ITEM", "null call", "null I/O", "stat", "open clos", "slct TCP",\
         "sig inst", "sig hndl", "fork proc(k)", "exec porc(k)", "sh proc(k)"],
    ],
    [
        ["Context switching - times in microseconds - smaller is better",\
        "Context switching"],
        ["ITEM", "2p/0k", "2p/16k", "2p/64k", "8p/16k", "8p/64k", "16p/16k",\
        "16p/64k"],
    ],
    [
        ["*Local* Communication latencies in microseconds - smaller is better", "*Local* Communication latencie"],
        ["ITEM", "2p/0K ctxsw", "Pipe", "AF UNIX", "UDP", "TCP", "TCP conn"],
    ],
]

patternmath = {'Perf_cpu': ["execution time \(avg\/stddev\):(.*?)\/0.00"], 'Perf_mem': ["Operations performed: 2097152 \((.*?)ops\/sec\)", "8192.00 MB transferred \((.*?)MB\/sec\)"]}
totaldata = { 'speccpu': sheet_speccpu_data, 'Perf_cpu': sheet_syscpu_data, "lmbench": sheet_lmbench_data, "Perf_mem": sheet_sysmem_data}

class Control_processing(object):
    def __init__(self, myargs):
        '''{'items': ['cpu'], 'type': ['xls'], 'osnames': ['iSoft_Desktop_4.0']}'''
        self.args = myargs

    def _getdata(self, oslist, itemlist):
        for testitem in itemlist:
            for os in oslist:
                for i, pattern in enumerate (patternmath[testitem]):
                    data=ResultSorting()
                    testdata = data.datasearch(pattern, "finalresult/%s/%s/result/result.out" %(os, testitem), 3)
                    totaldata[testitem][i].append(testdata)
        return totaldata

    def _mkxls(self):
        '''infolist=[sheet_speccpu_info, sheet_lmbench_info, sheet_syscpu_info]
           datalist=[sheet_speccpu_data, sheet_lmbench_data, sheet_syscpu_data]
        ''' 
        itemlist = self.args['items']
        oslist = self.args['osnames']
        totaldata = self._getdata(oslist, itemlist)
        mkxls(totaldata, itemlist, oslist)

#testcase
#a=Control_processing()
#a._mkxls()


