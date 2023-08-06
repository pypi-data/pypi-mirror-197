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

"""
The grid is the container of Grid object.
"""

import null as null

from openpyxl_grid.xl.xlocation import XLocation
from openpyxl_grid.xl.xoper import VType
from openpyxl_grid.xl.xoper import OType
from openpyxl_grid.xl.xgrid import XParam
from openpyxl_grid.xl.xgrid import XGrid
from openpyxl_grid.xl.xoper import XOperation

from openpyxl_grid.xl.xstyle import DefaultHeadFont
from openpyxl_grid.xl.xstyle import DefaultHeadFill
from openpyxl_grid.xl.xstyle import DefaultCellFont
from openpyxl_grid.xl.xstyle import DefaultBorder

class GAttr(XLocation):
    name = null
    vType = VType.none
    vals = []

    def __init__(self, name, vals=[], sheet_name=null, row=0, col=0):
        try:
            if (name == null):
                raise RuntimeError('attr name can not be null')
        except RuntimeError as e:
            raise e
        self.name = name
        if (len(vals) > 0):
            for v in vals:
                if (v != null):
                    self.vType = VType.get_type(v)
                    break
        try:
            for v in vals:
                if (v != null and VType.get_type(v) != self.vType):
                    raise RuntimeError('val list has different types')
        except RuntimeError as e:
            raise e
        self.vals = vals
        self.set_loc(row=row, col=col, sheet_name=sheet_name)

    def get_loc(self):
        return XLocation(sheet_name=self.sheetName, row=self.sRow, col=self.sCol, e_row=self.eRow, e_col=self.eCol)

    def to_x_param(self):
        return XParam(name=self.name, v_type=self.vType, o_type=OType.none, vals=self.vals)


class OA:
    """
    The object of OA which specified by name can be attr or oper in Grid object.
    And the params of type or custom oper in Grid object can be a OA object which is
    used to establish a relation with attr or oper in the Grid object.
    """
    name = null
    isCol = False

    def __init__(self, name, is_col=False):
        """
        Init OA object by name of attr or oper in a Grid object.
        :param name: name of attr or oper for specified
        :param is_col: If is_col is True, OA object will be the whole column link in the output Excel file.
                       And it will be corresponding cell link when is_col is set as default value of False.
        """
        self.name = name
        self.isCol = is_col

    def __find_attr(self, m_obj):
        for a in m_obj.attrs:
            if (a.name == self.name):
                return a
        return null

    def __find_oper(self, m_obj):
        for o in m_obj.opers:
            if (o.name == self.name):
                return o
        return null

    def get_verb(self, m_obj):
        l = null
        a = self.__find_attr(m_obj)
        if (a != null):
            l = a.get_loc()
            if (self.isCol):
                l.set_col()
            l.set_sheet_name(sheet_name=m_obj.get_g_sheet_name())
            return {'vt': a.vType, 'verb': l}
        o = self.__find_oper(m_obj)
        if (o != null):
            l = o.get_loc()
            l.set_col_shift(True)
            if (self.isCol):
                l.set_col()
            return {'vt': o.vType, 'verb': l}
        try:
            if (o == null):
                raise RuntimeError('verb {0} can not be null'.format(self.name))
        except RuntimeError as e:
            raise e


class TO(XOperation):
    """
    The TO object is a type operation for child recursion usage in a parent or child operation.
    """
    params = []

    def __init__(self, o_type, *params):
        """
        To init TO object by OType and params
        :param o_type: Operation type which defined as OType
        :param params: The params can be a set of object as:
                        1.'OA' object which specified by name of attrs or opers has set in the grid;
                        2.'TO' object which type operation of child recursion in parent opers;
                        3.'CO' object which custom operation of child recursion in parent opers;
                        4. The value of int, float, string or datetime object.
        """
        self.oType = o_type
        self.params = params

    def get_oper(self, m_obj):
        d = Grid.get_oper_verbs(m_obj=m_obj, params=self.params)
        if (d != null):
            return XOperation(v_type=d.get('vt'), o_type=self.oType, verbs=d.get('verbs'), is_sub=True)
        return null


class CO(XOperation):
    """
    The CO object is a custom operation for child recursion usage in a parent or child operation.
    """
    params = []
    customOper = null

    def __init__(self, custom_oper, v_type, *params):
        """
        To init CO object by custom oper string, value type and params.
        :param custom_oper: A format string of function for write into Excel file filled with params.
        :param v_type: The value type of custom operation as VType of num, str or dateTime.
        :param params: The params can be a set of object as:
                        1.'OA' object which specified by name of attrs or opers has set in the grid;
                        2.'TO' object which type operation of child recursion in parent opers;
                        3.'CO' object which custom operation of child recursion in parent opers;
                        4. The value of int, float, string or datetime object.
        """
        try:
            if (custom_oper == null):
                raise RuntimeError('custom oper can not be null')
        except RuntimeError as e:
            raise e
        self.customOper = custom_oper
        self.params = params
        self.vType = v_type

    def get_oper(self, m_obj):
        d = Grid.get_oper_verbs(m_obj=m_obj, params=self.params)
        if (d != null):
            return XOperation(v_type=self.vType, custom_oper=self.customOper, verbs=d.get('verbs'), is_sub=True)
        return null


