
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Gerenciador import TipoToken
from AnalisadorSintatico.ArvoreSintatica import *

POSICAO_TOKEN_ERRO = []
ARVORE_SINTATICA = ArvoreSintatica()

def erroEstouro(esperado):
    POSICAO_TOKEN_ERRO.append((-1, esperado))
    return "ERRO: estourou o numero de tokens antes do token esperado (" + esperado + ")!"

def erroTokenInesperado(tokenInesperado, tokenEsperado, i):
    POSICAO_TOKEN_ERRO.append((i, tokenEsperado))
    return "ERRO: inesperado token " + str(tokenInesperado) + ". Esperado <" + str(tokenEsperado) + ">!"

def acabaramOsTokens(tokens, i):
    return i >= len(tokens)


def eUmQualifiedIdentifier(tokens, i):
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken == TipoToken.Identificador)):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            return True
        if(tokens[i].tipoToken == TipoToken.SepPonto):
            i += 1
        else:
            return True
    if(acabaramOsTokens(tokens, i)):
        return False
    return False

def eUmModifier(token):
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

def eUmBasicType(token):
    if(token.tipoToken == TipoToken.PCBoolean):
        return True
    if(token.tipoToken == TipoToken.PCChar):
        return True
    if(token.tipoToken == TipoToken.PCInt):
        return True
    return False

def eUmReferenceType(tokens, i):
    if(eUmBasicType(tokens[i])):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            return False
        if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
            return False
    elif(eUmQualifiedIdentifier(tokens, i)):
        i = qualifiedIdentifier(tokens, i, None)
        if((acabaramOsTokens(tokens, i)) or
           (tokens[i].tipoToken != TipoToken.SepAbreColchetes)):
            return True
    else:
        return False
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            return False
        if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
            return False
        i += 1
    return True

def eUmType(tokens, i):
    return (eUmBasicType(tokens[i]) or eUmReferenceType(tokens, i))

def eUmLiteral(token):
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

def addArvoreSintatica(pai, nomeFilho):
    if(pai == None):
        return None
    filho = Noh(nomeFilho)
    ARVORE_SINTATICA.addFilho(pai, filho)
    return filho

def compilationUnit(tokens, i):
    noh = Noh("compilationUnit")
    ARVORE_SINTATICA.addRaiz(noh)

    if(acabaramOsTokens(tokens, i)):
        return i
    if(tokens[i].tipoToken == TipoToken.PCPackage):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = qualifiedIdentifier(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepPontoVirgula")
            return i
        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
        else:
            erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
    if(acabaramOsTokens(tokens, i)):
        return i
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken == TipoToken.PCImport)):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = qualifiedIdentifier(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepPontoVirgula")
            return i
        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
        else:
            erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
    while(not acabaramOsTokens(tokens, i)):
        i = typeDeclaration(tokens, i, noh)

    if(acabaramOsTokens(tokens, i)):
        return i
    erroTokenInesperado(tokens[i], "fim de arquivo", i)


def qualifiedIdentifier(tokens, i, pai):
    noh = addArvoreSintatica(pai, "qualifiedIdentifier")
    if(acabaramOsTokens(tokens, i)):
        return i
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken == TipoToken.Identificador)):
        addArvoreSintatica(noh, str(tokens[i]))

        i += 1
        if(acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.SepPonto):
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
        else:
            return i
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("Identificador")
        return i
    erroTokenInesperado(tokens[i], "Identificador", i)
    if(acabaramOsTokens(tokens, i + 1)):
        return i
    return i

def typeDeclaration(tokens, i, pai):
    noh = addArvoreSintatica(pai, "typeDeclaration")
    i = modifiers(tokens, i, noh)
    i = classDeclaration(tokens, i, noh)
    return i

def modifiers(tokens, i, pai):
    noh = addArvoreSintatica(pai, "modifiers")
    while((not acabaramOsTokens(tokens, i)) and
          (eUmModifier(tokens[i]))):
          addArvoreSintatica(noh, str(tokens[i]))
          i += 1
    return i

