import re


class ResultSorting(object):

    def readfile(self, resultfile):
        fopen = open(resultfile, 'r')
        f = fopen.read().strip()
        return f

    def datasearch(self, searchmode, resultfile, times):
        times = int(times)
        f = self.readfile(resultfile)
        re_list = re.findall(r"%s" % searchmode, f, re.S)
        print re_list
        testarry = []
        for i in re_list:
            testarry.append(float(i))
        j = 0
        averge = []
        for i, data in enumerate(testarry, 1):
            if i % times == 0:
                averge.append((sum(testarry[j:i]) / times))
                j = i
        result = []
        for i in averge:
            result.append(float(format(i, '0.2f')))
        return result
# useage
#a=ResultSorting()
#d = a.datasearch("Children see throughput for 1 random writers \t=   (.*?)KB\\/sec",
#"finalresult/iSoft_Desktop_4.0/Perf_io/result/result.out", 3)
#print d
