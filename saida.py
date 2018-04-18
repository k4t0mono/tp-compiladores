#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from Token import Token
from TabelaDeSimbolos import TabelaDeSimbolos

tabela = TabelaDeSimbolos()
tokens = []

def q0(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return True
    if(codigo[indice] == "b"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "c"):
        indice+=1
        return q1(codigo,indice)
    if(codigo[indice] == "("):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "="):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "0"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "2"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == ")"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "1"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "a"):
        indice+=1
        return q2(codigo,indice)
    return False

def q1(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return True
    if(codigo[indice] == "b"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "c"):
        indice+=1
        return q1(codigo,indice)
    if(codigo[indice] == "("):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "l"):
        indice+=1
        return q3(codigo,indice)
    if(codigo[indice] == "="):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "0"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "2"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == ")"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "1"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "a"):
        indice+=1
        return q2(codigo,indice)
    return False

def q2(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return True
    if(codigo[indice] == "b"):
        indice+=1
        return q5(codigo,indice)
    if(codigo[indice] == "c"):
        indice+=1
        return q1(codigo,indice)
    if(codigo[indice] == "("):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "="):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "0"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "2"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == ")"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "1"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "a"):
        indice+=1
        return q2(codigo,indice)
    return False

def q3(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "a"):
        indice+=1
        return q4(codigo,indice)
    return False

def q4(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "s"):
        indice+=1
        return q7(codigo,indice)
    return False

def q5(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return True
    if(codigo[indice] == "b"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "c"):
        indice+=1
        return q1(codigo,indice)
    if(codigo[indice] == "("):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "s"):
        indice+=1
        return q6(codigo,indice)
    if(codigo[indice] == "="):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "0"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "2"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == ")"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "1"):
        indice+=1
        return q0(codigo,indice)
    if(codigo[indice] == "a"):
        indice+=1
        return q2(codigo,indice)
    return False

def q6(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "t"):
        indice+=1
        return q8(codigo,indice)
    return False

def q7(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "s"):
        indice+=1
        return q0(codigo,indice)
    return False

def q8(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "r"):
        indice+=1
        return q9(codigo,indice)
    return False

def q9(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "a"):
        indice+=1
        return q10(codigo,indice)
    return False

def q10(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "c"):
        indice+=1
        return q11(codigo,indice)
    return False

def q11(codigo, indice):
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = tabela.insere(palavra)
        tokens.append(Token(palavra, linha))
        return False
    if(codigo[indice] == "t"):
        indice+=1
        return q0(codigo,indice)
    return False

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
        nova = []
        j = 0
        while(j < len(linhas[i])):
            if(j < (len(linhas[i]) - 1)):
                teste = linhas[i][j:j + 2]
                if(teste in dicBinarios):
                    nova.append(" ")
                    nova.append(linhas[i][j])
                    nova.append(linhas[i][j + 1])
                    nova.append(" ")
                    j += 1
                elif(linhas[i][j] in dicUnarios):
                    nova.append(" ")
                    nova.append(linhas[i][j])
                    nova.append(" ")
                elif(linhas[i][j] == "	"):
                    nova.append(" ")
                else:
                    nova.append(linhas[i][j])
                    
            elif(linhas[i][j] in dicUnarios):
                nova.append(" ")
                nova.append(linhas[i][j])
                nova.append(" ")
            elif(linhas[i][j] == "	"):
                nova.append(" ")
            else:
                nova.append(linhas[i][j])
                j += 1
            j += 1
        linhas[i] = "".join(nova)

    return linhas

def main(args):
    arquivo = open(args[1], 'r')
    linhas = arquivo.read().splitlines()
    linhas = preProcessamento(linhas)
    print(linhas)
    for lin in range(len(linhas)):
        linhas[lin] = linhas[lin].split(' ')
        print(lin)
        cont = 0
        for item in range(len(linhas[lin])):
            if(linhas[lin][item] != ''):
                if(not q0(linhas[lin][item], 0)):
                    print('Erro na linha ' + str(lin + 1) + ' e coluna ' + str(cont + 1))
                cont += len(linhas[lin][item])
            else:
                cont += 1
    for item in tokens:
        print(item)
main(sys.argv)
