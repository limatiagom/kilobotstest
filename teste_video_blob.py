import cv2
import numpy as np



cap = cv2.VideoCapture("/Users/marinastavares/Google Drive/PETEEL/6. Pesquisas e Projetos/2018.2/1. Projetos Externos/TML + MST - Kilobotics/Materiais/Kilobots/videoplayback.mp4")
    # cv2.VideoCapture recebe como argumento o diretório do vídeo.
    # Se estiver, usando webcam, o argumento é um número (0 = câmera primária,
    # 1 = secundária etc

cap.set(1, 480)
    # Escolhe um frame específico do video. O primeiro argumento (1) se refere
    # ao código para escolher um FRAME com base em um número.
    # Por chute e teste, descobri que uma parte interessante para testar é a que
    # começa no frame 480 e acaba no 600.

i = 480
    # contador para ir do 480 ao 600. Usei uma lógica bem simples só de teste.

font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX




while True:
    # Loop infinito para ver frame por frame e só sair por um Break em um IF
    
    ret, frame = cap.read()
        # cap.read() retorna duas váriaveis. Uma booleana (ret) que indica se
        # foi encontrado um frame (para não dar erro), e a segunda p/ armazenar
        # o frame
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # converte frame para cinza e armazena em gray para trabalhar mais fácil
    m=1
####### SETANDO PARAMETROS E ENCONTRANDO BLOBS
    params = cv2.SimpleBlobDetector_Params()
         
    # Change thresholds
    params.minThreshold = 1;
    params.maxThreshold = 500;
      
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 500
       
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
    detector = cv2.SimpleBlobDetector_create(params)
  
    # Detect blobs
    keypoints = detector.detect(gray)
        # usei o "gray" pra definir os keypoints (mais rápido)
        
    #print (keypoints)
        # (comentei porque tava enchendo o saco no loop)

         
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]),
                (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)    

    for k in keypoints:
            # arr.append(Rect(int(k.pt[0] - k.size), int(k.pt[1] - k.size), int(k.size * 2), int(k.size * 2)))
        print("x = %.1f y= %.1f tamanho=%d" % (k.pt[0],k.pt[1],k.size))
        x=int(k.pt[0])
        y=int(k.pt[1])
        po=str(m)
        cv2.putText(im_with_keypoints,po,(x,y), font, 1, (200,0,0), 2, cv2.LINE_AA)
    # labeled_array, num_features = label(im)
    # print(num_array)
        m=m+1
    
        # desenhei em cima do vídeo colorido (frame)

############## FIM DOS PARÂMETROS
    
    roi = im_with_keypoints[0:180, 320:640]
        # cria uma Region Of Interest somente com a região interessante do
        # vídeo (Assistir video na pasta pra entender porque precisei fazer
        # isso.
    
    i = i + 1
    if i == 600:
        i = 480
            # Volta o contador pra 480 quando ele chegar em 600 (ultimo frame de
            # interesse pra gente). Meudeus, que lixo de lógica essa minha.  
        cap.set(1, 480)
            # Seta o frame pra 480 de novo, assim como no começo. Ou seja,
            # isso vai fazer o vídeo dar LOOP
        
    cv2.imshow('video', roi)
        # imprime frame por frame, já colorido e com o Blob (lembrando que
        # tá no while)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
            # Condição pra dar break no While. O vídeo vai dar loop até você
            # pressionar q.

cap.release()
    # Agora que saiu do loop, antes de destruir as imagens, é importante usar
    # esse comando! É como se liberasse a câmera/placa de vídeo pra poder usar
    # em outras coisas. Não fazer isso pode causar o risco de ficar dando que
    # sua câmera tá sendo usada, mesmo com o python fechado.
    
cv2.destroyAllWindows()

