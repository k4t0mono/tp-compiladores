
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from AnalisadorLexico import AnalisadorLexico
from AnalisadorSintatico import AnalisadorSintatico
from texttable import Texttable
from AnalisadorSemantico import AnalisadorSemantico
import sys

def main(args):
    if(len(args) != 2):
        print("MODO DE EXECUCAO DO PROGRAMA: ")
        print("python3", "<main.py>", "<arquivo-codigo-fonte>")
        print("Obs: O <arquivo-codigo-fonte> deve conter o código em j--")
        return
    arquivo = open(args[1], 'r')
    linhas = arquivo.read().splitlines()
    linhas = preProcessamento(linhas)
    resultadoAnaliseLexica = AnalisadorLexico.main(linhas)

    tokens = resultadoAnaliseLexica[0]
    tabela = resultadoAnaliseLexica[1]
    dadosTokens = resultadoAnaliseLexica[2]
    errosLexicos = resultadoAnaliseLexica[3]

    if(len(errosLexicos) > 0):
        imprimeErrosAnaliseLexica(errosLexicos)
        return

    # imprimeTokens(dadosTokens)
    # imprimeTabela(tabela)
    # imprimeFluxoDeTokens(tokens)

    resultadoAnaliseSintatica = AnalisadorSintatico.main(tokens, tabela)
    errosSintaticos = resultadoAnaliseSintatica[0]
    if(len(errosSintaticos)):
        imprimeErrosAnaliseSintatica(errosSintaticos, dadosTokens)
        return
    errosSemanticos = resultadoAnaliseSintatica[1]
    if(len(errosSemanticos)):
        imprimeErrosAnaliseSemantica(resultadoAnaliseSintatica[1], dadosTokens)
        return
    
    tabelaAux = resultadoAnaliseSintatica[2]
    resultadoAnaliseSemantica = AnalisadorSemantico.main(tokens, tabela, tabelaAux)
    
    errosAnaliseSemantica = resultadoAnaliseSemantica[0]
    if(len(errosAnaliseSemantica) > 0):
        imprimeErrosAnaliseSemantica(errosAnaliseSemantica, dadosTokens)
        return
        
    tabela = resultadoAnaliseSemantica[1]
    
    imprimeTabela(tabelaAux)
    imprimeTabela(tabela)

def imprimeErrosAnaliseSemantica(erros, dadosTokens):
    saida = ''

    for erro in erros:
        saida += 'Erro: {} \t\tLinha: {} \t\tColuna {}\n'.format(erro[1], dadosTokens[erro[0]][1], dadosTokens[erro[0]][2])

    print(saida)

def imprimeErrosAnaliseSintatica(erros, dadosTokens):
    saida = ""
    for erro in erros:
        if(erro[0] == -1):
            saida += "Esperado o token <" + erro[1] + "> antes do fim do arquivo.\n"
        else:
            saida += "Esperado o token <" + str(erro[1])
            saida += "> porém foi encontrado '"
            saida += str(dadosTokens[erro[0]][0])
            saida += "', a.k.a <" + str(dadosTokens[erro[0]][3]) + ">\n"
            saida += "Linha: " + str(dadosTokens[erro[0]][1]) + "\nColuna "
            saida += str(dadosTokens[erro[0]][2]) + "\n"
    print(saida)



def imprimeFluxoDeTokens(tokens):
    i = 0
    for item in tokens:
        print(item, i)
        i += 1

def imprimeTokens(dadosTokens):
    for item in dadosTokens:
        print('Lexema: {:24} Linha: {:3}   Coluna: {:3}   Tipo do Token: {}'.format(item[0], item[1],
                                                                                    item[2], item[3]))

def imprimeErrosAnaliseLexica(erros):
    for item in erros:
        print('Lexema: {:24} Linha: {:3}   Coluna: {:3}   Erro: {}'.format(item[0], item[1],
                                                                                    item[2], item[3]))

def imprimeTabela(tabela):
   print(tabela)



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
            if(linhas[i][j] == "/" and linhas[i][j] == "/"):
                j = len(linhas[i]) - 1
            elif(teste in dicBinarios):
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
        if(len(arrayLinha) == 0):
            arrayLinha.append('')
        linhas[i] = arrayLinha
    return linhas


main(sys.argv)
