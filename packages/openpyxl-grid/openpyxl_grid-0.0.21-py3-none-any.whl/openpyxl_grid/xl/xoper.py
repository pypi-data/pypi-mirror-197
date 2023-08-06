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
import null
import types
from datetime import *
from openpyxl_grid.xl.xlocation import XLocation
from openpyxl_grid.xl.xlocation import LType


class VType:
    """
    The value type of attrs or opers defined in a Grid object.
    """
    none = 0
    num = 1
    dateTime = 2
    str = 3

    @staticmethod
    def get_type(v):
        if (type(v) == int or type(v) == float):
            return VType.num
        elif (type(v) == datetime or type(v) == date or type(v) == time):
            return VType.dateTime
        else:
            return VType.str


class OType:
    """
    The operation type of type operation for add to a Grid object.
    """
    none = 0
    plus = 1
    minus = 2
    multipy = 3
    divide = 4
    max = 5
    min = 6
    maxIf = 7
    minIf = 8
    indexOf = 9
    equal = 10
    upper = 11
    lower = 12
    length = 13
    replace = 14
    day = 15
    hour = 16
    minute = 17
    month = 18
    second = 19
    weekday = 20
    weeknum = 21
    year = 22
    sqrt = 23
    mod = 24
    avg = 25
    sumIf = 26
    avgIf = 27
    addDays = 28
    isNull = 29

    @staticmethod
    def is_array_oper(o):
        arr = [OType.maxIf, OType.minIf]
        return True if o in arr else False

    @staticmethod
    def is_parentheses(o):
        parentheses = [OType.plus, OType.minus, OType.multipy, OType.divide]
        return True if o in parentheses else False

    @staticmethod
    def is_qualified(v_type, o_type):
        num_dis = [OType.indexOf, OType.upper, OType.lower, OType.day, OType.hour, OType.minute
                   , OType.month, OType.second, OType.weekday, OType.weeknum, OType.year
                   , OType.addDays]
        date_dis = [OType.plus, OType.multipy, OType.divide, OType.indexOf, OType.upper, OType.lower
                    , OType.sqrt, OType.mod, OType.avg, OType.sumIf, OType.avgIf, OType.length]
        str_dis = [OType.minus, OType.multipy, OType.divide, OType.max, OType.min, OType.maxIf
                   , OType.minIf, OType.day, OType.hour, OType.minute, OType.month, OType.second
                   , OType.weekday, OType.weeknum, OType.year, OType.sqrt, OType.mod, OType.avg
                   , OType.sumIf, OType.avgIf, OType.addDays]
        if (v_type == VType.num and o_type not in num_dis):
            return o_type
        elif (v_type == VType.dateTime and o_type not in date_dis):
            return o_type
        elif (v_type == VType.str and o_type not in str_dis):
            return o_type
        else:
            return OType.none




    

