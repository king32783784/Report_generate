# coding: utf-8
import sys
from datasorting import ResultSorting
from mkxls import *
from mkhtml import *
reload(sys)
sys.setdefaultencoding('utf8')
# spec2000_cpau
sheet_speccpu_data = [
    [
        ["spec2000， bigger is better", "spec2000"],
        ["ITEM", "SPECint2000", "SPECfp2000", "SPECint_rate2000",\
        "SPECfp_rate2000"],
        ],
]
# sysbench_cpu
# sysbench_cpu_xls
sheet_syscpu_data = [
    [
        ["execution time, less is better", "sysbench"],
        ["ITEM", "10000", "20000", "30000"],
    ],
]
# sysbench_cpu_html
html_syscpu_data = []
# perf_graphics_xls
sheet_graphics_data = [
    [
        ["2D test results", "2D"],
        ["ITEM", "Qtperf", "unixbench-x11perf"],
    ],
    [
        ["3D test results", "3D"],
        ["ITEM", "Glmark", "unixbench-glxgears"],
    ],
]
html_graphics_data = []
# sysbench_mem
# sysbench_mem_xls
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
# sysbench_mem_html
html_sysmem_data=[]
# iozone_io
# iozone_io_html
html_iozone_data = []
# iozone_io_xls
sheet_io_data = [
    [
        ["Variety of file operations KB/sec", "iozone"],
        ["ITEM", "Writer", "Re-writer", "Reader", "Re-reader", "Random Read", "Random Write"],
    ],
]
# pingpong_html
html_pingpong_data = []
# pingpong_xls
sheet_pingpong_data = [
    [
        ["Threads initialised usec", "pingpong"],
        ["ITEM", "32threads", "64threads", "128threads"],
    ],
    [
        ["Games completed usec", "pingpong"],
        ["ITEM", "16Games", "32Games", "64Games"],
    ],
]
# stream_html
html_stream_data = []
# stram_xls
sheet_stream_data = [
    [
        ["1Thread(MB/s)", "stream"],
        ["ITEM", "Copy", "Scale", "Add", "Triad"],
    ],
    [
        ["4Thread(MB/s)", "stream"],
        ["ITEM", "Copy", "Scale", "Add", "Triad"],
    ],
    [
        ["16Thread(MB/s)", "stream"],
        ["ITEM", "Copy", "Scale", "Add", "Triad"],
    ],
]
# system_html
html_system_data = []
# system_xls
sheet_system_data = [
    [
        ["unixbench system index", "unixbench"],
        ["ITEM", "1threads", "4thread"],
    ],
]
# browser_html
html_browser_data = []
# browser_xls
sheet_browser_data = [
    [
        ["Browser test", "browser"],
        ["ITEM", "css4", "acid3", "V8test", "octane", "html5", "dromaeotest"],
    ],
]  
# lmbench_html
html_lmbench_data = []
# lmbench_xls
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
    [
        ["File & VM system latencies in microseconds - smaller is better", "File & VM system latencies"],
        ["ITEM", "0K Create", "0K Delete", "10K Create", "10K Delete", "Mmap Latency(K)", "Port Fault",
         "Page Fault", "100fd selct"],
    ],
    [
        ["*Local* Communication bandwidths in MB/s - bigger is better", "*Local* Communication bandwidths"],
        ["ITEM", "Pipe", "AF UNIX", "TCP", "File reread", "Mmap reread", "Bcopy(libc)", "Bcopy(hand)", "Mem read", "Mem write"],
    ],
]

patternmath = {'Perf_cpu': [["execution time \(avg\/stddev\):(.*?)\/0.00", ],],
               'Perf_mem': [["Operations performed: 2097152 \((.*?)ops\/sec\)",],
                            ["8192.00 MB transferred \((.*?)MB\/sec\)",]],
               'Perf_io': [["Children see throughput for  1 initial writers \t=  (.*?)KB\\/sec",
                           "Children see throughput for  1 rewriters \t=  (.*?)KB\\/sec",
                           "Children see throughput for  1 readers \t\t= (.*?)KB\\/sec",
                           "Children see throughput for 1 re-readers \t= (.*?)KB\\/sec",
                           "Children see throughput for 1 random readers \t= (.*?)KB\\/sec",
                           "Children see throughput for 1 random writers \t=  (.*?)KB\\/sec"],],
               'Perf_thread': [["32 threads initialised in(.*?)usec", "64 threads initialised in(.*?)usec",
                                "128 threads initialised in(.*?)usec"],
                               ["16 games completed in(.*?)msec", "32 games completed in(.*?)msec",
                                "64 games completed in(.*?)msec",]],
               'Perf_kernel': [["Process_r(.*?)\n"], ["Context_r(.*?)\n"],
                               ["Local_r(.*?)\n"], ["File_VM_r(.*?)\n"],
                               ["Bandwidth(.*?)\n"]],
               'Perf_stream': [["\\(1\\)threads_result:(.*?)\n"], ["\\(4\\)threads_result:(.*?)\n"],
                               ["\\(4\\)threads_result:(.*?)\n"]],
               'Perf_graphics': [["Total: (.*?) s","2D Graphics Benchmarks Index Score(.*?)\n",],
                                  ["Your GLMark08 Score is (.*?)\\^\\_\\^", "3D Graphics Benchmarks Index Score(.*?)\n"],],
               'Perf_system': [["Threads_1: (.*?)\n", "Threads_4: (.*?)\n"],],
               'Perf_browser': [["css4 result is (.*?)\n", "acid3 result is (.*?)\\/100", "V8test result is 总成绩: (.*?)\n",
                                 "octane result is 您的浏览器得分: (.*?)\n", "html5test result is (.*?)\n",
                                 "dromaeotest result is (.*?)\n"],],
                            }
