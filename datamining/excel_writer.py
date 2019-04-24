import xlwt


def write_excel(filename, sheetname, headers, data):
    book = xlwt.Workbook()
    work_sheet = book.add_sheet(sheetname)

    for cell, header in enumerate(headers):
        work_sheet.write(0, cell, header)

    for row, rowdata in enumerate(data):
        for cell, celldata in enumerate(rowdata):
            work_sheet.write(row+(1 if len(headers)>0 else 0), cell, celldata)

    book.save(filename)
    print("Saved excel", filename)