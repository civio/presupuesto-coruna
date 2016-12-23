# -*- coding: UTF-8 -*-
from budget_app.models import *
from budget_app.loaders import SimpleBudgetLoader
from decimal import *
import csv
import os
import re

class CorunaBudgetLoader(SimpleBudgetLoader):

    def parse_item(self, filename, line):
        is_expense = (filename.find('gastos.csv')!=-1)
        is_actual = (filename.find('/ejecucion_')!=-1)
        if is_expense:
            # We got 3- or 4- digit functional codes as input, so add a trailing zero
            fc_code = line[3].ljust(4, '0')
            ec_code = line[4][:5]   # Ignore additional digits after the fifth

            return {
                'is_expense': True,
                'is_actual': is_actual,
                'fc_code': fc_code,
                'ec_code': ec_code[:-2],        # First three digits (everything but last two)
                'ic_code': '000',
                'item_number': ec_code[-2:],    # Last two digits
                'description': line[5],
                'amount': self._parse_amount(line[9 if is_actual else 6])
            }

        else:
            ec_code = line[2][:5]   # Ignore additional digits after the fifth

            return {
                'is_expense': False,
                'is_actual': is_actual,
                'ec_code': ec_code[:3],         # First three digits
                'ic_code': '000',               # All income goes to the root node
                'item_number': ec_code[-2:],    # Last two digits
                'description': line[3],
                'amount': self._parse_amount(line[7 if is_actual else 4])
            }
