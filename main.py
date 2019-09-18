#Grupo: Lucas Augusto de Castro; Bryan Verneck; Lucas Dall Agnol; Rodrigo Zanella; Leonardo Cleyton

from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { ID, MAIS, MENOS, DIV, MULT, E, OU, MENOR, MAIOR, IGUAL, MAIORIGUAL, MENORIGUAL, DIFERENTE, ATRIBUICAO, SE, ENTAO, SENAO, FIMSE, PARA, FIMPARA, IMPRIMA, LEIA, TIPO, DOISPONTOS, INTEIRO, PONTOVIRGULA, INICIO,FIM, LPAREN,RPAREN,NUM ,STRING, ATE, PASSO}
    ignore = ' \t'

    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*\"'
    NUM = r'\d+'
    LPAREN = r'\('
    RPAREN = r'\)'
    MAIS = r'\+'
    MENOS = r'-'
    MULT = r'\*'
    DIV = r'/'
    ATRIBUICAO = r'\<-'
    MENOR = r'<'
    MAIOR = r'>'
    IGUAL = r'='
    MAIORIGUAL = r'>='
    MENORIGUAL = r'<='
    DIFERENTE = r'<>'
    PONTOVIRGULA = r';'
    DOISPONTOS = r'\:'


    # Special cases (ex.: palavras reservadas)
    ID['se']=SE
    ID['inicio']= INICIO
    ID['fim'] = FIM
    ID['inteiro'] = INTEIRO
    ID['entao'] = ENTAO
    ID['senao'] = SENAO
    ID['fim_se'] = FIMSE
    ID['para'] = PARA
    ID['fim_para'] = FIMPARA
    ID['imprima'] = IMPRIMA
    ID['leia'] = LEIA
    ID['E'] = E
    ID['OU'] = OU
    ID['ate'] = ATE
    ID['passo'] = PASSO


    # Ignored pattern
    ignore_newline = r'\n+'

    # Sintatico (Parser)
