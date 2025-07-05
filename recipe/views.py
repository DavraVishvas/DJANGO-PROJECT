from django.shortcuts import render,redirect
from .models import *
import random
from django.http import HttpResponse 
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from openpyxl import Workbook
import csv

# Create your views here.

def register(request):
  if request.method == 'POST':
    uname=request.POST.get('uname')
    fname=request.POST.get('fname')
    lname=request.POST.get('lname')
    email=request.POST.get('email')
    password=request.POST.get('password')
    print(uname,password,fname,email,lname)
    if User.objects.filter(username=uname).exists():
      messages.info(request,'User already taken')
      return render(request,'register.html')
    u=User.objects.create(username=uname,first_name=fname,last_name=lname,email=email)
    u.set_password(password)
    u.save()
    return redirect('/login')
  return render(request,'register.html')

def login_view(request):
  if request.method == 'POST':
    uname=request.POST.get('uname')
    password=request.POST.get('password')
    print(uname,password)
    if not User.objects.filter(username=uname).exists():
      messages.info(request,'User not exist')
      return render(request,'login.html')
    else:
      u=authenticate(username=uname,password=password)
      print(u)
      if u is not None:
        login(request,u)
        return redirect('/recipe')
      else:
        messages.info(request,'Invalid credintial')
        return render(request,'login.html')
      return render(request,'register.html')
  return render(request,'login.html')

def logout_view(request):
  logout(request)
  return redirect('/recipe/')

@login_required(login_url='/login')
def recipe(request):
  user_id=request.user.id
  print(user_id,'user id')
  # r1 = Recipe.objects.all().order_by('-id')
  # r1 = Recipe.objects.all().filter(name='Mayur')
  r1 = Recipe.objects.all()
  paginator=Paginator(r1,2)
  page_num=request.GET.get('page')
  r=paginator.get_page(page_num)
  print(paginator)
  print(r)
  print(page_num)
  if request.method == 'POST':
    data=request.POST
    n=request.POST.get('name')
    d=request.POST.get('des')
    i=request.FILES.get('image')
    # print('name',n)
    # print('des',d)
    print('image',i)

    r=Recipe.objects.create(user_id_id=user_id,name=n,des=d,images=i)
    # print(r)
    return redirect('/recipe/')
  if request.GET.get('search'):
    s=request.GET.get('search')
    # print(s)
    q=Q(Q(name__icontains=s) | Q(des__icontains=s))
    r=Recipe.objects.filter(q)
    
  context={
    'r':r
  }
  
  return render(request,'recipe.html',context)
  
@login_required(login_url='/login')
def update(request,id):
  r=Recipe.objects.get(id=id)

  if request.method == 'POST':
    n=request.POST.get('name')
    d=request.POST.get('des')
    i=request.FILES.get('image')
    r.name=n
    r.des=d
    if i:
      r.images=i
    r.save()
    return redirect('/recipe/')
  context={
    'r':r
  }
  return render(request,'update.html',context)

@login_required(login_url='/login')
def delete(request,id):
  r=Recipe.objects.get(id=id)
  r.delete()
  return redirect('/recipe/')

def emailsend(request):
    subject = "Demo mail"
    message = "Open this image"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['vishvasdavra@gmail.com']

    send_mail(subject, message, from_email, recipient_list)

    return redirect('/recipe/')
  

def emailattachment(subject,message,recipent_list,file_path):
  mail=EmailMessage(subject=subject,body=message,from_email=settings.EMAIL_HOST_USER,to=recipent_list)
  mail.attach_file(file_path)
  mail.send()

def email_attachment(request):
    subject = "File Attachment"
    message = "Please check the attached image."
    recipent_list = ['davravishvas6165@gmail.com']
    file_path = f"{settings.BASE_DIR}/media/recipe/cafe.jpg"

    emailattachment(subject, message, recipent_list, file_path)

    return redirect('/recipe/')

def export_csv(request):
  response =HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="recipe.csv"'

  writer= csv.writer(response)
  writer.writerow(['ID','NAME','Description','Image'])

  for r in Recipe.objects.all():
    writer.writerow([r.id,r.name,r.des,r.images])

  return response

def export_excel(request):
  workbook = Workbook()
  sheet = workbook.active
  sheet.title = 'Recipe_Exel'

  sheet.append(['ID','NAME','Des','Images'])
  
  for r in Recipe.objects.all():
    image_path = r.images.path if r.images else 'No image'
    sheet.append([r.id, r.name, r.des, image_path])
    # sheet.append([r.id,r.name,r.des,r.images.path])
  
  response =HttpResponse(content_type='application/vnd.openexmlformats-officedocument.spreadsheetml.sheet')
  response['Content-Disposition'] = 'attachment; filename=Students_with_photos.xlsx'
  workbook.save(response)
  return response