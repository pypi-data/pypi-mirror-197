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
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font



DefaultBorder = Border(left=Side(border_style=None, color='FF000000')
                , right=Side(border_style=None, color='FF000000')
                , top=Side(border_style=None, color='FF000000')
                , bottom=Side(border_style=None, color='FF000000')
                , diagonal=Side(border_style=None, color='FF000000')
                , diagonal_direction=0
                , outline=Side(border_style=None, color='FF000000')
                , vertical=Side(border_style=None, color='FF000000')
                , horizontal=Side(border_style=None, color='FF000000'))




DefaultHeadFont = Font(name='Arial', size=12, bold=True, italic=False, vertAlign=None
                       , underline='none', strike=False, color='00FFFFFF')

DefaultHeadFill = PatternFill(fill_type='solid', bgColor='003366FF')

DefaultCellFont = Font(name='Arial', size=11, bold=False, italic=False, vertAlign=None
                       , underline='none', strike=False, )

