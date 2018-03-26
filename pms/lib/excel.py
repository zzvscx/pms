# -*- coding: utf-8 -*-


import xlsxwriter

from cStringIO import StringIO
from xlwt import Workbook, easyxf

def generate_xls(name, data):

    book = Workbook(encoding='utf-8')
    sheet1 = book.add_sheet(name)
    max_col = [0,0,0,0,0,0]
    merge_format = book.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter'})

    def adjust_col_width():
        for x in xrange(len(max_col)):
            if max_col[x] > 0:
                sheet1.col(x).width = min(256*(max_col[x] + 4), 65535/3)

    def row_write(r, msg):
        row1 = sheet1.row(r)
        if len(msg) > len(max_col):
            max_col.extend([0 for x in xrange(len(msg) - len(max_col))])
        for x in xrange(len(msg)):
            if msg[x]:
                row1.write(x, msg[x], easyxf('align: vertical center'))
                max_col[x] = max(max([len(i) for i in str(msg[x]).split("\n")]), max_col[x])
        return r + 1

    def write_title(msg):
        sheet1.merge_range(0, 0, 0, 5, msg,
                easyxf(
                    'align: vertical center, horizontal center;', 
                        ))
        sheet1.row(0).height_mismatch = True
        sheet1.row(0).height = 37*16
        return 1


    def write_label(r, label):
        return row_write(r, label)

    r = 0
    r = write_label(r, data[0])
    for x in data[1:]:
        r = row_write(r, x)
    adjust_col_width()
    temp = StringIO()
    book.save(temp)
    return temp.getvalue()

def generate_xls_multisheet(data):

    temp = StringIO()
    book = xlsxwriter.Workbook(temp)
    max_col = [0,0,0,0,0,0]

    merge_format = book.add_format({'align': 'center','valign': 'vcenter'})

    def adjust_col_width():
        for x in xrange(len(max_col)):
            if max_col[x] > 0:
                sheet1.col(x).width = min(256*(max_col[x] + 4), 65535/3)

    def row_write(worksheet, r, msg):
        #row1 = sheet1.row(r)
        if len(msg) > len(max_col):
            max_col.extend([0 for x in xrange(len(msg) - len(max_col))])
        for x in xrange(len(msg)):
            if msg[x]:
                #if isinstance(msg[x], int) or isinstance(msg[x], float):
                    #worksheet.write_number(r, x, msg[x])
                #else:
                worksheet.write(r, x, msg[x])
                max_col[x] = max(max([len(i) for i in str(msg[x]).split("\n")]), max_col[x])
        return r + 1

    def write_title(sheet1, msg):
        sheet1.merge_range(0, 0, 0, 5, msg, merge_format)
        #sheet1.row(0).height_mismatch = True
        #sheet1.row(0).height = 37*16
        return 1


    def write_label(worksheet, r, label):
        return row_write(worksheet, r, label)

    #sheet_length = 10
    #for index, sheet in enumerate(data):
        #num = len(sheet['data']) / sheet_length
        #if len(sheet['data']) > 10:
            #data[index] = {'name': sheet['name'], 'data': sheet['data'][:10]}
            #data.append({'name': sheet['name'], 'data': sheet['data'][10:]}
#)
    for sheet in data:
        sheet1 = book.add_worksheet(sheet['name'])
        title = sheet.get('title')
        if title:
            r = write_title(sheet1, title)
        else:
            r = 0
        r = write_label(sheet1, r, sheet['data'][0])
        for x in sheet['data'][1:]:
            r = row_write(sheet1, r, x)
        #adjust_col_width()
    #book.save(temp)
    book.close()
    return temp.getvalue()
