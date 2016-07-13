#!/usr/bin/env python
# coding: utf-8

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.patches as mpatches
reload(sys)


#colour
colours = (
    '#4169E1', #Blue
    '#A52A2A', #Brown
    '#82B446', #Green
    '#FF8C00', #Orange
    '#8A2BE2' #BlueViolet
    )



class MkChart(object):
    def __init__(self, chartargs='test'):
        self.custom_font = mpl.font_manager.FontProperties(fname='%s' %
                           chartargs['custom_font'])
        self.names = chartargs['osnames']   # 对比OS名称 *
        self.subjects = chartargs['subjects'] # 对比项目 *
        self.scores = chartargs['scores'] # 项目数值*
        self.title = chartargs['title']
        self.pngname = chartargs['pngname']
    
    def _setfigsize(self):   
        ''' 根据对比OS数量及对比项目的多少进行图表尺寸的调整'''
        step = 0.5
        base = 9
        figlong = base + len(self.scores[0]) / 2.0 * 0.5
        return figlong
    
    def _setbarwidth(self):
        ''' 根据对比OS数量及对比项目的多少及图表的大小进
            行柱形a图宽度的调整'''
        base = 0.32
        rate = 0.9
        barwid = base * (rate ** len(self.names))
        return barwid

    def _setymax(self):
        '''根据项目数值范围进行Y轴数值的设定'''
        max = 0
        for i in self.scores:
            for j in i:
                if j > max:
                    max = j
        return max * 1.2
    
    def _setscores(self):
        '''增加空项目用于存放图例'''
        scores=self.scores
        for i in self.scores:
            i.append(0)
            i.append(0)
        return scores

    def _setlegend(self):
        if len(self.scores[0]) < 5:
            return 0.7
        else:
            return 0.75

    def graphing(self):
        font_size = 10 # 字体大小
        fig_size = (self._setfigsize(), 4) # 图表大小 *
        scores=self._setscores()
        mpl.rcParams['font.size'] = font_size #更新字体大小
        mpl.rcParams['figure.figsize'] = fig_size #更新图表大小
        bar_width = self._setbarwidth()  #设置柱形图宽度 *
        index = np.arange(len(scores[0]))
        for i in range(0,len(self.names)):
            rects = plt.bar(index + i * bar_width, scores[i], bar_width,
                    color=colours[i], label=self.names[i])
        # X轴标题
        plt.xticks(index + bar_width, self.subjects, fontproperties=
                   self.custom_font)
        # Y轴范围
        maxscore = self._setymax()
        plt.ylim(ymax=maxscore, ymin=0)
        # 图表标题
        plt.title(u'%s' % self.title, fontproperties=self.custom_font)
        # 图例显示在图表下方
        # plt.legend(loc='center right', bbox_to_anchor=(0.8, -0.1),
        #            fancybox=True, ncol=3, prop=custom_font)
        # 图例显示在右侧
        plt.legend(bbox_to_anchor=(self._setlegend(), 0.9), loc=2,
                   prop=self.custom_font,  borderaxespad=0.)
        # 图例显示在上部
        # plt.legend(bbox_to_anchor=(0., 0.9, 1., 0.102), loc=1,
        # ncol=2, mode="expand", borderaxespad=0.1)

    def _mkchart(self):
        self.graphing()
        plt.savefig(self.pngname)
