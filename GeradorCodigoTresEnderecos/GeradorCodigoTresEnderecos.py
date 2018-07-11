#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import pprint
from Gerenciador import TipoToken
from Gerenciador import Gerenciador

class ID:
    id = 0

    def getID(self):
        self.id += 1
        return self.id -1

id = ID()
class Arvore:
    def __init__(self, instrucoes, tabelaSimbolos, idMaster):
        self.raiz = Noh(instrucoes)
        self.tabelaSimbolos = tabelaSimbolos
        self.idVariaveisTemporarias = idMaster
        self.codigoGerado = ""
        self.gerenciador = Gerenciador()

    def __str__(self):
        return str(self.raiz)

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
        saida += str(noh.id) + " "
        # print('O erro aqui: {}'.format(noh.valor))
        if(noh.valor.tipoToken == TipoToken.Identificador or noh.valor.tipoToken == TipoToken.IntLiteral):
            saida += self.tabelaSimbolos.tabela[noh.valor.linhaTabela].valor
        else:
            saida += str(noh.valor.getTipoToken())
        saida += " " + str(noh.nivel) + " " + str(pai) + "\n"
        # print(noh.id, noh.nome, noh.nivel, pai)
        if(noh.filhoEsq != None):
            saida = self.percorreArvoreRecursivo(noh.filhoEsq, saida)
        if(noh.filhoDir != None):
            saida = self.percorreArvoreRecursivo(noh.filhoDir, saida)
        return saida

    def geraCodigo(self):
        self.geraCodigoRec(self.raiz)
        # return self.percorreArvoreDireitaParaEsquerda(self.raiz, "")

    def ehFolha(self, noh):
        return (noh.filhoDir == None and noh.filhoEsq == None)

    def geraCodigoRec(self, noh):
        if not self.ehFolha(noh.filhoDir):
            self.geraCodigoRec(noh.filhoDir)
        # else:
            # print("----------------")
            # print(noh.filhoDir.valor)
        if not self.ehFolha(noh.filhoEsq):
            self.geraCodigoRec(noh.filhoEsq)
        # else:
            # print("----------------")
            # print(noh.filhoEsq.valor)
        

        if(noh.valor.tipoToken == TipoToken.OpAtribuicao):
            valorEsquerda = noh.filhoEsq.temporario
            valorDireita = noh.filhoDir.temporario
            if(noh.filhoEsq.temporario == None):
                valorEsquerda = self.tabelaSimbolos.tabela[noh.filhoEsq.valor.linhaTabela].valor
            if(noh.filhoDir.temporario == None):
                valorDireita = self.tabelaSimbolos.tabela[noh.filhoDir.valor.linhaTabela].valor
            self.codigoGerado += str(valorEsquerda) + " "
            self.codigoGerado += self.gerenciador.getStringOperador(noh.valor.tipoToken) + " "
            self.codigoGerado += str(valorDireita) + "\n"
        else:
            valorEsquerda = noh.filhoEsq.temporario
            valorDireita = noh.filhoDir.temporario
            if(noh.filhoEsq.temporario == None):
                valorEsquerda = self.tabelaSimbolos.tabela[noh.filhoEsq.valor.linhaTabela].valor
            if(noh.filhoDir.temporario == None):
                valorDireita = self.tabelaSimbolos.tabela[noh.filhoDir.valor.linhaTabela].valor
            variavelT = "t" + str(self.idVariaveisTemporarias.getID())
            self.codigoGerado += variavelT + " = "
            self.codigoGerado += str(valorEsquerda) + " "
            self.codigoGerado += self.gerenciador.getStringOperador(noh.valor.tipoToken) + " "
            self.codigoGerado += str(valorDireita) + "\n"
            noh.temporario = variavelT




    def percorreArvoreDireitaParaEsquerda(self, noh, saida):
        if(noh.filhoDir != None):
            saida = self.percorreArvoreDireitaParaEsquerda(noh.filhoDir, saida)
        if(noh.filhoEsq != None):
            saida = self.percorreArvoreDireitaParaEsquerda(noh.filhoEsq, saida)
        
        if(noh.pai == None and noh.valor.tipoToken == TipoToken.OpAtribuicao):
            fe = self.tabelaSimbolos.tabela[noh.filhoEsq.valor.linhaTabela].valor
            saida += fe + " = "
            return saida
        return saida


