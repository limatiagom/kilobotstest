import cv2
import numpy as np



cap = cv2.VideoCapture("/Users/marinastavares/Google Drive/PETEEL/6. Pesquisas e Projetos/2018.2/1. Projetos Externos/TML + MST - Kilobotics/Materiais/Kilobots/kilobots_marina/video1.MOV")

font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX

class KiloBlobs:
       # construtor 
    def __init__(self,ID,x,y,tamanho):
        self.ID = ID
        self.x = x
        self.y =  y
        self.tamanho = tamanho
     
        # aqui é um método para printar as informações que serão colocadas no objeto
    def printarInfos(self):
        print("BLOB ID=%d x = %.1f y= %.1f tamanho=%d" % (self.ID,self.x,self.y,self.tamanho))
    pass

i = 0

while True:
    # Loop infinito para ver frame por frame e só sair por um Break em um IF
    # quando esse i chegar ao último frame, fará loop
    i += 1

    ret, frame = cap.read()
    if ret: # else it means the movie is over !
        res = cv2.resize(frame, (320,300))
    
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    
    m = 1

####### SETANDO PARAMETROS E ENCONTRANDO BLOBS
    params = cv2.SimpleBlobDetector_Params()
         
    # Change thresholds
    params.minThreshold = 1
    params.maxThreshold = 500
      
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 500
    params.maxArea = 100000

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.800

    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.80

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.81

    # Set up the detector with set parameters.
    detector = cv2.SimpleBlobDetector_create()
  
    # Detect blobs
    keypoints = detector.detect(gray)
        # usei o "gray" pra definir os keypoints (mais rápido)
        
    #print (keypoints)
        # (comentei porque tava enchendo o saco no loop)

         
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(res, keypoints, np.array([]),
                (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)    

    for k in keypoints:
        # arr.append(Rect(int(k.pt[0] - k.size), int(k.pt[1] - k.size), int(k.size * 2), int(k.size * 2)))
        blobs=KiloBlobs(i,k.pt[0],k.pt[1],k.size)
        print("x = %.1f y= %.1f tamanho=%d" % (k.pt[0],k.pt[1],k.size))
        x=int(k.pt[0])
        y=int(k.pt[1])
        po=str(m)
        cv2.putText(im_with_keypoints,"%.1f, %.1f size=%d" % (k.pt[0],k.pt[1],k.size),(int(blobs.x),int(blobs.y)), font, 0.5, (0,0,0), 1, cv2.LINE_AA)
        m=m+1
    
        # desenhei em cima do vídeo colorido (frame)

############## FIM DOS PARÂMETROS
    
    # roi = im_with_keypoints[0:180, 320:640]
        # cria uma Region Of Interest somente com a região interessante do
        # vídeo (Assistir video na pasta pra entender porque precisei fazer
        # isso.
    
    # i = i + 1
    # if i == res.get(cv2.CV_CAP_PROP_FRAME_COUNT)
    #     i = 0
    #     res.set(1,0)    

    cv2.imshow('video', im_with_keypoints)
        # imprime frame por frame, já colorido e com o Blob (lembrando que
        # tá no while)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
            # Condição pra dar break no While. O vídeo vai dar loop até você
            # pressionar q.

cap.release()
cv2.destroyAllWindows()