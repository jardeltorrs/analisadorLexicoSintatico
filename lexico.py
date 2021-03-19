import pandas as pd

class Lexico:
    def __init__(self, file):
        self.file = open(file)
        self.out = pd.DataFrame(columns=["Lexema", "Padrão", "Token", "Linha"])
        self.symbolTable = pd.DataFrame(columns=["value", "number" ])
        self.lexemasReserveString = [
            "class",
            "public",
            "static",
            "void",
            "main",
            "String",
            "extends",
            "return",
            "int",
            "boolean",
            "if",
            "while",
            "System.out.println",
            "length",
            "true",
            "false",
            "new"
        ]
        self.symbols = [
            "(", ")",
            "[", "]",
            "{", "}"
        ]
        self.stackK = [] #pilha de chaves
        self.stackP = [] #pilha de parenteses
        self.stackC = [] #pilha de cochetes
        self.stack  = []

    def structure(self):
        list = self.mainClass()
        if list != "":
            self.classDeclaration(list[0], list[1])
        print("-----------------------")
        print(self.symbolTable)

    def mainClass(self):
        mc = ["class", "Identifier", "{", "public", "static", "void", "main", "(", "String", "[", "]", "Identifier", ")",
              "{", "Statement", "}", "}"]
        token = ""
        countIdentifier = 0;
        countLine = 0
        est = 0
        for line in self.file:
            countLine += 1
            i = 0
            while i < len(line):
                if line[i] != " " and line[i] != "" and line[i] != "\n":
                    token = token + line[i]
                    if token == mc[est] or mc[est] == "Identifier" or mc[est] == "Statement":
                        if mc[est] == "Identifier":
                            l = self.identifier(line, i)
                            if l == "":
                                print("erro line ", countLine)
                                return ""
                            else:
                                countIdentifier += 1
                                self.createRow(l[0], countLine)
                                self.symbolTable = self.symbolTable.append(
                                    {"value": l[0], "number": countIdentifier}, ignore_index=True)

                                i = l[2] - 1
                                token = ""
                            est += 1
                        elif mc[est] == "Statement":
                            self.statement(i+1, countLine)
                            est += 1
                            token = ""
                        elif mc[est] in self.symbols:
                            for j in range(len(self.symbols)):
                                if mc[est] == self.symbols[j]:
                                    if j % 2 == 0:
                                        self.createRow(token, countLine)
                                        self.stack.append("#")
                                        break
                                    else:
                                        self.createRow(token, countLine)
                                        self.stack.pop()
                                        break
                            est += 1
                            token = ""
                        else:
                            self.createRow(token, countLine)
                            token = ""
                            est += 1

                i += 1
        print(est)


        print(self.out)
        return [line, i]

    def classDeclaration(self, r, e):
        for r in self.file:
            for e in r:
                print("", end="")
                #print(e, end="")

    def identifier(self, re, be):
        stt = 1
        txt = ""
        for b in range(len(re)):
            b = be
            if stt == 1:
                if re[b] >= "a" and re[b] <= "z":
                    txt += re[b]
                    stt+=1
                elif re[b] >= "A" and re[b] <= "Z":
                    txt += re[b]
                    stt += 1
                elif re[b] == "_":
                    txt += re[b]
                    stt += 1
                elif re[b] != " " and re[b] != "" and re[b] != "\n":
                    return ""
            else:
                if re[b] >= "a" and re[b] <= "z":
                    txt +=re[b]
                elif re[b] >="A" and re[b] <="Z":
                    txt +=re[b]
                elif re[b] >="0" and re[b] <="9":
                    txt +=re[b]
                elif re[b] == "_":
                    txt +=re[b]
                else:
                    if txt in self.lexemasReserveString:
                        print("palavra reservada")
                        return ""
                    else:
                        return [txt, re, b]
            be += 1

    def createToken(self, text, cont):
        if text == "identifier":
            return "<Identifier, " + cont + ">"
        return "<" + text + ",>"

    def pattern(self, text):
        for r in self.lexemasReserveString:
            if (r == text):
                return "ReserveString"
        for r in self.symbols:
            if r == text:
                return r
        return "Identifier"

    def createRow(self, aux, cont):
        tk = self.createToken(aux, cont)
        stdd = self.pattern(aux)
        self.out = self.out.append(
            {"Lexema": aux, "Padrão": stdd, "Token": tk, "Linha": cont},
            ignore_index=True)

    def statement(self, i, countLine):
        cont = 1
        print(i)
        tk =""
        for l in self.file:
            if cont >= countLine:
                while i < len(l):
                    if l[i] != " " and l[i] != "" and l[i] != "\n":
                        tk += l[i]
                        if tk == "System.out.println":
                            self.createRow(tk, cont)
                            i+=1

                            if l[i] != " " and l[i] != "" and l[i] != "\n":
                                if l[i] =="(":
                                    self.createRow(l[i], cont)
                            print(tk, end="")
                    i += 1
                i = 0

            cont += 1
        return [i, cont]

    def close(self):
        self.file.close()

'''if token == "class" and est == 1:
                        self.createRow(token, countLine)

                        est += 1

                        l = self.identifier(line, i + 1)
                        if l == "":
                            print("erro line ", countLine)
                            return ""
                        else:
                            self.createRow(l[0], countLine)
                            i = l[2] - 1
                            token = ""

                    elif token == "{" and est == 2:
                        est += 1
                        self.createRow(token, countLine)
                        self.stackK.append("{")
                        token = ""
                    elif token == "public" and est == 3:
                        est += 1
                        print(est)
                        self.createRow(token, countLine)
                        token = ""
                    elif token == "static" and est == 4:
                        est += 1
                        self.createRow(token, countLine)
                        token = ""
                    elif token == "void" and est == 5:
                        est += 1
                        self.createRow(token, countLine)
                        token = ""
                    elif token == "main" and est == 6:
                        est += 1
                        self.createRow(token, countLine)
                        token = ""
                    elif token == "(" and est == 7:
                        est += 1
                        self.createRow(token, countLine)
                        self.stackP.append("(")
                        token = ""
                    elif token == "String" and est == 8:
                        est += 1
                        self.createRow(token, countLine)
                        token = ""
                    elif token == "[" and est == 9:
                        est += 1
                        self.createRow(token, countLine)
                        self.stackC.append("[")
                        token = ""
                    elif token == "]" and est == 10:
                        est += 1
                        self.createRow(token, countLine)
                        self.stackC.pop()
                        l = self.identifier(line, i+1)
                        if l == "":
                            print("erro line ", countLine)
                            return ""
                        else:
                            self.createRow(l[0], countLine)
                            i = l[2] - 1
                            token = ""
                    elif token == ")" and est == 11:
                        est += 1
                        self.createRow(token, countLine)
                        self.stackP.pop()
                        token = ""
                    elif token == "{" and est == 12:
                        est += 1
                        self.createRow(token, countLine)
                        self.stackK.append("{")
                        self.statement(i, countLine)
                        token = ""
                    elif token == "}" and est == 13:
                        est += 1
                        print(est)
                        token = ""
                    elif token == "}" and est == 14:
                        est += 1
                        print(est)
                        token = ""
                    else:
                        print(end="")'''