class XOperation:
    oper = null
    func_name = null
    split = null
    range_func = null
    ignore_err = True
    oType = OType.none
    vType = VType.none
    isSub = False

    def __init__(self, v_type, o_type=OType.none, func_name=null, split=null, verbs=[], custom_oper=null, range_func=null, ignore_err=True, is_sub=False):
        self.oType = o_type
        self.vType = v_type
        self.isSub = is_sub
        self.func_name = func_name
        self.split = split
        self.range_func = range_func
        self.ignore_err = ignore_err
        if (v_type == VType.num):
            self.oper = OperNum(verbs=verbs, custom_oper=custom_oper)
        elif (v_type == VType.str):
            self.oper = OperStr(verbs=verbs, custom_oper=custom_oper)
        elif (v_type == VType.dateTime):
            self.oper = OperDate(verbs=verbs, custom_oper=custom_oper)

    def set_o_row_increment(self, i, is_inner_sheet, col_shift=0):
        for v in self.oper.verbs:
            if (type(v) == XLocation):
                v.is_inner_sheet(is_inner_sheet)
                v.colShift = col_shift
                v.set_row_increment(i)
            elif (type(v) == XOperation):
                v.set_o_row_increment(i, is_inner_sheet)

    def to_str(self):
        s = null
        if (self.oper.customOper != null):
            s = self.oper.get_custom_oper()
        elif (OType.is_qualified(self.vType, self.oType) == OType.plus):
            s = self.oper.get_plus()
        elif (OType.is_qualified(self.vType, self.oType) == OType.minus):
            s = self.oper.get_minus()
        elif (OType.is_qualified(self.vType, self.oType) == OType.divide):
            s = self.oper.get_divide()
        elif (OType.is_qualified(self.vType, self.oType) == OType.multipy):
            s = self.oper.get_multipy()
        elif (OType.is_qualified(self.vType, self.oType) == OType.max):
            s = self.oper.get_max()
        elif (OType.is_qualified(self.vType, self.oType) == OType.min):
            s = self.oper.get_min()
        elif (OType.is_qualified(self.vType, self.oType) == OType.maxIf):
            s = self.oper.get_max_if()
        elif (OType.is_qualified(self.vType, self.oType) == OType.minIf):
            s = self.oper.get_min_if()
        elif (OType.is_qualified(self.vType, self.oType) == OType.indexOf):
            s = self.oper.get_index_of()
        elif (OType.is_qualified(self.vType, self.oType) == OType.equal):
            s = self.oper.get_equal()
        elif (OType.is_qualified(self.vType, self.oType) == OType.upper):
            s = self.oper.get_upper()
        elif (OType.is_qualified(self.vType, self.oType) == OType.lower):
            s = self.oper.get_lower()
        elif (OType.is_qualified(self.vType, self.oType) == OType.length):
            s = self.oper.get_length()
        elif (OType.is_qualified(self.vType, self.oType) == OType.replace):
            s = self.oper.get_replace()
        elif (OType.is_qualified(self.vType, self.oType) == OType.day):
            s = self.oper.get_day()
        elif (OType.is_qualified(self.vType, self.oType) == OType.hour):
            s = self.oper.get_hour()
        elif (OType.is_qualified(self.vType, self.oType) == OType.minute):
            s = self.oper.get_minute()
        elif (OType.is_qualified(self.vType, self.oType) == OType.month):
            s = self.oper.get_month()
        elif (OType.is_qualified(self.vType, self.oType) == OType.second):
            s = self.oper.get_second()
        elif (OType.is_qualified(self.vType, self.oType) == OType.weekday):
            s = self.oper.get_weekday()
        elif (OType.is_qualified(self.vType, self.oType) == OType.weeknum):
            s = self.oper.get_weeknum()
        elif (OType.is_qualified(self.vType, self.oType) == OType.year):
            s = self.oper.get_year()
        elif (OType.is_qualified(self.vType, self.oType) == OType.sqrt):
            s = self.oper.get_sqrt()
        elif (OType.is_qualified(self.vType, self.oType) == OType.mod):
            s = self.oper.get_mod()
        elif (OType.is_qualified(self.vType, self.oType) == OType.avg):
            s = self.oper.get_avg()
        elif (OType.is_qualified(self.vType, self.oType) == OType.sumIf):
            s = self.oper.get_sum_if()
        elif (OType.is_qualified(self.vType, self.oType) == OType.avgIf):
            s = self.oper.get_avg_if()
        elif (OType.is_qualified(self.vType, self.oType) == OType.addDays):
            s = self.oper.get_add_days()
        elif (OType.is_qualified(self.vType, self.oType) == OType.isNull):
            s = self.oper.get_is_null()
        elif(self.func_name != null and self.split != null):
            s = self.oper.get_oper(func_name=self.func_name, split=self.split
                                   , range_func=self.range_func, ignore_err=self.ignore_err)
        else:
            try:
                print(self.vType, self.oType)
                raise RuntimeError('oper does not exists')
            except RuntimeError as e:
                raise e
        return '({0})'.format(s) if self.isSub and OType.is_parentheses(self.oType) else s


