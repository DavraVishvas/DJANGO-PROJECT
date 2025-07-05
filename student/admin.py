from django.contrib import admin
from .models import Student,div
from .models import Teacher
admin.site.register(div)
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
  list_display=['id','name','mark']

class TeacherAdmin(admin.ModelAdmin):
  list_display=['id','name','email','contact']
admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,TeacherAdmin)