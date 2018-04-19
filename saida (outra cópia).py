#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from Token import Token
from TabelaDeSimbolos import TabelaDeSimbolos

TABELA = TabelaDeSimbolos()
TOKENS = []

def q0(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True
    if(codigo[indice] == "'"):
        indice+=1
        return charLiteral(codigo, indice)
    if(codigo[indice] == "("):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "="):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "0"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == '"'):
        indice+=1
        return stringLiteral(codigo, indice)
    if(codigo[indice] == "b"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "1"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "2"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == ")"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "a"):
        indice+=1
        return q1(codigo,indice)
    if(codigo[indice] == "c"):
        indice+=1
        return q2(codigo,indice)
    return False

def q1(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True
    if(codigo[indice] == "'"):
        indice+=1
        return charLiteral(codigo, indice)
    if(codigo[indice] == "("):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "="):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "0"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == '"'):
        indice+=1
        return stringLiteral(codigo, indice)
    if(codigo[indice] == "b"):
        indice+=1
        return q3(codigo,indice)
    if(codigo[indice] == "1"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "2"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == ")"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "a"):
        indice+=1
        return q1(codigo,indice)
    if(codigo[indice] == "c"):
        indice+=1
        return q2(codigo,indice)
    return False

def q2(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True
    if(codigo[indice] == "'"):
        indice+=1
        return charLiteral(codigo, indice)
    if(codigo[indice] == "("):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "="):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "0"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == '"'):
        indice+=1
        return stringLiteral(codigo, indice)
    if(codigo[indice] == "b"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "1"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "2"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == ")"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "a"):
        indice+=1
        return q1(codigo,indice)
    if(codigo[indice] == "l"):
        indice+=1
        return q5(codigo,indice)
    if(codigo[indice] == "c"):
        indice+=1
        return q2(codigo,indice)
    return False

def q3(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True
    if(codigo[indice] == "'"):
        indice+=1
        return charLiteral(codigo, indice)
    if(codigo[indice] == "("):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "="):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "0"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "s"):
        indice+=1
        return q4(codigo,indice)
    if(codigo[indice] == '"'):
        indice+=1
        return stringLiteral(codigo, indice)
    if(codigo[indice] == "b"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "1"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "2"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == ")"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "a"):
        indice+=1
        return q1(codigo,indice)
    if(codigo[indice] == "c"):
        indice+=1
        return q2(codigo,indice)
    return False

def q4(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "t"):
        indice+=1
        return q7(codigo,indice)
    return False

def q5(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "a"):
        indice+=1
        return q6(codigo,indice)
    return False

def q6(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "s"):
        indice+=1
        return q9(codigo,indice)
    return False

def q7(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "r"):
        indice+=1
        return q8(codigo,indice)
    return False

def q8(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "a"):
        indice+=1
        return q10(codigo,indice)
    return False

def q9(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "s"):
        indice+=1
        return q0(codigo,indice)
    return False

def q10(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "c"):
        indice+=1
        return q11(codigo,indice)
    return False

def q11(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "t"):
        indice+=1
        return q0(codigo,indice)
    return False

def charLiteral(codigo, indice):
    if(len(codigo) == 4):
        if(codigo[1] != '\\'):
            return False
        if(codigo[3] != "'"):
            return False
        if(codigo[2] == '"' or
           codigo[2] == "'" or
           codigo[2] == 'f'or
           codigo[2] == 'b' or
           codigo[2] == 't' or
           codigo[2] == 'r' or
           codigo[2] == 'n' or
           codigo[2] == '\\'):
            palavra = codigo[0:4]
            linha = TABELA.insere(palavra)
            TOKENS.append(Token(palavra, linha))
            return True
    if(len(codigo) == 3):
        if(codigo[2] != "'"):
            return False
        if(codigo[1] == '\\' or codigo[1] == "'"):
            return False
        palavra = codigo[0:3]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True
    return False


