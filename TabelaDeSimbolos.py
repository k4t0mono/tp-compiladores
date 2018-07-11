#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Gerenciador import Gerenciador, TipoToken
from texttable import Texttable


class Item:
    valor = None
    linhaTabelaAux = None
    def __init__(self, valor):
        self.valor = valor

class TabelaDeSimbolos:
    tabela = None
    def __init__(self):
        self.tabela = []

    def insere(self, palavra):
        g = Gerenciador()
        if(g.getTipoToken(palavra) != TipoToken.Identificador and
           g.getTipoToken(palavra) != TipoToken.IntLiteral and
           g.getTipoToken(palavra) != TipoToken.CharLiteral and
           g.getTipoToken(palavra) != TipoToken.StringLiteral):
            return -1
        item = Item(palavra)
        self.tabela.append(item)
        return (len(self.tabela) - 1)


    def __str__(self):
        linhas = [["Linha", "Lexema", "Linha (Tabela de Variaveis)"]]
        for i in range(len(self.tabela)):
            linhas.append([i, self.tabela[i].valor, self.tabela[i].linhaTabelaAux])
        t = Texttable()
        t.add_rows(linhas)
        return t.draw()