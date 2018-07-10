
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from Gerenciador import *
from AnalisadorSintatico.TabelaAux import *

class AnalisadorSemantico:
    FLUXO_DE_TOKENS = None
    TABELA_SIMBOLOS = None
    TABELA_AUX = None
    nivelEscopo = 0
    escopo = 0
    pilhaEscopo = []
    proximoEscopo = 1
    ERROS_ESCOPO = []

    def __init__(self, tokens, tabelaSim, tabelaAux):
        self.FLUXO_DE_TOKENS = tokens
        self.TABELA_SIMBOLOS = tabelaSim
        self.TABELA_AUX = tabelaAux
        # print(self.FLUXO_DE_TOKENS)
        print(self.TABELA_AUX)
        # print(self.TABELA_SIMBOLOS)
    
    def verificaEscopoAnterior(self, escopo, valor, linha):
        achou = False
        escopoVerificado = copy.deepcopy(escopo)
        while(not achou and (escopoVerificado > 0)):
            resultado = self.TABELA_AUX.get(valor, escopoVerificado)
            if(resultado == None):
                escopoVerificado -= 1
                continue
            if(resultado['nivelEscopo'] >= self.nivelEscopo):
                escopoVerificado -= 1
                continue
            if(resultado["linha"] > linha):
                escopoVerificado -= 1
                continue
            achou = True
        return achou

    def verificaEscopoDaVariavel(self, i, token):
        valor = self.TABELA_SIMBOLOS.tabela[token.linhaTabela].valor
        resultado = self.TABELA_AUX.get(valor, self.escopo)
        if(self.FLUXO_DE_TOKENS[i-1].tipoToken == TipoToken.PCClass):
            return True
        if(self.FLUXO_DE_TOKENS[i+1].tipoToken == TipoToken.SepAbreParenteses):
            return True
        if(resultado == None):
            if(not self.verificaEscopoAnterior(self.escopo - 1, valor , token.linhaTabela)):
                return False
            return
        if(resultado["linha"] > token.linhaTabela):
            if(not self.verificaEscopoAnterior(self.escopo - 1, valor, token.linhaTabela)):
                return False
        return True

    def fazerAnaliseSemantica(self):
        # gerenciador = Gerenciador()
        for i in range(len(self.FLUXO_DE_TOKENS)):
            token  = self.FLUXO_DE_TOKENS[i]
            if(token.tipoToken == TipoToken.SepAbreChaves):
                self.nivelEscopo += 1
                self.pilhaEscopo.append(self.escopo)
                self.escopo = self.proximoEscopo
                self.proximoEscopo += 1
            if(token.tipoToken == TipoToken.SepFechaChaves):
                self.nivelEscopo -= 1
                self.escopo = self.pilhaEscopo.pop()
            if(token.tipoToken == TipoToken.Identificador):
                if(not self.verificaEscopoDaVariavel(i, token)):
                    self.ERROS_ESCOPO.append((i, "Variavel não declarada"))

        
            # verificar tipo
            if(token.tipoToken == TipoToken.OpAtribuicao):
                valor = self.TABELA_SIMBOLOS.tabela[token.linhaTabela].valor
                tokenAnterior = self.FLUXO_DE_TOKENS[i - 1]
                if(len(self.ERROS_ESCOPO) > 0):
                    continue
                
                valorAnterior = self.TABELA_SIMBOLOS.tabela[tokenAnterior.linhaTabela].valor
                resultadoAnterior = self.TABELA_AUX.get(valorAnterior, self.escopo)
                tokenProximo = self.FLUXO_DE_TOKENS[i + 1]

                if(tokenProximo.tipoToken != TipoToken.Identificador):
                    if(tokenProximo.tipoToken == TipoToken.IntLiteral):
                        if(resultadoAnterior["tipo"] != "PCInt"):
                            self.ERROS_ESCOPO.append((i, 'intliteral atribuido a variavel que nao e int'))
                        continue
                    if(tokenProximo.tipoToken == TipoToken.CharLiteral):
                        if(resultadoAnterior["tipo"] != "PCChar"):
                            self.ERROS_ESCOPO.append((i, 'charliteral atribuido a variavel que nao e char'))
                        continue
                    
                    if(tokenProximo.tipoToken == TipoToken.PCTrue):
                        if(resultadoAnterior["tipo"] != "PCBoolean"):
                            self.ERROS_ESCOPO.append((i, 'true atribuido a variavel que nao e boolean'))
                        continue
                    if(tokenProximo.tipoToken == TipoToken.PCFalse):
                        if(resultadoAnterior["tipo"] != "PCBoolean"):
                            self.ERROS_ESCOPO.append((i, 'false atribuido a variavel que nao e boolean'))
                        continue
                    continue
                
                if(self.verificaEscopoDaVariavel(i + 1, tokenProximo)):
                    valorProximo = self.TABELA_SIMBOLOS.tabela[tokenProximo.linhaTabela].valor
                    resultadoProximo = self.TABELA_AUX.get(valorProximo, self.escopo)
                    if(resultadoAnterior["tipo"] != resultadoProximo["tipo"]):
                        self.ERROS_ESCOPO.append((i, 'Atribuicao de tipos diferentes'))



            # if(token.tipoToken in gerenciador.operadores):
            #     if(token.tipoToken == TipoToken.OpSomaAtribuicao):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpIgualdade):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpIncremento):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpAnd):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpMenorIgual):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpDecremento):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpAtribuicao):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpMaior):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpSoma):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpNot):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpMenos):
            #         if()
            #         continue
            #     if(token.tipoToken == TipoToken.OpMultiplicacao):
            #         if()
            #         continue




def main(tokens, tabelaSimbolos, tabelaAux):
    analisadorSemantico = AnalisadorSemantico(tokens, tabelaSimbolos, tabelaAux)
    analisadorSemantico.fazerAnaliseSemantica()
    return analisadorSemantico.ERROS_ESCOPO