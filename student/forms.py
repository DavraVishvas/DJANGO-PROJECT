from django import forms
from student.models import *

class studForms(forms.ModelForm):
  class Meta:
    model=Student
    fields='__all__'