# samples
'''
sysbenchcpu = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'CPU Execution time (sec)',
          'osnames': ('isoft-4.0\n-beta3', 'Fedora-23'),
          'subjects': ('1000', '2000', '3000'),
          'scores': [[10.844, 28.028, 48.917], [11.304, 28.860, 50.346]],
          'pngname': 'vsysbench.cpu.png'
           }

sysbenchmema = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'MEM Operations performed (ops/sec)',
          'osnames': ('isoft-4.0\n-beta3', 'Fedora-23'),
          'subjects': ('4threads', '8threads'),
          'scores': ([3324739.04, 3298945.06], [3351746.42, 3457950.96]),
          'pngname': 'sysMEMA.png'
           }

sysbenchmemb = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'Mem Transfer Rate (MB/s)',
          'osnames': ('isoft-4.0\n-beta3', 'Fedora-23'),
          'subjects': ('4threads', '8threads'),
          'scores': ([12987.26, 12886.51], [13092.76, 13507.62]),
          'pngname': 'sysMEMB.png'
           }

iozone = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'Iozone Test (Kb/s)',
          'osnames': ('isoft-4.0\n-beta3', 'Fedora-23'),
          'subjects': ('Write', 'Rewrite', 'Read', 'Reread',
                       'Rondom\nread', 'Rondom\nwrite'),
          'scores': ([110277, 111773, 108626, 108941, 4067, 6657.67],
                     [127506, 128270, 124400, 124539, 4081.33, 6947.33]),
          'pngname': 'viozone.png'
           }

lmbench1 = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'Processor(usec)',
          'osnames': ('isoft-4.0\n-beta3', 'Fedora-23', 'deepin',
                      'yiming', 'neokylin'),
          'subjects': ('null\ncall', 'null\nI/O', 'stat', 'open\nclos',
                      'slct\nTCP', 'sig\ninst', 'sig\nhndl',
                       'fork\nproc', 'exec\nproc', 'sh\nproc'),
          'scores': ([0.08, 0.13, 0.70, 1.03, 2.96, 0.16, 0.86, 0.11,
                      0.35, 2.80], [0.08, 0.13, 0.70, 1.03, 2.96, 0.16,
                      0.86, 0.11, 0.35, 2.80], [0.08, 0.13, 0.70, 1.03,
                      2.96, 0.16, 0.86, 0.11, 0.35, 2.80], [0.08, 0.13,
                      0.70, 1.03, 2.96, 0.16, 0.86, 0.11, 0.35, 2.80],
                      [0.07, 0.14, 0.85, 1.44, 2.92, 0.13, 0.90, 0.12,
                      0.41, 4.34]),
          'pngname': 'LMPROCESS1.png'
           }

lmbenchint = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'Basic integer (usec)',
          'osnames': ('isoft-4.0\n-beta3', 'Fedora-23', 'neokylin',
                      'deepin', 'yiming'),
          'subjects': ('intgr\nbit', 'intgr\nadd', 'intgr\nmul',
                       'intgr\ndiv', 'intgr\nmod'),
          'scores': ([0.32, 0.12, 0, 11.48, 10.97], [0.33, 0.12, 0, 7.89,
                    8.1], [0.34, 0.12, 1, 8, 7], [0.34, 0.12, 1, 8, 7],
                   [0.34, 0.12, 1, 8, 7]),
          'pngname': 'LMINT.png'
           }

lmdouble = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'Basic double (usec)',
          'osnames': ('isoft-4.0\n-beta3', 'Fedora-23', 'hello',
                       'world', 'nihao'),
          'subjects': ('double\nadd', 'double\nmul', 'double\ndiv',
                       'double\nbogo'),
          'scores': ([1.39, 2.33, 10.34, 11.77], [0.98, 1.62, 8.74, 8.78],
                     [0.98, 1.62, 8.74, 8.78], [0.98, 1.62, 8.74, 8.78],
                     [0.98, 1.62, 8.74, 8.78]),
          'pngname': 'LMDOUBLE.png'
           }

lmcontext = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'Context switching (usec)',
          'osnames': ('isoft-4.0\n-beta3', 'Fedora-23'),
          'subjects': ('2p/0k', '2p/16k', '2p/64k', '8p/16k',
                       '8p/64k', '16p/16k', '16p/64k'),
          'scores': ([2.44, 1.63, 2.30, 1.58, 2.19, 1.61, 1.73], [
                     1.98, 1.82, 0.99, 2.2, 1.37, 2.27, 1.55]),
          'pngname': 'LMCONTEXT.png'
           }

lmfile = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'File & VM system latencies (usec)',
          'osnames': ('isoft-4.0\n-beta3', 'Fedora-23'),
          'subjects': ('0K File\nCreate', '0K File\n Delete',
           '10K File\nCreate', '10K File\nDelete', 'Mmap\nLatency',
            'Prot\nFault', 'Page\nFault', '100fd\nselct'),
          'scores': ([8.84, 5.96, 16.07, 7.94, 140.67, 0.48, 0.20, 1.28],
          [19.06, 4.89, 21.23, 8.47, 86, 0.28, 0.20, 0.98]),
          'pngname': 'LMFILEVM.png'
           }
test = {'title': 'CPU Execution time (sec)', 'custom_font': '/usr/share/fonts/goffer.ttf', 'subjects': ('10000', '20000', '30000'), 'osnames': ['iSoft_Desknktop_4.0'], 'scores': [[13.0775, 31.9033, 55.9291]], 'pngname': 'chart.cpu.png'}
'''
#testsample = (sysbenchcpu, sysbenchmema, sysbenchmemb, iozone, lmbench1,
 #             lmbenchint, lmdouble, lmcontext, lmfile)
#g = MkChart(chartargs=sysbenchcpu)
#g._mkchart()
