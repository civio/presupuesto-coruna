# -*- coding: UTF-8 -*-
import re

from budget_app.loaders import PaymentsLoader
from budget_app.models import Budget

class CorunaPaymentsLoader(PaymentsLoader):

    # Parse an input line into fields
    def parse_item(self, budget, line):
        policy = self._spanish_titlecase( re.sub('\.$', '', line[6].strip()) )
        amount = self._read_english_number( line[2].strip() )
        payee = self._titlecase( line[4].strip() )

        return {
            'area': policy,
            'programme': None,
            'fc_code': None,
            'ec_code': None,
            'date': line[1].strip(),
            'contract_type': None,
            'payee': payee,
            'anonymized': False,
            'description': line[5].strip(),
            'amount': amount
        }
