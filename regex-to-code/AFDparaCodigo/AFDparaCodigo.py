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

    condicaoCaractere = Template('    if(codigo[indice] == "$letraTransicao"):\n' +\
                                 '        indice+=1\n' +\
                                 '        return q$estadoDestino(codigo,indice)\n')

    condicaoFinal = Template('    if(indice == len(codigo)):\n' +\
                             '        palavra = codigo[0:indice]\n' +\
                             '        linha = TABELA.insere(palavra)\n' +\
                             '        TOKENS.append(Token(palavra, linha))\n' +\
                             '        return $retorno\n')
    cabecalho = "#!/usr/bin/env python3\n" +\
                "# -*- coding: utf-8 -*-\n\n" +\
                "import sys\n\n" +\
                "from Token import Token\n" +\
                "from TabelaDeSimbolos import TabelaDeSimbolos\n\n" +\
                "TABELA = TabelaDeSimbolos()\n" +\
                "TOKENS = []\n\n"
    mainPrograma = Template("def main(args):\n" +\
                            "    arquivo = open(args[1], 'r')\n" +\
                            "    linhas = arquivo.read().splitlines()\n" +\
                            "    linhas = preProcessamento(linhas)\n" +\
                            "    print(linhas)\n" +\
                            "    for lin in range(len(linhas)):\n" +\
                            "        linhas[lin] = linhas[lin].split(' ')\n" +\
                            "        print(lin)\n" +\
                            "        cont = 0\n" +\
                            "        for item in range(len(linhas[lin])):\n" +\
                            "            if(linhas[lin][item] != ''):\n" +\
                            "                if(not q$estadoInicial(linhas[lin][item], 0)):\n" +\
                            "                    print('Erro na linha ' + str(lin + 1) + ' e coluna ' + str(cont + 1))\n" +\
                            "                cont += len(linhas[lin][item])\n" +\
                            "            else:\n" +\
                            "                cont += 1\n" +\
                            "    for item in TOKENS:\n" +\
                            "        print(item)\n" +\
                            "main(sys.argv)\n")
    preProcessamento = 'def preProcessamento(linhas):\n' +\
                       '    dicBinarios = {\n' +\
                       '        "+=" : "+=",\n' +\
                       '        "==" : "==",\n' +\
                       '        "++" : "++",\n' +\
                       '        "&&" : "&&",\n' +\
                       '        "<=" : "<=",\n' +\
                       '        "--" : "--"\n' +\
                       '    }\n' +\
                       '    \n' +\
                       '    dicUnarios = {\n' +\
                       '        "=" : "=",\n' +\
                       '        ">" : ">",\n' +\
                       '        "+" : "+",\n' +\
                       '        "!" : "!",\n' +\
                       '        "-" : "-",\n' +\
                       '        "*" : "*",\n' +\
                       '        "," : ",",\n' +\
                       '        "." : ".",\n' +\
                       '        "[" : "[",\n' +\
                       '        "{" : "{",\n' +\
                       '        "(" : "(",\n' +\
                       '        ")" : ")",\n' +\
                       '        "}" : "}",\n' +\
                       '        "]" : "]",\n' +\
                       '        ";" : ";"\n' +\
                       '    }\n' +\
                       '    for i in range(len(linhas)):\n' +\
                       '        nova = []\n' +\
                       '        j = 0\n' +\
                       '        while(j < len(linhas[i])):\n' +\
                       '            if(j < (len(linhas[i]) - 1)):\n' +\
                       '                teste = linhas[i][j:j + 2]\n' +\
                       '                if(teste in dicBinarios):\n' +\
                       '                    nova.append(" ")\n' +\
                       '                    nova.append(linhas[i][j])\n' +\
                       '                    nova.append(linhas[i][j + 1])\n' +\
                       '                    nova.append(" ")\n' +\
                       '                    j += 1\n' +\
                       '                elif(linhas[i][j] in dicUnarios):\n' +\
                       '                    nova.append(" ")\n' +\
                       '                    nova.append(linhas[i][j])\n' +\
                       '                    nova.append(" ")\n' +\
                       '                elif(linhas[i][j] == "\\t"):\n' +\
                       '                    nova.append(" ")\n' +\
                       '                else:\n' +\
                       '                    nova.append(linhas[i][j])\n' +\
                       '                    \n' +\
                       '            elif(linhas[i][j] in dicUnarios):\n' +\
                       '                nova.append(" ")\n' +\
                       '                nova.append(linhas[i][j])\n' +\
                       '                nova.append(" ")\n' +\
                       '            elif(linhas[i][j] == "\\t"):\n' +\
                       '                nova.append(" ")\n' +\
                       '            else:\n' +\
                       '                nova.append(linhas[i][j])\n' +\
                       '                j += 1\n' +\
                       '            j += 1\n'  +\
                       '        linhas[i] = "".join(nova)\n\n'  +\
                       '    return linhas\n\n'

    charLiteral = "def charLiteral(codigo, indice):\n" +\
                  "    if(len(codigo) == 4):\n" +\
                  "        if(codigo[1] != '\\\\'):\n" +\
                  "            return False\n" +\
                  "        if(codigo[3] != \"'\"):\n" +\
                  "            return False\n" +\
                  "        if(codigo[2] == '\"' or\n" +\
                  "           codigo[2] == \"'\" or\n" +\
                  "           codigo[2] == 'f'or\n" +\
                  "           codigo[2] == 'b' or\n" +\
                  "           codigo[2] == 't' or\n" +\
                  "           codigo[2] == 'r' or\n" +\
                  "           codigo[2] == 'n' or\n" +\
                  "           codigo[2] == '\\\\'):\n" +\
                  "            palavra = codigo[0:4]\n" +\
                  "            linha = TABELA.insere(palavra)\n" +\
                  "            TOKENS.append(Token(palavra, linha))\n" +\
                  "            return True\n" +\
                  "    if(len(codigo) == 3):\n" +\
                  "        if(codigo[2] != \"'\"):\n" +\
                  "            return False\n" +\
                  "        if(codigo[1] == '\\\\' or codigo[1] == \"'\"):\n" +\
                  "            return False\n" +\
                  "        palavra = codigo[0:3]\n" +\
                  "        linha = TABELA.insere(palavra)\n" +\
                  "        TOKENS.append(Token(palavra, linha))\n" +\
                  "        return True\n" +\
                  "    return False\n\n\n"



    stringLiteral = "def stringLiteral(codigo, indice):\n" +\
                  "    while(indice < len(codigo) - 1):\n" +\
                  "        if(codigo[indice] == '\\\\'):\n" +\
                  "            if(codigo[indice+1] == \"'\" or\n" +\
                  "               codigo[indice+1] == '\"' or\n" +\
                  "               codigo[indice+1] == 'f'or\n" +\
                  "               codigo[indice+1] == 'b' or\n" +\
                  "               codigo[indice+1] == 't' or\n" +\
                  "               codigo[indice+1] == 'r' or\n" +\
                  "               codigo[indice+1] == 'n' or\n" +\
                  "               codigo[indice+1] == '\\\\'):\n" +\
                  "                indice += 1\n\n" +\
                  "            else: \n" +\
                  "                return False\n" +\
                  "        indice+=1\n\n" +\
                  "    if(codigo[indice] != '\"'):\n" +\
                  "         return False\n" +\
                  "    else: \n" +\
                  "        palavra = codigo[0:indice+1]\n" +\
                  "        linha = TABELA.insere(palavra)\n" +\
                  "        TOKENS.append(Token(palavra, linha))\n" +\
                  "        return True\n"

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
