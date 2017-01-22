from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.

class HitGroupInfo(models.Model):
    hitGroupId = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    questionsPerHit = models.IntegerField()
    TASK_KIND_CHOICES = (
        ('SC', 'SingleLabel'),
        ('MC', 'Multilabel'),
        ('CL', 'collect'),
        ('FL', 'FILL'),
        ("DIY", 'your own task')
    )
    cNum = models.IntegerField()
    taskType = models.CharField(max_length=3,choices=TASK_KIND_CHOICES,default='CIC')
    taskFile = models.CharField(max_length=50)
    taskUI = models.CharField(max_length=50)
    hitRemains = models.IntegerField(default=0)

class HitInfo(models.Model):
    hitGroupId = models.CharField(max_length=50)
    hitId = models.CharField(max_length=50)

class TaskInfo(models.Model):
    taskId = models.UUIDField(primary_key=True,default=uuid.uuid4)
    taskDescription = models.CharField(max_length=250)
    taskLabels = models.CharField(max_length=250)
    hitGroupId = models.CharField(max_length=50)
    answered = models.IntegerField(default=0)
    result = models.CharField(max_length=50)
    distribution = models.CharField(max_length=250,default="")

class Assignment(models.Model):
    assignmentId =  models.CharField(max_length=50)
    workerId = models.CharField(max_length=50)
    hitId =  models.CharField(max_length=50)
    arriveTime = models.DateTimeField(null=True)
    finishTime = models.DateTimeField(null=True)
    accept = models.BooleanField(default=True)

class Submission(models.Model):
    hitGroupId = models.CharField(max_length=50)
    workerId = models.CharField(max_length=50)
    taskId = models.CharField(max_length=50)
    hitId = models.CharField(max_length=50)
    result = models.CharField(max_length=50)

class WorkerInfo(models.Model):
    workerId = models.CharField(max_length=50)
    quality = models.FloatField(default=0.7)






