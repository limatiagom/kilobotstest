import numpy as np
import cv2
globalDistance = 130
numberFrame = -1

cap = cv2.VideoCapture('video2.MOV')
cap.set(1, 480)

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

def minDistance(x1,y1,x2,y2):
    distx = (x1 - x2) ** 2
    disty = (y1 - y2) ** 2
    d = (distx + disty) ** 0.5
    return d

i = 0

while True:
    
    ret, frame = cap.read()
    numberFrame = numberFrame + 1
    frame = cv2.resize(frame, (300,300))
    detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(frame)
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]),(0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  

    ## cria lógica para Frame 0
    if (numberFrame == 0):
        for k in keypoints: 
            blob=KiloBlobs(i,k.pt[0],k.pt[1],k.size)
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
        print('Novo frame')
        for n in ListaBlob:
            # contador l
            for l in keypoints:
                # print(n.ID)
                dist = minDistance(l.pt[0],l.pt[1],n.x,n.y)
                print('X,Y DO KEYPOINF %.1f %.1f E DO BLOB %.1f %.1f' % (l.pt[0],l.pt[1],n.x,n.y))
                print('A comparacao entre o blob FIXO %d e %d deu uma distancia %.1f, o tamanho do %.1f' % (n.ID,a,dist,n.tamanho))
                if (dist < n.tamanho):
                    print('Atualizar o ID %d' % (n.ID))
                    n.atualizarXY(l.pt[0],l.pt[1],l.size)
                    n.printarInfos()
                    cv2.putText(im_with_keypoints,str(n.ID),(int(n.x),int(n.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
                a=a+1


    cv2.imshow("Video", im_with_keypoints)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
print(len(keypoints))
cap.release()
cv2.destroyAllWindows()