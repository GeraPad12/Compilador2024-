#############################################################
# Compilador Lexico                                         #
# Fecha:      7 de Marzo del 2024                           #
# Integrantes:                                              #
#             Jose RafaeL Ruvalcaba Sierra                  #
#             Carlos Eduardo Arriaga Yañez                  #
#             Gerardo Yair Padilla Belmonte                 #
#############################################################
import sys
sys.stdout.reconfigure(encoding='utf-8')#caracteres especiales


ERR = -1
ACP = 999
entrada = '' 
idx = 0
bERR = False
lex = ''
tok = ''
archE = ''
conLin = 1
conCol = 0
conCod = 1
ctelog = ['verdadero', 'falso']
palRes = ['fn', 'principal', 'imprimeln!', 'imprimeln', 'entero', 'const',
          'decimal', 'logico', 'alfabetico', 'sea', 'si', 'sino', 
          'para', 'en', 'mientras', 'ciclo', 'regresa', 'leer', 'interrumpe', 
          'continua','mut']

tabSim = {}

progm = [
        ]

def initPrgm():
    global progm
    for i in range(0, 10000):
        progm.append([])


def insCodigo(Lin, cod):
    global progm
    progm[conLin] = cod


def insTabSim(key, colec):
    global tabSim
    tabSim[key] = colec

def colCar( c ):
    if c.isalpha():     return 0
    if c == '_':        return 1
    if c == '.':        return 2
    if c.isdigit():     return 3
    if c in opa:        return 4
    if c == '&':        return 5
    if c == '!':        return 6
    if c == '=':        return 7
    if c == '"':        return 8
    if c == '/':        return 9
    if c in ['<', '>']: return 10
    if c == '|':        return 11
    if c in dlm:        return 12
    if c in sym:        return 13
    if c in [' ', '\t', '\n']: return 0
    print(c ,'NO es valido en el alfabeto del Lenguaje')
    return ERR


matran = [  #letra  #_   #.    #dig  #opa  #&   #!   #=   #""  #/   #<>  #|  #dlm #sym   
            [1,     1,   18,   2,    7,    8,   19,  14,  12,  5,   15,  10,  18  ,21 ], #0   
            [1,     1,   ACP,  1,    ACP,  ACP, 1,   ACP, ACP, ACP, ACP, ACP, ACP, ACP], #1
            [ACP,   ACP, 3,    2,    ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #2
            [ERR,   ERR, ERR,  4,    ERR,  ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR], #3
            [ACP,   ACP, ACP,  4,    ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #4
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, 6,   ACP, ACP, ACP, ACP], #5  
            [6,     6,   6,    6,    6,    6,   6,   6,   6,   6,   6,   6  , 6  , 6  ], #6
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #7
            [ERR,   ERR, ERR,  ERR,  ERR,  9,   ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR], #8
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #9 
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, ACP, ACP, 11 , ACP, ACP], #10 cambien todo ERR por ACP para sym |
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #11
            [12,    12,  12,   12,   12,   12,  12,  12,  13,  12,  12,  12,  12 , 12 ], #12 si llega " se va al 13
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #13
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, 20,  ACP, ACP, ACP, ACP, ACP, ACP], #14 aqui el 20 para ==
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, 16,  ACP, ACP, ACP, ACP, ACP, ACP], #15 aqui edite el 16 para <= >=
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #16 = 
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #17 = OPR
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #18 DLM
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, 17,  ACP, ACP, ACP, ACP, ACP, ACP], #19 ! OpL
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP], #20 agregue este para el == OpR
            [ACP,   ACP, ACP,  ACP,  ACP,  ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP]  #21 SYM
]

opa = ['+', '-', '*', '%', '^']
dlm = ['[', ']', '{', '}', '(', ')', ',', ';', ':']
sym = ['#','$','¿','?','¡','°','¬', '@', '`', '~',"\\"]