def stringLiteral(codigo, indice):
    while(indice < len(codigo) - 1):
        if(codigo[indice] == '\\'):
            if(codigo[indice+1] == "'" or
               codigo[indice+1] == '"' or
               codigo[indice+1] == 'f'or
               codigo[indice+1] == 'b' or
               codigo[indice+1] == 't' or
               codigo[indice+1] == 'r' or
               codigo[indice+1] == 'n' or
               codigo[indice+1] == '\\'):
                indice += 1

            else: 
                return False
        indice+=1

    if(codigo[indice] != '"'):
         return False
    else: 
        palavra = codigo[0:indice+1]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True
        
def preProcessamento(linhas):
    dicBinarios = {
        "+=" : "+=",
        "==" : "==",
        "++" : "++",
        "&&" : "&&",
        "<=" : "<=",
        "--" : "--"
    }
    
    dicUnarios = {
        "=" : "=",
        ">" : ">",
        "+" : "+",
        "!" : "!",
        "-" : "-",
        "*" : "*",
        "," : ",",
        "." : ".",
        "[" : "[",
        "{" : "{",
        "(" : "(",
        ")" : ")",
        "}" : "}",
        "]" : "]",
        ";" : ";"
    }
    for i in range(len(linhas)):
        arrayLinha = []
        j = 0
        while(j < len(linhas[i]) - 1):
            teste = linhas[i][j : j + 2]
            if(teste in dicBinarios):
                arrayLinha.append(teste)
                j += 1
            elif(linhas[i][j] in dicUnarios):
                arrayLinha.append(linhas[i][j])
            elif(linhas[i][j] == "\t" or linhas[i][j] == " "):
                arrayLinha.append('')
            else:           #faz magica nao mexa
                palavra = linhas[i][j]
                k = j + 1
                aspasSimples = False
                aspasDuplas = False
                if(linhas[i][j] == "'"):
                    aspasSimples = True
                elif(linhas[i][j] == '"'):
                    aspasDuplas = True
                acabou = False
                if(aspasSimples):
                    while(k < len(linhas[i]) and (linhas[i][k] != "'" or linhas[i][k - 1] == "\\")):
                        palavra += linhas[i][k]
                        k += 1
                    if(k < len(linhas[i])):
                        palavra += linhas[i][k]
                    arrayLinha.append(palavra)
                    j = k
                
                elif(aspasDuplas):
                    while(k < len(linhas[i]) and (linhas[i][k] != '"' or linhas[i][k - 1] == "\\")):
                        palavra += linhas[i][k]
                        k += 1
                    if(k < len(linhas[i])):
                        palavra += linhas[i][k]
                    arrayLinha.append(palavra)
                    j = k
                
                else:
                    while(k < (len(linhas[i]) - 1) and not acabou):
                        teste = linhas[i][k : k + 2]
                        if(teste in dicBinarios or
                           linhas[i][k] in dicUnarios or
                           linhas[i][k] == "\t" or
                           linhas[i][k] == " "):
                            arrayLinha.append(palavra)
                            acabou = True
                            j = k - 1
                        else:
                            palavra += linhas[i][k]
                            k += 1
                    if(k == len(linhas[i]) - 1):
                        if(linhas[i][k] in dicUnarios or
                           linhas[i][k] == "\t" or
                           linhas[i][k] == " "):
                            arrayLinha.append(palavra)
                            j = k - 1
                        else:
                            palavra += linhas[i][k]
                            arrayLinha.append(palavra)
                            j = k
                        
            j += 1
        if(j == len(linhas[i]) - 1):
            if(linhas[i][j] == "\t" or linhas[i][j] == " "):
                arrayLinha.append('')
            else:
                arrayLinha.append(linhas[i][j])
                
        linhas[i] = arrayLinha
        print(arrayLinha)
        
    return linhas

def main(args):
    arquivo = open(args[1], 'r')
    linhas = arquivo.read().splitlines()
    print(linhas)
    linhas = preProcessamento(linhas)
    print(linhas)
    for lin in range(len(linhas)):
        #~ linhas[lin] = linhas[lin].split(' ')
        #~ print(linhas[lin])
        cont = 0
        for item in range(len(linhas[lin])):
            if(linhas[lin][item] != ''):
                if(not q0(linhas[lin][item], 0)):
                    print('Erro na linha ' + str(lin + 1) + ' e coluna ' + str(cont + 1))
                cont += len(linhas[lin][item])
            else:
                cont += 1
    for item in TOKENS:
        print(item)
main(sys.argv)
