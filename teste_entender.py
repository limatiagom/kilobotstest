import numpy as np
import cv2

imagem = cv2.imread('/Users/marinastavares/Google Drive/PETEEL/6. Pesquisas e Projetos/2018.2/1. Projetos Externos/TML + MST - Kilobotics/Materiais/Kilobots/kilobots_marina/blob.png', 1)

img = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

params = cv2.SimpleBlobDetector_Params()

font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX

     
# Change thresholds
params.minThreshold = 10;
params.maxThreshold = 500;
  
# Filter by Area.
params.filterByArea = True
params.minArea = 100
   
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.001
    
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.01
    
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)

#detector2 = cv2.SimpleBlobDetector_create()
     
# Detect blobs
keypoints = detector.detect(img)
# print (keypoints)

#keypoints2 = detector2.detect(img)

arr = []

     
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(imagem, keypoints, np.array([]),
            (0,0,255), 4)
# x=int(k.pt[0])
# y=int(k.pt[1])
# po=str(i)
# cv2.putText(im_with_keypoints,po,(x,y), font, 1, (200,0,0), 2, cv2.LINE_AA)

        # O último parâmetro (4) de drawKeypoints refere-se a:  
# 0 = cv2.DRAW_MATCHES_FLAGS_DEFAULT = círculo só em volta do centro do Blob
# 4 = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS =círculo tenta cobrir todo Blob
# 1 = cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG = não funciona com np.array
# 2 = cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS = igual ao 0, mas ignora
#                                               keypoints que não estão em blobs

 
cv2.imshow('image', im_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()



#is it possible to count those blobs ? can you help me please
#Yes it is. The Blobs are stored in keypoints and you can get the size of it
# with keypoints.size() which is equal to the Blob amount :)

## Ou seja, os keypoints são coordenadas x,y do centro do Blob já!
