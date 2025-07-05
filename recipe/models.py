from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
  user_id=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
  name=models.CharField(max_length=100)
  des=models.CharField(max_length=300)
  images=models.ImageField(upload_to='recipe')
  class Meta:
    db_table="RECIPE"
    verbose_name = "Recipe"
    verbose_name_plural = "Recipe"

  def __str__(self):
    return self.name
  