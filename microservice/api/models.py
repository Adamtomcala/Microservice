from django.db import models


class PostApi(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
