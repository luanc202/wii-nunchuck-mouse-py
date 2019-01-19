# ESTE PROGRAMA � PARA USAR COM O SENSOR DE ANAL�GICO!!!
# Importando as bibliotecas para usar
import math, string, time, serial, win32api, win32con

# a porta a ser usada pelo arduino
port = 'COM5'

# caso queira inverter o eixo y
invertY = False

# velocidade do ponteiro
cursorSpeed = 20

# o baudrate usado no programa do arduino
baudrate = 19200

# vari�veis para indicar se o bot�o do mouse est� funcionando ou n�o
leftDown = False
rightDown = False

# valores indicando a posi��o de centro(sem movimento) dos eixos
midAccelX = 530 # Aceler�metro X
midAccelY = 510 # Aceler�metro Y
midAnalogY = 134 # Anal�gico Y
midAnalogX = 137 # Anal�gico X

if port == 'arduino_port':
    print 'Por favor defina uma porta do Arduino.'
    while 1:
        time.sleep(1)

# conectando a porta serial
ser = serial.Serial(port, baudrate, timeout = 1)

# esperando 1 segundo para estabilizar
time.sleep(3)

# enquanto a porta serial est� aberta
while ser.isOpen():

    # ler uma linha
    line = ser.readline()

    # tira o final (\r\n)
    line = string.strip(line, '\r\n')

    # separar a string em uma ordem contendo os dados do nunchuck do wii
    line = string.split(line, ' ')
    print(line)

    # atribuir vari�veis a cada um dos valores
    analogX = int(line[0])
    analogY = int(line[1])

    zButton = int(line[5])
    cButton = int(line[6])

    # bot�o esquerdo do mouse
    # se apertar o bot�o Z do controle, mas n�o foi anteriormente
    if(zButton and not leftDown):
        # simule um mouse apertando o bot�o esquerdo
        leftDown = True
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    # ou se foi pressionado, mas n�o est� mais
    elif(leftDown and not zButton):
        # simule soltar o bot�o esquerdo do mouse
        leftDown = False
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)


    # bot�o direito do mouse
    # o mesmo feito com o bot�o esquerdo do mouse mas com o bot�o C do controle
    if(cButton and not rightDown):
        rightDown = True
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0,0)
    elif(rightDown and not cButton):
        rightDown = False
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0,0,0)
        

    # Roda do mouse
    # nesta parte o valor era > 5 mas o joystick continuava a mover sozinho
    # ent�o diminu� a sensibilidade dele aumentando para 10 o valor
    # >se o joystick anal�gico n�o estiver centrado
    #if(abs(analogY - midAnalogY) > 10):
        # simular movimento da roda do mouse
    #    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,int(math.floor((analogY - midAnalogY)/2)),0)
    #else:
        # simular parada da roda do mouse
    #    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,0,0)


    # movimento do mouse
    # criando vari�veis para indicar o quando o ponteiro do mouse se mexe em
    # cada dire��o
    dx = 0
    dy = 0

    # se o controle � rodado em torno do eixo X
    if(abs(analogX - midAnalogX) > 10):
        # calculando o quanto o ponteiro se move horizontalmente
        dx = int(math.floor((analogX - midAnalogX)*cursorSpeed/400))

    # se o controle � rodado em torno do eixo Y
    if(abs(analogY - midAnalogY) > 10) :
        # calculando o quanto o ponteiro se move verticalmente
        dy = int(math.floor((analogY - midAnalogY)*cursorSpeed/400))
        # para inverter o eixo Y
        if invertY:
            dy = dy*-1

    # simular o movimento do mouse com os valores calculados acima
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,dx,dy,0,0)
    

# Ao terminar de usar o programa fechar a porta serial, MUITO IMPORTANTE!!
ser.close()
