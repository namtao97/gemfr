import os
import datetime

import cv2
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import loader

from ai_models.recognition import recognized_img
from ai_models.tensorflow_human_detection import human_detect


def webcam(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def get_start_time(file_name):
    time_str = file_name.split('_')[3]
    year = int(time_str[:4])
    month = int(time_str[4:6])
    day = int(time_str[6:8])
    hour = int(time_str[8:10])
    minute = int(time_str[10:12])
    second = int(time_str[12:14])

    res = datetime.datetime(year, month, day, hour, minute, second)
    return res


# def process_video(file_name):
#     video_path = 'video/' + file_name
#     cap = cv2.VideoCapture(video_path)
#     time_begin = get_start_time(file_name)

#     face_times = []

#     indice = 0
#     count_frame = 0
#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             print("Error: failed to capture image")
#             break

#         if (indice % 40 == 0):
#             frame, curr_face_times = process_func(frame, indice)

#         ret, frame = cv2.imencode('.jpg', frame)
#         face_times.extend(curr_face_times)

#         yield (b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

#         indice += 1

#     with open('result.txt', 'a') as result:
#         for name, frame_idex in face_times:
#             time_appear = time_begin + datetime.timedelta(0, frame_index / 25)
#             result.write(name + '\t' + str(time_appear))



def stream(process_func):
    result = open('result.txt', 'a')

    for file in os.listdir('video'):
        if file.endswith('.mp4'):
            video_path = 'video/' + file
            print(video_path)
            cap = cv2.VideoCapture(video_path)
            time_begin = get_start_time(file)

            print(time_begin)
            
            face_times = []

            indice = 0
            count_frame = 0
            while True:
                ret, frame = cap.read()

                if not ret:
                    print("Error: failed to capture image")
                    break

                if (indice % 40 == 0):
                    frame, curr_face_times = process_func(frame, indice)

                ret, frame = cv2.imencode('.jpg', frame)
                if (len(curr_face_times) > 0):
                    name, frame_indice = curr_face_times[0]
                    if (frame_indice == indice):
                        face_times.extend(curr_face_times)
                        for name, frame_indice in curr_face_times:
                            time_appear = time_begin + datetime.timedelta(0, int(frame_indice / 25))
                            result.write(name + '\t' + str(time_appear) + '\n')
                            print(name, str(time_appear), frame_indice)
                            print()

                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

                indice += 1

            # print(face_times)
            # for name, frame_index in face_times:
            #     time_appear = time_begin + datetime.timedelta(0, frame_index / 25)
            #     result.write(name + '\t' + str(time_appear))       


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