def classDeclaration(tokens, i, pai):
    noh = addArvoreSintatica(pai, "classDeclaration")

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("PCClass")
        return i
    if(tokens[i].tipoToken != TipoToken.PCClass):
        erroTokenInesperado(tokens[i], "PCClass", i)
        return i + 1

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("Identificador")
        return i
    if(tokens[i].tipoToken != TipoToken.Identificador):
        erroTokenInesperado(tokens[i], "Identificador", i)
        return i + 1

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreChaves")
        return i
    if(tokens[i].tipoToken == TipoToken.PCExtends):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1

        if(acabaramOsTokens(tokens, i)):
            erroEstouro("Identificador")
            return i + 1
        i = qualifiedIdentifier(tokens, i, noh)


    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreChaves")
        return i

    i = classBody(tokens, i, noh)
    return i

def classBody(tokens, i, pai):
    noh = addArvoreSintatica(pai, "classBody")

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreChaves")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
        erroTokenInesperado(tokens[i], "SepAbreChaves", i)
        return i + 1

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken != TipoToken.SepFechaChaves)):
        if(eUmModifier(tokens[i])):
            i = modifiers(tokens, i, noh)
        else:
            erroTokenInesperado(tokens[i], "um modifier", i)
            i += 1
            continue
        i = memberDecl(tokens, i, noh)

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    return i + 1

