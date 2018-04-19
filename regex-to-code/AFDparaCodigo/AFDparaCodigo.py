#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
#~ from desenhaGrafo.fileHandler import lerAutomato
from string import Template
from AFDparaCodigo.Estado import Estado
from AFDparaCodigo.Transicao import Transicao
from AFDparaCodigo.Automato import Automato

class GeradorDeCodigo:

    automato = None

    definicaoClasse = Template('def q$nomeEstado(codigo, indice):\n')

    condicaoCaractere = Template(
"""
    if(codigo[indice] == "$letraTransicao"):
        indice+=1
        return q$estadoDestino(codigo,indice)
        
""")


    condicaoFinal = Template(
"""
    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return $retorno

""")


    cabecalho =''+\
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from Token import Token
from TabelaDeSimbolos import TabelaDeSimbolos

TABELA = TabelaDeSimbolos()
TOKENS = []


"""
 
                
    mainPrograma = Template(
"""def main(args):
    arquivo = open(args[1], 'r')
    linhas = arquivo.read().splitlines()
    linhas = preProcessamento(linhas)
    print(linhas)
    
    for lin in range(len(linhas)):
        print(linhas[lin])
        cont = 0
        
        for item in range(len(linhas[lin])):
            if(linhas[lin][item] != ''):
                if(not q$estadoInicial(linhas[lin][item], 0)):
                    print('Erro na linha ' + str(lin + 1) + ' e coluna ' + str(cont + 1))
                    
                cont += len(linhas[lin][item])
                
            else:
                cont += 1
                
    for item in TOKENS:
        print(item)

main(sys.argv)

""")
    preProcessamento = ''+\
"""
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
                    while(k < len(linhas[i]) and (linhas[i][k] != "'" or linhas[i][k - 1] == "\\\\")):
                        palavra += linhas[i][k]
                        k += 1
                    if(k < len(linhas[i])):
                        palavra += linhas[i][k]
                    arrayLinha.append(palavra)
                    j = k
                
                elif(aspasDuplas):
                    while(k < len(linhas[i]) and (linhas[i][k] != '"' or linhas[i][k - 1] == "\\\\")):
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
"""

    charLiteral = ''+\
"""def charLiteral(codigo, indice):
    if(len(codigo) == 4):
        if(codigo[1] != '\\\\'):
            return False
        if(codigo[3] != \"'\"):
            return False
        if(codigo[2] == '\"' or
           codigo[2] == \"'\" or
           codigo[2] == 'f'or
           codigo[2] == 'b' or
           codigo[2] == 't' or
           codigo[2] == 'r' or
           codigo[2] == 'n' or
           codigo[2] == '\\\\'):
            palavra = codigo[0:4]
            linha = TABELA.insere(palavra)
            TOKENS.append(Token(palavra, linha))
            return True
    if(len(codigo) == 3):
        if(codigo[2] != \"'\"):
            return False
        if(codigo[1] == '\\\\' or codigo[1] == \"'\"):
            return False
        palavra = codigo[0:3]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True
    return False
    
    
    
"""


    stringLiteral = ''+\
"""
def stringLiteral(codigo, indice):
    while(indice < len(codigo) - 1):
        if(codigo[indice] == '\\\\'):
            if(codigo[indice+1] == \"'\" or
               codigo[indice+1] == '\"' or
               codigo[indice+1] == 'f'or
               codigo[indice+1] == 'b' or
               codigo[indice+1] == 't' or
               codigo[indice+1] == 'r' or
               codigo[indice+1] == 'n' or
               codigo[indice+1] == '\\\\'):
                indice += 1
                
            else: 
                return False
                
        indice+=1
        
    if(codigo[indice] != '\"'):
         return False
         
    else: 
        palavra = codigo[0:indice+1]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True

"""

    def __init__(self,automato):
        self.automato = automato




    def gerarCodigo(self):
        resultado = self.cabecalho
        for estado in self.automato.estados:
            resultado += self.criaFuncao(estado)
        resultado += self.charLiteral
        resultado += self.stringLiteral
        resultado += self.preProcessamento
        resultado += self.criaMain(self.automato.estadosDic[self.automato.inicial])
        return resultado


    def criaFuncao(self,estado):
        if(estado.idEstado == "qERRO1"):
            return ""
        resultado = self.definicaoClasse.substitute(nomeEstado = estado.idEstado)
        if estado.final:
            resultado += self.condicaoFinal.substitute(retorno = 'True')
        else:
            resultado += self.condicaoFinal.substitute(retorno = 'False')
        for transicao in estado.transicoes:
            if(transicao.letra == "␣"):
                transicao.letra = " "
            if(transicao.letra == "virg"):
                transicao.letra = ","
            if(transicao.letra == "'anything'"):
                resultado += '    if(codigo[indice] == "\'"):\n' +\
                             '        indice+=1\n' +\
                             '        return charLiteral(codigo, indice)\n'
            elif(transicao.letra == '"anything"'):
                resultado += '    if(codigo[indice] == \'"\'):\n' +\
                             '        indice+=1\n' +\
                             '        return stringLiteral(codigo, indice)\n'
            else:
                resultado += self.condicaoCaractere.substitute(letraTransicao = transicao.letra, estadoDestino = transicao.destino.idEstado)
        resultado += "    return False\n\n"
        return resultado

    def criaMain(self, estadoInicial):
        return self.mainPrograma.substitute(estadoInicial = estadoInicial.idEstado)


def AFDparaCodigo(argv):
    if(len(argv) < 2):
        return
    entrada = argv[0]
    saida = argv[1]

    a = Automato(entrada)
    arquivo = open(saida, 'w')

    gdc = GeradorDeCodigo(a)
    arquivo.write(gdc.gerarCodigo())