def erra(rn, cl, erx, desE):
    global bERR
    bERR = True
    print('['+str(rn)+']['+str(cl)+']' +erx + " " + desE)
    

def lexico():
    global entrada, ERR, ACP, matran, idx, conLin, conCol
    estado = 0
    estAnt = 0
    lex = ''
    tok = ''
    while idx < len(entrada) and estado != ERR and estado != ACP:
        while(idx < len(entrada) and entrada[idx] in [' ', '\n', '\t', ''] 
              and estado == 0):
            if entrada[idx] == '\n':
                conLin +=1
                conCol = 0
            elif entrada[idx] == ' ': conCol +=1
            elif entrada[idx] == '\t': conCol += 4
            idx += 1
        if idx >= len(entrada):break

        x = entrada[idx]
        idx += 1
        if x != '\t' and x != '\n' and x != '': conCol +=1
        if x == '\t': conCol +=4
        if x == '\n':
            conLin += 0     #aqui era +=1
            conCol += 1     #aqui era = 0

        if estado == 6 and x == '\n': 
            break
        if estado == 6 and x == '\n':
            estAnt = 6
            estado = ERR
            break
        if estado == 1 and x in [' ', '\t', '\n']: 
            estAnt = estado
            estado = ACP
            break





#aqui es para la matriz, col <= (numero de columna)
        col = colCar(x)
        if col>=0 and col <= 13 and estado != ERR: 
            estAnt = estado
            estado = matran[estado][col]
            if estado != ACP and estado != ERR: 
                lex += x
        

        if estado == ACP or estado == ERR:
            if x == '\n' and conCol < 2:
                conLin -= 1
                conCol = 1
            idx -= 1
            conCol -= 1
            break


    #print(estAnt, estado, lex)
    if estado != ACP and estado != ERR: estAnt = estado
    if estAnt == 3:
        erra(conLin, conCol, 'Error Lexico', lex + ' CtE decimal en ERROR')    
    if estAnt == 12:
        erra(conLin, conCol, 'Error Lexico', lex + ' Cte Alfabetica SIN CERRAR')

    #nuevo

    #elif estado == 5 :
        #tok = 'OpA' 
        #if lex in opa : tok = 'OpA' #para / division
    #Aceptores
    elif estAnt == 1: 
        tok = 'Ide'
        if lex in palRes: tok = 'Res'
        elif lex in ctelog: tok = 'CtL'
    elif estAnt == 2:
        tok = 'Ent'
    elif estAnt == 4:
        tok = 'Dec'
    elif estAnt in [9, 11, 19]:
        tok = 'OpL'
    elif estado == 6: #para // comentario
        tok = 'Com'
        lex = '//'
        print(tok)
    elif estAnt == 7:
        tok = 'OpA'
    elif estAnt == 8:
        tok = 'Sym'
    elif estAnt == 10:
        tok = 'Sym'
    elif estAnt == 13:
        tok = 'CtA'
    elif estAnt == 14:
        tok = 'OpS'
    elif estAnt == 15:
        tok = 'OpR'
    elif estAnt == 16:
        tok = 'OpR'
    elif estAnt == 17:
        tok = 'OpR'    
    elif estAnt == 20:
        tok = 'OpR'
    elif estAnt == 18:
        tok = 'Del'   
    elif estAnt == 21:
        tok = 'Sym'
    else: tok = 'NtK'



    return tok, lex #Termina lexico

def tokeniza():
    global idx, entrada
    if idx >= len(entrada):
        return '', ''
    
    token = 'NtK'
    lexema = ''
    while (token in ['Com', 'NtK'] and idx < len(entrada)):
       token, lexema = lexico()
    
    return token, lexema

