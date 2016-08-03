# usr/bin/env python
# coding: utf-8
#######################################################################
#
# Performance Excel chart with Python and XlsxWriter.
#
# by lp 2016.6.24
#
import xlsxwriter
import sys
import string
reload(sys)
sys.setdefaultencoding('utf8')

# xls_dirt字典保存基础信息
sheet_speccpu_info = {
    'sheetname': '处理器运算',
    'testinfo': ("处理器运算性能", "测试工具：SPEC CPU 2000",
        "性能指标：Spec2000 包括 SPECint2000、SPECfp2000、\
             SPECint_rate2000、 SPECfp_rate2000 4个测试项",
        "对比说明：其中的得分越大说明CPU性能越高",
        "测试参数：runspec -c test.cfg -i ref -n 3 -r -u 4 -I all;\
                   runspec -c test.cfg -i ref -n 3 -I all", ),
    "oslist": ["isoft_desktop V4.0 loongson", "Deepin15_mips_20160520",
               "Neokylin Desktop-7.0-loongson"],
    }

sheet_syscpu_info = {
    'sheetname': '处理器运算_B',
    'testinfo': ("处理器运算性能", "测试工具：sysbench",
        "性能指标: 包括10000、20000、30000",
        "对比说明: 数值越小越好",
        "测试参数：sysbench --test=cpu --cpu-max-prime=10000/20000/30000 run",
         ),
     'oslist': ["isoft_desktop V4.0 loongson", "Deepin15_mips_20160520",
                "Neokylin Desktop-7.0-loongson"],}
sheet_iozone_info = {
    'sheetname': 'IO读写',
    'testinfo': ("I/O读写性能", "测试工具:iozone3",
        "性能指标: 包括IO的写、重复写、读、重复读、随机写、随机读等指标",
        "对比说明：测试结果均为3次平均值， 数值越大，说明I/O性能越好",
        "测试参数：./iozone -s 16G -i 0 -i 1 -i 2 -t 1 -r 1M",),
    'oslist': [],}
sheet_pingpong_info = {
    'sheetname': "线程操作",
    'testinfo': ("线程操作性能", "测试工具： ping-pong",
         "性能指标： 包含 16、32、64 tables的性能",
         "对比说明：测试结果均为3次平均值， 数值越小，说明响应越快，性能越好",
         "测试参数：#./Runtest.sh 16 32 64",),
    'oslist':[],}
sheet_sysmem_info = {
    'sheetname': "内存操作",
    'testinfo': ("内存操作性能", "测试工具: sysbench", "性能指标: \
                 包括4/8线程内存操作速度和带宽", "对比说明：\
                 测试结果为３次求平均值","测试参数:sysbench\
                 --test=memory --num-threads=4/8 --memory-block-size=8192\
                 --memory-total-size=4G run"),
    'oslist':["testos"]
}
sheet_lmbench_info = {
    'sheetname': '内核',
    'testinfo': ("内核性能测试","测试工具：lmbench", 
        "性能指标：选取了Processor、Context switching、*Local* Communication\
         latencies 、File & VM system latencies 、\n    *Local* Communication\
         bandwidths等指标", "对比说明：测试结果均为测试3次求平均值",
         "测试参数：以root用户执行测试，运行make result，之后继续运行两次\
         make rerun，最后执行make see"),
    'oslist': ["isoft_desktop V4.0 loongson", "Deepin15_mips_20160520",
               "Neokylin Desktop-7.0-loongson"],
    }

# format_dirt字典保存格式化信息
# 结果图表title格式
formtitle_format = {
    'bold': False,   # 设置加粗
    'border': 1,  # 设置边框格式
    'fg_color': '#CC99FF',  # 设置单元格填充颜色
    'font_size': 10,   # 设置字体大小
    'align': 'center',  # 设置对齐方式
    'valign': 'vcenter',  # 设置对齐方式
}
# 页title格式
sheettitle_format = {
    'bold':     True,
    'border':   1,
    'font_size': 14,
    'font_color': '#FFFF99',
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#333399',
}

# 测试说明信息格式

info_fortmat = {
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': '#B8CCE4',
}

# 测试结果表格副标题格式
formsubtitle_format = {
    'bold': True,
    'border': 1,
    'font_size': 12,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': '#339966',
}

# 测试结果数值格式
result_format = {
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'center',
    'valign': 'vcenter',
    'num_format': '0.00',
}

# 测试项目名称格式
item_format = {
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': '#CCFFFF',
}

