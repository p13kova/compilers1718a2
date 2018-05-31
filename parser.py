



 

import plex
'''
Stmt_list-> Stmt Stmt_list | ε.
Stmt->Expr | print Expr.
Expr-> Term Term_tail.
Term_tail->Logic Term Term_tail | ε.
Term-> Factor Factor_tail.
Factor_tail ->Neg Factor Factor_tail | ε.
Factor->(Expr) | id |boolean | e.
Logic->and|or.
Neg-> not.
'''

 #dimiourgia klashs parser opou dhlwnontai oi aparaithtes plhrfories kanontas xrhsh toy plex    
class ParseError(Exception):
	pass

class MyParser:   
    def _init_(self):
        self.st = {}

    def create_scanner(self,fp):
        letter = plex.Range ('azAZ')                  
        digit = plex.Range ('09')                     


        telestis = plex.Str ('=')                     
        parenthesi = plex.Str ('(',')')               
        int_num = plex.Rep1(digit)
        name = letter+plex.Rep(letter | digit)
        space = plex.Rep1(plex.Any(' \n\t'))           
        keyword = plex.Str('print')
                   
        logic = plex.NoCase (plex.Str('and','or'))
        logicNot = plex.NoCase (plex.Str('not'))
        booleanT = plex.NoCase(plex.Str('true','t','1'))
        booleanF = plex.NoCase (plex.Str('false','f','0'))

        lexicon = plex.Lexicon ([                      
			(keyword, plex.TEXT),
			(name, 'Identifier'),
			(space, plex.IGNORE),
			(telestis, '='),
			(parenthesi, plex.TEXT),
			(int_num, 'INTEGER'),
			(logicNot, 'not'),
			(booleanT ,'BooleanT'),
            (booleanF, 'BooleanF'),
            (logic , plex.TEXT)
			
					])

        self.scanner = plex.Scanner(lexicon,fp)
        self.la,self.val = self.next_token()
	
    def parse(self,fp):
        self.create_scanner(fp)		
        self.stmt_list()
		
    def match(self,token):		
        if self.la == token:
           self.la,self.val = self.next_token()				
        else:			
            raise ParseError("Cant match self.la with current token ( self.la: {} current token: {} )".format(self.la,token))
			
    def next_token(self):
        return self.scanner.read()
    def getValue(self,token,text):
        pass

    def stmt_list(self):
#prwtos kanonas ths grammatikis poy perimenei san eisodo mia metavliti h thn desmeumeni leksi print kai thn apostelei sto epomeno vima ths grammatikis
        if self.la == 'Identifier':  
           self.stmt()
           self.stmt_list()
        elif self.la == 'print':
            self.stmt()
            self.stmt_list()
        elif self.la is None:
           return
        else:
            raise ParseError('perimenw identifier h print')

    def stmt(self): #analoga ti exei lavei ws eisodo apostelei tis plirofories sthn klasi expr() h deixnei minima lathous se periptwsh poy den plhroi tis proupotheseis to arxeio eisodou
        if self.la == 'Identifier' :
			
            self.match ('Identifier')
            self.match ('=')
            self.expr()

        elif self.la == 'print':
             self.match('print')
             self.expr()
        else:
           raise ParseError('perimenw identifier h print')

    def expr(self): # o sugkekrimenos kanonas ths grammatikis analoga thn eisodo poy lavei apo to proigoymeno vima apostelei tis plirofories. oi apodektes times einai parenthesi, metavliti h kapoia boolean metavliti

        if self.la == '(' or self.la == 'Identifier' or self.la == 'booleanT' or  self.la == ('booleanF') or self.la == ('logicNot'):
            self.term()
            self.term_tail()
			

        else:
            raise ParseError ('1perimenontas kati allo')
#oi epomenes 3 klaseis anagnwrizoyn ton telesth boolean twn dedomenwn kai ekteloun tis analoges energeies symfwna me toys kanones poy exoyn oristei sthn grammatiki

    def term_tail(self):   
        if self.la in ('or', 'and'):
            self.logic()
            self.term()
            self.term_tail()
        elif self.la in ('IDENTIFIER','print',None,')'):
           return   
        else:
            raise ParseError ('2perimenontas kati allo')


    def term(self):
        if self.la == '(' or self.la == 'booleanT' or self.la == 'booleanF' or self.la == ('logicNot') or self.la == 'Identifier':
            self.factor ()
            self.factor_tail()
            
        else:
                raise ParseError('3perimenontas kati allo')

    def factor_tail(self):
        if self.la in ('not'):
            self.neg()
            self.factor()
            self.factor_tail()
          
        else:
            raise ParseError ('4perimenontas kati allo')
    


    def factor(self):
        if self.la == '(':
            self.match('(')
            self.expr()
            self.match(')')
            return e
        elif self.la == 'Identifier':   
             self.match('Identifier')
            
        elif self.la == "booleanT":
            
            self.match('booleanT')
        elif self.la == 'booleanF':
            self.match('booleanF')  
        elif self.la in ('and','or','not','IDENTIFIER','print',None,')'):
           return     
        else:
            raise ParseError ('5perimenontas kati allo')


    def logic(self): #klasi pou matsarei tis eiserxomenes logikes times
        if self.la == 'and':
            self.match('and')
           
        elif self.la == 'or':
            self.match('or')
           
        
        else:
            raise ParseError('error')

    def neg(self):
        if self.la == 'not':
            self.match ('not')
        else:
            raise ParseError ('error')

parser = MyParser()  # adikeimeno ths klasshs myparser

with open('recursive.txt') as fp:
   try:

    print('Checking Syntax \n')
    parser.parse(fp)
    print('Syntax is correct !!')
    
   except ParseError as perr:
    print (perr)


