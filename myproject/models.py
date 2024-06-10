from django.db import models


class Resume(models.Model):
    name = models.CharField(max_length=100)
    education = models.TextField()
    experience = models.TextField()
    skills = models.TextField()

    def __str__(self):
        return self.name