def termino():
    global tok, lex
    if lex == '(':
        tok, lex = tokeniza()
        expr()
        tok, lex = tokeniza()
        if lex != ')':
            erra(conLin, conCol, 'Error de sintaxis', 'Se esperaba ) y llego' +lex)
    if tok in ['Ent', 'Dec', 'CtA', 'CtL']:
        if tok in ['Ent', 'Dec', 'CtA']:
            insCodigo(['LIT', lex, '0'])
        elif lex == 'Verdadero':
            insCodigo(conLin, ['LIT', 'V', '0'])
        elif lex == 'Falso':
            insCodigo(conLin, ['LIT', 'F', '0'])
        tok, lex = tokeniza()
def expr():
    termino()

def imprimel():
    global tok, lex
    tok, lex = tokeniza()
    if lex != '(':
            erra(conLin, conCol, 'Error de sintaxis', 'Se esperaba ( y llego' +lex)
    tok, lex = tokeniza()
    if lex != ')':
        sep = ','
        while sep == ',':
            expr()
            insCodigo(conLin, 'OPR', '0', '20')
            conLin = conLin + 1
            sep = lex


    if lex != ')': tok, lex = tokeniza()
    if lex != ')':
            erra(conLin, conCol, 'Error de sintaxis', 'Se esperaba ) y llego' +lex)

def comando():
    global tok, lex, entrada, idx
    if lex == 'imprimeln!': imprimel()

def estatutos():
    global tok, lex, entrada, idx
    sep = ';'
    while sep == ';':
        if lex == ';':
            tok, lex = tokeniza()
        if lex == '}': break
        comando()
        if lex == ')': 
            tok, lex = tokeniza()
        sep = '*'
        if lex == ';': sep = lex
        if lex != ';':
            erra(conLin, conCol, 'Error de sintaxis', 'Se esperaba ; y llego' +lex)
  
        

def prgm():
    global bERR, archE, tok, lex
    tok, lex = tokeniza()
    variables()
    funciones()
    if not (bERR):
        print(archE, 'COMPILO con EXITO!!!')

def variables():
    tok, lex = tokeniza()
    while lex == 'sea':
        pass
    
def params():
    global tok, lex, idx, entrada
    sec = ','
    while sec == ',':
        if tok != 'Ide':
            erra(conLin, conCol, 'Error de sintaxis', 'Se esperaba Ide y llego' +lex)
        tok, lex = tokeniza()
        if lex != ':':
            erra(conLin, conCol, 'Error de sintaxis', 'Se esperaba : y llego' +lex)
        tipo()
        tok, lex = tokeniza()
        sec = lex

def tipo():
    global tok, lex
    tok, lex = tokeniza()
    if not(lex in ['entero', 'decimal', 'logico', 'palabra']):
        erra(conLin, conCol, 'Error de sintaxis', 'Se esperaba algo y llego' +lex)

def funciones():
    global lex, tok, idx, entrada, conCol, conLin
    if idx >= len(entrada): return

    while idx < len(entrada) and lex == 'fn':
        tok, lex = tokeniza()
        if tok != 'Ide' or lex != 'principal':
            if lex == 'principal':
                insTabSim('principal', ['F', 'I', '0', '0'])
                insTabSim('_P',['I', 'I', str(conCod),'0','0'])
            erra('Error de sintaxis','se esperaba un Ide o principal y llego' +lex)
        tok, lex = tokeniza();
        if lex != '(':
            erra('Error de sintaxis','se esperaba ( y llego' +lex)

        

if __name__ == '__main__':
    archE = ''
    print(archE[len(archE)-3:])
    while (archE[len(archE)-3:] != 'icc'):
        archE = input('Archivo a compilar (*.icc) [.]=Salir: ')
        if archE == '.': exit(0)
        aEnt = None
        try:
            aEnt = open(archE, 'r+', encoding=('UTF-8'))
            break
        except FileNotFoundError:
            print(archE, 'No exite volver a intentar')
    
    if aEnt != None:
        while (linea := aEnt.readline()):
            entrada += linea
        aEnt.close()

    print('\n\n' + entrada + '\n\n')    
    while idx < len(entrada):
        token, lexema = tokeniza()
        print(token, lexema)
