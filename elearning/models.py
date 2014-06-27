from django.db import models

from modules.models import Activity

class ELearningResource(models.Model):

    project = models.ForeignKey(Activity)
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to=lambda instance, filename: filename)

    def __str__(self):
        return self.title
