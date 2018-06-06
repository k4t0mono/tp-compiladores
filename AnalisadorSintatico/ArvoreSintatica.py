#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Noh:
    nome = None
    filhos = None
    pai = None
    nivel = None
    idArvore = None

    def __init__(self, nome):
        self.nome = nome
        self.filhos = []
        self.nivel = -1

class ArvoreSintatica:
    raiz = None
    nextId = None

    def __init__(self):
        self.nextId = 0

    def addRaiz(self, noh):
        self.raiz = noh
        self.raiz.nivel = 0
        self.raiz.idArvore = self.nextId
        self.nextId += 1

    def addFilho(self, nohPai, nohFilho):
        if(self.raiz == None):
            return
        nohFilho.pai = nohPai
        nohFilho.nivel = nohPai.nivel + 1
        nohFilho.idArvore = self.nextId
        self.nextId += 1
        nohPai.filhos.append(nohFilho)


    def percorreArvore(self):
        self.percorreArvoreRecursivo(self.raiz)

    def percorreArvoreRecursivo(self, noh):
        if(noh == None):
            return

        pai = None
        if(noh.pai != None):
            pai = noh.pai.idArvore
        print(noh.idArvore, noh.nome, noh.nivel, pai)
        if(len(noh.filhos) > 0):
            for filho in noh.filhos:
                self.percorreArvoreRecursivo(filho)


    def percorrePorNivel(self):
        niveis = {}
        self.percorrePorNivelRecursivo(self.raiz, niveis)
        for key in niveis:
            print(key, ":")
            print(niveis[key])

    def percorrePorNivelRecursivo(self, noh, niveis):
        if(noh == None):
            return
        if(noh.nivel not in niveis):
            niveis[noh.nivel] = []

        pai = None
        if(noh.pai != None):
            pai = noh.pai.nome
        niveis[noh.nivel].append((noh.nome, pai))
        if(len(noh.filhos) > 0):
            for filho in noh.filhos:
                self.percorrePorNivelRecursivo(filho, niveis)
