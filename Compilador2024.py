import sys
sys.stdout.reconfigure(encoding='utf-8')#caracteres especiales


ERR = -1
ACP = 999
entrada = '' 
idx = 0
bERR = False
ctelog = ['verdadero', 'falso']
palRes = ['fn', 'principal', 'imprimeln!', 'imprimeln', 'entero', 'const',
          'decimal', 'logico', 'alfabetico', 'sea', 'si', 'sino', 
          'para', 'en', 'mientras', 'ciclo', 'regresa', 'leer', 'interrumpe', 
          'continua']


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


matran = [  #letra  #_   #*    #dig  #opa  #&   #!   #=   #""  #/   #<>  #|  #dlm #sym    
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
            [ERR,   ERR, ERR,  ERR,  ERR,  ERR, ERR, ERR, ERR, ERR, ERR, 9  , ERR, ERR], #10
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
sym = ['#','$','¿','?','¡','°','¬']
def erra(tipo, desc):
    print(tipo, desc)
    bERR = True
    

def lexico():
    global entrada, ERR, ACP, matran, idx
    estado = 0
    estAnt = 0
    lex = ''
    tok = ''
    while idx < len(entrada) and estado != ERR and estado != ACP:
        while(entrada[idx] in [' ', '\n', '\t', ''] 
              and estado == 0): idx += 1

        x = entrada[idx]
        idx += 1

        if estado == 6 and x == '\n': break
        if estado == 8 and x == '\n':
            estAnt = 8
            estado = ERR
            break
        if estado == 1 and x in [' ', '\t', '\n']: 
            estAnt = estado
            estado = ACP
            break

#cta error
        if estado == 12 and x == '\n': break
        if estado == 12 and x == '\n':
            estAnt = 12
            estado = ERR
            break




#aqui es para la matriz, col <= (numero de columna)
        col = colCar(x)
        if col>=0 and col <= 13 and estado != ERR: 
            estAnt = estado
            estado = matran[estado][col]
            if estado != ACP and estado != ERR: 
                lex += x

        if estado == ACP or estado == ERR:
            if estado == ACP: idx -= 1
            break

    #print(estAnt, estado)
    if estado != ACP and estado != ERR: estAnt = estado

    #Errores
    if estAnt == 3:
        tok = 'Dec'
        erra('Error Lexico', lex + ' CtE decimal incompleta')    
    if estAnt == 8:
        tok = 'OpL'
        erra('Error Lexico', lex + ' OpL incompleto')
    if estAnt == 10:
        tok = 'OpL'
        erra('Error Lexico', lex + ' OpL incompleto')
    if estado == 12:
        erra('Error Lexico', lex + ' CtA incompleta')

    #Aceptores
    elif estAnt == 1: 
        tok = 'Ide'
        if lex in palRes: tok = 'Res'
        elif lex in ctelog: tok = 'CtL'
    elif estAnt == 2:
        tok = 'Ent'
    elif estAnt == 4:
        tok = 'Dec'
    elif estAnt in [9, 19]:
        tok = 'OpL'
    elif estado == 6: 
        tok = 'Com'
        lex = '//'
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
    token = 'NtK'
    while (token in ['Com', 'NtK']):
       token, lexema = lexico()
    
    return token, lexema



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
