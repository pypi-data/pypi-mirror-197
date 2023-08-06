# Openpyxl Grid

This project aims to build a python module based on Openpyxl for writing datas and functions into Excel file as a grid.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

The tool of pip can be used to install this project module on local machine for development.

### Prerequisites

The minimal requirement to use this module is python3.7. The python3.7+ must be installed at first.

### Installing

The command to install the module of this project on a Unix liked system, such as Linux or macOS:

```unix
python3 -m pip install openpyxl-grid
```

The command to install on a Windows system as below:

```windows
py -m pip install openpyxl-grid
```

## Running the tests

There is a simple guide of how to use the module in a python file in this section. 
And an example python file named example_stock.py for test purpose is list in the project directory of test.

### Example code for test

The example code below show you how to use the module in a python file:

```python
from openpyxl_grid import Grid, OType, VType, OA, TO, CO
"""
Grid: The Grid object stored attrs and opers for writing into a Excel file.
OType: The Definition of Operation Type for opers added to Grid.
VType: The Value Type for Specified in Custom Operation.
OA: params linked to attrs and opers has added into a Grid object in the function of add opers in a Grid object.
TO: Sub Type Operation object for adding as params.
CO: Sub Custom Operation object for adding as params.
"""

# Init attr objects for Grid
a1 = [1, 2, 3, 4]
a2 = [4, 5, 6]
a3 = [7, 8, 9]
a4 = ['abc', 'bcd', 'cde']
a5 = ['def', 'efg', 'fgh']

# Init Grid object for test
g = Grid('test', a1=a1, a3=a3)

# append attrs to Grid object
g.add_attrs(a2=a2, a4=a4, a5=a5)

# add Type Operation to Grid object
g.add_oper('max_a', OType.max, OA('a1'), OA('a2'))
g.add_oper('con', OType.plus, OA('a4'), OA('a5'))
g.add_oper('sum_a', OType.plus, OA('a1'), OA('a2'), OA('a3'))
g.add_oper('a1+a2+a3', OType.plus, OA('a1'), OA('a2'), OA('a3'), 3)
g.add_oper('a1-a2-a3', OType.minus, OA('a1'), OA('a2'), OA('a3'), 3)

# add Type Operation including sub operation to Grid object
g.add_oper('a1+(a2-a3)', OType.plus, OA('a1'), TO(OType.minus, OA('a2'), OA('a3')))
g.add_oper('a1+(a2-(a3+a1))', OType.plus, OA('a1'), TO(OType.minus, OA('a2'), TO(OType.plus, OA('a3'), OA('a1'))))

# add Type Operation with operation parameter and normal value
g.add_oper('sum_a+2', OType.plus, OA('sum_a'), 2)

# add Custom Operation to Grid object
g.add_custom_oper('custom', 'IF({0}>{1}, TRUE, FALSE)', VType.num, OA('a1'), OA('a2'))

# add Type Operation with sub Type and Custom Operations
g.add_oper('a1+(a2-a3)+custom', OType.plus, OA('a1'), TO(OType.minus, OA('a2'), OA('a3'))
           , CO('IF({0}=TRUE, 1, 10)', VType.num, OA('custom')))

# add operations which will be converted to array formula when write Excel file
g.add_custom_oper('custom_max', 'MAX({0},{1})', VType.num, OA('a1'), OA('a2'))
g.add_oper('max_if_a', OType.maxIf, OA('a1', True), 1, OA('sum_a', True))

# add Type Operation for string attrs
g.add_oper('index_of', OType.indexOf, 'c', OA('a4'))

# write attrs and opers into different sheet in a Excel file
g.write_separate_xl('test.xlsx')

# write attrs and opers into same sheet in a Excel file
g.write_together_xl('test_t.xlsx')
```

### The Definition of Operation Type(OType)

The table below shows Operation Type(OType) for each Value Type(VType) defined in the module of this version:

| VType    | OType Support                                                                                                            |
|----------|--------------------------------------------------------------------------------------------------------------------------|
| num      | plus, minus, divide, multipy, mod, sqrt, equal, length, replace, max, min, avg, maxIf, minIf, sumIf, avgIf, isNull       |
| str      | plus, indexOf, equal, upper, lower, length, replace, isNull                                                              |
| dateTime | addDays, minus, equal, replace, max, min, maxIf, minIf, year, month, day, hour, minute, second, weekday, weeknum, isNull |

The Definition of OType is in the file of xoper.py for detail.

### Example file for test purpose

Example python file named example_stock.py for test purpose is list in the project directory of test. After module installation of this porject by the tool of pip, this example file can be executed successfully if the installation is correct.

## Versioning

Navigate to [tags on this repository](https://github.com/sitwjn/openpyxl-grid/tags)
to see all available versions.

## Authors

* **Jianai Wang** - *Initial work* - [Openpyxl-grid](https://github.com/sitwjn/openpyxl-grid)

See also the list of [contributors](https://github.com/sitwjn/openpyxl-grid/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