patternnum = {'Perf_cpu': 3, 'Perf_mem':3, 'Perf_io':3, 'Perf_thread':3, 'Perf_kernel':3, 'Perf_stream':3,
              'Perf_graphics': 3, 'Perf_system': 3, 'Perf_browser':3}
totaldata = { 'speccpu': sheet_speccpu_data, 'Perf_cpu': sheet_syscpu_data,
              "Perf_kernel": sheet_lmbench_data, "Perf_mem": sheet_sysmem_data,
              "Perf_io": sheet_io_data, "Perf_thread": sheet_pingpong_data,
              "Perf_stream": sheet_stream_data, "Perf_graphics": sheet_graphics_data,
              "Perf_system": sheet_system_data, "Perf_browser": sheet_browser_data}
htmldata = {'Perf_cpu' : html_syscpu_data, 'Perf_mem': html_sysmem_data,
            'Perf_io': html_iozone_data, 'Perf_thread': html_pingpong_data,
            'Perf_kernel': html_lmbench_data, 'Perf_stream': html_stream_data,
            'Perf_graphics': html_graphics_data, 'Perf_system': html_system_data,
            'Perf_browser': html_browser_data,}
exceptitem = ("Perf_kernel", "Perf_stream", "Perf_graphics", "Perf_browser")
class Control_processing(object):
    def __init__(self, myargs):
        '''{'items': ['cpu'], 'type': ['xls'], 'osnames': ['iSoft_Desktop_4.0']}'''
        self.args = myargs

    def _getxlsdata(self, oslist, itemlist):
        for testitem in itemlist:
            if testitem in exceptitem:
                for os in oslist:
                    for i, patterns in enumerate(patternmath[testitem]):
                        testdata=[]
                        datalist = []
                        for j, pattern in enumerate(patterns):
                            data = ResultSorting()
                            datatmp = data.datasearch_lm(pattern, "finalresult/%s/%s/result/result.out" %(os, testitem), patternnum[testitem])
                            for k, datasub in enumerate(datatmp):
                                datalist.append(datatmp[k])
                        testdata.append(datalist)   
                        for datasub in testdata:
                            totaldata[testitem][i].append(datasub)
            else:
                for os in oslist:
                    for i, patterns in enumerate (patternmath[testitem]):
                        testdata=[]
                        datalist = []
                        for j, pattern in enumerate(patterns):
                            data=ResultSorting()
                            datatmp = data.datasearch(pattern, "finalresult/%s/%s/result/result.out" %(os, testitem), patternnum[testitem])
                            for k, datasub in enumerate(datatmp):
                                datalist.append(datatmp[k])
                        testdata.append(datalist)   
                        for datasub in testdata:
                            totaldata[testitem][i].append(datasub)
        return totaldata
 
    def _gethtmldata(self, oslist, itemlist):
        for testitem in itemlist:
            if testitem in exceptitem:
                for i, patterns in enumerate (patternmath[testitem]):
                    for os in oslist:
                        testdata=[]
                        datalist = []
                        for j, pattern in enumerate(patterns):
                            data=ResultSorting()
                            datatmp = data.datasearch_lm(pattern, "finalresult/%s/%s/result/result.out" %(os, testitem), 3)
                            for k, datasub in enumerate(datatmp):
                                datalist.append(datatmp[k])
                        testdata.append(datalist)
                        for datasub in testdata:
                            htmldata[testitem].append(datasub)
            else:
                for i, patterns in enumerate (patternmath[testitem]):
                    for os in oslist:
                        testdata=[]
                        datalist = []
                        for j, pattern in enumerate(patterns):
                            data=ResultSorting()
                            datatmp = data.datasearch(pattern, "finalresult/%s/%s/result/result.out" %(os, testitem), 3)
                            for k, datasub in enumerate(datatmp):
                                datalist.append(datatmp[k])
                        testdata.append(datalist)
                        for datasub in testdata:
                            htmldata[testitem].append(datasub)
        return htmldata

    def _mkxls(self):
        '''infolist=[sheet_speccpu_info, sheet_lmbench_info, sheet_syscpu_info]
           datalist=[sheet_speccpu_data, sheet_lmbench_data, sheet_syscpu_data]
        ''' 
        itemlist = self.args['items']
        oslist = self.args['osnames']
        totaldata = self._getxlsdata(oslist, itemlist)
        mkxls(totaldata, itemlist, oslist)
        htmldata = self._gethtmldata(oslist, itemlist)
        mkhtml(htmldata, itemlist, oslist)

#testcase
#a=Control_processing()
#a._mkxls()
