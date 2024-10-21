import cv2

# URL RTSP de la cámara (reemplaza con tus credenciales)
rtsp_url = "rtsp://admin:contra@ip/cam/realmonitor?channel=4&subtype=1"

# Inicializar la captura de video desde el DVR
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error al abrir la transmisión RTSP")
    exit()

# Leer el primer frame como referencia
ret, frame_ref = cap.read()
if not ret:
    print("Error al capturar el frame de referencia")
    exit()

# Convertir el frame de referencia a escala de grises
frame_ref_gray = cv2.cvtColor(frame_ref, cv2.COLOR_BGR2GRAY)
# Aplicar desenfoque para reducir el ruido
frame_ref_gray = cv2.GaussianBlur(frame_ref_gray, (21, 21), 0)

while cap.isOpened():
    # Capturar un nuevo frame
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame actual")
        break

    # Convertir el frame actual a escala de grises
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Aplicar desenfoque para reducir el ruido
    frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)

    # Calcular la diferencia absoluta entre el frame de referencia y el frame actual
    frame_delta = cv2.absdiff(frame_ref_gray, frame_gray)

    # Aplicar un umbral para identificar áreas con cambios significativos
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    # Dilatar la imagen umbralizada para cubrir agujeros y mejorar la detección
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Encontrar contornos en la imagen umbralizada
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar contornos alrededor de las áreas donde se detecta movimiento
    for contour in contours:
        print(cv2.contourArea(contour))

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Movimiento detectado", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Mostrar el frame con las detecciones de movimiento
    cv2.imshow("Transmisión DVR - Detección de Movimiento", frame)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
