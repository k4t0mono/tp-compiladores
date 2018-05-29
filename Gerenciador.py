#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from Auto import Auto

class TipoToken(Enum):
    auto = Auto()

    OpAtribuicao = auto.get()
    OpIgualdade = auto.get()
    OpMaior = auto.get()
    OpIncremento = auto.get()
    OpAnd = auto.get()
    OpMenorIgual = auto.get()
    OpNot = auto.get()
    OpMenos = auto.get()
    OpDecremento = auto.get()
    OpSoma = auto.get()
    OpSomaAtribuicao = auto.get()
    OpMultiplicacao = auto.get()

    SepVirgula = auto.get()
    SepPonto = auto.get()
    SepAbreColchetes = auto.get()
    SepFechaColchetes = auto.get()
    SepAbreChaves = auto.get()
    SepFechaChaves = auto.get()
    SepAbreParenteses = auto.get()
    SepFechaParenteses = auto.get()
    SepPontoVirgula = auto.get()

    PCAbstract = auto.get()
    PCBoolean = auto.get()
    PCChar = auto.get()
    PCClass = auto.get()
    PCElse = auto.get()
    PCExtends = auto.get()
    PCFalse = auto.get()
    PCImport = auto.get()
    PCIf = auto.get()
    PCInstanceOf = auto.get()
    PCInt = auto.get()
    PCNew = auto.get()
    PCNull = auto.get()
    PCPackage = auto.get()
    PCPrivate = auto.get()
    PCProtected = auto.get()
    PCPublic = auto.get()
    PCReturn = auto.get()
    PCStatic = auto.get()
    PCSuper = auto.get()
    PCThis = auto.get()
    PCTrue = auto.get()
    PCVoid = auto.get()
    PCWhile = auto.get()

    IntLiteral = auto.get()
    CharLiteral = auto.get()
    StringLiteral = auto.get()

    Identificador = auto.get()

class Gerenciador:
    operadores = {
        "+=" : TipoToken.OpSomaAtribuicao,
        "==" : TipoToken.OpIgualdade,
        "++" : TipoToken.OpIncremento,
        "&&" : TipoToken.OpAnd,
        "<=" : TipoToken.OpMenorIgual,
        "--" : TipoToken.OpDecremento,
        "=" : TipoToken.OpAtribuicao,
        ">" : TipoToken.OpMaior,
        "+" : TipoToken.OpSoma,
        "!" : TipoToken.OpNot,
        "-" : TipoToken.OpMenos,
        "*" : TipoToken.OpMultiplicacao,
    }

    separadores = {
        "," : TipoToken.SepVirgula,
        "." : TipoToken.SepPonto,
        "[" : TipoToken.SepAbreColchetes,
        "]" : TipoToken.SepFechaColchetes,
        "{" : TipoToken.SepAbreChaves,
        "}" : TipoToken.SepFechaChaves,
        "(" : TipoToken.SepAbreParenteses,
        ")" : TipoToken.SepFechaParenteses,
        ";" : TipoToken.SepPontoVirgula
    }

    palavrasChaves = {
        "abstract" : TipoToken.PCAbstract,
        "boolean" : TipoToken.PCBoolean,
        "char" : TipoToken.PCChar,
        "class" : TipoToken.PCClass,
        "else" : TipoToken.PCElse,
        "extends" : TipoToken.PCExtends,
        "false" : TipoToken.PCFalse,
        "import" : TipoToken.PCImport,
        "if" : TipoToken.PCIf,
        "instanceof" : TipoToken.PCInstanceOf,
        "int" : TipoToken.PCInt,
        "new" : TipoToken.PCNew,
        "null" : TipoToken.PCNull,
        "package" : TipoToken.PCPackage,
        "private" : TipoToken.PCPrivate,
        "protected" : TipoToken.PCProtected,
        "public" : TipoToken.PCPublic,
        "return" : TipoToken.PCReturn,
        "static" : TipoToken.PCStatic,
        "super" : TipoToken.PCSuper,
        "this" : TipoToken.PCThis,
        "true" : TipoToken.PCTrue,
        "void" : TipoToken.PCVoid,
        "while" : TipoToken.PCWhile

    }


    def getTipoToken(self, palavra):
        if(palavra in self.operadores):
            return self.operadores[palavra]
        if(palavra in self.separadores):
            return self.separadores[palavra]
        if(palavra in self.palavrasChaves):
            return self.palavrasChaves[palavra]
        if(palavra.isdigit()):
            return TipoToken.IntLiteral
        if(palavra[0] == "'" and palavra[len(palavra) - 1] == "'"):
            return TipoToken.CharLiteral
        if(palavra[0] == '"' and palavra[len(palavra) - 1] == '"'):
            return TipoToken.StringLiteral
        return TipoToken.Identificador
