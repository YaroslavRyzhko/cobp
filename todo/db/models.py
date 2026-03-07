from django.db import models

# Create your models here.
class Todolist(models.Model):
    name = models.TextField(max_length=200)

    def __str__(self):
        return self.name

class Task(models.Model):
    todolist = models.ForeignKey(Todolist, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.due_date