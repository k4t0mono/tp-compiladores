#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Noh:
    nome = None
    filhos = None
    pai = None
    nivel = None
    
    def __init__(self, nome):
        self.nome = nome
        self.filhos = []
        self.nivel = -1

class ArvoreSintatica:
    raiz = None
    
    def addRaiz(self, noh):
        self.raiz = noh
        self.raiz.nivel = 0
    
    def addFilho(self, nohPai, nohFilho):
        if(self.raiz == None):
            return
        nohFilho.pai = nohPai
        nohFilho.nivel = nohPai.nivel + 1
        nohPai.filhos.append(nohFilho)
        
    def percorreArvore(self):
        self.percorreArvoreRecursivo(self.raiz)
        
    def percorreArvoreRecursivo(self, noh):
        if(noh == None):
            return
        print(noh.nome, noh.nivel)
        if(len(noh.filhos) > 0):
            for filho in noh.filhos:
                self.percorreArvoreRecursivo(filho)
        
            
    