class BaseOper:
    customOper = null
    verbs = []

    def __init__(self, verbs=[], custom_oper=null):
        self.verbs = verbs
        self.customOper = custom_oper

    def __get_val(self, v, range_func=null):
        if (type(v) == XOperation):
            return v.to_str()
        elif (type(v) == XLocation):
            return '{0}({1})'.format(range_func, v.label) if range_func != null and v.lType == LType.range else v.label
        else:
            s = '"{0}"'.format(v) if type(v) in (str, datetime, date, time) else '{0}'.format(v)
            if (type(v) in (datetime, date, time)):
                s = 'DATEVALUE({0})'.format(s)
            return s

    def __get_oper(self, func_name, func_content, v_type, ignore_err=True):
        if (func_name != null):
            content = '{0}({1})'.format(func_name, func_content)
        else:
            content = func_content
        if (ignore_err == False):
            content = 'IFERROR({0},{1})'.format(content, 0) 
        return content

    def check_verbs(self, oper_name, count):
        try:
            if (len(self.verbs) != count):
                raise RuntimeError('The verbs count of {0} should be {1}'.format(oper_name, count))
        except RuntimeError as e:
            raise e

    def get_common_oper(self, v_type, func_name, split, range_func=null, ignore_err=True):
        s = null
        for v in self.verbs:
            if (s != null):
                s += split + self.__get_val(v=v, range_func=range_func)
            else:
                s = self.__get_val(v, range_func=range_func)
        return self.__get_oper(func_name=func_name, func_content=s, v_type=v_type, ignore_err=ignore_err)

    def get_custom_oper(self):
        verbs = []
        for v in self.verbs:
            verbs.append(self.__get_val(v))
        return self.customOper.format(*verbs)



class OperStr(BaseOper):

    def __init__(self, verbs=[], custom_oper=null):
        super().__init__(verbs, custom_oper=custom_oper)

    def get_oper(self, func_name, split=',', range_func=null, ignore_err=True):
        return self.get_common_oper(v_type=VType.str, func_name=func_name
                                    , split=split, range_func=range_func, ignore_err=ignore_err)

    def get_plus(self):
        return self.get_oper(func_name='CONCATENATE')

    def get_index_of(self):
        return self.get_oper(func_name="FIND", ignore_err=False)

    def get_equal(self):
        self.check_verbs("equal", 2)
        return self.get_oper(func_name="EXACT")

    def get_upper(self):
        self.check_verbs("upper", 1)
        return self.get_oper(func_name="UPPER")

    def get_lower(self):
        self.check_verbs("lower", 1)
        return self.get_oper(func_name="LOWER")

    def get_length(self):
        self.check_verbs("length", 1)
        return self.get_oper(func_name="LEN")

    def get_replace(self):
        self.check_verbs("replace", 3)
        return self.get_oper(func_name="SUBSTITUTE")

    def get_is_null(self):
        self.check_verbs("isNull", 1)
        return self.get_oper(func_name="ISBLANK")


