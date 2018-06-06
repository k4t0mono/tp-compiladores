#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Noh:
    nome = None
    filhos = None
    pai = None
    
    def __init__(self, nome):
        self.nome = nome
        self.filhos = []

class ArvoreSintatica:
    raiz = None
    
    def addRaiz(self, noh):
        self.raiz = noh
    
    def addFilho(self, nohPai, nohFilho):
        if(self.raiz == None):
            return
        nohFilho.pai = nohPai
        nohPai.filhos.append(nohFilho)
    def percorreArvore(self):
        self.percorreArvoreRecursivo(self.raiz)
        
    def percorreArvoreRecursivo(self, noh):
        if(len(noh.filhos) > 0):
            for filho in noh.filhos:
                self.percorreArvoreRecursivo(filho)
        print(noh.nome)
            
    
