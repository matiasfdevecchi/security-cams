import cv2
import torch

# URL RTSP encontrada (reemplaza 'admin' y 'contra' con tus credenciales)
rtsp_url = "rtsp://admin:contra@192.168.1.35:554/cam/realmonitor?channel=4&subtype=1"

# Cargar el modelo YOLOv5 pre-entrenado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Inicializar la captura de video desde el DVR
cap = cv2.VideoCapture(rtsp_url)

new_width = 800
new_height = 600

CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", 
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", 
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", 
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", 
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", 
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", 
    "couch", "potted plant", "bed", "dining table", "toilet", "TV", "laptop", "mouse", "remote", 
    "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", 
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

if not cap.isOpened():
    print("Error al abrir la transmisión RTSP")
    exit()

print("Transmisión RTSP abierta con éxito")

# Configuración para procesar solo 1 de cada N frames
N = 10  # Número de frames a saltar (ajústalo según tus necesidades)
frameCount = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame")
        break

    # Incrementar el contador de frames
    frameCount += 1

    # Procesar solo 1 de cada N frames
    if frameCount % N != 0:
        continue

    # Redimensionar el frame al nuevo tamaño deseado
    frame_resized = cv2.resize(frame, (new_width, new_height))

    # Realizar la detección de personas usando YOLOv5
    results = model(frame_resized)

    # Filtrar detecciones por la clase 'person' (clase 0 en COCO)
    detections = results.pred[0].cpu().numpy()
    for *xyxy, conf, cls in detections:
        if int(cls) == 0:  # Clase 0 es 'person' en el modelo YOLOv5 COCO
            x1, y1, x2, y2 = map(int, xyxy)
            label = CLASSES[int(cls)]
            print(f'{label} {conf:.2f} - {x1} {y1} {x2} {y2}')
            cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame_resized, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Mostrar el frame con detecciones
    cv2.imshow("Transmisión DVR con Detección", frame_resized)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
