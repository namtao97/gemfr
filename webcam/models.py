import cv2
import json
import ast

import face_recognition
from django.db import models

# Create your models here.
from gemfr.settings import FACE_IMAGES_PATH


class Credential(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    facial_encoding = models.TextField(default='[]', blank=True)
    image = models.ImageField(upload_to=FACE_IMAGES_PATH, default=None)

    def get_facial_encoding(self):
        return ast.literal_eval(self.facial_encoding)

    def save(self, *args, **kwargs):
        img = face_recognition.load_image_file(self.image)
        facial_encoding_arr = face_recognition.face_encodings(img)
        if len(facial_encoding_arr) > 0:
            facial_encoding_arr = facial_encoding_arr[0].tolist()
        else:
            facial_encoding_arr = []

        self.facial_encoding = json.dumps(facial_encoding_arr)

        super(Credential, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + ' ' + self.name
