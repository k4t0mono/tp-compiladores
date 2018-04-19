
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
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q1(codigo,indice)
        

    if(codigo[indice] == "i"):
        indice+=1
        return q2(codigo,indice)
        

    if(codigo[indice] == "&"):
        indice+=1
        return q3(codigo,indice)
        

    if(codigo[indice] == "r"):
        indice+=1
        return q4(codigo,indice)
        

    if(codigo[indice] == "("):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "f"):
        indice+=1
        return q6(codigo,indice)
        

    if(codigo[indice] == "="):
        indice+=1
        return q7(codigo,indice)
        

    if(codigo[indice] == "b"):
        indice+=1
        return q8(codigo,indice)
        

    if(codigo[indice] == "-"):
        indice+=1
        return q9(codigo,indice)
        

    if(codigo[indice] == "}"):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "c"):
        indice+=1
        return q10(codigo,indice)
        

    if(codigo[indice] == "]"):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "t"):
        indice+=1
        return q11(codigo,indice)
        

    if(codigo[indice] == ";"):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "v"):
        indice+=1
        return q12(codigo,indice)
        

    if(codigo[indice] == "n"):
        indice+=1
        return q13(codigo,indice)
        

    if(codigo[indice] == ">"):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "s"):
        indice+=1
        return q14(codigo,indice)
        

    if(codigo[indice] == "{"):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "<"):
        indice+=1
        return q15(codigo,indice)
        

    if(codigo[indice] == "p"):
        indice+=1
        return q16(codigo,indice)
        

    if(codigo[indice] == "["):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == ")"):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "!"):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "*"):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "e"):
        indice+=1
        return q17(codigo,indice)
        

    if(codigo[indice] == "w"):
        indice+=1
        return q18(codigo,indice)
        

    if(codigo[indice] == "+"):
        indice+=1
        return q19(codigo,indice)
        
    return False

def q1(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "b"):
        indice+=1
        return q37(codigo,indice)
        
    return False

def q2(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "f"):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "n"):
        indice+=1
        return q20(codigo,indice)
        

    if(codigo[indice] == "m"):
        indice+=1
        return q21(codigo,indice)
        
    return False