class Grid(XGrid):
    """
    Represents a object to add attrs and opers to generate grid to Excel file.
    """
    attrs = []
    opers = []

    def __init__(self, name, **attrs):
        """
        Init Grid with name and attrs.
        :param name: The name of grid which will be the sheet name when write grid to Excel file.
        :param attrs: A dict variable which key will be the column name in Excel file at the first row
                    , value is a list which each element in it will write into Excel file in rows below name.
        """
        super().__init__(name)
        self.add_attrs(**attrs)

    def __add_attr(self, name, val):
        if (type(val) != list):
            self.attrs.append(GAttr(name=name, vals=[val], row=1, col=len(self.attrs) + 1))
            rows = 1
        else:
            self.attrs.append(GAttr(name=name, vals=val, row=1, col=len(self.attrs) + 1))
            rows = len(val)
        if (rows > self.rows):
            self.rows = rows

    def __write_oper_grid(self, file_name, head_font=DefaultHeadFont, head_fill=DefaultHeadFill
                          , cell_font=DefaultCellFont, border=DefaultBorder):
        self.clear_params()
        for p in self.opers:
            self.append_param(p)
        self.write_xl(file_name=file_name, sheet_name=self.get_oper_g_sheet_name(), head_font=head_font
                      , head_fill=head_fill, cell_font=cell_font, border=border)

    def get_g_sheet_name(self):
        return self.name

    def get_oper_g_sheet_name(self):
        return '{0}_oper'.format(self.name)

    @staticmethod
    def get_oper_verbs(m_obj, params):
        verbs = []
        vt = VType.none
        for p in params:
            if (type(p) == OA):
                vd = p.get_verb(m_obj=m_obj)
                verbs.append(vd['verb'])
                if (vt == VType.none):
                    vt = vd['vt']
            elif (type(p) in (TO, CO)):
                xo = p.get_oper(m_obj)
                if (xo != null):
                    verbs.append(xo)
                    if (vt == VType.none):
                        vt = xo.vType
            else:
                verbs.append(p)
                if (vt == VType.none):
                    vt = VType.get_type(p)  
        try:
            if (vt != VType.none and len(verbs) > 0):
                return dict(vt=vt, verbs=verbs)
            else:
                raise RuntimeError('verbs can not be null')
        except RuntimeError as e:
            raise e

    def add_attrs(self, **attrs):
        """
        Add attrs to grid after init.
        :param attrs: A dict variable which key will be the column name in Excel file at the first row
                    , value is a list which each element in it will write into Excel file in rows below name.
        :return:
        """
        for key, value in attrs.items():
            self.__add_attr(key, value)


    def attrs_from_dicts(self, dicts):
        """
        Cover attrs in Grid object by a list of dicts. After call the function, the old attrs will be cleared and
        replace by new attrs in dicts.
        :param dicts: Dicts to cover the attrs in Grid. The structure of the should like the example below:
                      dicts = [{ 'key1' = key1_value, 'key2' = key2_value, ..., 'key' = key_value },
                               { 'key1' = key1_value, 'key2' = key2_value, ..., 'key' = key_value },
                               ...
                               { 'key1' = key1_value, 'key2' = key2_value, ..., 'key' = key_value }]
        :return:
        """
        try:
            if (type(dicts) != list or len(dicts) == 0):
                raise RuntimeError('"dicts" is empty or not a list')
        except RuntimeError as e:
            raise e
        attrs = dict()
        keys = dicts[0].keys()
        for k in keys:
            attrs[k] = []
        for o in dicts:
            for k in keys:
                attrs[k].append(o[k])
        self.clear_params()
        self.add_attrs(**attrs)

    def add_oper(self, name, o_type, *params):
        """
        Add type operation to Grid, which will write into Excel file as function according to parameters.
        :param name: Name of operation, it is also the name of column at the first row in Excel file.
        :param o_type: Operation type which defined as OType
        :param params: The params can be a set of object as:
                        1.'OA' object which specified by name of attrs or opers has set in the grid;
                        2.'TO' object which type operation of child recursion in parent opers;
                        3.'CO' object which custom operation of child recursion in parent opers;
                        4. The value of int, float, string or datetime object.
        :return:
        """
        d = Grid.get_oper_verbs(self, params)
        self.opers.append(XParam(name=name, v_type=d.get('vt'), o_type=o_type
                                 , verbs=d.get('verbs'), row=1, col=len(self.opers) + 1))

    def add_custom_oper(self, name, custom_oper, v_type, *params):
        """
        Add custom operation to Grid, which will write into Excel file as function according to parameters
        :param name: Name of operation, it is also the name of column at the first row in Excel file.
        :param custom_oper: A format string of function for write into Excel file filled with params.
        :param v_type: The value type of custom operation as VType of num, str or dateTime.
        :param params: The params can be a set of object as:
                        1.'OA' object which specified by name of attrs or opers has set in the grid;
                        2.'TO' object which type operation of child recursion in parent opers;
                        3.'CO' object which custom operation of child recursion in parent opers;
                        4. The value of int, float, string or datetime object.
        :return:
        """
        try:
            if (custom_oper == null):
                raise RuntimeError('custom oper can not be null')
        except RuntimeError as e:
            raise e
        d = Grid.get_oper_verbs(self, params)
        self.opers.append(XParam(name=name, v_type=v_type, custom_oper=custom_oper
                                 , verbs=d.get('verbs'), row=1, col=len(self.opers) + 1))

    def write_attr_xl(self, file_name, head_font=DefaultHeadFont, head_fill=DefaultHeadFill
                      , cell_font=DefaultCellFont, border=DefaultBorder):
        """
        To write attrs in the Grid object into Excel file. The keys of attrs will be written in the fist row
        column by column, and the values of attrs will be written row by row after fist row.
        :param file_name: The name of output Excel file.
        :param head_font: To change font style of the first line in Excel file, it is an openpyxl.styles.Font object.
        :param head_fill: To change fill style of the first line in Excel file, it is an openpyxl.styles.Fill object.
        :param cell_font: To change font style in lines except first line in Excel file, it is an openpyxl.styles.Font object.
        :param border: To change border style of the grid in Excel file, it is an openpyxl.style.Border object.
        :return:
        """
        self.clear_params()
        for a in self.attrs:
            self.append_param(a.to_x_param())
        self.write_xl(file_name=file_name, sheet_name=self.get_g_sheet_name(), head_font=head_font, head_fill=head_fill
                      , cell_font=cell_font, border=border)

    def write_separate_xl(self, file_name, head_font=DefaultHeadFont, head_fill=DefaultHeadFill
                          , cell_font=DefaultCellFont, border=DefaultBorder):
        """
        To write attrs and opers in the Grid object into Excel file in different sheet.
        The keys of attrs or opers will be written in the fist row column by column
        , and the values of attrs or opers will be written row by row after fist row.
        :param file_name: The name of output Excel file.
        :param head_font: To change font style of the first line in Excel file, it is an openpyxl.styles.Font object.
        :param head_fill: To change fill style of the first line in Excel file, it is an openpyxl.styles.Fill object.
        :param cell_font: To change font style in lines except first line in Excel file, it is an openpyxl.styles.Font object.
        :param border: To change border style of the grid in Excel file, it is an openpyxl.style.Border object.
        :return:
        """
        self.write_attr_xl(file_name, head_font=head_font, head_fill=head_fill, cell_font=cell_font, border=border)
        self.__write_oper_grid(file_name, head_font=head_font, head_fill=head_fill, cell_font=cell_font, border=border)

    def write_together_xl(self, file_name, head_font=DefaultHeadFont, head_fill=DefaultHeadFill
                          , cell_font=DefaultCellFont, border=DefaultBorder):
        """
        To write attrs and opers in the Grid object into Excel file in same sheet.
        The keys of attrs or opers will be written in the fist row column by column
        , and the values of attrs or opers will be written row by row after fist row.
        :param file_name: The name of output Excel file.
        :param head_font: To change font style of the first line in Excel file, it is an openpyxl.styles.Font object.
        :param head_fill: To change fill style of the first line in Excel file, it is an openpyxl.styles.Fill object.
        :param cell_font: To change font style in lines except first line in Excel file, it is an openpyxl.styles.Font object.
        :param border: To change border style of the grid in Excel file, it is an openpyxl.style.Border object.
        :return:
        """
        self.clear_params()
        for a in self.attrs:
            self.append_param(a.to_x_param())
        col = 1
        for p in self.opers:
            self.append_param(p)
        self.write_xl(file_name=file_name, sheet_name=self.get_g_sheet_name(), is_inner_sheet=True
                      , col_shift=len(self.attrs), head_font=head_font, head_fill=head_fill, cell_font=cell_font
                      , border=border)