# 测试结果分析title格式
resulttitle_format = {
    'bold': True,
    'border': 1,
    'font_size': 12,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#339966',
}


class MkSinglesheet(object):
    def __init__(self, workbook, iteminfo, itemdata):
        self.info = iteminfo
        self.data = itemdata
        self.layoutinfo = self.layoutinformation()
        self.workbook = workbook

    def layoutinformation(self):
        formnum = {}
        formnum['seriesnum'] = len(self.info['oslist'])
        columnwidth = []
        for item in self.data:
            columnwidth.append(len(item[1])-1)
        columnno = []
        for i in columnwidth:
            columnno.append(string.uppercase[i])
        formnum['columnwidth'] = columnno
        return formnum

    def input_sheettitle(self, worksheet, formatinfo):
        format = self.workbook.add_format(sheettitle_format)
        worksheet.merge_range('A1:%s1' % formatinfo['largerow'],
                              self.info['testinfo'][0], format)

    def input_testinfo(self, worksheet, formatinfo):
        format = self.workbook.add_format(info_fortmat)
        worksheet.merge_range('A2:%s2' % formatinfo['largerow'],
                              self.info['testinfo'][1], format)
        worksheet.merge_range('A3:%s3' % formatinfo['largerow'],
                              self.info['testinfo'][2], format)
        worksheet.merge_range('A4:%s4' % formatinfo['largerow'],
                              self.info['testinfo'][3], format)
        worksheet.merge_range('A5:%s5' % formatinfo['largerow'],
                              self.info['testinfo'][4], format)

    def input_formsubtitle(self, worksheet, linenum, columnnum, iteminfo):
        format = self.workbook.add_format(formsubtitle_format)
        worksheet.merge_range('A%s:%s%s' % (linenum, columnnum, linenum),
                              iteminfo, format)

    def input_formtitle(self, worksheet, linenum, iteminfo):
        format = self.workbook.add_format(formtitle_format)
        worksheet.write_row('A%s' % linenum, iteminfo, format)

    def input_formitem(self, worksheet, linenum, seriesinfo):
        format = self.workbook.add_format(item_format)
        worksheet.write_column('A%s' % linenum, seriesinfo, format)

    def input_formdata(self, worksheet, linenum, testdata):
        format = self.workbook.add_format(result_format)
        lastline = linenum + self.layoutinfo['seriesnum']
        for data, line in zip(testdata[2:], range(linenum, lastline)):
            worksheet.write_row('B%s' % line, data, format)

    def setcellformat(self, worksheet):
        firstrow = float(self.setbandwith(self.dirt['basedata'][1]) / 1.2)
        otherrow = float(self.setbandwith(self.dirt['basedata'][0]) * 1.2)
        rows = formnum[0]
        lines = formnum[1]
        lastline = 8 + lines
        worksheet.set_column(0, 0, firstrow)
        worksheet.set_column(1, rows+1, otherrow)

    def setbandwidth(self, data):
        length = 0
        for charter in data:
            if len(charter) > length:
                length = len(charter)
        return length

    def formatinfo(self):
        formatinfodict = {}
        columnwidthst = float(self.setbandwidth(self.info['oslist']) / 1.2)
        formatinfodict['columnwidthst'] = columnwidthst
        columnwidthother = 0
        rows = 0
        for i, itemname in enumerate(self.data):
            if self.setbandwidth(self.data[i][1]) > columnwidthother:
                columnwidthother = self.setbandwidth(self.data[i][1])
            if len(self.data[i][1]) > rows:
                rows = len(self.data[i][1])
        columnwidthother = float(columnwidthother * 1.2)
        formatinfodict['columnwidthother'] = columnwidthother
        formatinfodict['rowslarge'] = rows
        formatinfodict['largerow'] = string.uppercase[rows-1]
        figwidelist = []
        for i, itemname in enumerate(self.data):
            figwidelist.append((columnwidthst + columnwidthother *
                                len(self.data[i][1])) * 5.5)
        formatinfodict['figwidelist'] = figwidelist
        return formatinfodict

    def sheetformatting(self, worksheet, formatinfo):
        worksheet.set_row(0, 45)
        startline = 7
        lastline = startline + 2 + self.layoutinfo['seriesnum']
        step = 20 + self.layoutinfo['seriesnum']
        for i, item in enumerate(self.data):
            for j in range(startline, lastline):
                worksheet.set_row(j, 19)
            startline = startline + step
            lastline = lastline + step
        for i in range(1, 5):
            worksheet.set_row(i, 21)
        worksheet.set_column(0, 0, formatinfo['columnwidthst'])

    def mk_chart(self, worksheet, chartwidth, linenum, figwide, itemdata):
        item_linenum = linenum + 1
        series_linenum = item_linenum + 1
        chart = self.workbook.add_chart({'type': 'column'})
        seriesnum = self.layoutinfo['seriesnum']
        chart.add_series({
            'name': '=%s!$A$%s' % (worksheet.name, series_linenum),  # 系列名称
            'categories': '=%s!$B$%s:$%s$%s' % (worksheet.name, item_linenum,\
                                                chartwidth, item_linenum),
            'values': '=%s!$B$%s:$%s$%s' % (worksheet.name, series_linenum,\
                                            chartwidth, series_linenum),
            'gap': 200,
            })
        if seriesnum > 1:
            for i, osname in enumerate(self.info['oslist'][0:-1]):
                lineno = i + series_linenum + 1
                chart.add_series({
                    'name': '=%s!$A$%s' % (worksheet.name, lineno),
                    'values': '=%s!$B$%s:$%s$%s' % (worksheet.name, lineno,
                                                    chartwidth, lineno)
                })
        chart.set_size({'width': figwide, 'height': 320})
        chart.set_x_axis({
            'position_axis': 'between',
        })
        chart_titlename = itemdata[0][1]
        chart.set_title({'name': chart_titlename})
        chart_insert_site = 'A%s' % int(series_linenum + 1 + seriesnum)
        worksheet.insert_chart(chart_insert_site, chart)

    def additems(self, worksheet, formatinfo):
        titleline = 7
        itemline = 8
        seriesline = 9
        step = 20 + self.layoutinfo['seriesnum']
        for i, additem in enumerate(self.data):
            self.input_formsubtitle(worksheet, titleline,
                                    self.layoutinfo['columnwidth'][i],
                                    self.data[i][0][0])
            self.input_formtitle(worksheet, itemline, self.data[i][1])
            self.input_formitem(worksheet, seriesline, self.info['oslist'])
            self.input_formdata(worksheet, seriesline, self.data[i])
            self.mk_chart(worksheet, self.layoutinfo['columnwidth'][i],
                          titleline, formatinfo['figwidelist'][i],
                          self.data[i])
            titleline = titleline + step
            itemline = itemline + step
            seriesline = seriesline + step
        self.addresultanalysistitle(worksheet, titleline,
                                    formatinfo['largerow'])
        self.addresultanalysis(worksheet, titleline+1, formatinfo['largerow'])

    def addresultanalysistitle(self, worksheet, lastline, columnwidth):
        format = self.workbook.add_format(resulttitle_format)
        worksheet.merge_range('A%s:%s%s' % (lastline, columnwidth,
                              lastline), "测试结果分析", format)

    def addresultanalysis(self, worksheet, lastline, columnwidth):
        format = self.workbook.add_format(item_format)
        worksheet.merge_range('A%s:%s%s' % (lastline, columnwidth,
                              lastline+3), " ", format)

    def addsheet(self):
        formatinfo = self.formatinfo()
        worksheet = self.workbook.add_worksheet(self.info['sheetname'])
        self.input_sheettitle(worksheet, formatinfo)
        self.input_testinfo(worksheet, formatinfo)
        self.additems(worksheet, formatinfo)
        self.sheetformatting(worksheet, formatinfo)

# infolist=[sheet_speccpu_info, sheet_lmbench_info, sheet_syscpu_info]
# datalist=[sheet_speccpu_data, sheet_lmbench_data, sheet_syscpu_data]
totalinfo = {'speccpu': sheet_speccpu_info, 'Perf_cpu': sheet_syscpu_info,
             "lmbench": sheet_lmbench_info, 'Perf_mem': sheet_sysmem_info,
             "Perf_io": sheet_iozone_info, 'Perf_thread': sheet_pingpong_info}


def mkxls(totaldata, itemlist, oslist):
    infolist = []
    datalist = []
    for test in itemlist:
        totalinfo[test]['oslist'] = oslist
        infolist.append(totalinfo[test])
        datalist.append(totaldata[test])
    workbook = xlsxwriter.Workbook("result.xlsx")
    for info, data in zip(infolist, datalist):
        a = MkSinglesheet(workbook, info, data)
        a.addsheet()
    workbook.close()