class Noh:
    def __init__(self, instrucoes,pai = None):
        self.id = id.getID()
        self.valor = instrucoes
        self.filhoEsq = None
        self.filhoDir = None
        self.pai = pai
        self.nivel = 0
        self.temporario = None

        if not self.ehAtomico():
            self.quebraNoh()

    def ehAtomico(self):
        if(len(self.valor) > 1):
            return False
        self.valor = self.valor[0]
        return True
    
    def quebraNoh(self):
        for i in range(len(self.valor)):
            # print("Thuza: {}".format(self.valor))
            # printInstrucao(self.valor)
            if(self.valor[i].tipoToken == TipoToken.OpAtribuicao):
                self.filhoEsq = Noh(self.valor[:i], self)
                self.filhoDir = Noh(self.valor[i+1:], self)
                self.valor = self.valor[i]
                return
            if(self.valor[i].tipoToken == TipoToken.OpSoma or self.valor[i].tipoToken == TipoToken.OpMenos):
                self.filhoEsq = Noh(self.valor[:i], self)
                self.filhoDir = Noh(self.valor[i+1:], self)
                self.valor = self.valor[i]
                return
        for i in range(len(self.valor)):
            if(self.valor[i].tipoToken == TipoToken.OpMultiplicacao):
                self.filhoEsq = Noh(self.valor[:i], self)
                self.filhoDir = Noh(self.valor[i+1:], self)
                self.valor = self.valor[i]
                return


    def __str__(self):
        saida = ""
        saida += self.valor.getTipoToken()
        saida += " "
        saida += " filhoEsq: "
        if(self.filhoEsq != None):
            saida += self.filhoEsq.valor.getTipoToken()
            saida += " "
        saida += " filhoDir: "
        if(self.filhoDir != None):
            saida += self.filhoDir.valor.getTipoToken()
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
    instrucoes = []
    lista_aux = []
    for i in range(len(tokens)):
        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            # print('gggg: {}'.format(lista_aux[0]))
            if(lista_aux[0].tipoToken == TipoToken.PCInt or lista_aux[0].tipoToken == TipoToken.PCBoolean or lista_aux[0].tipoToken == TipoToken.PCChar):
                lista_aux = lista_aux[1:]
            instrucoes.append(copy.deepcopy(lista_aux))
            lista_aux.clear()
        else:
            lista_aux.append(copy.deepcopy(tokens[i]))
    
    return instrucoes


def limpaTokens(tokens, tabela):
    corte1 = 0
    for i in range(len(tokens)):
        if(tokens[i].tipoToken == TipoToken.PCVoid and tabela.tabela[tokens[i+1].linhaTabela].valor == 'main'):
            corte1 = i + 5
    
    corte2 = corte1
    for i in range(corte1, len(tokens)):
        if(tokens[i].tipoToken == TipoToken.SepFechaChaves):
            corte2 = i-1

    t = tokens[corte1:corte2]
    
    return t

def main(tokensOld, tabelaSimbolos):
    tokens = limpaTokens(tokensOld, tabelaSimbolos)
    instrucoes = separaInstrucoes(tokens)
    idMaster = ID()
    saida = ""
    for instrucao in instrucoes:
        a = Arvore(instrucao, tabelaSimbolos, idMaster)
        print(a.percorreArvore(), file=open("arvore" + str(idMaster.id), "w"))
        a.geraCodigo()
        saida += a.codigoGerado
    return saida