# -*- coding: UTF-8 -*-
from budget_app.models import *
from budget_app.loaders import SimpleBudgetLoader
from decimal import *
import csv
import os
import re

class CorunaBudgetLoader(SimpleBudgetLoader):

    # We override this to allow a different classification per year
    def get_institutional_classification_path(self, path):
        return os.path.join(path, 'clasificacion_organica.csv')

    def parse_item(self, filename, line):
        # Programme codes have changed in 2015, due to new laws. Since the application expects a code-programme
        # mapping to be constant over time, we are forced to amend budget data prior to 2015.
        # See https://github.com/dcabo/presupuestos-aragon/wiki/La-clasificaci%C3%B3n-funcional-en-las-Entidades-Locales
        programme_mapping = {
            # old programme: new programme
            '1340': '1350',     # Protección Civil
            '1350': '1360',     # Servicio de prevención y extinción de incendios
            '1520': '1522',     # Conservación y rehabilitación de la edificación
            '1550': '1539',     # Vías públicas
            '1610': '1600',     # Alcantarillado
            '1790': '1729',     # Protección y mejora del medio ambiente. Otros
            '2300': '2310',     # Asistencia social primaria
            '2310': '2310',     # Asistencia social primaria
            '2320': '2310',     # Asistencia social primaria
            '2330': '2310',     # Asistencia social primaria
            '3130': '3110',     # Protección de la salubridad pública
            '3210': '3230',     # Funcionamiento de centros de enseñanza preescolar y primaria
            '3230': '3260',     # Servicios complementarios de educación
            '3240': '3260',     # Servicios complementarios de educación
            '3310': '3331',     # Diculgación científica y técnica
            '3390': '3341',     # Instituto Municipal Coruña Espectáculos
            '4410': '4411',     # Transporte colectivo urbano de viajeros
            '9230': '9239',     # Información básica y estadística. Otros
            '9350': '9321',     # Tribunal económico administrativo municipal
            '9450': '3342',     # Consorcio promoción música
            '9460': '4321',     # Consorcio de turismo
        }

        is_expense = (filename.find('gastos.csv')!=-1)
        is_actual = (filename.find('/ejecucion_')!=-1)
        if is_expense:
            # We got 3- or 4- digit functional codes as input, so add a trailing zero
            fc_code = line[3].ljust(4, '0')
            ec_code = line[4][:5]   # Ignore additional digits after the fifth

            # For years before 2015 we check whether we need to amend the programme code
            year = re.search('municipio/(\d+)/', filename).group(1)
            if int(year) < 2015:
                fc_code = programme_mapping.get(fc_code, fc_code)

            return {
                'is_expense': True,
                'is_actual': is_actual,
                'fc_code': fc_code,
                'ec_code': ec_code[:-2],        # First three digits (everything but last two)
                'ic_code': line[2].rjust(4, '0'),
                'item_number': ec_code[-2:],    # Last two digits
                'description': self._spanish_titlecase(line[5]).rstrip('.'),
                'amount': self._parse_amount(line[9 if is_actual else 6])
            }

        else:
            ec_code = line[2][:5]   # Ignore additional digits after the fifth

            return {
                'is_expense': False,
                'is_actual': is_actual,
                'ec_code': ec_code[:3],          # First three digits
                'ic_code': '0000',               # All income goes to the root node
                'item_number': ec_code[-2:],     # Last two digits
                'description': self._spanish_titlecase(line[3]).rstrip('.'),
                'amount': self._parse_amount(line[7 if is_actual else 4])
            }
