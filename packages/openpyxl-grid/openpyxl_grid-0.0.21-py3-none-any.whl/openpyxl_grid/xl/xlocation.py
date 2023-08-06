"""
MIT License

Copyright (c) 2023 Jianai Wang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import null as null
from openpyxl.utils import get_column_letter


class LType:
    single = 0
    range = 1
    col = 2
    row = 3


class XLocation:
    sheetName = null
    sRow = 1
    sCol = 1
    eRow = 1
    eCol = 1
    label = null
    lType = LType.single
    innerSheet = False
    isColShift = False
    colShift = 0

    def __init__(self, row, col, sheet_name=null, inner_sheet=False, e_row=0, e_col=0):
        self.is_inner_sheet(inner_sheet)
        self.set_loc(row, col, sheet_name, e_row, e_col)

    def __get_row_label(self, r):
        return '{0}'.format(r if r > 0 else '')

    def __get_col_label(self, c):
        return '{0}'.format(get_column_letter(c) if c > 0 else '')

    def __set_Col_Row(self, l_type):
        try:
            if (l_type in (LType.col, LType.row)):
                self.lType = l_type
                self.relabel()
            else:
                raise RuntimeError('must set to col or row')
        except RuntimeError as e:
            raise e

    def set_col(self):
        self.__set_Col_Row(LType.col)


    def set_col_shift(self, is_shift):
        self.isColShift = is_shift

    def set_loc(self, row, col, sheet_name=null, e_row=0, e_col=0):
        if (row > 0 or col > 0):
            self.sheetName = sheet_name
            self.sRow = row
            self.sCol = col
            self.eRow = e_row if e_row > 0 else self.sRow
            self.eCol = e_col if e_col > 0 else self.sCol
            self.relabel()

    def set_sheet_name(self, sheet_name=null):
        self.sheetName = sheet_name
        self.relabel()

    def is_inner_sheet(self, inner_sheet=False):
        self.innerSheet = inner_sheet

    def relabel(self):
        s_col = self.sCol + self.colShift if self.isColShift else self.sCol
        e_col = self.eCol + self.colShift if self.isColShift else self.eCol
        if (self.lType not in (LType.col, LType.row)):
            self.label = "{0}{1}".format(self.__get_col_label(s_col), self.__get_row_label(self.sRow))
            if (self.sRow != self.eRow or s_col != e_col):
                self.label += ":{0}{1}".format(self.__get_col_label(e_col), self.__get_row_label(self.eRow))
                self.lType = LType.range
            else:
                self.lType = LType.single
        elif (self.lType == LType.col):
            self.label = '{0}:{1}'.format(self.__get_col_label(s_col), self.__get_col_label(s_col))
        elif (self.lType == LType.row):
            self.label = '{0}:{1}'.format(self.__get_row_label(self.sRow), self.__get_row_label(self.sRow))

        if (self.sheetName != null and self.innerSheet == False):
            self.label = '{0}!{1}'.format(self.sheetName, self.label)

    def set_row_increment(self, i):
        if(self.sRow + i > 0):
            self.sRow += i
        else:
            self.sRow = 1
        if(self.eRow + i > 0):
            self.eRow += i
        else:
            self.eRow = 1
        self.relabel()