def q3(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "&"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q4(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "e"):
        indice+=1
        return q22(codigo,indice)
        
    return False

def q5(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True

    return False

def q6(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q23(codigo,indice)
        
    return False

def q7(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True


    if(codigo[indice] == "="):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q8(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "o"):
        indice+=1
        return q24(codigo,indice)
        
    return False

def q9(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True


    if(codigo[indice] == "-"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q10(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "h"):
        indice+=1
        return q60(codigo,indice)
        

    if(codigo[indice] == "l"):
        indice+=1
        return q61(codigo,indice)
        
    return False

def q11(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "r"):
        indice+=1
        return q38(codigo,indice)
        

    if(codigo[indice] == "h"):
        indice+=1
        return q39(codigo,indice)
        
    return False

def q12(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "o"):
        indice+=1
        return q76(codigo,indice)
        
    return False

def q13(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "u"):
        indice+=1
        return q25(codigo,indice)
        

    if(codigo[indice] == "e"):
        indice+=1
        return q26(codigo,indice)
        
    return False

def q14(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "u"):
        indice+=1
        return q27(codigo,indice)
        

    if(codigo[indice] == "t"):
        indice+=1
        return q28(codigo,indice)
        
    return False

def q15(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "="):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q16(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q40(codigo,indice)
        

    if(codigo[indice] == "u"):
        indice+=1
        return q41(codigo,indice)
        

    if(codigo[indice] == "r"):
        indice+=1
        return q42(codigo,indice)
        
    return False

def q17(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "l"):
        indice+=1
        return q29(codigo,indice)
        

    if(codigo[indice] == "x"):
        indice+=1
        return q30(codigo,indice)
        
    return False

def q18(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "h"):
        indice+=1
        return q62(codigo,indice)
        
    return False

def q19(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return True


    if(codigo[indice] == "="):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "+"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q20(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "t"):
        indice+=1
        return q5(codigo,indice)
        

    if(codigo[indice] == "s"):
        indice+=1
        return q31(codigo,indice)
        
    return False

def q21(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "p"):
        indice+=1
        return q80(codigo,indice)
        
    return False

def q22(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "t"):
        indice+=1
        return q32(codigo,indice)
        
    return False

def q23(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "l"):
        indice+=1
        return q29(codigo,indice)
        
    return False

def q24(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "o"):
        indice+=1
        return q33(codigo,indice)
        
    return False

def q25(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "l"):
        indice+=1
        return q63(codigo,indice)
        
    return False

def q26(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "w"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q27(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "p"):
        indice+=1
        return q43(codigo,indice)
        
    return False

def q28(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q34(codigo,indice)
        
    return False

def q29(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "s"):
        indice+=1
        return q35(codigo,indice)
        
    return False

def q30(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "t"):
        indice+=1
        return q44(codigo,indice)
        
    return False

def q31(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "t"):
        indice+=1
        return q45(codigo,indice)
        
    return False

def q32(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "u"):
        indice+=1
        return q36(codigo,indice)
        
    return False

def q33(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "l"):
        indice+=1
        return q77(codigo,indice)
        
    return False

def q34(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "t"):
        indice+=1
        return q46(codigo,indice)
        
    return False

def q35(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "e"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q36(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "r"):
        indice+=1
        return q64(codigo,indice)
        
    return False

def q37(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "s"):
        indice+=1
        return q47(codigo,indice)
        
    return False

def q38(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "u"):
        indice+=1
        return q35(codigo,indice)
        
    return False

def q39(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "i"):
        indice+=1
        return q65(codigo,indice)
        
    return False

def q40(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "c"):
        indice+=1
        return q48(codigo,indice)
        
    return False

def q41(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "b"):
        indice+=1
        return q84(codigo,indice)
        
    return False

def q42(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "i"):
        indice+=1
        return q49(codigo,indice)
        

    if(codigo[indice] == "o"):
        indice+=1
        return q50(codigo,indice)
        
    return False

def q43(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "e"):
        indice+=1
        return q51(codigo,indice)
        
    return False

def q44(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "e"):
        indice+=1
        return q72(codigo,indice)
        
    return False

def q45(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q52(codigo,indice)
        
    return False

def q46(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "i"):
        indice+=1
        return q66(codigo,indice)
        
    return False

def q47(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "t"):
        indice+=1
        return q53(codigo,indice)
        
    return False

def q48(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "k"):
        indice+=1
        return q54(codigo,indice)
        
    return False

def q49(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "v"):
        indice+=1
        return q67(codigo,indice)
        
    return False

def q50(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "t"):
        indice+=1
        return q55(codigo,indice)
        
    return False

def q51(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "r"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q52(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "n"):
        indice+=1
        return q56(codigo,indice)
        
    return False

def q53(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "r"):
        indice+=1
        return q68(codigo,indice)
        
    return False

def q54(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q57(codigo,indice)
        
    return False

def q55(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "e"):
        indice+=1
        return q81(codigo,indice)
        
    return False

def q56(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "c"):
        indice+=1
        return q58(codigo,indice)
        
    return False

def q57(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "g"):
        indice+=1
        return q35(codigo,indice)
        
    return False

def q58(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "e"):
        indice+=1
        return q59(codigo,indice)
        
    return False

def q59(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "o"):
        indice+=1
        return q73(codigo,indice)
        
    return False

def q60(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q51(codigo,indice)
        
    return False

def q61(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q69(codigo,indice)
        
    return False

def q62(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "i"):
        indice+=1
        return q74(codigo,indice)
        
    return False

def q63(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "l"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q64(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "n"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q65(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "s"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q66(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "c"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q67(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q78(codigo,indice)
        
    return False

def q68(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q70(codigo,indice)
        
    return False

def q69(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "s"):
        indice+=1
        return q65(codigo,indice)
        
    return False

def q70(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "c"):
        indice+=1
        return q71(codigo,indice)
        
    return False

def q71(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "t"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q72(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "n"):
        indice+=1
        return q75(codigo,indice)
        
    return False

def q73(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "f"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q74(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "l"):
        indice+=1
        return q35(codigo,indice)
        
    return False

def q75(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "d"):
        indice+=1
        return q65(codigo,indice)
        
    return False

def q76(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "i"):
        indice+=1
        return q82(codigo,indice)
        
    return False

def q77(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "e"):
        indice+=1
        return q79(codigo,indice)
        
    return False

def q78(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "t"):
        indice+=1
        return q35(codigo,indice)
        
    return False

def q79(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "a"):
        indice+=1
        return q64(codigo,indice)
        
    return False

def q80(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "o"):
        indice+=1
        return q83(codigo,indice)
        
    return False

def q81(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "c"):
        indice+=1
        return q85(codigo,indice)
        
    return False

def q82(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "d"):
        indice+=1
        return q5(codigo,indice)
        
    return False

def q83(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "r"):
        indice+=1
        return q71(codigo,indice)
        
    return False

def q84(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "l"):
        indice+=1
        return q46(codigo,indice)
        
    return False

def q85(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "t"):
        indice+=1
        return q86(codigo,indice)
        
    return False

def q86(codigo, indice):

    if(indice == len(codigo)):
        palavra = codigo[0:indice]
        linha = TABELA.insere(palavra)
        TOKENS.append(Token(palavra, linha))
        return False


    if(codigo[indice] == "e"):
        indice+=1
        return q82(codigo,indice)
        
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
            elif(linhas[i][j] == "	" or linhas[i][j] == " "):
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
                           linhas[i][k] == "	" or
                           linhas[i][k] == " "):
                            arrayLinha.append(palavra)
                            acabou = True
                            j = k - 1
                        else:
                            palavra += linhas[i][k]
                            k += 1
                    if(k == len(linhas[i]) - 1):
                        if(linhas[i][k] in dicUnarios or
                           linhas[i][k] == "	" or
                           linhas[i][k] == " "):
                            arrayLinha.append(palavra)
                            j = k - 1
                        else:
                            palavra += linhas[i][k]
                            arrayLinha.append(palavra)
                            j = k
                        
            j += 1
        if(j == len(linhas[i]) - 1):
            if(linhas[i][j] == "	" or linhas[i][j] == " "):
                arrayLinha.append('')
            else:
                arrayLinha.append(linhas[i][j])
                
        linhas[i] = arrayLinha
        print(arrayLinha)
        
    return linhas
def main(args):
    arquivo = open(args[1], 'r')
    linhas = arquivo.read().splitlines()
    linhas = preProcessamento(linhas)
    print(linhas)
    
    for lin in range(len(linhas)):
        #~ linhas[lin] = linhas[lin].split(' ')
        print(linhas[lin])
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

