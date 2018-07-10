#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from Gerenciador import Gerenciador, TipoToken

# class Item:
#     def __init__(self, lexema, idEscopo):
#         self.lexema = lexema
#         self.idEscopo = idEscopo

class TabelaAux:
    def __init__(self):
        self.dados = {}

    def insert(self, lexema, idEscopo, linha):
        key = ' '.join((lexema, str(idEscopo)))

        if(self.get(lexema, idEscopo) == None):
            self.dados[key] = { 'lexema': lexema, 'idEscopo': idEscopo, 'linha': linha }
            return False
        else:
            return True

    def get(self, lexema, idEscopo):
        key = ' '.join((lexema, str(idEscopo)))

        try:
            return self.dados[key]
        except KeyError:
            return None

    def __str__(self):
        return json.dumps(self.dados, indent=4, sort_keys=True)