class OperDate(BaseOper):

    def __init__(self, verbs=[], custom_oper=null):
        super().__init__(verbs, custom_oper=custom_oper)

    def get_oper(self, func_name, split=',', range_func=null, ignore_err=True):
        return self.get_common_oper(v_type=VType.dateTime, func_name=func_name
                                    , split=split, range_func=range_func, ignore_err=ignore_err)

    def get_add_days(self):
        self.check_verbs("addDays", 2)
        return self.get_oper(func_name=null, split='+')

    def get_minus(self):
        self.check_verbs("minus", 2)
        return self.get_oper(func_name=null, split='-')

    def get_equal(self):
        self.check_verbs("equal", 2)
        return self.get_oper(func_name=null, split='=')


    def get_replace(self):
        self.check_verbs("replace", 3)
        return self.get_oper(func_name="SUBSTITUTE")

    def get_max(self):
        return self.get_oper(func_name='MAX')

    def get_min(self):
        return self.get_oper(func_name='MIN')

    def get_max_if(self):
        self.check_verbs("maxIf", 3)
        self.customOper = 'MAX(IF({0}={1}, {2}))'
        return self.get_custom_oper()

    def get_min_if(self):
        self.check_verbs("minIf", 3)
        self.customOper = 'MIN(IF({0}={1}, {2}))'
        return self.get_custom_oper()

    def get_day(self):
        self.check_verbs("day", 1)
        return self.get_oper(func_name="DAY")

    def get_hour(self):
        self.check_verbs("hour", 1)
        return self.get_oper(func_name="HOUR")

    def get_minute(self):
        self.check_verbs("minute", 1)
        return self.get_oper(func_name="MINUTE")

    def get_month(self):
        self.check_verbs("month", 1)
        return self.get_oper(func_name="MONTH")

    def get_second(self):
        self.check_verbs("second", 1)
        return self.get_oper(func_name="SECOND")

    def get_weekday(self):
        self.check_verbs("weekday", 1)
        return self.get_oper(func_name="WEEKDAY")

    def get_weeknum(self):
        self.check_verbs("weeknum", 1)
        return self.get_oper(func_name="WEEKNUM")

    def get_year(self):
        self.check_verbs("year", 1)
        return self.get_oper(func_name="YEAR")

    def get_is_null(self):
        self.check_verbs("isNull", 1)
        return self.get_oper(func_name="ISBLANK")



class OperNum(BaseOper):

    def __init__(self, verbs=[], custom_oper=null):
        super().__init__(verbs, custom_oper=custom_oper)

    def get_oper(self, func_name, split=',', range_func=null, ignore_err=True):
        return self.get_common_oper(v_type=VType.num, func_name=func_name
                                    , split=split, range_func=range_func, ignore_err=ignore_err)

    def get_plus(self):
        return self.get_oper(func_name=null, split='+', range_func='SUM')

    def get_minus(self):
        return self.get_oper(func_name=null, split='-')

    def get_divide(self):
        return self.get_oper(func_name=null, split='/')

    def get_multipy(self):
        return self.get_oper(func_name=null, split='*')

    def get_mod(self):
        self.check_verbs("mod", 2)
        return self.get_oper(func_name='MOD')

    def get_sqrt(self):
        self.check_verbs("sqrt", 1)
        return self.get_oper(func_name="SQRT")

    def get_equal(self):
        self.check_verbs("equal", 2)
        return self.get_oper(func_name=null, split='=')

    def get_length(self):
        self.check_verbs("length", 1)
        return self.get_oper(func_name="LEN")

    def get_replace(self):
        self.check_verbs("replace", 3)
        return self.get_oper(func_name="SUBSTITUTE")

    def get_max(self):
        return self.get_oper(func_name='MAX')

    def get_min(self):
        return self.get_oper(func_name='MIN')

    def get_avg(self):
        return self.get_oper(func_name='AVERAGE')

    def get_max_if(self):
        self.check_verbs("maxIf", 3)
        self.customOper = 'MAX(IF({0}={1}, {2}))'
        return self.get_custom_oper()

    def get_min_if(self):
        self.check_verbs("minIf", 3)
        self.customOper = 'MIN(IF({0}={1}, {2}))'
        return self.get_custom_oper()

    def get_sum_if(self):
        self.check_verbs("sumIf", 3)
        self.customOper = 'SUMIF({0}, {1}, {2})'
        return self.get_custom_oper()

    def get_avg_if(self):
        self.check_verbs("avgIf", 3)
        self.customOper = 'AVERAGEIF({0}, {1}, {2})'
        return self.get_custom_oper()

    def get_is_null(self):
        self.check_verbs("isNull", 1)
        return self.get_oper(func_name="ISBLANK")
