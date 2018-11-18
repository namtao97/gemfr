import os

import cv2
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import loader

from ai_models.recognition import recognized_img
from ai_models.tensorflow_human_detection import human_detect


def webcam(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

# face_recognition đang bị lỗi argmin of empty sequence, lấy min của mảng rỗng
def stream(process_func):
    cap = cv2.VideoCapture('bach.mp4')

    indice = 0
    count_frame = 0
    while True:
        ret, frame = cap.read()

        if count_frame >= 2000:
            if not ret:
                print("Error: failed to capture image")
                break

            if (indice % 40 == 0):
                frame = process_func(frame)
            ret, frame = cv2.imencode('.jpg', frame)

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

            indice += 1
        
        count_frame += 1


def human_detection(request):
    return StreamingHttpResponse(stream(human_detect), content_type='multipart/x-mixed-replace; boundary=frame')

def face_recognition(request):
    return StreamingHttpResponse(stream(recognized_img), content_type='multipart/x-mixed-replace; boundary=frame')

# person_cascade = cv2.CascadeClassifier(os.path.join('/path/to/haarcascade_fullbody.xml'))

# def cascade_human_detection():
#     cap = cv2.VideoCapture(0)

#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             print("Error: failed to capture image")
#             break

#         frame = cv2.resize(frame, (640, 360))
#         gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#         # print(type(gray_frame))
#         rects = person_cascade.detectMultiScale(gray_frame)
#         # print(len(rects))
#         for (x, y, w, h) in rects:
#             cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)

#         ret, frame = cv2.imencode('.jpg', frame)

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

def stream_video(process_func):
    cap = cv2.VideoCapture('ronaldo.mp4')

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        frame = process_func(frame)
        ret, frame = cv2.imencode('.jpg', frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

def origin(frame):
    return frame

def local(request):
    return StreamingHttpResponse(stream_video(origin), content_type='multipart/x-mixed-replace; boundary=frame')