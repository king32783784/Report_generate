import os
import sys
from subprocess import call, PIPE, Popen
from mkchart import *
# sysbench_cpu
md_syscpu = [
    '''
##sysbench - Performance Test of CPU

###CPU Execution time(second) - 1thread

*OS* | *10000* | *20000* | *30000*
------ | --------- | --------- | ---------''',
]
chart_syscpu = [{
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'CPU Execution time (sec)',
          'osnames': [],
          'subjects': ('1000', '2000', '3000'),
          'scores': [[10.844, 28.028, 48.917], [11.304, 28.860, 50.346]],
          'pngname': 'result_html/svgfile/syscpu0.png'
           },]
#sysbench_mem
md_sysmem=[
    '''
##sysbench - Performance Test of MEM
### MEM Operations performed - 4threads & 8 threads

*OS* | *4threads(ops/sec)* | *8threads(ops/sec)*
------ | ------------------- | ----------------''',
    '''
### MEM Transfer rate - 4threads & 8 threads
*OS* | *4threads(MB/sec)* | *8threads(MB/sec)*
------ | ------------------- | ------------------'''
]
chart_sysmem = [{
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'MEM Operations performed (ops/sec)',
    'osnames': [],
    'subjects': ('4threads', '8threads'),
    'scores': ([3324739.04, 3298945.06], [3351746.42, 3457950.96]),
    'pngname': 'result_html/svgfile/sysmem0.png'},
    {
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'Mem Transfer Rate (MB/s)',
    'osnames': [],
    'subjects': ('4threads', '8threads'),
    'scores': ([12987.26, 12886.51], [13092.76, 13507.62]),
    'pngname': 'result_html/svgfile/sysmem1.png'},]

    
class MkHtml(object):
    def __init__(self, oslist, testitem, resultdata):
        self.oslist = oslist
        self.itemlist = testitem
        self.resultdata = resultdata
        print self.itemlist
 #       print self.resultdata

    def wraptreatment(self, length, charters):
        temp =''
        t = 0
        for i, charter in enumerate(charters, 1):
            if i % length == 0:
                temp = temp + charters[t:i] + "\n"
                t = i
        temp = temp + charters[t:]
        return temp
     
    def _mkchartdata(self, itemmddata, offset):
        print offset
        for osname in self.oslist:
            ostest = self.wraptreatment(9, osname)
            chartditlist[self.itemlist][offset]['osnames'].append(ostest)
        chartditlist[self.itemlist][offset]['scores'] = itemmddata
        if os.path.isdir("result_html/svgfile/") is not True:
            try:
                retcode = call("mkdir result_html/svgfile", shell=True)
                if retcode < 0:
                    print >> sys.stderr, "Child was terminated by signal", -retcode
                else:
                    print >>sys.stderr, "Child returned", retcode
            except OSError as e:
                print >>sys.stderr, "Execution failed:", e
        return chartditlist[self.itemlist][offset]
         
    def _mkchart(self, mdfile, charttmpdict):
        mkchart(charttmpdict)
        f = open(mdfile, 'a+')
        a = charttmpdict['pngname']
        f.write("![](./%s)" %(a.split("/")[1] + '/' + a.split("/")[2]))
        
    def _mkmdfile(self, mdfile, itemmdtitle, itemmddata, offset):
        f = open(mdfile, 'a+')
        f.write(itemmdtitle)
        f.write("\n")
        for i, osname in enumerate(self.oslist):
            datatemp = ""
            for datalist in itemmddata[i]:
                datatemp = datatemp + '|' + '%s' % datalist
            f.write("%s" % self.oslist[i] + datatemp + "|" + "\n")
        charttmpdict = self._mkchartdata(itemmddata, offset)
        print charttmpdict
        self._mkchart(mdfile, charttmpdict)

    def _mkresult(self):
        mdfile = os.path.join('result_html', 'Lpb_i.md')
        step = len(self.oslist)
        finaldata = []
        datatemp = []
        for i, data in enumerate(self.resultdata[self.itemlist]):
            datatemp.append(data)
            if i % step == 1:
                finaldata.append(datatemp)
                datatemp = []
        for i, itemmdtitle in enumerate(mdtitle[self.itemlist]):
            self._mkmdfile(mdfile, itemmdtitle, finaldata[i], i)
#        self._mkchart(mdfile)

mdtitle = {'Perf_cpu': md_syscpu ,'Perf_mem': md_sysmem}
chartditlist = {'Perf_cpu': chart_syscpu, 'Perf_mem': chart_sysmem}

def mkhtml(htmldata, itemlist, oslist):
    if os.path.isdir("result_html") is not True:
        try:
            retcode = call("mkdir result_html", shell=True)
            if retcode < 0:
                print >> sys.stderr, "Child was terminated by signal", -retcode
            else:
                print >>sys.stderr, "Child returned", retcode
        except OSError as e:
            print >>sys.stderr, "Execution failed:", e
#oslist = ['iSoft_Desktop_4.0', 'Deepin_4.0']
    for testitem in itemlist:
        mkhtml = MkHtml(oslist, testitem, htmldata)
        mkhtml._mkresult()
