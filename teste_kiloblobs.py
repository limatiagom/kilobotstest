import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar
globalDistance = 130

im = cv2.imread('frame.png', 1)

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
        # funcao para atualizar x,y
        def atualizarXY(self,x,y):
            self.x = x
            self.y = y

        pass


def minDistance(x1,y1,x2,y2):
    distx = (x1 - x2) ** 2
    disty = (y1 - y2) ** 2
    d = (distx + disty) ** 0.5
    return d
        
def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
 
  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data,'\n')
     
  return decodedObjects            

params = cv2.SimpleBlobDetector_Params()
     
# Change thresholds
# params.minThreshold = 1;
# params.maxThreshold = 5000;
  
# Filter by Area.
params.filterByArea = True
params.minArea = 10
# params.minDistBetweenBlobs = 1000

detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs
keypoints = detector.detect(img)

im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]),(0,0,255), 4)

font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX

#print(keypoints[0].pt[0])



ListaBlob = []
## estamos trabalhando os fors
for i in range(len(keypoints)): #vai de 0 até (quantidade de keypoints)-1
        if (i == 0):
                blobs = KiloBlobs(i,keypoints[i].pt[0],keypoints[i].pt[1],keypoints[i].size)
                cv2.putText(im_with_keypoints,str(blobs.ID),(int(blobs.x),int(blobs.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
                ListaBlob.append(blobs)
                
                # ListaBlob[i].printarInfos()
        else:
                for m in (range(i)): #isso quer dizer que vai de 0 até (quantidade de i)-1
                        dist = minDistance(keypoints[i].pt[0],keypoints[m].pt[0],keypoints[i].pt[1],keypoints[m].pt[1])
                        
                        if (dist < globalDistance):
                              
                                copia = KiloBlobs(i,keypoints[m].pt[0],keypoints[m].pt[1],keypoints[m].size)
                                #cv2.putText(im_with_keypoints,str(copia.ID),(int(copia.x),int(copia.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
                                ListaBlob.append(copia)
                                # print('Blob criado com mesmo ID de outro')
                                # ListaBlob[m].printarInfos()
                                
                                #print('Atualizou blob')
                                #ListaBlob[m].atualizarXY(keypoints[i].pt[0],keypoints[i].pt[1])
                                #ListaBlob[m].printarInfos()
                                # desenha no blob com cor preta a ordem que foi achado, e que foi adicionado
                                #cv2.putText(im_with_keypoints,str(blobs.ID),(int(blobs.x),int(blobs.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
                        else:
                                
                                # print('Criou novo blob')
                                blobs = KiloBlobs(i,keypoints[i].pt[0],keypoints[i].pt[1],keypoints[i].size)
                                cv2.putText(im_with_keypoints,str(blobs.ID),(int(blobs.x),int(blobs.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)

decode(im)
cv2.imshow("Blob",im_with_keypoints)

cv2.waitKey(0)
cv2.destroyAllWindows()
