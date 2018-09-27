import numpy as np
import cv2

# numero de Frames Inicial, vai ser o contador de numero de frames
numberFrame = -1

# Função para pegar video
cap = cv2.VideoCapture("video5.mp4")

# Fonte utilizada no vídeo
font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX

# Classe para armazenar os parâmetros de cada Kilobot, a método uptadeXY atualiza as coordenadas
class KiloBlobs:

        # construtor 
        def __init__(self,ID,x,y,size):
            self.ID = ID
            self.x = x
            self.y =  y
            self.size=size          
        # aqui é um método para printar as informações que serão colocadas no objeto
        def printInfos(self):
            print("BLOB ID=%d x = %.1f y= %.1f size=%d" % (self.ID,self.x,self.y,self.size))
        # funcao para uptade x,y
        def uptadeXY(self,x,y,size):
            self.x = x
            self.y = y
            self.size = size

        pass

# List onde os kilobots estarão armazenadas
blobList = []

# Classe para receber os parâmetros úteis do keypoints, como coor x,y,size e Match
class detectedBlobs:
    def __init__(self,x,y,size,match):
        self.x = x
        self.y =  y
        self.size = size
        # Esse match é um parâmetro responsável por determinar se um blob detectado já foi instanciado como um Kiloblob
        self.match = match
    # Caso for possível ligar um blob a um Kiloblob, é criado um Match
    def uptadeMatch(self,match):
        self.match = match

# List para receber os valores de detectedBlobs, que irão receber os parâmetros do Kilobot
detectedList = []

# Fórmula de mínima distância entre os pontos do plano
def minDistance(x1,y1,x2,y2):
    distx = (x1 - x2) ** 2
    disty = (y1 - y2) ** 2
    d = (distx + disty) ** 0.5
    return d

# Contador para cada Blob instanciado, será responsável por determinar o parâmetro ID
numberID = 0

## Parametros para a detecção de blobs
params = cv2.SimpleBlobDetector_Params()    
# Change thresholds
# params.minThreshold = 1;
# params.maxThreshold = 5000;
    
# Filter by Area.
params.filterByArea = True
params.minArea = 100

params.filterByInertia = True
params.minInertiaRatio = 0.0000001
    
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = .00001

# Enquanto o vídeo tem frame
while True:
    
    # Parametros para captar vídeo pelo OpenCV
    ret, frame = cap.read()
    numberFrame = numberFrame + 1
    frame = cv2.resize(frame, (200,200))

    # criar um detector de acordo com os parametros estabelecidos
    detector = cv2.SimpleBlobDetector_create(params)

    # Detecta blobs e coloca as informações em keypoints, como coord e tamanho. O keypoint é criado a cada frame
    keypoints = detector.detect(frame)

    # Função que cria uma imagem com os Keypoints indicados
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]),(0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  

    # for para passar as instâncias de keypoints para detected
    for detected in keypoints:
        
        # Cria um objeto de detectedBlob com os parâmetros de keypoints
        # O objetivo foi criar um parametro chamado match, para saber caso o blob já tenha sido criado como 
        # objeto de KiloBlob anteriormente
        found = detectedBlobs(detected.pt[0],detected.pt[1],detected.size,False)

        # Armazena o objeto de detectedBlobs em uma lista
        detectedList.append(found)

    # Lógica criada para o Frame 0
    if (numberFrame == 0):
        
        # for para passar a instancia de cada posição do array detectedList para k
        for k in detectedList: 
            # Cria um objeto de Kiloblobs para cada detected do detectedList
            kiloblob = KiloBlobs(numberID,k.x,k.y,k.size)
            
            # Adiciona em uma lista com os outros kiloblobs
            blobList.append(kiloblob)

            # Como no frame 0 não tem como comparar um possivel match, é colocado como verdadeiro
            k.uptadeMatch(True)

            # Funcao para escrever o numero do ID na imagem
            cv2.putText(im_with_keypoints,str(kiloblob.ID),(int(kiloblob.x),int(kiloblob.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)

            # Aumenta o contador responsavel pela numeração do ID
            numberID += 1

    # Frames depois de 0
    else: 
        
        # for para passar a instancia de cada posição do array detectedList para l
        for l in detectedList:
            
            # for para passar cada kiloblob para n
            for n in blobList:
                
                # Calcular a distancia entre um kiloblob e um detected
                dist = minDistance(l.x,l.y,n.x,n.y)
                
                # Condicao para checar se a distancia entre o centro do blob detectado e do já criado é menor que o tamanho do Kiloblob
                if (dist < n.size):
                    
                    # Caso a condição seja verdadeira, a coordenada é atualizada, sendo assim foi utilizada o método da classe
                    n.uptadeXY(l.x,l.y,l.size)

                    # Funcao para escrever na imagem os números referente aos IDs dos blobs
                    cv2.putText(im_with_keypoints,str(n.ID),(int(n.x),int(n.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)

                    # Como um objeto detected foi ligado a um blob de Kiloblob, ocorreu a "ligação" entre as coord
                    # Essa ligação foi denominada Match, sendo um parâmetro booleano
                    l.uptadeMatch(True)

    # Esse for tem como objetivo buscas os objetos de detected que não foram ligados a um Kiloblob
    # Sendo assim, perdido recebe cada as instancias de detectedList para perdidos
    for perdido in detectedList:
        
        #Condicao para checar se não houve ligação entre os blobs de frames diferentes
        if (perdido.match == False):
            
            # Criacao de um novo objeto em Kiloblob, adicionando ele a lista
            blob = KiloBlobs(numberID,perdido.x,perdido.y,perdido.size)
            blobList.append(blob)
            
            cv2.putText(im_with_keypoints,str(blob.ID),(int(blob.x),int(blob.y)), font, 1, (200,0,0), 2, cv2.LINE_AA)
            
            numberID += 1
    
    # Zera a detectedList a cada frame localizado
    detectedList = []                

    # Funcao para mostrar cada frame mostrando a im_with_keypoints
    cv2.imshow("Video", im_with_keypoints)

    # Condicao para fechar a janela do video
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()