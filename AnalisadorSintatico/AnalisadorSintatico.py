
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Gerenciador import TipoToken


POSICAO_TOKEN_ERRO = []

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
        i = qualifiedIdentifier(tokens, i)
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

def compilationUnit(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        return i
    if(tokens[i].tipoToken == TipoToken.PCPackage):
        i += 1
        i = qualifiedIdentifier(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepPontoVirgula")
            return i
        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            i += 1
        else:
            erroTokenInesperado(tokens[i], "Identificador", i)
    if(acabaramOsTokens(tokens, i)):
        return i
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken == TipoToken.PCImport)):
        i += 1
        i = qualifiedIdentifier(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepPontoVirgula")
            return i
        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            i += 1
        else:
            erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
    while(not acabaramOsTokens(tokens, i)):
        i = typeDeclaration(tokens, i)

    if(acabaramOsTokens(tokens, i)):
        return i
    erroTokenInesperado(tokens[i], "fim de arquivo", i)


def qualifiedIdentifier(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        return i
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken == TipoToken.Identificador)):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.SepPonto):
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

def typeDeclaration(tokens, i):
    i = modifiers(tokens, i)
    i = classDeclaration(tokens, i)
    return i

def modifiers(tokens, i):
    while((not acabaramOsTokens(tokens, i)) and
          (eUmModifier(tokens[i]))):
          i += 1
    return i