def memberDecl(tokens, i, pai):
    noh = addArvoreSintatica(pai, "memberDecl")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<primeiro token de memberDecl>")
        return i

    #Construtor
    if(tokens[i].tipoToken == TipoToken.Identificador):
        if((not acabaramOsTokens(tokens, i + 1)) and
           (tokens[i + 1].tipoToken == TipoToken.SepAbreParenteses)):
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = formalParamaters(tokens, i, noh)
            i = block(tokens, i, noh)
            return i

    if(tokens[i].tipoToken == TipoToken.PCVoid):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("Identificador")
            return i
    else:
        i = typeOfDeclaration(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("Identificador")
            return i
        if(tokens[i].tipoToken == TipoToken.Identificador):
            j = i + 1
            if(not acabaramOsTokens(tokens, j)):
                if(tokens[j].tipoToken != TipoToken.SepAbreParenteses):
                    i = variableDeclarators(tokens, i, noh)
                    if(acabaramOsTokens(tokens, i)):
                        erroEstouro("SepPontoVirgula")
                        return i
                    if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
                        erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
                        return i
                    addArvoreSintatica(noh, str(tokens[i]))
                    i += 1
                    return i

    if(tokens[i].tipoToken == TipoToken.Identificador):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
    i = formalParamaters(tokens, i, noh)

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<primeiro do bloco> ou SepPontoVirgula")
        return i

    if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i

    i = block(tokens, i, noh)
    return i

def block(tokens, i, pai):
    noh = addArvoreSintatica(pai, "block")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreChaves")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
        erroTokenInesperado(tokens[i], "SepAbreChaves", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i

    while(tokens[i].tipoToken != TipoToken.SepFechaChaves):
        i = blockStatement(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaChaves")
            return i

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    return i

#PROVAVELMENTE ESTA BOSTA ESTA MUITO ERRADA DEMAIS
def blockStatement(tokens, i, pai):
    noh = addArvoreSintatica(pai, "blockStatement")

    j = i
    if(not acabaramOsTokens(tokens, j)):
        entrou = False
        if(tokens[j].tipoToken == TipoToken.Identificador):
            k = j
            j = qualifiedIdentifier(tokens, j, noh)
            if(tokens[j].tipoToken == TipoToken.SepAbreColchetes):
                j = typeOfDeclaration(tokens, k, noh)
            if(tokens[j].tipoToken == TipoToken.Identificador):
                entrou = True
        elif(eUmBasicType(tokens[j])):
            j = typeOfDeclaration(tokens, j, noh)
            if(tokens[j].tipoToken == TipoToken.Identificador):
                entrou = True
        if(entrou):
            i = localVariableDeclarationStatement(tokens, i, noh)
            return i
        i = statement(tokens, i, noh)
        return i
    return i

def statement(tokens, i, pai):
    noh = addArvoreSintatica(pai, "statement")

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<token de statement>")
        return i

    if(tokens[i].tipoToken == TipoToken.SepAbreChaves):
        i = block(tokens, i, noh)
        return i
    #TEM PARADA ERRADA NISSO AE IRMAO
    # if(tokens[i].tipoToken == TipoToken.Identificador):
        #VERIFICAR DEPOIS
        # i += 1
        # if(acabaramOsTokens(tokens, i)):
        #     erroEstouro(":"))
        #     return i
        # i += 1
        # i = statement(tokens, i)
        # return i
    #ACHO QUE A PARADA ACABA NO RETURN AE DE CIMA IRMAO,
    #MAS NO FIM TA TUDO ERRADO IRMAO

    if(tokens[i].tipoToken == TipoToken.PCIf):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = parExpression(tokens, i, noh)
        i = statement(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.PCElse):
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = statement(tokens, i, noh)
        return i

    if(tokens[i].tipoToken == TipoToken.PCWhile):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = parExpression(tokens, i, noh)
        i = statement(tokens, i, noh)
        return i

    if(tokens[i].tipoToken == TipoToken.PCReturn):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepPontoVirgula")
            return i
        if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
            i = expression(tokens, i, noh)
            if(acabaramOsTokens(tokens, i)):
                erroEstouro("SepPontoVirgula")
                return i
            if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
                erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
                return i
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1  #PODE DAR ERRADO ISSO AQUI (TA ERRADO)
        return i

    if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i

    i = statementExpression(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepPontoVirgula")
        return i
    if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
        erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
        return i
    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    return i


def formalParamaters(tokens, i, pai):
    noh = addArvoreSintatica(pai, "formalParamaters")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreParenteses")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
        erroTokenInesperado(tokens[i], "SepAbreParenteses", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaParenteses")
        return i
    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        i = formalParamater(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaParenteses")
            return i
        while(tokens[i].tipoToken == TipoToken.SepVirgula):
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = formalParamater(tokens, i, noh)
            if(acabaramOsTokens(tokens, i)):
                erroEstouro("<token de formalParamater>")
                return i

    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    return i

def formalParamater(tokens, i, pai):
    noh = addArvoreSintatica(pai, "formalParamater")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<token de type>")
        return i
    i = typeOfDeclaration(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("Identificador")
        return i
    if(tokens[i].tipoToken != TipoToken.Identificador):
        erroTokenInesperado(tokens[i], "Identificador", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    return i

def parExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "parExpression")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreParenteses")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
        erroTokenInesperado(tokens[i], "SepAbreParenteses", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    i = expression(tokens, i, noh)

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaParenteses")
        return i

    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    return i

def localVariableDeclarationStatement(tokens, i, pai):
    noh = addArvoreSintatica(pai, "localVariableDeclarationStatement")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<token que define um type>")
        return i
    i = typeOfDeclaration(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<token de variableDeclarators>")
        return i
    i = variableDeclarators(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepPontoVirgula")
        return i
    if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
        erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    return i

def variableDeclarators(tokens, i, pai):
    noh = addArvoreSintatica(pai, "variableDeclarators")
    i = variableDeclarator(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        return i
    while(tokens[i].tipoToken == TipoToken.SepVirgula):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("<token de variableDeclarator>")
            return i
        i = variableDeclarator(tokens, i, noh)
    return i

def variableDeclarator(tokens, i, pai):
    noh = addArvoreSintatica(pai, "variableDeclarator")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("Identificador")
        return i
    if(tokens[i].tipoToken != TipoToken.Identificador):
        erroTokenInesperado(tokens[i], "Identificador", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    if(acabaramOsTokens(tokens, i)):
        return i
    if(tokens[i].tipoToken == TipoToken.OpAtribuicao):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = variableInitializer(tokens, i, noh)
    return i

def variableInitializer(tokens, i, pai):
    noh = addArvoreSintatica(pai, "variableInitializer")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<token de variableInitializer>")
        return i
    if(tokens[i].tipoToken == TipoToken.SepAbreChaves):
        i = arrayInitializer(tokens, i, noh)
        return i
    i = expression(tokens, i, noh)
    return i

def arrayInitializer(tokens, i, pai):
    noh = addArvoreSintatica(pai, "arrayInitializer")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreChaves")
        return i

    if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
        erroTokenInesperado(tokens[i], "SepAbreChaves", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i
    if(tokens[i].tipoToken == TipoToken.SepFechaChaves):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i

    i = variableInitializer(tokens, i, noh)

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i
    while(tokens[i].tipoToken == TipoToken.SepVirgula):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = variableInitializer(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaChaves")
            return i

    if(tokens[i].tipoToken != TipoToken.SepFechaChaves):
        erroTokenInesperado(tokens[i], "SepFechaChaves", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    return i

def typeOfDeclaration(tokens, i, pai):
    noh = addArvoreSintatica(pai, "type")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<primeiro token do tipo>")
        return i
    if(eUmBasicType(tokens[i])):
        if(not acabaramOsTokens(tokens, i + 1)):
            if(tokens[i + 1].tipoToken == TipoToken.SepAbreColchetes):
                i = referenceType(tokens, i, noh)
                return i
        i = basicType(tokens, i, noh)
        return i
    i = referenceType(tokens, i, noh)
    return i

def basicType(tokens, i, pai):
    noh = addArvoreSintatica(pai, "basicType")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<PCBoolean, PCChar ou PCInt>")
        return i
    if(not eUmBasicType(tokens[i])):
        erroTokenInesperado(tokens[i], "<PCBoolean, PCChar ou PCInt>", i)
        return i
    addArvoreSintatica(noh, str(tokens[i]))
    return i + 1

def referenceType(tokens, i, pai):
    noh = addArvoreSintatica(pai, "referenceType")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<PCBoolean, PCChar ou PCInt>")
        return i
    if(eUmBasicType(tokens[i])):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepAbreColchetes")
            return i
        if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
            erroTokenInesperado(tokens[i], "SepAbreColchetes", i)
            return i

    else:
        i = qualifiedIdentifier(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
            return i
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaColchetes")
            return i
        if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
            erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
            return i

        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
    return i

def arguments(tokens, i, pai):
    noh = addArvoreSintatica(pai, "arguments")

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreParenteses")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
        erroTokenInesperado(tokens[i], "SepAbreParenteses", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaParenteses")
        return i
    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        i = expression(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaParenteses")
            return i
        while(tokens[i].tipoToken == TipoToken.SepVirgula):
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = expression(tokens, i, noh)
            if(acabaramOsTokens(tokens, i)):
                erroEstouro("SepFechaParenteses")
                return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    return i

def statementExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "statementExpression")
    i = expression(tokens, i, noh)
    return i

def expression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "expression")
    i = assignmentExpression(tokens, i, noh)
    return i

def assignmentExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "assignmentExpression")
    i = conditionalAndExpression(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        return i
    if((tokens[i].tipoToken == TipoToken.OpAtribuicao) or
       (tokens[i].tipoToken == TipoToken.OpSomaAtribuicao)):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = assignmentExpression(tokens, i, noh)
    return i

def conditionalAndExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "conditionalAndExpression")
    i = equalityExpression(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        return i
    while(tokens[i].tipoToken == TipoToken.OpAnd):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = equalityExpression(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            return i
    return i

def equalityExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "equalityExpression")
    i = relationalExpression(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        return i
    while(tokens[i].tipoToken == TipoToken.OpIgualdade):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = relationalExpression(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            return i
    return i

def relationalExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "relationalExpression")
    i = additiveExpression(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        return i
    if((tokens[i].tipoToken == TipoToken.OpMaior) or
       (tokens[i].tipoToken == TipoToken.OpMenorIgual)):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = additiveExpression(tokens, i, noh)
        return i
    if(tokens[i].tipoToken == TipoToken.PCInstanceOf):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = referenceType(tokens, i, noh)
        return i
    return i

def additiveExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "additiveExpression")
    i = multiplicativeExpression(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        return i
    while((tokens[i].tipoToken == TipoToken.OpSoma) or
          (tokens[i].tipoToken == TipoToken.OpMenos)):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = multiplicativeExpression(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            return i
    return i

def multiplicativeExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "multiplicativeExpression")
    i = unaryExpression(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        return i
    while(tokens[i].tipoToken == TipoToken.OpMultiplicacao):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = unaryExpression(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            return i
    return i

def unaryExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "unaryExpression")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("expressao unaria")
        return i
    if(tokens[i].tipoToken == TipoToken.OpIncremento):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = unaryExpression(tokens, i, noh)
        return i

    if(tokens[i].tipoToken == TipoToken.OpMenos):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = unaryExpression(tokens, i, noh)
        return i
    i = simpleUnaryExpression(tokens, i, noh)
    return i

# PROBLEMA!!!!!!!
# DIFERENCIAR parExpression
#    de (referenceType) simpleUnaryExpression!!!!!!
def simpleUnaryExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "simpleUnaryExpression")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("expressao unaria simples")
        return i
    if(tokens[i].tipoToken == TipoToken.OpNot):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = unaryExpression(tokens, i, noh)
        return i

    #ESSA PARTE DO CODIGO TA ORRIVEL MAS FODACE
    if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("basicType ou referenceType")
            return i
        if(eUmBasicType(tokens[i])):
            addArvoreSintatica(noh, str(tokens[i-1].tipoToken))
            j = basicType(tokens, i, noh)
            if(acabaramOsTokens(tokens, j)):
                erroEstouro("SepFechaParenteses")
                return i
            if(tokens[j].tipoToken == TipoToken.SepAbreColchetes):
                i = referenceType(tokens, i, noh)
                if(acabaramOsTokens(tokens, i)):
                    erroEstouro("SepFechaParenteses")
                    return i
                if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
                    erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
                addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                i = simpleUnaryExpression(tokens, i, noh)
                return i
            else:
                i = j
                if(acabaramOsTokens(tokens, i)):
                    erroEstouro("SepFechaParenteses")
                    return i
                if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
                    erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
                addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                i = unaryExpression(tokens, i, noh)
                return i
        elif(eUmReferenceType(tokens, i)):
            addArvoreSintatica(noh, str(tokens[i-1].tipoToken))
            eUmReferenceType(tokens, i)

            i = referenceType(tokens, i, noh)
            if(acabaramOsTokens(tokens, j)):
                erroEstouro("SepFechaParenteses")
                return i
            if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
                erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            i = simpleUnaryExpression(tokens, i, noh)
            return i
        else:
            i -= 1
            i = postfixExpression(tokens, i, noh)
            return i

    i = postfixExpression(tokens, i, noh)
    return i

def postfixExpression(tokens, i, pai):
    noh = addArvoreSintatica(pai, "postfixExpression")
    i = primary(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        return i
    while((tokens[i].tipoToken == TipoToken.SepPonto) or
          (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):
        i = selector(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            return i
    while(tokens[i].tipoToken == TipoToken.OpDecremento):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(acabaramOsTokens(tokens, i)):
            return i
    return i

def selector(tokens, i, pai):
    noh = addArvoreSintatica(pai, "selector")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepPonto")
        return i
    if(tokens[i].tipoToken == TipoToken.SepPonto):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = qualifiedIdentifier(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = arguments(tokens, i, noh)
        return i
    if(tokens[i].tipoToken == TipoToken.SepAbreColchetes):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = expression(tokens, i, noh)

        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepAbreColchetes")
            return i
        if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
            erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
            return i

        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i
    return i

def primary(tokens, i, pai):
    noh = addArvoreSintatica(pai, "primary")

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("tokens de primary")
        return i
    if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
        i = parExpression(tokens, i, noh)
        return i
    if(tokens[i].tipoToken == TipoToken.PCThis):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = arguments(tokens, i, noh)
            return i
        return i
    if(tokens[i].tipoToken == TipoToken.PCSuper):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("argumentos")
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = arguments(tokens, i, noh)
            return i
        if(tokens[i].tipoToken == TipoToken.SepPonto):
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(acabaramOsTokens(tokens, i)):
                return i
            if(tokens[i].tipoToken != TipoToken.Identificador):
                erroTokenInesperado(tokens[i], "Identificador", i)
                return i
            print("AQUI?", tokens[i])
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            if(acabaramOsTokens(tokens, i)):
                return i
            if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                i = arguments(tokens, i, noh)
            return i
        erroTokenInesperado(tokens[i], "SepPonto ou argumentos", i)
        return i + 1
    if(eUmLiteral(tokens[i])):
        i = literal(tokens, i, noh)
        return i
    if(tokens[i].tipoToken == TipoToken.PCNew):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        i = creator(tokens, i, noh)
        return i
    j = i
    i = qualifiedIdentifier(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        return i
    if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
        i = arguments(tokens, i, noh)
    if(j == i):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
    return i

def creator(tokens, i, pai):
    noh = addArvoreSintatica(pai, "creator")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<primeiro de creator>")
        return i
    if(eUmType(tokens, i)):
        if(eUmReferenceType(tokens, i)):
            i = referenceType(tokens, i, noh)
            if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                i = arguments(tokens, i, noh)
                return i
            i = arrayInitializer(tokens, i, noh)
            return i
        i = basicType(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("argumentos")
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = arguments(tokens, i, noh)
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreColchetes):
            i = newArrayDeclarator(tokens, i, noh)
            return i
    elif(eUmQualifiedIdentifier(tokens, i)):
        i = qualifiedIdentifier(tokens, i, noh)
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = arguments(tokens, i, noh)
            return i
        i = newArrayDeclarator(tokens, i, noh)
        return i
    erroTokenInesperado(tokens[i], "token de type", i)
    return i

def newArrayDeclarator(tokens, i, pai):
    noh = addArvoreSintatica(pai, "newArrayDeclarator")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreColchetes")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
        erroTokenInesperado(tokens[i], "SepAbreColchetes", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    i = expression(tokens, i, noh)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaColchetes")
        return i
    if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
        erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
        return i

    addArvoreSintatica(noh, str(tokens[i]))
    i += 1
    while((not acabaramOsTokens(tokens, i)) and
        (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):

        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaColchetes")
            return i
        if(tokens[i].tipoToken == TipoToken.SepFechaColchetes):
            addArvoreSintatica(noh, str(tokens[i]))
            i += 1
            while((not acabaramOsTokens(tokens, i)) and
                (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):

                addArvoreSintatica(noh, str(tokens[i]))
                i += 1
                if(acabaramOsTokens(tokens, i)):
                    erroEstouro("SepFechaColchetes")
                    return i
                if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
                    erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
                    return i
                addArvoreSintatica(noh, str(tokens[i]))
                i += 1
            return i

        i = expression(tokens, i, noh)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaColchetes")
            return i
        if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
            erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
            return i
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
    return i

def literal(tokens, i, pai):
    noh = addArvoreSintatica(pai, "literal")
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<valor literal>")
        return i
    if(eUmLiteral(tokens[i])):
        addArvoreSintatica(noh, str(tokens[i]))
        i += 1
        return i
    erroTokenInesperado(tokens[i], "valor literal", i)
    return i + 1


def main(tokens):
    # print("=====================================")
    # for token in tokens:
    #     print(token)
    # print("=====================================")
    i = compilationUnit(tokens, 0)
    print("______ARVORE_____")
    retorno = ARVORE_SINTATICA.percorreArvore()
    print(retorno)
    file = open("AnalisadorSintatico/arquivoParaGraphViz", "w")
    file.write(retorno)
    print("_______FIM ARVORE_______")
    # print("______ARVORE ZUADA______")
    # ARVORE_SINTATICA.percorrePorNivel()
    # print("____FIM ARVORE ZUADA____")
    return POSICAO_TOKEN_ERRO
