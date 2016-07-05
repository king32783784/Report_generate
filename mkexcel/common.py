#/usr/bin/env python
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

#xls_dirt字典保存基础信息
sheet_cpu = {
    'sheetname':'处理器运算',
    'testinfo' : ("处理器运算性能", "测试工具：SPEC CPU 2000",\
        "性能指标： Spec2000 包括 SPECint2000、SPECfp2000、SPECint_rate2000、 SPECfp_rate2000 4个测试项",
        "对比说明：其中的得分越大说明CPU性能越高", 
        "测试参数： runspec -c test.cfg -i ref -n 3 -r -u 4 -I all; runspec -c test.cfg -i ref -n 3 -I all",
                   "SPEC2000 测试数据"),
    'basedata' : [
        ["ITEM", "SPECint2000", "SPECfp2000", "SPECint_rate2000", "SPECfp_rate2000"],
        ["isoft_desktop V4.0 loongson", "Deepin15_mips_20160520", "Neokylin Desktop-7.0-loongson"],
        [611.00, 775.00, 776.00, 777.00],
        [608.00, 776.00, 777.00, 778.00],
        [610.00, 777.00, 778.00, 779.00],
        [120.00, 124.00, 492.00, 340.00],
        [120.00, 124.00, 492.00, 340.00],
        ],
    'layout' : [
    ['A1:E1', 'A2:E2', 'A3:E3', 'A4:E4', 'A5:E5', 'A7:E7', 'A8', 'A9'],
    ['45', '21', '24']],
    'chart' : (730, 320, "Spec2000"),
}
sheet_lmbench_info = {
    'sheetname': '处理器运算',
    'testinfo': ("测试工具：lmbench", "性能指标：选取了Processor、Context switching、*Local* Communication latencies 、File & VM system latencies 、*Local* Communication bandwidths等指标", "对比说明：测试结果均为测试3次求平均值"),
    'oslist': ["isoft_desktop V4.0 loongson", "Deepin15_mips_20160520", "Neokylin Desktop-7.0-loongson"],
    }
sheet_lmbench_data1 = {
    'basedata': [
        ["ITEM", "null call", "null I/O", "stat", "open clos", "slct TCP", "sig inst", "sig hndl", "fork proc(k)", "exec porc(k)", "sh proc(k)"],
        [0.44, 0.70, 8.18, 12.26, 12.38, 0.80, 4.06, 0.42, 1.36, 4.46],
        [0.33, 0.67, 3.74, 7.24, 12.64, 1.04, 4.27, 0.39, 1.31, 5.24],
        [0.44, 0.68, 8.14, 13.10, 9.97, 0.82, 4.50, 0.43, 1.38, 4.29],
    ]
    }
       
    
#format_dirt字典保存格式化信息
#结果图表title格式
formtitle_format = {
    'bold': False, #设置加粗
    'border': 1, #设置边框格式
    'fg_color': '#CC99FF',  #设置单元格填充颜色
    'font_size': 10,   #设置字体大小
    'align': 'center', #设置对齐方式
    'valign': 'vcenter', #设置对齐方式
}

#页title格式
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

#测试结果数值格式
result_format = {
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'center',
    'valign': 'vcenter',
    'num_format': '0.00',
}

#测试项目名称格式
item_format = {
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': '#CCFFFF',
}


