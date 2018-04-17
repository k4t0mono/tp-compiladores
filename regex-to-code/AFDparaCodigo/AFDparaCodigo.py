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
                             '        print("token: " + palavra)\n' +\
                             '        return $booleano\n')
    cabecalho = "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\nimport sys\n\n"
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
                            "                    print('ERRO: ' + str(lin + 1) + ' ' + str(cont + 1))\n" +\
                            "                cont += len(linhas[lin][item])\n" +\
                            "            else:\n" +\
                            "                cont += 1\n" +\
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
                       '                elif(linhas[i][j] == "\t"):\n' +\
                       '                    nova.append(" ")\n' +\
                       '                else:\n' +\
                       '                    nova.append(linhas[i][j])\n' +\
                       '                    \n' +\
                       '            elif(linhas[i][j] in dicUnarios):\n' +\
                       '                nova.append(" ")\n' +\
                       '                nova.append(linhas[i][j])\n' +\
                       '                nova.append(" ")\n' +\
                       '            elif(linhas[i][j] == "\t"):\n' +\
                       '                nova.append(" ")\n' +\
                       '            else:\n' +\
                       '                nova.append(linhas[i][j])\n' +\
                       '                j += 1\n' +\
                       '            j += 1\n'  +\
                       '        linhas[i] = "".join(nova)\n\n'  +\
                       '    return linhas\n\n'
                       
    def __init__(self,automato):
        self.automato = automato
    
    def gerarCodigo(self):
        resultado = self.cabecalho
        for estado in self.automato.estados:
            resultado += self.criaFuncao(estado)
        resultado += self.preProcessamento
        resultado += self.criaMain(self.automato.estadosDic[self.automato.inicial])
        return resultado
        
    
    def criaFuncao(self,estado):
        if(estado.idEstado == "qERRO1"):
            return ""
        resultado = self.definicaoClasse.substitute(nomeEstado = estado.idEstado)
        if estado.final:
            resultado += self.condicaoFinal.substitute(booleano = 'True')
        else:
            resultado += self.condicaoFinal.substitute(booleano = 'False')
        for transicao in estado.transicoes:
            if(transicao.letra == "␣"):
                transicao.letra = " "
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
