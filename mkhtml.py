import os
from datasorting import ResultSorting
#from mkchart import MkChart

chartdata = {
          'custom_font': '/usr/share/fonts/goffer.ttf',  # chart font
          'title': '',      # chart title
          'osnames': [],    # os names
          'subjects': (''), 
          'scores': [],   
          'pngname': ''     
           }
Mk_temp={
    "sysbenchmemops" :'''
MEM Operations performed - 4threads & 8 threads -bigger is better

*OS* | *4threads(ops/sec)* | *8threads(ops/sec)*
------ | ------------------- | ----------------''',
    "sysbenchmemmrate" :'''
MEM Transfer rate - 4threads & 8 threads -bigger is better
*OS* | *4threads(MB/sec)* | *8threads(MB/sec)*
------ | ------------------- | ------------------'''
}


data_cpu_aidinfo = {
    "search_path": "execution time \(avg\/stddev\):(.*?)\/0.00",
    "chart_title": ('CPU Execution time (sec)'),
    "subjects": ('10000', '20000', '30000'),
    "itemname" : "sysbench_cpu",
    "mdtitle" : '''
## Sysbench - Performance Test of CPU

CPU Execution time(second) - 1thread - smaller is better

*OS* | *10000* | *20000* | *30000*
------ | --------- | --------- | ---------
'''
}

data_search_path = {
    "sysbench_mem_ops": "Operations performed: 2097152 \((.*?)ops\/sec\)",
    "sysbench_mem_rate": "8192.00 MB transferred \((.*?)MB\/sec\)",
    "sysbench_cpu" : "execution time \(avg\/stddev\):(.*?)\/0.00"
}


class MkResult(ResultSorting):
     def __init__(self, testitemaidinfo, times, resultfile, resultdir, oslist):
         self.testaidinfo = testitemaidinfo
         self.times = times
         self.resultfile = resultfile
         self.resultdir = resultdir
         self.oslist = oslist
     
     def wraptreatment(self, length, charters):
         temp =''
         t = 0
         for i, charter in enumerate(charters, 1):
              if i % length == 0:
                  temp = temp + charters[t:i] + "\n"
                  t = i
         temp = temp + charters[t:]
         return temp
     
     def _mkdata(self):
         dataresult = self.datasearch(self.testaidinfo['search_path'], self.resultfile, self.times)
         osname = self.wraptreatment(9, ReadSysinfo.os_name())
         charttmpdict = chartdata
         charttmpdict['title'] = self.testaidinfo['chart_title']     
         charttmpdict['subjects'] = self.testaidinfo['subjects']
         charttmpdict['osnames'].append(osname)
         charttmpdict['scores'].append(dataresult)
         pngdir = os.path.join(self.resultdir, self.testaidinfo['chart_pngname'])
         charttmpdict['pngname'] = pngdir
         return charttmpdict
         
     def _mkchart(self, mdfile):
         charttmpdit = self._mkdata()
         mkchart = MkChart(chartargs=charttmpdit)
         mkchart._mkchart()
         f = open(mdfile, 'a+')
         f.write("![](.%s)" %self.testaidinfo['chart_pngname'])
        
     def _mkmdfile(self, mdfile):
         dataresult = self.datasearch(self.testaidinfo['search_path'], self.resultfile, self.times)
         datatemp = ""
         for charter in dataresult:
              datatemp = datatemp + "|" + "%s" % charter
         f = open(mdfile, 'a+')
         f.write(self.testaidinfo['mdtitle'])
         f.write("%s" % self.oslist[0] +  datatemp + "|" + "\n" + "\n")
    
     def mkresult(self):
         mdfile = os.path.join(self.resultdir, 'Lpb_i.md')
         self._mkmdfile(mdfile)
     #    self._mkchart(mdfile)
oslist = ['iSoft_Desktop_4.0', 'Deepin_4.0']
a = MkResult(data_cpu_aidinfo, 3, '/home/isoft_lp/Github/Lpbs-i/resulttmp/performance/Perf_cpu/result/result.out', '/home/isoft_lp/Github/Lpbs-i/finalresult', oslist)
a.mkresult()
