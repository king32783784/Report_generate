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
reload(sys)
sys.setdefaultencoding('utf8')
workbook = xlsxwriter.Workbook('chart.xlsx') #创建xlsx文件
worksheet1 = workbook.add_worksheet('处理器运算') #增加标签页
#　格式一“加粗、紫色填充、字体大小为10、宋体”
# 设置格式
charttitle_format = workbook.add_format({
    'bold': False, #设置加粗
    'border': 1, #设置边框格式
    'fg_color': '#CC99FF',  #设置单元格填充颜色
    'font_size': 10,   #设置字体大小
    'align': 'center', #设置对齐方式
    'valign': 'vcenter', #设置对齐方式
})

#format1.set_shrink() #缩小字体适应单元格
#worksheet.set_row(0, 45) #设置单元格长度
# Create a new Chart object.


#设置单元格大小
#setrow_format = workbook.add_format({'bold': True})
#worksheet.set_row(1, 45, setrow_format)

#title 格式， 合并单元格
title_format = workbook.add_format({
    'bold':     True,
    'border':   1,
    'font_size': 14,
    'font_color': '#FFFF99',
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#333399',
})
#测试信息格式
info_format = workbook.add_format({
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': '#B8CCE4',
})
#worksheet.merge_range('B3:D4', 'Merged Cells', merge_format)
ltitle_format = workbook.add_format({
    'bold': True,
    'border': 1,
    'font_size': 12,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': '#339966',
})

#测试结果数值格式
result_format = workbook.add_format({
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'center',
    'valign': 'vcenter',
})
#ITEM名称格式
item_format = workbook.add_format({
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': '#CCFFFF',
})

# Write some data to add to plot on the chart.
data = [
    ["OS", "isoft_desktop 4.0", "fedora23", "deepin", "neokylin"],
    ["type1", 1, 2, 3, 4],
    ["type2", 2, 4, 6, 8],
    ["type3", 3, 6, 9, 12],
    ["type4", 4, 8, 12, 16],
    ["type5", 5, 10, 15, 2000],
]
#第1行写入“处理器运算性能结果”ｔｉｔｌｅ
worksheet1.merge_range('A1:E1', "处理器运算性能", title_format)
worksheet1.set_row(0, 45)
#第2-5行写入“测试工具名称”
worksheet1.merge_range('A2:E2', "测试工具：SPEC CPU 2000", info_format)
worksheet1.merge_range('A3:E3',"性能指标： Spec2000 包括 SPECint2000、SPECfp2000、SPECint_rate2000、 SPECfp_rate2000 4个测试项", info_format)
worksheet1.merge_range('A4:E4', "对比说明：其中的得分越大说明CPU性能越高", info_format)
worksheet1.merge_range('A5:E5', "测试参数： runspec -c test.cfg -i ref -n 3 -r -u 4 -I all; runspec -c test.cfg -i ref -n 3 -I all", info_format)
for i in range(1,5):
    worksheet1.set_row(i,21)
#第７行写入副标题
worksheet1.merge_range('A7:E7', "SPEC2000 测试数据", ltitle_format)
for i in range(7,11): 
    worksheet1.set_row(i, 24)
#第30行写入“结果分析”
worksheet1.merge_range('A30:E30', "结果分析", ltitle_format)
#第８行+'n'行为测试数据表格（n为对比os数量,此处３个为例）
#data 为原始数据
data = [
    ["ITEM", "SPECint2000", "SPECfp2000", "SPECint_rate2000", "SPECfp_rate2000"],
    ["isoft_desktop V4.0 loongson", "Deepin15_mips_20160520", "Neokylin Desktop-7.0-loongson"],
    [611.00, 775.00, 776.00, 777.00],
    [608.00, 776.00, 777.00, 778.00],
    [610.00, 777.00, 778.00, 779.00],
]
worksheet1.write_row('A8', data[0], charttitle_format)
worksheet1.set_column(0, 0, 22) #设置单元格宽度
worksheet1.set_column(1, 6, 18) #设置单元格宽度
worksheet1.write_column('A9', data[1], item_format)
worksheet1.write_row('B9', data[2], result_format)
worksheet1.write_row('B10', data[3], result_format) 
worksheet1.write_row('B11', data[4], result_format)
# Configure the charts. In simplest case we just add some data series.
# 增加图表
chart = workbook.add_chart({'type': 'column'})
#制作表格
chart.add_series({
    'name' : '=处理器运算!$A$9', #系列名称
    'categories': '=处理器运算!$B$8:$E$8', #对比项目名称
    'values': '=处理器运算!$B$9:$E$9', 
    'gap': 200,
})
chart.add_series({
    'name' : '=处理器运算!$A$10',
    'values': '=处理器运算!$B$10:$E$10'
})
chart.add_series({
    'name' : '=处理器运算!$A$11',
    'values': '=处理器运算!$B$11:$E$11'
})
chart.set_size({'width': 680, 'height': 320})
chart.set_x_axis({
    'position_axis': 'between',
})
chart.set_title({'name': 'Spec2000'})
# 增加图形下方表格
#cahart.set_table()
# Insert the chart into the worksheet.
worksheet1.insert_chart('A13', chart)
#workbook.add_chart({'type': 'bar', 'subtype': 'stacked'})
workbook.close()
