from django.test import TestCase
import time
from faker import Faker
f=Faker()
from .models import Student
import random

# Create your tests here.

def test():
  print('hello')
  time.sleep(3)
  print('exit')

def data(n=5):
    try:
      for i in range(0,n):
        name=f.name()
        mark=random.randint(15,50)
        stu=Student.objects.create(name=name,
                                   mark=mark)
    except Exception as e:
      print(e) 