class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', MAIS, MENOS),
        ('left', MULT, DIV)
    )

    def __init__(self):
        print('Inicializando...')
    @_('codigo')
    def statement(self,p):
        print(p.codigo)

    @_('comando')
    def statement(self,p):
        print(p.comando)

    @_('boolean')
    def statement(self,p):
        print(p.verifica)

    #definiçao id ou num
    @_('id_num')
    def statement(self, p):
        print(p.id_num)
        
    @_('ID')
    def id_num(self,p):
        return p.ID

    @_('NUM')
    def id_num(self, p):
        return p.NUM

    @_('id_num IGUAL id_num')
    def boolean(self, p):
        return(p.id_num0 == p.id_num1)
    
    @_('id_num MAIOR id_num')
    def boolean(self, p):
        return(p.id_num0 > p.id_num1)

    @_('id_num MENOR id_num')
    def boolean(self, p):
        return(p.id_num0 < p.id_num1)
    
    @_('id_num DIFERENTE id_num')
    def boolean(self, p):
        return(p.id_num0 != p.id_num1)

    @_('id_num MENORIGUAL id_num')
    def boolean(self, p):
        return(p.id_num0 <= p.id_num1)

    @_('id_num MAIORIGUAL id_num')
    def boolean(self, p):
        return(p.id_num0 >= p.id_num1)     

 

    @_('INICIO comando FIM')
    def codigo(self,p):
        return(p.INICIO, p.comando, p.FIM)


    @_('ID ATRIBUICAO NUM PONTOVIRGULA')
    def comando(self,p):
        return (p.ID, p.ATRIBUICAO, p.NUM, p.PONTOVIRGULA)

    @_('ID ATRIBUICAO NUM PONTOVIRGULA comando')
    def comando(self, p):
        return (p.ID, p.ATRIBUICAO, p.NUM, p.PONTOVIRGULA, p.comando)

    @_('INTEIRO DOISPONTOS ID PONTOVIRGULA')
    def comando(self,p):
        return(p.INTEIRO,p.DOISPONTOS, p.ID, p.PONTOVIRGULA)

    @_('INTEIRO DOISPONTOS ID PONTOVIRGULA comando')
    def comando(self, p):
        return (p.INTEIRO, p.DOISPONTOS, p.ID, p.PONTOVIRGULA, p.comando)

    @_('IMPRIMA LPAREN STRING RPAREN PONTOVIRGULA')
    def comando(self,p):
        return(p.IMPRIMA, p.LPAREN, p.STRING, p.RPAREN, p.PONTOVIRGULA)

    @_('IMPRIMA LPAREN STRING RPAREN PONTOVIRGULA comando')
    def comando(self, p):
        return (p.IMPRIMA, p.LPAREN, p.STRING, p.RPAREN, p.PONTOVIRGULA, p.comando)

    @_('LEIA LPAREN ID RPAREN PONTOVIRGULA')
    def comando(self, p):
        return (p.LEIA, p.LPAREN, p.ID, p.RPAREN, p.PONTOVIRGULA)

    @_('LEIA LPAREN ID RPAREN PONTOVIRGULA comando')
    def comando(self, p):
        return (p.LEIA, p.LPAREN, p.ID, p.RPAREN, p.PONTOVIRGULA, p.comando)

    @_('SE boolean ENTAO comando FIMSE')
    def comando(self, p):
        if(p.boolean):
            return (p.SE, p.boolean, p.ENTAO, p.comando, p.FIMSE)
        else:
            return print("nao")

    @_('SE boolean ENTAO comando FIMSE comando')
    def comando(self, p):
        if (p.boolean):
            return (p.SE, p.boolean, p.ENTAO, p.comando, p.FIMSE,p.comando1)
        else:
            return print("nao")

    
    @_('SE boolean ENTAO comando SENAO comando FIMSE')
    def comando(self,p):
        if(p.boolean):
            return(p.SE, p.boolean, p.ENTAO, p.comando0,p.FIMSE)
        return p.SE, p.boolean, p.SENAO, p.comando1,p.FIMSE

    @_('SE boolean ENTAO comando SENAO comando FIMSE comando')
    def comando(self,p):
        if (p.boolean):
            return (p.SE, p.boolean, p.ENTAO, p.comando0, p.FIMSE,p.comando2)
        return p.SE, p.boolean, p.SENAO, p.comando1, p.FIMSE,p.comando2

    @_('PARA ID ATRIBUICAO id_num ATE id_num PASSO id_num comando FIMPARA')
    def comando(self,p):
        print(p.PARA, p.ID, p.ATRIBUICAO, p.id_num0, p.ATE,p.id_num1, p.PASSO, p.id_num2)
        for i in range(int(p.id_num0), int(p.id_num1), int(p.id_num2)):

            print(p.comando)
        print(p.FIMPARA)

    @_('PARA ID ATRIBUICAO id_num ATE id_num PASSO id_num comando FIMPARA comando')
    def comando(self,p):
        print(p.PARA, p.ID, p.ATRIBUICAO, p.id_num0, p.ATE, p.id_num1, p.PASSO, p.id_num2)
        for i in range(int(p.id_num0), int(p.id_num1), int(p.id_num2)):
            print(p.comando0)
        print(p.FIMPARA)
        return p.comando1
    

    
    

    # Regras gramaticais
    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('expr MAIS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MENOS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr MULT expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIV expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUM')
    def expr(self, p):
        return int(p.NUM)


diretorio = 'teste.txt'
fp = open(diretorio, "r")
texto = fp.read()
fp.close

lexer = CalcLexer()
parser = CalcParser()

for tok in lexer.tokenize(texto):
    print('token=%r, lexema=%r' % (tok.type, tok.value))

result = parser.parse(lexer.tokenize(texto))
print(result)