def classDeclaration(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("PCClass")
        return i
    if(tokens[i].tipoToken != TipoToken.PCClass):
        erroTokenInesperado(tokens[i], "PCClass", i)
        return i + 1
    i += 1
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("Identificador")
        return i
    if(tokens[i].tipoToken != TipoToken.Identificador):
        erroTokenInesperado(tokens[i], "Identificador", i)
        return i + 1
    i += 1
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<primeiro token de classBody>")
        return i
    if(tokens[i].tipoToken == TipoToken.PCExtends):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("Identificador")
            return i + 1
        i = qualifiedIdentifier(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<primeiro token de classBody>")
        return i
    i = classBody(tokens, i)
    return i

def classBody(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreChaves")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
        erroTokenInesperado(tokens[i], "SepAbreChaves", i)
        return i + 1

    i += 1
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken != TipoToken.SepFechaChaves)):
        if(eUmModifier(tokens[i])):
            i = modifiers(tokens, i)
        else:
            erroTokenInesperado(tokens[i], "um modifier", i)
            i += 1
            continue
        i = memberDecl(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i

        return i + 1
    return i + 1

def memberDecl(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<primeiro token de memberDecl>")
        return i

    #Construtor
    if(tokens[i].tipoToken == TipoToken.Identificador):
        if((not acabaramOsTokens(tokens, i + 1)) and
           (tokens[i + 1].tipoToken == TipoToken.SepAbreParenteses)):
            i += 1
            i = formalParamaters(tokens, i)
            i = block(tokens, i)
            return i

    if(tokens[i].tipoToken == TipoToken.PCVoid):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("Identificador")
            return i
    else:
        i = typeOfDeclaration(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("Identificador")
            return i
        if(tokens[i].tipoToken == TipoToken.Identificador):
            j = i + 1
            if(not acabaramOsTokens(tokens, j)):
                if(tokens[j].tipoToken != TipoToken.SepAbreParenteses):
                    i = variableDeclarators(tokens, i)
                    if(acabaramOsTokens(tokens, i)):
                        erroEstouro("SepPontoVirgula")
                        return i
                    if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
                        erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
                        return i
                    i += 1
                    return i

    if(tokens[i].tipoToken == TipoToken.Identificador):
        i += 1
    i = formalParamaters(tokens, i)

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<primeiro do bloco> ou SepPontoVirgula")
        return i

    if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
        i += 1
        return i

    i = block(tokens, i)
    return i

def block(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreChaves")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
        erroTokenInesperado(tokens[i], "SepAbreChaves", i)
        return i

    i += 1
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i

    while(tokens[i].tipoToken != TipoToken.SepFechaChaves):
        i = blockStatement(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaChaves")
            return i

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i

    i += 1
    return i

#PROVAVELMENTE ESTA BOSTA ESTA MUITO ERRADA DEMAIS
def blockStatement(tokens, i):
    j = i
    if(not acabaramOsTokens(tokens, j)):
        entrou = False
        if(tokens[j].tipoToken == TipoToken.Identificador):
            k = j
            j = qualifiedIdentifier(tokens, j)
            if(tokens[j].tipoToken == TipoToken.SepAbreColchetes):
                j = typeOfDeclaration(tokens, k)
            if(tokens[j].tipoToken == TipoToken.Identificador):
                entrou = True
        elif(eUmBasicType(tokens[j])):
            j = typeOfDeclaration(tokens, j)
            if(tokens[j].tipoToken == TipoToken.Identificador):
                entrou = True
        if(entrou):
            i = localVariableDeclarationStatement(tokens, i)
            return i
        i = statement(tokens, i)
        return i
    return i + 1

def statement(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<token de statement>")
        return i

    if(tokens[i].tipoToken == TipoToken.SepAbreChaves):
        i = block(tokens, i)
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
        i += 1
        i = parExpression(tokens, i)
        i = statement(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.PCElse):
            i += 1
            i = statement(tokens, i)
        return i

    if(tokens[i].tipoToken == TipoToken.PCWhile):
        i += 1
        i = parExpression(tokens, i)
        i = statement(tokens, i)
        return i

    if(tokens[i].tipoToken == TipoToken.PCReturn):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepPontoVirgula")
            return i
        if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
            i = expression(tokens, i)

    if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
        i += 1
        return i

    i = statementExpression(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepPontoVirgula")
        return i
    if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
        erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
        return i
    i += 1
    return i


def formalParamaters(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreParenteses")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
        erroTokenInesperado(tokens[i], "SepAbreParenteses", i)
        return i

    i += 1
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaParenteses")
        return i
    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        i = formalParamater(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaParenteses")
            return i
        while(tokens[i].tipoToken == TipoToken.SepVirgula):
            i += 1
            i = formalParamater(tokens, i)
            if(acabaramOsTokens(tokens, i)):
                erroEstouro("<token de formalParamater>")
                return i

    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
        return i

    i += 1
    return i

def formalParamater(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<token de type>")
        return i
    i = typeOfDeclaration(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("Identificador")
        return i
    if(tokens[i].tipoToken != TipoToken.Identificador):
        erroTokenInesperado(tokens[i], "Identificador", i)
        return i
    i += 1
    return i

def parExpression(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreParenteses")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
        erroTokenInesperado(tokens[i], "SepAbreParenteses", i)
        return i

    i += 1
    i = expression(tokens, i)

    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaParenteses")
        return i

    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
        return i
    i += 1
    return i

def localVariableDeclarationStatement(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<token que define um type>")
        return i
    i = typeOfDeclaration(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<token de variableDeclarators>")
        return i
    i = variableDeclarators(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepPontoVirgula")
        return i
    if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
        erroTokenInesperado(tokens[i], "SepPontoVirgula", i)
        return i
    i += 1
    return i

def variableDeclarators(tokens, i):
    i = variableDeclarator(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        return i
    while(tokens[i].tipoToken == TipoToken.SepVirgula):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("<token de variableDeclarator>")
            return i
        i = variableDeclarator(tokens, i)
    return i

def variableDeclarator(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("Identificador")
        return i
    if(tokens[i].tipoToken != TipoToken.Identificador):
        erroTokenInesperado(tokens[i], "Identificador", i)
        return i
    i += 1
    if(acabaramOsTokens(tokens, i)):
        return i
    if(tokens[i].tipoToken == TipoToken.OpAtribuicao):
        i += 1
        i = variableInitializer(tokens, i)
    return i

def variableInitializer(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<token de variableInitializer>")
        return i
    if(tokens[i].tipoToken == TipoToken.SepAbreChaves):
        i = arrayInitializer(tokens, i)
        return i
    i = expression(tokens, i)
    return i

def arrayInitializer(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreChaves")
        return i

    if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
        erroTokenInesperado(tokens[i], "SepAbreChaves", i)
        return i

    i += 1
    i = variableInitializer(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaChaves")
        return i
    while(tokens[i].tipoToken == TipoToken.SepVirgula):
        i += 1
        i = variableInitializer(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaChaves")
            return i

    if(tokens[i].tipoToken != TipoToken.SepFechaChaves):
        erroTokenInesperado(tokens[i], "SepFechaChaves", i)
        return i

    i += 1
    return i

def typeOfDeclaration(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<primeiro token do tipo>")
        return i
    if(eUmBasicType(tokens[i])):
        if(not acabaramOsTokens(tokens, i + 1)):
            if(tokens[i + 1].tipoToken == TipoToken.SepAbreColchetes):
                i = referenceType(tokens, i)
                return i
        i = basicType(tokens, i)
        return i
    i = referenceType(tokens, i)
    return i

def basicType(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<PCBoolean, PCChar ou PCInt>")
        return i
    if(not eUmBasicType(tokens[i])):
        erroTokenInesperado(tokens[i], "<PCBoolean, PCChar ou PCInt>", i)
        return i
    return i + 1

def referenceType(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<PCBoolean, PCChar ou PCInt>")
        return i
    if(eUmBasicType(tokens[i])):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepAbreColchetes")
            return i
        if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
            erroTokenInesperado(tokens[i], "SepAbreColchetes", i)
            return i
    else:
        i = qualifiedIdentifier(tokens, i)
        if((acabaramOsTokens(tokens, i)) or
           (tokens[i].tipoToken != TipoToken.SepAbreColchetes)):
            return i
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaColchetes")
            return i
        if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
            erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
            return i
        i += 1
    return i

def arguments(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreParenteses")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
        erroTokenInesperado(tokens[i], "SepAbreParenteses", i)
        return i
    i += 1
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaParenteses")
        return i
    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        i = expression(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaParenteses")
            return i
        while(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            i += 1
            i = expression(tokens, i)
            if(acabaramOsTokens(tokens, i)):
                erroEstouro("SepFechaParenteses")
                return i
    i += 1
    return i

def statementExpression(tokens, i):
    i = expression(tokens, i)
    return i

def expression(tokens, i):
    i = assignmentExpression(tokens, i)
    return i

def assignmentExpression(tokens, i):
    i = conditionalAndExpression(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        return i
    if((tokens[i].tipoToken == TipoToken.OpAtribuicao) or
       (tokens[i].tipoToken == TipoToken.OpSomaAtribuicao)):
        i += 1
        i = assignmentExpression(tokens, i)
    return i

def conditionalAndExpression(tokens, i):
    i = equalityExpression(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        return i
    while(tokens[i].tipoToken == TipoToken.OpAnd):
        i += 1
        i = equalityExpression(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            return i
    return i

def equalityExpression(tokens, i):
    i = relationalExpression(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        return i
    while(tokens[i].tipoToken == TipoToken.OpIgualdade):
        i += 1
        i = relationalExpression(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            return i
    return i

def relationalExpression(tokens, i):
    i = additiveExpression(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        return i
    if((tokens[i].tipoToken == TipoToken.OpMaior) or
       (tokens[i].tipoToken == TipoToken.OpMenorIgual)):
        i += 1
        i = additiveExpression(tokens, i)
        return i
    if(tokens[i].tipoToken == TipoToken.PCInstanceOf):
        i += 1
        i = referenceType(tokens, i)
        return i
    return i

def additiveExpression(tokens, i):
    i = multiplicativeExpression(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        return i
    while((tokens[i].tipoToken == TipoToken.OpSoma) or
          (tokens[i].tipoToken == TipoToken.OpMenos)):
        i += 1
        i = multiplicativeExpression(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            return i
    return i

def multiplicativeExpression(tokens, i):
    i = unaryExpression(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        return i
    while(tokens[i].tipoToken == TipoToken.OpMultiplicacao):
        i += 1
        i = unaryExpression(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            return i
    return i

def unaryExpression(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("expressao unaria")
        return i
    if(tokens[i].tipoToken == TipoToken.OpIncremento):
        i += 1
        i = unaryExpression(tokens, i)
        return i

    if(tokens[i].tipoToken == TipoToken.OpMenos):
        i += 1
        i = unaryExpression(tokens, i)
        return i
    i = simpleUnaryExpression(tokens, i)
    return i

# PROBLEMA!!!!!!!
# DIFERENCIAR parExpression
#    de (referenceType) simpleUnaryExpression!!!!!!
def simpleUnaryExpression(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("expressao unaria simples")
        return i
    if(tokens[i].tipoToken == TipoToken.OpNot):
        i += 1
        i = unaryExpression(tokens, i)
        return i

    #ESSA PARTE DO CODIGO TA ORRIVEL MAS FODACE
    if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("basicType ou referenceType")
            return i
        if(eUmBasicType(tokens[i])):
            j = basicType(tokens, i)
            if(acabaramOsTokens(tokens, j)):
                erroEstouro("SepFechaParenteses")
                return i
            if(tokens[j].tipoToken == TipoToken.SepAbreColchetes):
                i = referenceType(tokens, i)
                if(acabaramOsTokens(tokens, i)):
                    erroEstouro("SepFechaParenteses")
                    return i
                if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
                    erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
                i += 1
                i = simpleUnaryExpression(tokens, i)
                return i
            else:
                i = j
                if(acabaramOsTokens(tokens, i)):
                    erroEstouro("SepFechaParenteses")
                    return i
                if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
                    erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
                i += 1
                i = unaryExpression(tokens, i)
                return i
        elif(eUmReferenceType(tokens, i)):
            eUmReferenceType(tokens, i)
            
            i = referenceType(tokens, i)
            if(acabaramOsTokens(tokens, j)):
                erroEstouro("SepFechaParenteses")
                return i
            if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
                erroTokenInesperado(tokens[i], "SepFechaParenteses", i)
            i += 1
            i = simpleUnaryExpression(tokens, i)
            return i
        else:
            i -= 1
            i = postfixExpression(tokens, i)
            return i

    i = postfixExpression(tokens, i)
    return i

def postfixExpression(tokens, i):
    i = primary(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        return i
    while((tokens[i].tipoToken == TipoToken.SepPonto) or
          (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):
        i = selector(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            return i
    while(tokens[i].tipoToken == TipoToken.OpDecremento):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            return i
    return i

def selector(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepPonto")
        return i
    if(tokens[i].tipoToken == TipoToken.SepPonto):
        i += 1
        i = qualifiedIdentifier(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = arguments(tokens, i)
        return i
    if(tokens[i].tipoToken == TipoToken.SepAbreColchetes):
        i += 1
        i = expression(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepAbreColchetes")
            return i
        if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
            erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
            return i
        i += 1
        return i
    return i

def primary(tokens, i):
    # print("NAO ENTRA?", tokens[i])
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("tokens de primary")
        return i
    if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
        i = parExpression(tokens, i)
        return i
    if(tokens[i].tipoToken == TipoToken.PCThis):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = arguments(tokens, i)
            return i
        return i
    if(tokens[i].tipoToken == TipoToken.PCSuper):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("argumentos")
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = arguments(tokens, i)
            return i
        if(tokens[i].tipoToken == TipoToken.SepPonto):
            i += 1
            i = qualifiedIdentifier(tokens, i)
            if(acabaramOsTokens(tokens, i)):
                return i
            if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                i = arguments(tokens, i)
            return i
        erroTokenInesperado(tokens[i], "SepPonto ou argumentos", i)
        return i + 1
    if(eUmLiteral(tokens[i])):
        i = literal(tokens, i)
        return i
    if(tokens[i].tipoToken == TipoToken.PCNew):
        i += 1
        i = creator(tokens, i)
        return i
    j = i
    i = qualifiedIdentifier(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        return i
    if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
        i = arguments(tokens, i)
    if(j == i):
        i += 1
    return i

def creator(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<primeiro de creator>")
        return i
    if(eUmType(tokens, i)):
        if(eUmReferenceType(tokens, i)):
            i = referenceType(tokens, i)
            if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
                i = arguments(tokens, i)
                return i
            i = arrayInitializer(tokens, i)
            return i
        i = basicType(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("argumentos")
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = arguments(tokens, i)
            return i
        if(tokens[i].tipoToken == TipoToken.SepAbreColchetes):
            i = newArrayDeclarator(tokens, i)
            return i
    elif(eUmQualifiedIdentifier(tokens, i)):
        i = qualifiedIdentifier(tokens, i)
        if(tokens[i].tipoToken == TipoToken.SepAbreParenteses):
            i = arguments(tokens, i)
            return i
        i = newArrayDeclarator(tokens, i)
        return i
    erroTokenInesperado(tokens[i], "token de type", i)
    return i

def newArrayDeclarator(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepAbreColchetes")
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
        erroTokenInesperado(tokens[i], "SepAbreColchetes", i)
        return i
    i += 1
    i = expression(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("SepFechaColchetes")
        return i
    if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
        erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
        return i
    i += 1
    while((not acabaramOsTokens(tokens, i)) and
        (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaColchetes")
            return i
        if(tokens[i].tipoToken == TipoToken.SepFechaColchetes):
            i += 1
            while((not acabaramOsTokens(tokens, i)) and
                (tokens[i].tipoToken == TipoToken.SepAbreColchetes)):
                i += 1
                if(acabaramOsTokens(tokens, i)):
                    erroEstouro("SepFechaColchetes")
                    return i
                if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
                    erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
                    return i
                i += 1
            return i

        i = expression(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            erroEstouro("SepFechaColchetes")
            return i
        if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
            erroTokenInesperado(tokens[i], "SepFechaColchetes", i)
            return i
        i += 1
    return i

def literal(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        erroEstouro("<valor literal>")
        return i
    if(eUmLiteral(tokens[i])):
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
    print(i)
    return POSICAO_TOKEN_ERRO
