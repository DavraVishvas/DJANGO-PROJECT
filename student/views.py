from django.shortcuts import render,redirect
from django.http import HttpResponse
from student.forms import *

# Create your views here.
def student(request):
  msg='This is Student name'
  sl=['amit','Rina','Hiren']
  l=[
    {'id':1,'Name':'Ronak','age':18,'email':'r@gmail.com'},
    {'id':2,'Name':'Tarang','age':19,'email':'t@gmail.com'},
    {'id':3,'Name':'Vinay','age':18,'email':'v@gmail.com'},
    {'id':4,'Name':'Aarti','age':17,'email':'a@gmail.com'},
    {'id':5,'Name':'Hardik','age':20,'email':'h@gmail.com'},
  ]

  context={
    'msg':msg,
    'sl':sl,
    'l':l
  }
  return render(request,'student.html',context)

def studentData(request):
  if request.method == "POST":
    s=studForms(request.POST)
    if s.is_valid:
      try:
        s.save()
        return redirect('/read/')
      except:
        print("form is invalid")
    
  else:
    s=studForms()
  context={
    's':s
  }
  return render(request,'studentdata.html',context)

def read(request):
  f=Student.objects.all()
  context={
    'f':f
  }
  return render(request,'read.html',context)

def delete(request,id):
  f=Student.objects.get(id=id)
  f.delete()
  return redirect('/read/')

def update(request,id):
  f=Student.objects.get(id=id)
  if request.method=='POST':
    stu=studForms(request.POST,instance=f)
    if stu.is_valid():
      stu.save()
      return redirect('/read/')
  else:
    stu=studForms(instance=f)
  context={
    'stu':stu
  }
  return render(request,'update.html',context)