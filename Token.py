#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Gerenciador import Gerenciador

class Token:
    tipoToken = None
    linhaTabela = None
    
        #~ "," : ",",
        #~ "." : ".",
        #~ "[" : "[",
        #~ "{" : "{",
        #~ "(" : "(",
        #~ ")" : ")",
        #~ "}" : "}",
        #~ "]" : "]",
        #~ ";" : ";"
    #~ }
    
    def __init__(self, palavra, linha):
        g = Gerenciador()
        self.linhaTabela = linha
        self.tipoToken = g.getTipoToken(palavra)
        #~ elif()
            
            
    def __str__(self):
        return "<" + str(self.tipoToken) + ", " + str(self.linhaTabela) + ">"


    