class mk_singleitem(object):
    def __init__(self, xls_dirt, xlsname):
        self.dirt = xls_dirt
        self.xlsname = xlsname
        self.workbook = self.mkxls()

    def mkxls(self):
        workbook = xlsxwriter.Workbook(self.xlsname)
        return workbook

    def addsheet(self):
        worksheet = self.workbook.add_worksheet(self.dirt['sheetname'])
        self.input_sheettitle(worksheet)
        self.input_testinfo(worksheet)
        self.input_formsubtitle(worksheet)
        self.input_formtitle(worksheet)
        self.input_formitem(worksheet)
        self.input_formdata(worksheet)
        self.setcellformat(worksheet)
        self.mk_chart(worksheet)
        self.workbookclose()

    def numbersystems(self):
        itemsnum = len(self.dirt['basedata'][0])
        seriesnum = len(self.dirt['basedata'][1])
        formnum = (itemsnum, seriesnum)
        return formnum

    def input_sheettitle(self, worksheet):
        format = self.workbook.add_format(sheettitle_format)
        worksheet.merge_range(self.dirt['layout'][0][0], self.dirt['testinfo'][0], format)
        
    def input_testinfo(self, worksheet):
        format = self.workbook.add_format(info_fortmat)
        worksheet.merge_range(self.dirt['layout'][0][1], self.dirt['testinfo'][1], format)
        worksheet.merge_range(self.dirt['layout'][0][2], self.dirt['testinfo'][2], format)
        worksheet.merge_range(self.dirt['layout'][0][3], self.dirt['testinfo'][3], format)
        worksheet.merge_range(self.dirt['layout'][0][4], self.dirt['testinfo'][4], format)
   
    def input_formsubtitle(self, worksheet):
        format = self.workbook.add_format(formsubtitle_format)
        worksheet.merge_range(self.dirt['layout'][0][5], self.dirt['testinfo'][5], format)

    def input_formtitle(self, worksheet):
        format = self.workbook.add_format(formtitle_format)
        worksheet.write_row(self.dirt['layout'][0][6], self.dirt['basedata'][0], format)

    def input_formitem(self, worksheet):
        format = self.workbook.add_format(item_format)
        worksheet.write_column(self.dirt['layout'][0][7], self.dirt['basedata'][1], format)

    def input_formdata(self, worksheet):
        format = self.workbook.add_format(result_format)
        formnum = self.numbersystems()
        lastline = 9 + formnum[1]
        for data, line in zip(self.dirt['basedata'][2:], range(9,lastline)):
            worksheet.write_row('B%s' % line, data, format)
 
    def setbandwith(self, data):
        length = 0
        for charter in data:
            if len(charter) > length:
                length = len(charter)
        return length

    def setcellformat(self, worksheet):
        formnum = self.numbersystems()
        firstrow = float(self.setbandwith(self.dirt['basedata'][1]) / 1.2)
        otherrow = float(self.setbandwith(self.dirt['basedata'][0]) * 1.2)
        rows = formnum[0]
        lines = formnum[1]
        lastline = 8 + lines
        worksheet.set_column(0, 0, firstrow)
        worksheet.set_column(1, rows+1, otherrow)
        worksheet.set_row(0, float(self.dirt['layout'][1][0]))
        for i in range(1, 5):
            worksheet.set_row(i, float(self.dirt['layout'][1][1]))
        for i in range(7, lastline):
            worksheet.set_row(i, float(self.dirt['layout'][1][2]))
    

    def mk_chart(self, worksheet):
        chart = self.workbook.add_chart({'type': 'column'})     
        formnum =self.numbersystems()
        seriesnum = formnum[1]
        itemsnum = formnum[0]
        columnnumber = string.uppercase[itemsnum] #E
        print formnum
        if seriesnum < 1:
            print(" There is no data ")
            exit()
        chart.add_series({
            'name' : '=%s!$A$9' % (worksheet.name) ,#系列名称
            'categories': '=%s!$B$8:$%s$8' % (worksheet.name, columnnumber), #对比项目名称
            'values': '=%s!$B$9:$%s$9' % (worksheet.name, columnnumber),
            'gap': 200,
            })
        for i, osname in enumerate(self.dirt['basedata'][1][1:]):
            chart.add_series({
                'name' : '=%s!$A$%s' % (worksheet.name, i+10),
                'values': '=%s!$B$%s:$%s$%s' % (worksheet.name, i+10, columnnumber, i+10)
            })
        chart_width = self.dirt['chart'][0]
        chart_height = self.dirt['chart'][1]
        chart.set_size({'width': chart_width, 'height': chart_height})
        chart.set_x_axis({
            'position_axis': 'between',
        })
        chart_titlename = self.dirt['chart'][2]
        chart.set_title({'name': chart_titlename})
        chart_insert_site = 'A%s' % int(10+seriesnum)
        worksheet.insert_chart(chart_insert_site, chart)

    def workbookclose(self):
        self.workbook.close()


a = mk_singleitem(sheet_cpu, 'test.xlsx')
a.addsheet()
