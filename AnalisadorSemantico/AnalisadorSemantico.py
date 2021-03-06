
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import json
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
    ERROS_TIPAGEM = []

    def __init__(self, tokens, tabelaSim, tabelaAux):
        self.FLUXO_DE_TOKENS = tokens
        self.TABELA_SIMBOLOS = tabelaSim
        self.TABELA_AUX = tabelaAux
    
    def verificaEscopoAnterior(self, escopo, valor, linha):
        # print(self.pilhaEscopo)
        
        achou = False
        i = len(self.pilhaEscopo) - 1
        while(not achou and i > -1):
            resultado = self.TABELA_AUX.get(valor, self.pilhaEscopo[i])
            if(resultado == None):
                i -= 1
                continue
            achou = True
        if(achou):
             self.TABELA_SIMBOLOS.tabela[linha].linhaTabelaAux = resultado["id"]
        return achou
        
        # achou = False
        # escopoVerificado = copy.deepcopy(escopo)
        # while(not achou and (escopoVerificado > 0)):
        #     resultado = self.TABELA_AUX.get(valor, escopoVerificado)
        #     if(resultado == None):
        #         escopoVerificado -= 1
        #         continue
        #     if(resultado['nivelEscopo'] >= self.nivelEscopo):
        #         escopoVerificado -= 1
        #         continue
        #     if(resultado["linha"] > linha):
        #         escopoVerificado -= 1
        #         continue
        #     achou = True
        # if(achou):
        #     self.TABELA_SIMBOLOS.tabela[linha].linhaTabelaAux = resultado["id"]
        # return achou

    def verificaEscopoDaVariavel(self, i, token):
        valor = self.TABELA_SIMBOLOS.tabela[token.linhaTabela].valor
        resultado = self.TABELA_AUX.get(valor, self.escopo)
        if(self.FLUXO_DE_TOKENS[i-1].tipoToken == TipoToken.PCClass):
            return True
        if(self.FLUXO_DE_TOKENS[i+1].tipoToken == TipoToken.SepAbreParenteses):
            return True
        if(resultado == None):
            return self.verificaEscopoAnterior(self.escopo - 1, valor , token.linhaTabela)
        if(resultado["linha"] > token.linhaTabela):
            return self.verificaEscopoAnterior(self.escopo - 1, valor , token.linhaTabela)
        self.TABELA_SIMBOLOS.tabela[token.linhaTabela].linhaTabelaAux = resultado["id"]
        return True

    def verificaAtribuicoesTiposPrimitivos(self, tokenProximo, i, resultadoAnterior, mensagem):
        if(tokenProximo.tipoToken == TipoToken.IntLiteral):
            if(resultadoAnterior["tipo"] != "PCInt"):
                self.ERROS_TIPAGEM.append((i, 'IntLiteral ' + mensagem + ' que nao e int'))
            return
        if(tokenProximo.tipoToken == TipoToken.CharLiteral):
            if(resultadoAnterior["tipo"] != "PCChar"):
                self.ERROS_TIPAGEM.append((i, 'CharLiteral ' + mensagem + ' que nao e char'))
            return
        
        if(tokenProximo.tipoToken == TipoToken.PCTrue):
            if(resultadoAnterior["tipo"] != "PCBoolean"):
                self.ERROS_TIPAGEM.append((i, 'true ' + mensagem + ' que nao e boolean'))
            return
        if(tokenProximo.tipoToken == TipoToken.PCFalse):
            if(resultadoAnterior["tipo"] != "PCBoolean"):
                self.ERROS_TIPAGEM.append((i, 'false ' + mensagem + ' que nao e boolean'))
            return

    def pegaResultadoEscopoAnteriores(self, valor, linha):
        escopoVerificado = copy.deepcopy(self.escopo)
        while(escopoVerificado > 0):
            resultado = self.TABELA_AUX.get(valor, escopoVerificado)
            if(resultado == None):
                escopoVerificado -= 1
                continue
            if(resultado['nivelEscopo'] > self.nivelEscopo):
                escopoVerificado -= 1
                continue
            if(resultado["linha"] > linha):
                escopoVerificado -= 1
                continue
            return resultado
        return None


    def verificaTiposDaOperacaoDeAtribuicao(self, i):
        gerenciador = Gerenciador()
        token = self.FLUXO_DE_TOKENS[i + 2]
        while(token.tipoToken != TipoToken.SepPontoVirgula and 
              token.tipoToken != TipoToken.SepVirgula and 
              token.tipoToken != TipoToken.OpAtribuicao):
            if(gerenciador.retornaBoolean(token.tipoToken)):
                return 'bool'
            token = self.FLUXO_DE_TOKENS[i + 2]
            i += 2
        return 'int'


    def verificaAtribuicao(self, token, i):
        tokenAnterior = self.FLUXO_DE_TOKENS[i - 1]
        valorAnterior = self.TABELA_SIMBOLOS.tabela[tokenAnterior.linhaTabela].valor
        resultadoAnterior = self.pegaResultadoEscopoAnteriores(valorAnterior, tokenAnterior.linhaTabela)
        
        if(self.FLUXO_DE_TOKENS[i + 2].tipoToken != TipoToken.SepPontoVirgula and
           self.FLUXO_DE_TOKENS[i + 2].tipoToken != TipoToken.SepVirgula):
            retorno = self.verificaTiposDaOperacaoDeAtribuicao(i)
            tipo = self.tipoBasico(resultadoAnterior["tipo"])
            if(tipo != retorno):
                self.ERROS_TIPAGEM.append((i, "Atribuição inválida - O resultado da operação não bate com a variavel"))
            return


        tokenProximo = self.FLUXO_DE_TOKENS[i + 1]
        if(tokenProximo.tipoToken != TipoToken.Identificador):
            self.verificaAtribuicoesTiposPrimitivos(tokenProximo, i, resultadoAnterior, "atribuido a variavel")
            return
        
        if(self.verificaEscopoDaVariavel(i + 1, tokenProximo)):
            valorProximo = self.TABELA_SIMBOLOS.tabela[tokenProximo.linhaTabela].valor
            resultadoProximo = self.pegaResultadoEscopoAnteriores(valorProximo, tokenProximo.linhaTabela)
            if(resultadoAnterior["tipo"] != resultadoProximo["tipo"]):
                self.ERROS_TIPAGEM.append((i, 'Atribuicao de tipos diferentes'))


    def verificaOperacaoValor(self, token, i):
        tokenAnterior = self.FLUXO_DE_TOKENS[i - 1]
        valorAnterior = self.TABELA_SIMBOLOS.tabela[tokenAnterior.linhaTabela].valor
        resultadoAnterior = None
        if(tokenAnterior.tipoToken == TipoToken.Identificador):
            resultadoAnterior = self.pegaResultadoEscopoAnteriores(valorAnterior, tokenAnterior.linhaTabela)

        tokenProximo = self.FLUXO_DE_TOKENS[i + 1]
        if((tokenProximo.tipoToken == TipoToken.Identificador) and 
           (not self.verificaEscopoDaVariavel(i, tokenProximo))):
                return
        valorProximo = self.TABELA_SIMBOLOS.tabela[tokenProximo.linhaTabela].valor
        resultadoProximo = None
        if(tokenProximo.tipoToken == TipoToken.Identificador):
            resultadoProximo = self.pegaResultadoEscopoAnteriores(valorProximo, tokenProximo.linhaTabela)
        if(resultadoAnterior == None):
            if(tokenAnterior.tipoToken != TipoToken.IntLiteral):
                self.ERROS_ESCOPO.append((i, "Essa operacao é invalida para esse tipo."))
                return
            
            if(resultadoProximo == None):
                if(tokenProximo.tipoToken != TipoToken.IntLiteral):
                    self.ERROS_ESCOPO.append((i, "Essa operacao é invalida para esse tipo."))
                return
            self.verificaAtribuicoesTiposPrimitivos(tokenAnterior, i, resultadoProximo, "fez operacao com variavel")
            return
            

        if(resultadoProximo == None):
            if(tokenProximo.tipoToken != TipoToken.IntLiteral):
                self.ERROS_ESCOPO.append((i, "Essa operacao é invalida para esse tipo."))
                return
            self.verificaAtribuicoesTiposPrimitivos(tokenProximo, i, resultadoAnterior, "fez operacao com variavel")
            return

        if(resultadoAnterior['tipo'] != resultadoProximo['tipo']):
            self.ERROS_ESCOPO.append((i, "Operação com tipos de dados diferentes."))
            return

        if(resultadoAnterior['tipo'] != 'PCInt'):
            self.ERROS_ESCOPO.append((i, "Operação inválida para esses tipos."))
            return

        return

    def verificaOperacaoBoolean(self, token, i):
        if(token.tipoToken == TipoToken.OpIgualdade):
            if(not self.mesmoTipo(i-1, i+1)):
                self.ERROS_TIPAGEM.append((i, 'Comparação entre tipos diferentes'))
            return
        
        if(token.tipoToken == TipoToken.OpAnd):
            tokenEsquerda = self.FLUXO_DE_TOKENS[i-1]
            valorEquerda = self.TABELA_SIMBOLOS.tabela[tokenEsquerda.linhaTabela].valor
            resultadoEsquerda = self.pegaResultadoEscopoAnteriores(valorEquerda, tokenEsquerda.linhaTabela)
            tipoEsquerda = None
            if(resultadoEsquerda == None):
                tipoEsquerda = tokenEsquerda.tipoToken
            else:
                tipoEsquerda = resultadoEsquerda['tipo']
            if(not self.tipoBasico(tipoEsquerda) == 'bool'):
                self.ERROS_TIPAGEM.append((i, 'Operador && deve ser usado com boolean.'))
                return
            if((not self.mesmoTipo(i-1, i+1))):
                self.ERROS_TIPAGEM.append((i, 'Comparação entre tipos diferentes'))
            return

        if(token.tipoToken == TipoToken.OpMaior or token.tipoToken == TipoToken.OpMenorIgual):
            if(not self.mesmoTipo(i-1, i+1)):
                self.ERROS_TIPAGEM.append((i, 'Comparação entre tipos diferentes'))
                return
            
            tokenEsquerda = self.FLUXO_DE_TOKENS[i-1]
            valorEquerda = self.TABELA_SIMBOLOS.tabela[tokenEsquerda.linhaTabela].valor
            resultadoEsquerda = self.pegaResultadoEscopoAnteriores(valorEquerda, tokenEsquerda.linhaTabela)
            tipoEsquerda = None
            if(resultadoEsquerda == None):
                tipoEsquerda = tokenEsquerda.tipoToken
            else:
                tipoEsquerda = resultadoEsquerda['tipo']
            if(self.tipoBasico(tipoEsquerda) == 'bool'):
                self.ERROS_TIPAGEM.append((i, 'Operador não deve ser usado com boolean.'))
                return

        return

    def tipoBasico(self, tipo):
        if(tipo == 'PCInt'):
            return 'int'
        if(tipo == TipoToken.IntLiteral):
            return 'int'
        if(tipo == 'PCChar'):
            return 'char'
        if(tipo == TipoToken.CharLiteral):
            return 'char'
        if(tipo == 'PCBoolean'):
            return 'bool'
        if(tipo == TipoToken.PCTrue or tipo == TipoToken.PCFalse):
            return 'bool'

    def mesmoTipo(self, i, j):
        tokenI = self.FLUXO_DE_TOKENS[i]
        valorI = self.TABELA_SIMBOLOS.tabela[tokenI.linhaTabela].valor
        resultadoI = self.pegaResultadoEscopoAnteriores(valorI, tokenI.linhaTabela)
        tipoI = None
        if(resultadoI == None):
            tipoI = tokenI.tipoToken
        else:
            tipoI = resultadoI['tipo']

        tokenJ = self.FLUXO_DE_TOKENS[j]
        valorJ = self.TABELA_SIMBOLOS.tabela[tokenJ.linhaTabela].valor
        resultadoJ = self.pegaResultadoEscopoAnteriores(valorJ, tokenJ.linhaTabela)
        tipoJ = None
        if(resultadoJ == None):
            tipoJ = tokenJ.tipoToken
        else:
            tipoJ = resultadoJ['tipo']

        return self.tipoBasico(tipoI) == self.tipoBasico(tipoJ)

    def verificaOperadores(self, token, i, gerenciador):
        if(len(self.ERROS_ESCOPO) > 0):
            return
        if(token.tipoToken == TipoToken.OpAtribuicao):
            self.verificaAtribuicao(token, i)
            return
        if(gerenciador.retornaValor(token.tipoToken)):
            self.verificaOperacaoValor(token, i)
            return
        if(gerenciador.retornaBoolean(token.tipoToken)):
            self.verificaOperacaoBoolean(token, i)
            return


    def fazerAnaliseSemantica(self):
        gerenciador = Gerenciador()
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
                continue

        
            # verificar tipo
            self.verificaOperadores(token, i, gerenciador)
            




def main(tokens, tabelaSimbolos, tabelaAux):
    analisadorSemantico = AnalisadorSemantico(tokens, tabelaSimbolos, tabelaAux)
    analisadorSemantico.fazerAnaliseSemantica()
    return (analisadorSemantico.ERROS_ESCOPO + analisadorSemantico.ERROS_TIPAGEM, 
            analisadorSemantico.TABELA_SIMBOLOS)