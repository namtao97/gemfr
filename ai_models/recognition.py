import glob
import os
import time
import datetime

import cv2
import face_recognition
import numpy as np
import tensorflow as tf

from ai_models.utilities import *
from webcam.models import Credential


def get_encodings(folder):
    known_face_encodings = []
    known_face_names = []
    for file_path in glob.glob(os.path.join(folder, "*.jpg")):
        image = face_recognition.load_image_file(file_path)
        encoding = face_recognition.face_encodings(image, num_jitters=10)
        if len(encoding) == 0:
            print("No face found in image " + file_path)
        encoding = encoding[0]
        known_face_encodings.append(encoding)
        known_face_names.append(file_path)
    return known_face_encodings, known_face_names


def get_encodings_db():
    credentials = Credential.objects.all()

    known_face_encodings = []
    known_face_names = []

    for credential in credentials:
        known_face_encodings.append(credential.get_facial_encoding())
        known_face_names.append(credential.name)

    return known_face_encodings, known_face_names


#  known_face_encodings, known_face_names = get_encodings('./face_db')
known_face_encodings, known_face_names = get_encodings_db()
known_face_frame = {}
for face_name in known_face_names:
    known_face_frame[face_name] = -1000



def detection(img):
    return face_recognition.face_locations(img, model='hog')


def recognition(img, locations=None, frame_index=0, known_face_encodings=known_face_encodings, known_face_names=known_face_names,
                threshold=0.4):
    face_encodings = face_recognition.face_encodings(img, locations, num_jitters=1)
    face_names = []

    for face_encoding in face_encodings:
        distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        min_idx = np.argmin(distances)

        if distances[min_idx] < threshold:
            face_names.append(known_face_names[min_idx])
            
            diff_frame = frame_index - known_face_frame[known_face_names[min_idx]]
            if (diff_frame > 100):
                print(known_face_names[min_idx] + '\t' + str(datetime.datetime.now()) + '\n')
                with open('result.txt', 'a') as result:
                    result.write(known_face_names[min_idx] + '\t' + str(datetime.datetime.now()) + '\n')

            known_face_frame[known_face_names[min_idx]] = frame_index
        else:
            face_names.append("Unknown")

    return face_names


def preprocessing(img, fx=1, fy=1):
    return cv2.resize(RGB_revert(img), (0, 0), fx=fx, fy=fy)


def recognized_img(img, indice, fx=1, fy=1):
    procecced_img = preprocessing(img, fx, fy)

    face_locations = detection(procecced_img)
    face_names = recognition(procecced_img, frame_index=indice, locations=face_locations)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top = int(top / fy)
        right = int(right / fx)
        bottom = int(bottom / fy)
        left = int(left / fx)

        # Draw a box around the face
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    return img
