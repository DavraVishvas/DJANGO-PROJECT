from django.db import models
# Create your models here.

class div(models.Model):
  name=models.CharField(max_length=100)
  def __str__(self):
    return self.name

class Student(models.Model):
  div_id=models.ForeignKey(div,on_delete=models.SET_NULL,null=True,blank=True)
  name=models.CharField(max_length=20)
  mark=models.IntegerField(null=True)

class Teacher(models.Model):
  id=models.IntegerField(primary_key=True)
  name=models.CharField(max_length=20)
  email=models.EmailField(unique=True)
  contact=models.IntegerField()