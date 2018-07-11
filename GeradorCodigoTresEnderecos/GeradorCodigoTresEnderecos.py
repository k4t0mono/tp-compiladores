#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import pprint
from Gerenciador import TipoToken

class ID:
    id = 0

    def getID(self):
        self.id += 1
        return self.id -1

id = ID()
class Arvore:
    def __init__(self, instrucoes):
        self.raiz = Noh(instrucoes)

    def __str__(self):
        return str(self.raiz)
    
    def toDot(self):
        nodes = [self.raiz.valor]
        relacoes = []

        pilha = []
        pilha.append(self.raiz)
        # while(len(pilha) > 0):


    def percorreArvore(self):
        saida = self.percorreArvoreRecursivo(self.raiz, "")
        # print(saida)
        return saida


    def percorreArvoreRecursivo(self, noh, saida):
        if(noh == None):
            return ""
        pai = None
        if(noh.pai != None):
            pai = noh.pai.id
        saida += str(noh.id) + " " + str(noh.valor[0].getTipoToken()) + " " + str(noh.nivel) + " " + str(pai) + "\n"
        # print(noh.id, noh.nome, noh.nivel, pai)
        if(noh.filhoEsq != None):
            saida = self.percorreArvoreRecursivo(noh.filhoEsq, saida)
        if(noh.filhoDir != None):
            saida = self.percorreArvoreRecursivo(noh.filhoDir, saida)
        return saida

class Noh:
    def __init__(self, instrucoes,pai = None):
        self.id = id.getID()
        self.valor = instrucoes
        self.filhoEsq = None
        self.filhoDir = None
        self.pai = pai
        self.nivel = 0

        if not self.ehAtomico():
            self.quebraNoh()

    def ehAtomico(self):
        if(len(self.valor) > 1):
            return False
        return True
    
    def quebraNoh(self):
        print("quebrando noh: {}".format(strListaTokens(self.valor)))
        for i in range(len(self.valor)):
            print(i, len(self.valor))
            if(self.valor[i].tipoToken == TipoToken.OpAtribuicao):
                self.filhoEsq = Noh(self.valor[:i], self)
                self.filhoDir = Noh(self.valor[i+1:], self)
                self.valor = [self.valor[i]]
                return
            if(self.valor[i].tipoToken == TipoToken.OpSoma or self.valor[i].tipoToken == TipoToken.OpMenos):
                self.filhoEsq = Noh(self.valor[:i], self)
                self.filhoDir = Noh(self.valor[i+1:], self)
                self.valor = [self.valor[i]]
                return
                

    def __str__(self):
        saida = ""
        for item in self.valor:
            saida += item.getTipoToken()
            saida += " "
        saida += " filhoEsq: "
        if(self.filhoEsq != None):
            for item in self.filhoEsq.valor:
                saida += item.getTipoToken()
                saida += " "
        saida += " filhoDir: "
        if(self.filhoDir != None):
            for item in self.filhoDir.valor:
                saida += item.getTipoToken()
                saida += " "
        saida += "\n"
        if(self.filhoEsq != None):
            saida += str(self.filhoEsq)
        if(self.filhoDir != None):
            saida += str(self.filhoDir)
        return saida

def strListaTokens(tokens):
    s = '['
    for t in tokens:
        s += '{},'.format(t)
    
    s = s[:-1]
    return s+']'


def printInstrucao(tokens):
    s = '[\n'
    for t in tokens:
        s += '  {}\n'.format(t)

    s += ']'
    print(s)


def separaInstrucoes(tokens):
    print('separa')
    instrucoes = []
    lista_aux = []
    for i in range(len(tokens)):
        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            instrucoes.append(copy.deepcopy(lista_aux))
            lista_aux.clear()
        else:
            lista_aux.append(copy.deepcopy(tokens[i]))
    
    return instrucoes


def limpaTokens(tokens):
    print('limpado')
    corte1 = 0
    for i in range(len(tokens)):
        if(tokens[i].tipoToken == TipoToken.PCVoid):
            corte1 = i + 5
    
    t = tokens[corte1:-2]
    return t

def main(tokensOld):
    tokens = limpaTokens(tokensOld)
    instrucoes = separaInstrucoes(tokens)
    # printInstrucao(instrucoes[0])
    a = Arvore(instrucoes[0])
    print(a)
    print(a.percorreArvore(), file=open('aaaaa', 'w'))
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(instrucoes)

    return