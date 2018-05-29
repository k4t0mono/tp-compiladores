
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Gerenciador import TipoToken

def acabaramOsTokens(tokens, i):
    return i >= len(tokens)

def compilationUnit(tokens, i):
    if(acabaramOsTokens(tokens, i)):
        return i
    if(tokens[i].tipoToken == TipoToken.PCPackage):
        i += 1
        i = qualifiedIdentifier(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            print("ERRO: estourou o numero de tokens")
            return i
        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            i += 1
        else:
            print("ERRO: TOKEN", tokens[i])
    if(acabaramOsTokens(tokens, i)):
        return i
    while((not acabaramOsTokens(tokens, i)) and
         (tokens[i].tipoToken == TipoToken.PCImport)):
        i += 1
        i = qualifiedIdentifier(tokens, i)
        if(acabaramOsTokens(tokens, i)):
            print("ERRO: estourou o numero de tokens", )
            return i
        if(tokens[i].tipoToken == TipoToken.SepPontoVirgula):
            i += 1
        else:
            print("ERRO: TOKEN", tokens[i])
    i = typeDeclaration(tokens, i)

    if(acabaramOsTokens(tokens, i)):
        return i
    print("ERRO: TOKEN", tokens[i])


def qualifiedIdentifier(tokens, i):
    return i + 1

def typeDeclaration(tokens, i):
    return i + 1



def main(tokens):
    i = compilationUnit(tokens, 0)
    print(i)
    return "OK"
