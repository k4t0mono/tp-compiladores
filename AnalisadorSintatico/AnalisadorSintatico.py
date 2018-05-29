
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Gerenciador import TipoToken

def erroEstouro(esperado):
    return "ERRO: estourou o numero de tokens antes do token esperado (" + esperado + ")!"

def erroTokenInesperado(tokenInesperado, tokenEsperado):
    return "ERRO: inesperado token " + str(tokenInesperado) + ". Esperado " + str(tokenEsperado) + "!"

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
    return i + 1

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
        return i
    i += 1
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("Identificador"))
        return i
    if(tokens[i].tipoToken != TipoToken.Identificador):
        print(erroTokenInesperado(tokens[i], "Identificador"))
        return i
    i += 1
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<primeiro token de classBody>"))
        return i
    if(tokens[i].tipoToken == TipoToken.PCExtends):
        i += 1
        if(acabaramOsTokens(tokens, i)):
            print(erroEstouro("Identificador"))
            return i
        i = qualifiedIdentifier(tokens, i)
    if(acabaramOsTokens(tokens, i)):
        print(erroEstouro("<primeiro token de classBody>"))
        return i
    i = classBody(tokens, i)
    return i

def classBody(tokens, i):
    return i + 1

def main(tokens):
    i = compilationUnit(tokens, 0)
    print(i)
    return "OK"
