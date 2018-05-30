
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
            entrou = True
        elif(eUmBasicType(tokens[j])):
            j = typeOfDeclaration(tokens, j)
            entrou = True
        if(entrou):
            i = localVariableDeclarationStatement(tokens, i)
            return i
        i = statement(tokens, i)
    return i

def statement(tokens, i):
    return i + 1

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
        i = variableInitializer(tokens, i)
    return i

def variableInitializer(tokens, i):
    return i + 1


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




def main(tokens):
    i = compilationUnit(tokens, 0)
    print(i)
    return "OK"
