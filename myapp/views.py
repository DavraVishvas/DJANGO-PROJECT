from django.shortcuts import render
from datetime import datetime

# Create your views here.
def a(request):
  current_time=datetime.now().time()
  current_date=datetime.now().date()
  return render(request,'index.html',{'current_time':current_time,'current_date':current_date})

