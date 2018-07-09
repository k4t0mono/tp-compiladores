
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

from Gerenciador import TipoToken
from AnalisadorSintatico.ArvoreSintatica import *

class AnalisadorSintatico:
    POSICAO_TOKEN_ERRO = []
    ARVORE_SINTATICA = ArvoreSintatica()
    ESCOPO = 0
    TABELA = None

    def __init__(self, tabela):
        self.TABELA = tabela

    def erroEstouro(self, esperado):
        self.POSICAO_TOKEN_ERRO.append((-1, esperado))
        return "ERRO: estourou o numero de tokens antes do token esperado (" + esperado + ")!"

    def erroTokenInesperado(self, tokenInesperado, tokenEsperado, i):
        self.POSICAO_TOKEN_ERRO.append((i, tokenEsperado))
        return "ERRO: inesperado token " + str(tokenInesperado) + ". Esperado <" + str(tokenEsperado) + ">!"

    def acabaramOsTokens(self, tokens, i):
        return i >= len(tokens)


    def eUmQualifiedIdentifier(self, tokens, i):
        while((not self.acabaramOsTokens(tokens, i)) and
            (tokens[i].tipoToken == TipoToken.Identificador)):
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                return True
            if(tokens[i].tipoToken == TipoToken.SepPonto):
                i += 1
            else:
                return True
        if(self.acabaramOsTokens(tokens, i)):
            return False
        return False

    def eUmModifier(self, token):
        if(token.tipoToken == TipoToken.PCPublic):
            return True
        if(token.tipoToken == TipoToken.PCPrivate):
            return True
        if(token.tipoToken == TipoToken.PCProtected):
            return True
        if(token.tipoToken == TipoToken.PCStatic):
            return True
        if(token.tipoToken == TipoToken.PCAbstract):
            return True
        return False

    def eUmBasicType(self, token):
        if(token.tipoToken == TipoToken.PCBoolean):
            return True
        if(token.tipoToken == TipoToken.PCChar):
            return True
        if(token.tipoToken == TipoToken.PCInt):
            return True
        return False

    def eUmReferenceType(self, tokens, i):
        if(self.eUmBasicType(tokens[i])):
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                return False
            if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
                return False
        elif(self.eUmQualifiedIdentifier(tokens, i)):
            i = self.qualifiedIdentifier(tokens, i, None)
            if((self.acabaramOsTokens(tokens, i)) or
            (tokens[i].tipoToken != TipoToken.SepAbreColchetes)):
                return True
        else:
            return False
        while((not self.acabaramOsTokens(tokens, i)) and
            (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                return False
            if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
                return False
            i += 1
        return True

    def eUmType(self, tokens, i):
        return (self.eUmBasicType(tokens[i]) or self.eUmReferenceType(tokens, i))

    def eUmLiteral(self, token):
        if(token.tipoToken == TipoToken.IntLiteral):
            return True
        if(token.tipoToken == TipoToken.CharLiteral):
            return True
        if(token.tipoToken == TipoToken.StringLiteral):
            return True
        if(token.tipoToken == TipoToken.PCTrue):
            return True
        if(token.tipoToken == TipoToken.PCFalse):
            return True
        if(token.tipoToken == TipoToken.PCNull):
            return True
        return False

    def addArvoreSintatica(self, pai, nomeFilho):
        if(pai == None):
            return None
        filho = Noh(nomeFilho)
        self.ARVORE_SINTATICA.addFilho(pai, filho)
        return filho

    def compilationUnit(self, tokens, i):
        noh = Noh("compilationUnit")
        self.ARVORE_SINTATICA.addRaiz(noh)

        if(self.acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.PCPackage):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.qualifiedIdentifier(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepPontoVirgula")
                return i
            if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
            else:
                self.erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
        if(self.acabaramOsTokens(tokens, i)):
            return i
        while((not self.acabaramOsTokens(tokens, i)) and
            (tokens[i].tipoToken == TipoToken.PCImport)):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.qualifiedIdentifier(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepPontoVirgula")
                return i
            if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
            else:
                self.erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
        while(not self.acabaramOsTokens(tokens, i)):
            i = self.typeDeclaration(tokens, i, noh)

        if(self.acabaramOsTokens(tokens, i)):
            return i
        self.erroTokenInesperado(tokens[i], "fim de arquivo", i)


    def qualifiedIdentifier(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.qualifiedIdentifier")
        if(self.acabaramOsTokens(tokens, i)):
            return i
        while((not self.acabaramOsTokens(tokens, i)) and
            (tokens[i].tipoToken == TipoToken.Identificador)):
            self.addArvoreSintatica(noh, str(tokens[i]))

            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                return i
            if(tokens[i].tipoToken == TipoToken.SepPonto):
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
            else:
                return i
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("Identificador")
            return i
        self.erroTokenInesperado(tokens[i], "Identificador", i)
        if(self.acabaramOsTokens(tokens, i + 1)):
            return i
        return i

    def typeDeclaration(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.typeDeclaration")
        i = self.modifiers(tokens, i, noh)
        i = self.classDeclaration(tokens, i, noh)
        return i

    def modifiers(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "modifiers")
        while((not self.acabaramOsTokens(tokens, i)) and
            (self.eUmModifier(tokens[i]))):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
        return i

    def classDeclaration(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.classDeclaration")

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("PCClass")
            return i
        if(tokens[i].tipoToken != TipoToken.PCClass):
            self.erroTokenInesperado(tokens[i], "PCClass", i)
            return i + 1

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("Identificador")
            return i
        if(tokens[i].tipoToken != TipoToken.Identificador):
            self.erroTokenInesperado(tokens[i], "Identificador", i)
            return i + 1

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepAbreChaves")
            return i
        if(tokens[i].tipoToken == TipoToken.PCExtends):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1

            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("Identificador")
                return i + 1
            i = self.qualifiedIdentifier(tokens, i, noh)


        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepAbreChaves")
            return i

        i = self.classBody(tokens, i, noh)
        return i

    def classBody(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "classBody")

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepAbreChaves")
            return i
        if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
            self.erroTokenInesperado(tokens[i], "SepAbreChaves", i)
            return i + 1

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepFechaChaves")
            return i
        while((not self.acabaramOsTokens(tokens, i)) and
            (tokens[i].tipoToken != TipoToken.SepFechaChaves)):
            if(self.eUmModifier(tokens[i])):
                i = self.modifiers(tokens, i, noh)
            else:
                self.erroTokenInesperado(tokens[i], "um modifier", i)
                i += 1
                continue
            i = self.memberDecl(tokens, i, noh)

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepFechaChaves")
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        return i + 1

    def memberDecl(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "memberDecl")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<primeiro token de memberDecl>")
            return i

        #Construtor
        if(tokens[i].tipoToken == TipoToken.Identificador):
            if((not self.acabaramOsTokens(tokens, i + 1)) and
            (tokens[i + 1].tipoToken == TipoToken.SepAbreParenteses)):
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                i = self.formalParamaters(tokens, i, noh)
                i = self.block(tokens, i, noh)
                return i

        if(tokens[i].tipoToken == TipoToken.PCVoid):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("Identificador")
                return i
        else:
            i = self.typeOfDeclaration(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("Identificador")
                return i
            if(tokens[i].tipoToken == TipoToken.Identificador):
                j = i + 1
                if(not self.acabaramOsTokens(tokens, j)):
                    if(tokens[j].tipoToken != TipoToken.SepAbreParenteses):
                        i = self.variableDeclarators(tokens, i, noh)
                        if(self.acabaramOsTokens(tokens, i)):
                            self.erroEstouro("SepPontoVirgula")
                            return i
                        if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
                            self.erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
                            return i
                        self.addArvoreSintatica(noh, str(tokens[i]))
                        i += 1
                        return i

        if(tokens[i].tipoToken == TipoToken.Identificador):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
        i = self.formalParamaters(tokens, i, noh)

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<primeiro do bloco> ou SepPontoVirgula")
            return i

        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            return i

        i = self.block(tokens, i, noh)
        return i

    def block(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.block")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepAbreChaves")
            return i
        if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
            self.erroTokenInesperado(tokens[i], "SepAbreChaves", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepFechaChaves")
            return i

        while(tokens[i].tipoToken != TipoToken.SepFechaChaves):
            i = self.blockStatement(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepFechaChaves")
                return i

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepFechaChaves")
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i

    #PROVAVELMENTE ESTA BOSTA ESTA MUITO ERRADA DEMAIS
    def blockStatement(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "blockStatement")

        j = i
        if(not self.acabaramOsTokens(tokens, j)):
            entrou = False
            if(tokens[j].tipoToken == TipoToken.Identificador):
                k = j
                j = self.qualifiedIdentifier(tokens, j, noh)
                if(tokens[j].tipoToken == TipoToken.SepAbreColchetes):
                    j = self.typeOfDeclaration(tokens, k, noh)
                if(tokens[j].tipoToken == TipoToken.Identificador):
                    entrou = True
            elif(self.eUmBasicType(tokens[j])):
                j = self.typeOfDeclaration(tokens, j, noh)
                if(tokens[j].tipoToken == TipoToken.Identificador):
                    entrou = True
            if(entrou):
                i = self.localVariableDeclarationStatement(tokens, i, noh)
                return i
            i = self.statement(tokens, i, noh)
            return i
        return i

    def statement(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "statement")

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<token de statement>")
            return i

        if(tokens[i].tipoToken == TipoToken.SepAbreChaves):
            i = self.block(tokens, i, noh)
            return i
        #TEM PARADA ERRADA NISSO AE IRMAO
        # if(tokens[i].tipoToken == TipoToken.Identificador):
            #VERIFICAR DEPOIS
            # i += 1
            # if(self.acabaramOsTokens(tokens, i)):
            #     self.erroEstouro(":"))
            #     return i
            # i += 1
            # i = self.statement(tokens, i)
            # return i
        #ACHO QUE A PARADA ACABA NO RETURN AE DE CIMA IRMAO,
        #MAS NO FIM TA TUDO ERRADO IRMAO

        if(tokens[i].tipoToken == TipoToken.PCIf):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.parExpression(tokens, i, noh)
            i = self.statement(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                return i
            if(tokens[i].tipoToken == TipoToken.PCElse):
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                i = self.statement(tokens, i, noh)
            return i

        if(tokens[i].tipoToken == TipoToken.PCWhile):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.parExpression(tokens, i, noh)
            i = self.statement(tokens, i, noh)
            return i

        if(tokens[i].tipoToken == TipoToken.PCReturn):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepPontoVirgula")
                return i
            if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
                i = self.expression(tokens, i, noh)
                if(self.acabaramOsTokens(tokens, i)):
                    self.erroEstouro("SepPontoVirgula")
                    return i
                if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
                    self.erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
                    return i
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1  #PODE DAR ERRADO ISSO AQUI (TA ERRADO)
            return i

        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            return i

        i = self.statementExpression(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepPontoVirgula")
            return i
        if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
            self.erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
            return i
        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i


    def formalParamaters(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.formalParamaters")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepAbreParenteses")
            return i
        if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
            self.erroTokenInesperado(tokens[i], "SepAbreParenteses", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepFechaParenteses")
            return i
        if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
            i = self.formalParamater(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepFechaParenteses")
                return i
            while(tokens[i].tipoToken == TipoToken.SepVirgula):
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                i = self.formalParamater(tokens, i, noh)
                if(self.acabaramOsTokens(tokens, i)):
                    self.erroEstouro("<token de formalParamater>")
                    return i

        if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
            self.erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i

    def formalParamater(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.formalParamater")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<token de type>")
            return i
        i = self.typeOfDeclaration(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("Identificador")
            return i
        if(tokens[i].tipoToken != TipoToken.Identificador):
            self.erroTokenInesperado(tokens[i], "Identificador", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i

    def parExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "parExpression")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepAbreParenteses")
            return i
        if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
            self.erroTokenInesperado(tokens[i], "SepAbreParenteses", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = self.expression(tokens, i, noh)

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepFechaParenteses")
            return i

        if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
            self.erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i

    def localVariableDeclarationStatement(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.localVariableDeclarationStatement")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<token que define um type>")
            return i
        i = self.typeOfDeclaration(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<token de self.variableDeclarators>")
            return i
        i = self.variableDeclarators(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepPontoVirgula")
            return i
        if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
            self.erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i

    def variableDeclarators(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.variableDeclarators")
        i = self.variableDeclarator(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            return i
        while(tokens[i].tipoToken == TipoToken.SepVirgula):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("<token de self.variableDeclarator>")
                return i
            i = self.variableDeclarator(tokens, i, noh)
        return i

    def variableDeclarator(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.variableDeclarator")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("Identificador")
            return i
        if(tokens[i].tipoToken != TipoToken.Identificador):
            self.erroTokenInesperado(tokens[i], "Identificador", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))

        # Adiciona na tabela de sym
        print("****")
        print(tokens[i])
        print(self.TABELA)
        print("****")

        self.TABELA.tabela[tokens[i].linhaTabela].escopo = self.ESCOPO

        i += 1
        if(self.acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.OpAtribuicao):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.variableInitializer(tokens, i, noh)
        return i

    def variableInitializer(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "variableInitializer")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<token de variableInitializer>")
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreChaves):
            global ESCOPO
            self.ESCOPO += 1
            i = self.arrayInitializer(tokens, i, noh)
            return i
        i = self.expression(tokens, i, noh)
        return i

    def arrayInitializer(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "arrayInitializer")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepAbreChaves")
            return i

        if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
            self.erroTokenInesperado(tokens[i], "SepAbreChaves", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepFechaChaves")
            return i
        if(tokens[i].tipoToken == TipoToken.SepFechaChaves):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            return i

        i = self.variableInitializer(tokens, i, noh)

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepFechaChaves")
            return i
        while(tokens[i].tipoToken == TipoToken.SepVirgula):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.variableInitializer(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepFechaChaves")
                return i

        if(tokens[i].tipoToken != TipoToken.SepFechaChaves):
            self.erroTokenInesperado(tokens[i], "SepFechaChaves", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i

    def typeOfDeclaration(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "type")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<primeiro token do tipo>")
            return i
        if(self.eUmBasicType(tokens[i])):
            if(not self.acabaramOsTokens(tokens, i + 1)):
                if(tokens[i + 1].tipoToken == TipoToken.SepAbreColchetes):
                    i = self.referenceType(tokens, i, noh)
                    return i
            i = self.basicType(tokens, i, noh)
            return i
        i = self.referenceType(tokens, i, noh)
        return i

    def basicType(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "basicType")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<PCBoolean, PCChar ou PCInt>")
            return i
        if(not self.eUmBasicType(tokens[i])):
            self.erroTokenInesperado(tokens[i], "<PCBoolean, PCChar ou PCInt>", i)
            return i
        self.addArvoreSintatica(noh, str(tokens[i]))
        return i + 1

    def referenceType(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.referenceType")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<PCBoolean, PCChar ou PCInt>")
            return i
        if(self.eUmBasicType(tokens[i])):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepAbreColchetes")
                return i
            if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
                self.erroTokenInesperado(tokens[i], "SepAbreColchetes", i)
                return i

        else:
            i = self.qualifiedIdentifier(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                return i
            if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
                return i
        while((not self.acabaramOsTokens(tokens, i)) and
            (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepFechaColchetes")
                return i
            if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
                self.erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
                return i

            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
        return i

    def arguments(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.arguments")

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepAbreParenteses")
            return i
        if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
            self.erroTokenInesperado(tokens[i], "SepAbreParenteses", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepFechaParenteses")
            return i
        if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
            i = self.expression(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepFechaParenteses")
                return i
            while(tokens[i].tipoToken == TipoToken.SepVirgula):
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                i = self.expression(tokens, i, noh)
                if(self.acabaramOsTokens(tokens, i)):
                    self.erroEstouro("SepFechaParenteses")
                    return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i

    def statementExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.statementExpression")
        i = self.expression(tokens, i, noh)
        return i

    def expression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.expression")
        i = self.assignmentExpression(tokens, i, noh)
        return i

    def assignmentExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.assignmentExpression")
        i = self.conditionalAndExpression(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            return i
        if((tokens[i].tipoToken == TipoToken.OpAtribuicao) or
        (tokens[i].tipoToken == TipoToken.OpSomaAtribuicao)):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.assignmentExpression(tokens, i, noh)
        return i

    def conditionalAndExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "conditionalAndExpression")
        i = self.equalityExpression(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            return i
        while(tokens[i].tipoToken == TipoToken.OpAnd):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.equalityExpression(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                return i
        return i

    def equalityExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "equalityExpression")
        i = self.relationalExpression(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            return i
        while(tokens[i].tipoToken == TipoToken.OpIgualdade):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.relationalExpression(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                return i
        return i

    def relationalExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.relationalExpression")
        i = self.additiveExpression(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            return i
        if((tokens[i].tipoToken == TipoToken.OpMaior) or
        (tokens[i].tipoToken == TipoToken.OpMenorIgual)):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.additiveExpression(tokens, i, noh)
            return i
        if(tokens[i].tipoToken == TipoToken.PCInstanceOf):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.referenceType(tokens, i, noh)
            return i
        return i

    def additiveExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "self.additiveExpression")
        i = self.multiplicativeExpression(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            return i
        while((tokens[i].tipoToken == TipoToken.OpSoma) or
            (tokens[i].tipoToken == TipoToken.OpMenos)):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.multiplicativeExpression(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                return i
        return i

    def multiplicativeExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "multiplicativeExpression")
        i = self.unaryExpression(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            return i
        while(tokens[i].tipoToken == TipoToken.OpMultiplicacao):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.unaryExpression(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                return i
        return i

    def unaryExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "unaryExpression")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("expressao unaria")
            return i
        if(tokens[i].tipoToken == TipoToken.OpIncremento):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.unaryExpression(tokens, i, noh)
            return i

        if(tokens[i].tipoToken == TipoToken.OpMenos):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.unaryExpression(tokens, i, noh)
            return i
        i = self.simpleUnaryExpression(tokens, i, noh)
        return i

    # PROBLEMA!!!!!!!
    # DIFERENCIAR self.parExpression
    #    de (self.referenceType) self.simpleUnaryExpression!!!!!!
    def simpleUnaryExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "simpleUnaryExpression")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("expressao unaria simples")
            return i
        if(tokens[i].tipoToken == TipoToken.OpNot):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.unaryExpression(tokens, i, noh)
            return i

        #ESSA PARTE DO CODIGO TA ORRIVEL MAS FODACE
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("self.basicType ou self.referenceType")
                return i
            if(self.eUmBasicType(tokens[i])):
                self.addArvoreSintatica(noh, str(tokens[i-1].tipoToken))
                j = self.basicType(tokens, i, noh)
                if(self.acabaramOsTokens(tokens, j)):
                    self.erroEstouro("SepFechaParenteses")
                    return i
                if(tokens[j].tipoToken == TipoToken.SepAbreColchetes):
                    i = self.referenceType(tokens, i, noh)
                    if(self.acabaramOsTokens(tokens, i)):
                        self.erroEstouro("SepFechaParenteses")
                        return i
                    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
                        self.erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
                    self.addArvoreSintatica(noh, str(tokens[i]))
                    i += 1
                    i = self.simpleUnaryExpression(tokens, i, noh)
                    return i
                else:
                    i = j
                    if(self.acabaramOsTokens(tokens, i)):
                        self.erroEstouro("SepFechaParenteses")
                        return i
                    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
                        self.erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
                    self.addArvoreSintatica(noh, str(tokens[i]))
                    i += 1
                    i = self.unaryExpression(tokens, i, noh)
                    return i
            elif(self.eUmReferenceType(tokens, i)):
                self.addArvoreSintatica(noh, str(tokens[i-1].tipoToken))
                self.eUmReferenceType(tokens, i)

                i = self.referenceType(tokens, i, noh)
                if(self.acabaramOsTokens(tokens, j)):
                    self.erroEstouro("SepFechaParenteses")
                    return i
                if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
                    self.erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                i = self.simpleUnaryExpression(tokens, i, noh)
                return i
            else:
                i -= 1
                i = self.postfixExpression(tokens, i, noh)
                return i

        i = self.postfixExpression(tokens, i, noh)
        return i

    def postfixExpression(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "postfixExpression")
        i = self.primary(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            return i
        while((tokens[i].tipoToken == TipoToken.SepPonto) or
            (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):
            i = self.selector(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                return i
        while(tokens[i].tipoToken == TipoToken.OpDecremento):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                return i
        return i

    def selector(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "selector")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepPonto")
            return i
        if(tokens[i].tipoToken == TipoToken.SepPonto):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.qualifiedIdentifier(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                return i
            if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                i = self.arguments(tokens, i, noh)
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreColchetes):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.expression(tokens, i, noh)

            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepAbreColchetes")
                return i
            if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
                self.erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
                return i

            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            return i
        return i

    def primary(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "primary")

        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("tokens de self.primary")
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = self.parExpression(tokens, i, noh)
            return i
        if(tokens[i].tipoToken == TipoToken.PCThis):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                return i
            if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                i = self.arguments(tokens, i, noh)
                return i
            return i
        if(tokens[i].tipoToken == TipoToken.PCSuper):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("argumentos")
                return i
            if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                i = self.arguments(tokens, i, noh)
                return i
            if(tokens[i].tipoToken == TipoToken.SepPonto):
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                if(self.acabaramOsTokens(tokens, i)):
                    return i
                if(tokens[i].tipoToken != TipoToken.Identificador):
                    self.erroTokenInesperado(tokens[i], "Identificador", i)
                    return i
                print("AQUI?", tokens[i])
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                if(self.acabaramOsTokens(tokens, i)):
                    return i
                if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                    i = self.arguments(tokens, i, noh)
                return i
            self.erroTokenInesperado(tokens[i], "SepPonto ou argumentos", i)
            return i + 1
        if(self.eUmLiteral(tokens[i])):
            i = self.literal(tokens, i, noh)
            return i
        if(tokens[i].tipoToken == TipoToken.PCNew):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = self.creator(tokens, i, noh)
            return i
        j = i
        i = self.qualifiedIdentifier(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = self.arguments(tokens, i, noh)
        if(j == i):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
        return i

    def creator(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "creator")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<primeiro de creator>")
            return i
        if(self.eUmType(tokens, i)):
            if(self.eUmReferenceType(tokens, i)):
                i = self.referenceType(tokens, i, noh)
                if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                    i = self.arguments(tokens, i, noh)
                    return i
                i = self.arrayInitializer(tokens, i, noh)
                return i
            i = self.basicType(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("argumentos")
                return i
            if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                i = self.arguments(tokens, i, noh)
                return i
            if(tokens[i].tipoToken == TipoToken.SepAbreColchetes):
                i = self.newArrayDeclarator(tokens, i, noh)
                return i
        elif(self.eUmQualifiedIdentifier(tokens, i)):
            i = self.qualifiedIdentifier(tokens, i, noh)
            if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                i = self.arguments(tokens, i, noh)
                return i
            i = self.newArrayDeclarator(tokens, i, noh)
            return i
        self.erroTokenInesperado(tokens[i], "token de type", i)
        return i

    def newArrayDeclarator(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "newArrayDeclarator")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepAbreColchetes")
            return i
        if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
            self.erroTokenInesperado(tokens[i], "SepAbreColchetes", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = self.expression(tokens, i, noh)
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("SepFechaColchetes")
            return i
        if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
            self.erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
            return i

        self.addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        while((not self.acabaramOsTokens(tokens, i)) and
            (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):

            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepFechaColchetes")
                return i
            if(tokens[i].tipoToken == TipoToken.SepFechaColchetes):
                self.addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                while((not self.acabaramOsTokens(tokens, i)) and
                    (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):

                    self.addArvoreSintatica(noh, str(tokens[i]))
                    i += 1
                    if(self.acabaramOsTokens(tokens, i)):
                        self.erroEstouro("SepFechaColchetes")
                        return i
                    if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
                        self.erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
                        return i
                    self.addArvoreSintatica(noh, str(tokens[i]))
                    i += 1
                return i

            i = self.expression(tokens, i, noh)
            if(self.acabaramOsTokens(tokens, i)):
                self.erroEstouro("SepFechaColchetes")
                return i
            if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
                self.erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
                return i
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
        return i

    def literal(self, tokens, i, pai):
        noh = self.addArvoreSintatica(pai, "literal")
        if(self.acabaramOsTokens(tokens, i)):
            self.erroEstouro("<valor literal>")
            return i
        if(self.eUmLiteral(tokens[i])):
            self.addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            return i
        self.erroTokenInesperado(tokens[i], "valor literal", i)
        return i + 1


def main(tokens, tabela):
    analisadorSintatico = AnalisadorSintatico(tabela)

    # print("=====================================")
    # for token in tokens:
    #     print(token)
    # print("=====================================")
    i = analisadorSintatico.compilationUnit(tokens, 0)
    print("______ARVORE_____")
    retorno = analisadorSintatico.ARVORE_SINTATICA.percorreArvore()
    print(retorno)
    file = open("AnalisadorSintatico/arquivoParaGraphViz", "w")
    file.write(retorno)
    print("_______FIM ARVORE_______")
    # print("______ARVORE ZUADA______")
    # self.ARVORE_SINTATICA.percorrePorNivel()
    # print("____FIM ARVORE ZUADA____")
    return analisadorSintatico.POSICAO_TOKEN_ERRO
