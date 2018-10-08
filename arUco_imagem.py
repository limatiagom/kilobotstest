import cv2
import numpy as np
import cv2.aruco as aruco
import re

font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX


class KiloBlobs:

        # construtor 
        def __init__(self,ID,x,y,tamanho):
            self.ID = ID
            self.x = x
            self.y =  y
            self.tamanho=tamanho          
        # aqui é um método para printar as informações que serão colocadas no objeto
        def printarInfos(self):
            print("BLOB ID=%d x = %.1f y= %.1f tamanho=%d" % (self.ID,self.x,self.y,self.tamanho))
        # funcao para atualizar x,y
        def atualizarXY(self,x,y,tamanho):
            self.x = x
            self.y = y
            self.tamanho = tamanho

        pass



dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

img = cv2.imread('aruco1.png')
img = cv2.resize(img, (500,500))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blank = np.zeros((720,720,3), np.uint8)


res = aruco.detectMarkers(gray, dictionary) #res[0] refere-se aos corners e res[1] aos IDs

Corners = str(0 if res[0] is None else res[0])
Corners = [int(s) for s in re.findall(r'\d+', Corners)]

IDs = str(0 if res[1] is None else res[1])
IDs = [int(s) for s in re.findall(r'\d+', IDs)]

# TML: MARINA, Eu posso te explicar a lógica depois. Por enquanto, saiba o seguinte:
# Em cada interação do "for" eu tô calculando o x e o y do centro de cada quadrado e jogando
# na lista KiloBlobs junto com seu ID.
# Se você quiser usar alguma informação, pega dos Kiloblobs do lado de fora do "for"!

ListaBlob = []
if len(res[0]) > 0: #Se tiver achado algum Corner
    i = int(len(Corners)/9)

    for c in range(i):
        x1 = Corners[0+9*c] + Corners[2+9*c]
        x2 = Corners[4+9*c] + Corners[6+9*c]
        x = int(((x1 + x2)/4))

        y1 = Corners[1+9*c] + Corners[3+9*c]
        y2 = Corners[5+9*c] + Corners[7+9*c]
        y = int(((y1 + y2)/4))

        kiloblob = KiloBlobs(IDs[c], x, y, 23)
        ListaBlob.append(kiloblob)
        kiloblob.printarInfos()

        # cv2.putText(img,'.',(int(kiloblob.x),int(kiloblob.y)), font, 1, (0,0,200), 2, cv2.LINE_AA)


# if len(res[0]) > 0:
#     aruco.drawDetectedMarkers(img,res[0],res[1])
cv2.line(blank, (ListaBlob[0].x,ListaBlob[0].y), (ListaBlob[1].x,ListaBlob[1].y), (0,0,250), 1)
cv2.imshow('arUco', img)

# print('----')
# print(IDs)
print(res[0])
# print(Corners)

cv2.waitKey(0)
cv2.destroyAllWindows()


# PODE IGNORAR ISSO TAMBEM. É PRA MIM DEPOIS
''' Para achar índice do valor xm e ym:
list_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
element = 3
list_numbers.index(element) '''
