import os
import sys
import shutil
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
           }, ]
# sysbench_mem
md_sysmem = [
    '''

##sysbench - Performance Test of MEM

###MEM Operations performed - 4threads & 8 threads

*OS* | *4threads(ops/sec)* | *8threads(ops/sec)*
------ | ------------------- | ----------------''',
    '''

###MEM Transfer rate - 4threads & 8 threads

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
    'pngname': 'result_html/svgfile/sysmem1.png'}, ]
# pingpong_thread
md_pingpong = [
    '''

##Pingpong - Performance Test of Threads

Threads initialised - times in microseconds - smaller is better

*OS* | *Tables 16* | *Tables 32* | *Tables 64*
------ | ------------- | ------------- | ------------''',
    '''

Games completed - times in microseconds - smaller is better

*OS* | *Tables 16* | *Tables 32* | *Tables 64*
------ | ------------ | ------------ | ------------'''
]
chart_pingpong = [{
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'Threads initialised(usec)',
    'osnames': [],
    'subjects': ('32threads', '64threads', '128threads'),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'result_html/svgfile/pingpong0.png'},
    {
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'Games completed (usec)',
    'osnames': [],
    'subjects': ('16Games', '32Games', '64Games'),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'result_html/svgfile/pinpong1.png'}, ]

# iozone_io
md_iozone = [
    '''

##iozone - Performance Test of IO

###Variety of file operations

*OS* | *Write* | *Rewrite* | *Read* | *Reread* | *Rondom read* | *Rondom write*
-----| ------- | --------- | ------ | -------- | ------------- | --------------'''
]
chart_iozone = [{
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'Variety of file operatios KB/sec',
    'osnames': [],
    'subjects': ('Write', 'Rewrite', 'Read', 'Reread', 'Rondom read', 'Rondom write'),
    'scores': ([3324739.04, 3298945.06, 12222, 124123, 12344, 12344],),
    'pngname': 'result_html/svgfile/iozone0.png'},]


class MkHtml(object):
    def __init__(self, oslist, testitem, resultdata):
        self.oslist = oslist
        self.itemlist = testitem
        self.resultdata = resultdata

    def wraptreatment(self, length, charters):
        temp = ''
        t = 0
        for i, charter in enumerate(charters, 1):
            if i % length == 0:
                temp = temp + charters[t:i] + "\n"
                t = i
        temp = temp + charters[t:]
        return temp

    def _mkchartdata(self, itemmddata, offset):
        for osname in self.oslist:
            ostest = self.wraptreatment(30, osname)
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
        mkcontrol(charttmpdict)
        f = open(mdfile, 'a+')
        a = charttmpdict['pngname']
        f.write("\n")
        f.write("![](./%s)" % (a.split("/")[1] + '/' + a.split("/")[2]))
        f.close()

    def _mkmdfile(self, mdfile, itemmdtitle, itemmddata, offset):
        f = open(mdfile, 'a+')
        f.write(itemmdtitle)
        f.write("\n")
        for i, osname in enumerate(self.oslist):
            datatemp = ""
            for datalist in itemmddata[i]:
                datatemp = datatemp + '|' + '%s' % datalist
            f.write("%s" % self.oslist[i] + datatemp + "|" + "\n")
        f.close()
        charttmpdict = self._mkchartdata(itemmddata, offset)
        self._mkchart(mdfile, charttmpdict)

    def _mkresult(self):
        mdfile = os.path.join('result_html', 'Lpb_i.md')
        step = len(self.oslist)
        print step
        finaldata = []
        datatemp = []
        for i, data in enumerate(self.resultdata[self.itemlist]):
            datatemp.append(data)
            if step > 1:
                if i % step == step-1:
                    finaldata.append(datatemp)
                    datatemp = []
            else:
                finaldata.append(datatemp)
                datatemp = []
        print finaldata
        for i, itemmdtitle in enumerate(mdtitle[self.itemlist]):
            self._mkmdfile(mdfile, itemmdtitle, finaldata[i], i)

mdtitle = {'Perf_cpu': md_syscpu, 'Perf_mem': md_sysmem, 'Perf_io': md_iozone, 'Perf_thread':
           md_pingpong}
chartditlist = {'Perf_cpu': chart_syscpu, 'Perf_mem': chart_sysmem, 'Perf_io': chart_iozone,
                'Perf_thread': chart_pingpong}


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
    for testitem in itemlist:
        mkhtml = MkHtml(oslist, testitem, htmldata)
        mkhtml._mkresult()
    shutil.copy("style.css", "result_html")
    try:
        retcode = call("pandoc --toc -c ./style.css -o result_html/test.html \
                       result_html/Lpb_i.md", shell=True)
        if retcode < 0:
            print >> sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", retcode
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e
