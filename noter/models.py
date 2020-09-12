from django.db import models
from django.contrib.auth.models import User


class Notebook(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 30)
    desc = models.CharField(default = None, max_length = 300, null = True)
    def __str__(self):
        return self.name



class Note(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete = models.CASCADE)
    title = models.CharField(default = None, max_length = 200, null = True)
    text = models.TextField()

    def __str__(self):
        return 'Note from ' + self.notebook.name

