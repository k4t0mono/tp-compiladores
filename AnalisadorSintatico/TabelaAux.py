#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from texttable import Texttable
from Gerenciador import Gerenciador, TipoToken

# class Item:
#     def __init__(self, lexema, idEscopo):
#         self.lexema = lexema
#         self.idEscopo = idEscopo

class TabelaAux:
    def __init__(self):
        self.dados = {}

    def insert(self, tipo, lexema, idEscopo, nivelEscopo, linha, ):
        key = ' '.join((lexema, str(idEscopo)))

        if(self.get(lexema, idEscopo) == None):
            self.dados[key] = {
                'lexema': lexema,
                'idEscopo': idEscopo,
                'nivelEscopo': nivelEscopo,
                'linha': linha,
                'tipo': tipo,
                'id': len(self.dados)+1
            }
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
        linhas = [['Id', "Lexema", "Escopo", "Linha (Tabela de Simbolos)", "Tipo"]]
        for key in self.dados:
            linhas.append([
                self.dados[key]['id'], self.dados[key]["lexema"],
                self.dados[key]["idEscopo"], self.dados[key]["linha"], self.dados[key]["tipo"]
            ])
        t = Texttable()
        t.add_rows(linhas)
        return t.draw()
