import null
from datetime import datetime

from openpyxl_grid import Grid
from openpyxl_grid import OType
from openpyxl_grid import VType
from openpyxl_grid import OA
from openpyxl_grid import TO


stock_dict = [
    {'Stock Name': 'MSFT', 'Date Purchased': datetime(2012, 5, 1, 0, 0)
        , 'Shares': 10, 'Purchase Price': 241, 'Fees': 0
        , 'Current Price': 260.0, 'Date Sold': null, 'Sell Price': 0}
    , {'Stock Name': 'GOOG', 'Date Purchased': datetime(2016, 8, 23, 0, 0)
        , 'Shares': 25, 'Purchase Price': 156, 'Fees': 0
        , 'Current Price': 92.66, 'Date Sold': datetime(2023, 3, 9, 0, 0), 'Sell Price': 93}
    , {'Stock Name': 'AAPL', 'Date Purchased': datetime(2019, 3, 7, 0, 0)
        , 'Shares': 40, 'Purchase Price': 156, 'Fees': 0
        , 'Current Price': 150.59, 'Date Sold': null, 'Sell Price': 0}
]

grid = Grid(name="stocks")
grid.attrs_from_dicts(stock_dict)

a_stock_name = OA('Stock Name')
a_date_purchased = OA('Date Purchased')
a_Shares = OA('Shares')
a_purchase_price = OA('Purchase Price')
a_Fees = OA('Fees')
a_current_price = OA('Current Price')
a_date_sold = OA('Date Sold')
a_sell_price = OA('Sell Price')

grid.add_oper('Purchase Cost', OType.plus, TO(OType.multipy, a_Shares, a_purchase_price), a_Fees)
grid.add_oper('Current Value', OType.multipy, a_current_price, a_Shares)
grid.add_custom_oper('Unrealized Gain(Loss)', 'IF({0}, {1}, 0)', VType.num, TO(OType.isNull, a_date_sold)
                     , TO(OType.minus, OA('Current Value'), OA('Purchase Cost')))
grid.add_custom_oper('Unrealized Change', 'IF({0}, {1}, 0)', VType.num, TO(OType.isNull, a_date_sold)
                     , TO(OType.divide, OA('Unrealized Gain(Loss)'), OA('Purchase Cost')))
grid.add_custom_oper('Income from Sale', 'IF({0}, 0, {1})', VType.num, TO(OType.isNull, a_date_sold)
                     , TO(OType.multipy, a_sell_price, a_Shares))
grid.add_custom_oper('Realized Gain(Loss)', 'IF({0}, 0, {1})', VType.num, TO(OType.isNull, a_date_sold)
                     , TO(OType.minus, OA('Income from Sale'), OA('Purchase Cost')))
grid.add_custom_oper('Gain(Loss)', 'IF({0}, 0, {1})', VType.num, TO(OType.isNull, a_date_sold)
                     , TO(OType.divide, OA('Realized Gain(Loss)'), OA('Purchase Cost')))
grid.add_custom_oper('CAGR'
                     , 'IF(ISBLANK({0}),"-",(1+(IF(ISBLANK({1}),{2},{3})-{4})/{4})^(365/(IF(ISBLANK({2}),TODAY(),{2})-{0}))-1)'
                     , VType.num, a_date_purchased, a_date_sold, OA('Current Value'), OA('Income from Sale')
                     , OA('Purchase Cost'), a_date_sold)

grid.write_together_xl('example_stock.xlsx')



