
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Gerenciador import TipoToken


def erroEstouro(esperado):
    return "ERRO: estourou o numero de tokens antes do token esperado (" + esperado + ")!"

def erroTokenInesperado(tokenInesperado, tokenEsperado):
    return "ERRO: inesperado token " + str(tokenInesperado) + ". Esperado <" + str(tokenEsperado) + ">!"

def acabaramOsTokens(tokens, i):
    return i >= len(tokens)

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
            print(erroEstouro("SepPontoVirgula"))
            return i
        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            i += 1
        else:
            print(erroTokenInesperado(tokens[i], "Identificador"))
    if(acabaramOsTokens(tokens, i)):
        return i
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken == TipoToken.PCImport)):
        i += 1
        i = qualifiedIdentifier(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            print(erroEstouro("SepPontoVirgula"))
            return i
        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            i += 1
        else:
            print(erroTokenInesperado(tokens[i], "SepPontoVirgula"))
    while(not acabaramOsTokens(tokens, i)):
        i = typeDeclaration(tokens, i)

    if(acabaramOsTokens(tokens, i)):
        return i
    print(erroTokenInesperado(tokens[i], "fim de arquivo"))


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
        print(erroEstouro("Identificador"))
        return i
    print(erroTokenInesperado(tokens[i], "Identificador"))
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
        print(erroEstouro("PCClass"))
        return i
    if(tokens[i].tipoToken != TipoToken.PCClass):
        print(erroTokenInesperado(tokens[i], "PCClass"))
        return i + 1
    i += 1
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("Identificador"))
        return i
    if(tokens[i].tipoToken != TipoToken.Identificador):
        print(erroTokenInesperado(tokens[i], "Identificador"))
        return i + 1
    i += 1
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<primeiro token de classBody>"))
        return i
    if(tokens[i].tipoToken == TipoToken.PCExtends):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            print(erroEstouro("Identificador"))
            return i + 1
        i = qualifiedIdentifier(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<primeiro token de classBody>"))
        return i
    i = classBody(tokens, i)
    return i

def classBody(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepAbreChaves"))
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
        print(erroTokenInesperado(tokens[i], "SepAbreChaves"))
        return i + 1

    i += 1
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepFechaChaves"))
        return i
    while((not acabaramOsTokens(tokens, i)) and
          (tokens[i].tipoToken != TipoToken.SepFechaChaves)):
        if(eUmModifier(tokens[i])):
            i = modifiers(tokens, i)
        else:
            print(erroTokenInesperado(tokens[i], "um modifier"))
            i += 1
            continue
        i = memberDecl(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepFechaChaves"))
        return i

        return i + 1
    return i + 1

def memberDecl(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<primeiro token de memberDecl>"))
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
            print(erroEstouro("Identificador"))
            return i
    else:
        i = typeOfDeclaration(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            print(erroEstouro("Identificador"))
            return i
        if(tokens[i].tipoToken == TipoToken.Identificador):
            j = i + 1
            if(not acabaramOsTokens(tokens, j)):
                if(tokens[j].tipoToken != TipoToken.SepAbreParenteses):
                    i = variableDeclarators(tokens, i)
                    if(acabaramOsTokens(tokens, i)):
                        print(erroEstouro("SepPontoVirgula"))
                        return i
                    if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
                        print(erroTokenInesperado(tokens[i], "SepPontoVirgula"))
                        return i
                    i += 1
                    return i

    if(tokens[i].tipoToken == TipoToken.Identificador):
        i += 1
    i = formalParamaters(tokens, i)

    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<primeiro do bloco> ou SepPontoVirgula"))
        return i

    if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
        i += 1
        return i

    i = block(tokens, i)
    return i

def block(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepAbreChaves"))
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
        print(erroTokenInesperado(tokens[i], "SepAbreChaves"))
        return i

    i += 1
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepFechaChaves"))
        return i

    while(tokens[i].tipoToken != TipoToken.SepFechaChaves):
        i = blockStatement(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            print(erroEstouro("SepFechaChaves"))
            return i

    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepFechaChaves"))
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
                j = typeDeclaration(tokens, k)
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
        print(erroEstouro("<token de statement>"))
        return i

    if(tokens[i].tipoToken == TipoToken.SepAbreChaves):
        i = block(tokens, i)
        return i
    #TEM PARADA ERRADA NISSO AE IRMAO
    # if(tokens[i].tipoToken == TipoToken.Identificador):
        #VERIFICAR DEPOIS
        # i += 1
        # if(acabaramOsTokens(tokens, i)):
        #     print(erroEstouro(":"))
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
            print(erroEstouro("SepPontoVirgula"));
            return i
        if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
            i = expression(tokens, i)

    if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
        i += 1
        return i

    i = statementExpression(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepPontoVirgula"))
        return i
    if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
        print(erroTokenInesperado(tokens[i], "SepPontoVirgula"))
        return i
    i += 1
    return i


def formalParamaters(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepAbreParenteses"))
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
        print(erroTokenInesperado(tokens[i], "SepAbreParenteses"))
        return i

    i += 1
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepFechaParenteses"))
        return i
    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        i = formalParamater(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            print(erroEstouro("SepFechaParenteses"))
            return i
        while(tokens[i].tipoToken == TipoToken.SepVirgula):
            i += 1
            i = formalParamater(tokens, i)
            if(acabaramOsTokens(tokens, i)):
                print(erroEstouro("<token de formalParamater>"))
                return i

    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        print(erroTokenInesperado(tokens[i], "SepFechaParenteses"))
        return i

    i += 1
    return i

def formalParamater(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<token de type>"))
        return i
    i = typeOfDeclaration(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("Identificador"))
        return i
    if(tokens[i].tipoToken != TipoToken.Identificador):
        print(erroTokenInesperado(tokens[i], "Identificador"))
        return i
    i += 1
    return i

def parExpression(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepAbreParenteses"))
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
        print(erroTokenInesperado(tokens[i], "SepAbreParenteses"))
        return i

    i += 1
    i = expression(tokens, i)

    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepFechaParenteses"))
        return i

    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        print(erroTokenInesperado(tokens[i], "SepFechaParenteses"))
        return i
    i += 1
    return i

def localVariableDeclarationStatement(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<token que define um type>"))
        return i
    i = typeOfDeclaration(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<token de variableDeclarators>"))
        return i
    i = variableDeclarators(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepPontoVirgula"))
        return i
    if(tokens[i].tipoToken != TipoToken.SepPontoVirgula):
        print(erroTokenInesperado(tokens[i], "SepPontoVirgula"))
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
            print(erroEstouro("<token de variableDeclarator>"))
            return i
        i = variableDeclarator(tokens, i)
    return i

def variableDeclarator(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("Identificador"))
        return i
    if(tokens[i].tipoToken != TipoToken.Identificador):
        print(erroTokenInesperado(tokens[i], "Identificador"))
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
        print(erroEstouro("<token de variableInitializer>"))
        return i
    if(tokens[i].tipoToken == TipoToken.SepAbreChaves):
        i = arrayInitializer(tokens, i)
        return i
    i = expression(tokens, i)
    return i

def arrayInitializer(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepAbreChaves"))
        return i

    if(tokens[i].tipoToken != TipoToken.SepAbreChaves):
        print(erroTokenInesperado(tokens[i], "SepAbreChaves"))
        return i

    i += 1
    i = variableInitializer(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepFechaChaves"))
        return i
    while(tokens[i].tipoToken == TipoToken.SepVirgula):
        i += 1
        i = variableInitializer(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            print(erroEstouro("SepFechaChaves"))
            return i

    if(tokens[i].tipoToken != TipoToken.SepFechaChaves):
        print(erroTokenInesperado(tokens[i], "SepFechaChaves"))
        return i

    i += 1
    return i

def typeOfDeclaration(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<primeiro token do tipo>"))
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
        print(erroEstouro("<PCBoolean, PCChar ou PCInt>"))
        return i
    if(not eUmBasicType(tokens[i])):
        print(erroTokenInesperado(tokens[i], "<PCBoolean, PCChar ou PCInt>"))
        return i
    return i + 1

def referenceType(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<PCBoolean, PCChar ou PCInt>"))
        return i
    if(eUmBasicType(tokens[i])):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            print(erroEstouro("SepAbreColchetes"))
            return i
        if(tokens[i].tipoToken != TipoToken.SepAbreColchetes):
            print(erroTokenInesperado(tokens[i], "SepAbreColchetes"))
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
            print(erroEstouro("SepFechaColchetes"))
            return i
        if(tokens[i].tipoToken != TipoToken.SepFechaColchetes):
            print(erroTokenInesperado(tokens[i], "SepFechaColchetes"))
            return i
        i += 1
    return i

def arguments(tokens, i):
    print("CHAMOU ARGUMENTS")
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepAbreParenteses"))
        return i
    if(tokens[i].tipoToken != TipoToken.SepAbreParenteses):
        print(erroTokenInesperado(tokens[i], "SepAbreParenteses"))
        return i
    i += 1
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("SepFechaParenteses"))
        return i
    if(tokens[i].tipoToken != TipoToken.SepFechaParenteses):
        i = expression(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            print(erroEstouro("SepFechaParenteses"))
            return i
        while(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            i += 1
            i = expression(tokens, i)
            if(acabaramOsTokens(tokens, i)):
                print(erroEstouro("SepFechaParenteses"))
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
        print(erroEstouro("expressao unaria"))
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

def simpleUnaryExpression(tokens, i):
    i = postfixExpression(tokens, i)
    return i

def postfixExpression(tokens, i):
    i = primary(tokens, i)
    return i

def primary(tokens, i):
    i = literal(tokens, i)
    return i

def literal(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<valor literal>"))
        return i
    if(eUmLiteral(tokens[i])):
        i += 1
        return i
    print(erroTokenInesperado(tokens[i], "valor literal"))
    return i + 1


def main(tokens):
    i = compilationUnit(tokens, 0)
    print(i)
    return "OK"
