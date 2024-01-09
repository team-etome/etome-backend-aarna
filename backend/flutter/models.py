from django.db import models




class Byte(models.Model):
    image_name   = models.CharField(max_length=50)
    data         = models.BinaryField()


