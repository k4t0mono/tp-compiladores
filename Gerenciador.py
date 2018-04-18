#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from Auto import Auto

class TipoToken(Enum):
    auto = Auto()
    OpAtribuicao = auto.get()
    OpIgualdade = auto.get()
    OpMaior = auto.get()
    OpIncremento = auto.get()
    OpAnd = auto.get()
    OpMenorIgual = auto.get()
    OpNot = auto.get()
    OpMenos = auto.get()
    OpDecremento = auto.get()
    OpSoma = auto.get()
    OpSomaAtribuicao = auto.get()
    OpMultiplicacao = auto.get()
    
    Identificador = auto.get()

class Gerenciador:
    operadores = {
        "+=" : TipoToken.OpSomaAtribuicao,
        "==" : TipoToken.OpIgualdade,
        "++" : TipoToken.OpIncremento,
        "&&" : TipoToken.OpAnd,
        "<=" : TipoToken.OpMenorIgual,
        "--" : TipoToken.OpDecremento,
        "=" : TipoToken.OpAtribuicao,
        ">" : TipoToken.OpMaior,
        "+" : TipoToken.OpSoma,
        "!" : TipoToken.OpNot,
        "-" : TipoToken.OpMenos,
        "*" : TipoToken.OpMultiplicacao,
    }
    
    def getTipoToken(self, palavra):
        if(palavra in self.operadores):
            return self.operadores[palavra]
