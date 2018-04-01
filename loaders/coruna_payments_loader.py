# -*- coding: UTF-8 -*-
import re

from budget_app.loaders import PaymentsLoader
from budget_app.models import Budget

class CorunaPaymentsLoader(PaymentsLoader):

    # Parse an input line into fields
    def parse_item(self, budget, line):
        amount = self._read_english_number( line[2].strip() )
        payee = self._titlecase( line[4].strip() )
        anonymized = (payee == '[Anonimizado]*')

        area = line[6].strip()
        if area != '[ANTICIPO DE CAJA]':
            match = re.search('^(\d+)', area)
            # We got 3- or 4- digit functional codes as input, so add a trailing zero
            area_id = match.group(1).ljust(4, '0')
            area = Budget.objects.get_all_descriptions(budget.entity)['functional'][area_id]
        else:
            area = '(Anticipo de caja)'

        return {
            'area': area,
            'programme': None,
            'fc_code': None,
            'ec_code': None,
            'date': line[1].strip(),
            'payee': payee,
            'anonymized': anonymized,
            'description': line[5].strip(),
            'amount': amount
        }
