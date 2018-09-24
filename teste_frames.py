import numpy as np
import cv2
globalDistance = 130
numberFrame = -1

cap = cv2.VideoCapture("/Users/marinastavares/video5.mp4")
# cap.set(1, 100)

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

# Lista onde os kilobots estarão armazenadas
ListaBlob = []
Encontrados = []

class blobsEncontrados:
    def __init__(self,x,y,tamanho,match):
        self.x = x
        self.y =  y
        self.tamanho = tamanho
        self.match = match

    def atualizarMatch(self,match):
        self.match = match
pass


def minDistance(x1,y1,x2,y2):
    distx = (x1 - x2) ** 2
    disty = (y1 - y2) ** 2
    d = (distx + disty) ** 0.5
    return d

i = 0
ListaMatch = []

while True:
    
    ret, frame = cap.read()
    numberFrame = numberFrame + 1
    frame = cv2.resize(frame, (200,200))
    detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(frame)
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]),(0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  

    for detectados in keypoints:
        encontrado = blobsEncontrados(detectados.pt[0],detectados.pt[1],detectados.size,False)
        Encontrados.append(encontrado)

    ## cria lógica para Frame 0
    if (numberFrame == 0):
        for k in Encontrados: 
            blob=KiloBlobs(i,k.x,k.y,k.tamanho)
            ListaBlob.append(blob)
            print('Primeiros Blobs criados')
            ListaBlob[i].printarInfos()
            cv2.putText(im_with_keypoints,str(blob.ID),(int(blob.x),int(blob.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
            i = i + 1

    else: 
        # for para comparar distancias encontradas com as que já foram definidas
        # compara keypoints de um frame com os keypoints do frame anterior (tentar todas combinacoes) 
        # n = listablob0 , n = listablob1
        a=0
        # print('Novo frame')
        for l in Encontrados:
            # contador l
            for n in ListaBlob:
                # Calcular a distancia
                dist = minDistance(l.x,l.y,n.x,n.y)
                
                if (dist < n.tamanho):
                    print('Atualizar o ID %d' % (n.ID))
                    n.atualizarXY(l.x,l.y,l.tamanho)
                    n.printarInfos()
                    cv2.putText(im_with_keypoints,str(n.ID),(int(n.x),int(n.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
                    l.atualizarMatch(True)

    if (len(Encontrados) > len(ListaBlob)):
        for perdido in Encontrados:
            if (perdido.match == False):
                blob = KiloBlobs(i,perdido.x,perdido.y,perdido.tamanho)
                ListaBlob.append(blob)
                cv2.putText(im_with_keypoints,str(blob.ID),(int(blob.x),int(blob.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
                i+=1
    
    Encontrados = []
                
    cv2.imshow("Video", im_with_keypoints)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
print(len(keypoints))
cap.release()
cv2.destroyAllWindows()