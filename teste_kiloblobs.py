import numpy as np
import cv2
globalDistance = 80000

im = cv2.imread("/Users/marinastavares/Google Drive/PETEEL/6. Pesquisas e Projetos/2018.2/1. Projetos Externos/TML + MST - Kilobotics/Materiais/Kilobots/kilobots_marina/kilo3.JPG", 11)
img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


## aqui foi criado uma classe com atributos que serão colocados pelo keypoits 

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
        pass


def minDistance(x1,y1,x2,y2):
    distx = (x1 - x2) ** 2
    disty = (y1 - y2) ** 2
    d = (distx + disty) ** 1/2
    return d
        
            

params = cv2.SimpleBlobDetector_Params()
     
# Change thresholds
# params.minThreshold = 1;
# params.maxThreshold = 5000;
  
# Filter by Area.
params.filterByArea = True
params.minArea = 10
# params.minDistBetweenBlobs = 1000

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)

#detector2 = cv2.SimpleBlobDetector_create()

# Detect blobs
keypoints = detector.detect(img)

im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]),(0,0,255), 4)

font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
i = 0
n = 0
ListaBlob = []
print(keypoints[0].pt[0])
# cv2.imshow('image', im_with_keypoints)
for k in keypoints:
    
    if (i >= 1):
        while m < len(keypoints): 
            print('m=%d and i=%d' % (m,i))
            distCalculated = minDistance(keypoints[i].pt[0],keypoints[m].pt[0],keypoints[i].pt[1],keypoints[m].pt[1])
            print(distCalculated)
            if (distCalculated > globalDistance):
                # Criar um novo blob
                print('Entrou na condicao')
                blobs=KiloBlobs(i,keypoints[i].pt[0],keypoints[i].pt[1],k.size)
                cv2.putText(im_with_keypoints,str(blobs.ID),(int(blobs.x),int(blobs.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
                ListaBlob.append(blobs)
                print('Blob criado')
                ListaBlob[i].printarInfos()
                i = i + 1
                m = m + 1
            else: 
                print('Entrou no else')
                ListaBlob[m].x=keypoints[i].pt[0]
                ListaBlob[m].y=keypoints[i].pt[1]
                cv2.putText(im_with_keypoints,str(ListaBlob[m].ID),(int(ListaBlob[m].x),int(ListaBlob[m].y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
                ListaBlob[m].printarInfos()
                m = m + 1
                break

    else:
        blobs=KiloBlobs(i,k.pt[0],k.pt[1],k.size)
        cv2.putText(im_with_keypoints,str(blobs.ID),(int(blobs.x),int(blobs.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
        ListaBlob.append(blobs)
        ListaBlob[i].printarInfos()
        i = i + 1
        m = 0
    
#x, y, _ = ListaBlob
#print(x,y)



cv2.imshow("Blob",im_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()



# is it possible to count those blobs ? can you help me please
# Yes it is. The Blobs are stored in keypoints and you can get the size of it
#  with keypoints.size() which is equal to the Blob amount :)

# Ou seja, os keypoints são coordenadas x,y do centro do Blob já!
